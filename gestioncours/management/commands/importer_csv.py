import csv
import re
from datetime import time
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from gestioncours.models import Cours, Professeur, HoraireCours

# Mapping fixe : pour chaque code, sessions possibles (liste)
SESSIONS_COURS = {
    "DROIT101": ["session1"],
    "SH101":    ["session1"],
    "FR101":    ["session1"],
    "CREO101":  ["session1"],
    "OT101":    ["session1"],

    # Cours pouvant réapparaître en session2
    "HIPS101":  ["session1", "session2"],
    "PHIL101":  ["session1", "session2"],
    "ECO101":   ["session1", "session2"],
    "MC101":    ["session1", "session2"],
    "MATH101":  ["session1", "session2"],
    "HH101":    ["session1", "session2"],
    "OT101":    ["session1", "session2"],  # si OTI doit repasser
    # … ajouter les autres codes si besoin
}

class Command(BaseCommand):
    help = "Importer les horaires de cours à partir d'un fichier CSV"

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help="Chemin vers le fichier CSV à importer")

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        try:
            with open(csv_file, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                # Normaliser en-têtes en minuscules
                reader.fieldnames = [h.strip().lower() for h in reader.fieldnames]
                self.stdout.write(f"✅ En-têtes détectées : {reader.fieldnames}")

                for row in reader:
                    # Nettoyage clés/valeurs
                    row = {k.strip().lower(): v.strip() for k, v in row.items()}

                    # Conversion horaire
                    try:
                        heure_debut, heure_fin = self.convertir_heure(row.get('heure', ''))
                    except ValueError as e:
                        self.stdout.write(self.style.ERROR(
                            f"Ligne {reader.line_num} — horaire invalide « {row.get('heure')} » : {e}"
                        ))
                        continue

                    # Extraction champs
                    jour    = row.get('jour', '').upper()
                    code    = row.get('code') or None
                    nom_c   = row.get('cours')
                    prenom  = row.get('prenom', '').title()
                    nom     = row.get('nom', '').upper()
                    credits = self.parse_credits(row.get('credits'))
                    niveau  = row.get('niveau', 'Premiere Annee')

                    # Détection de la session
                    session_csv = row.get('session', '').strip().lower()
                    session     = session_csv or SESSIONS_COURS.get(code, ["session2"])[0]

                    # Vérification des champs obligatoires
                    missing = [k for k,v in {
                        'jour': jour, 'cours': nom_c, 'prenom': prenom,
                        'nom': nom, 'session': session
                    }.items() if not v]
                    if missing:
                        self.stdout.write(self.style.ERROR(
                            f"Ligne {reader.line_num} — champs manquants : {missing}"
                        ))
                        continue

                    with transaction.atomic():
                        # Création / mise à jour du cours
                        cours, created = Cours.objects.get_or_create(
                            code=code,
                            defaults={
                                'nom': nom_c,
                                'credits': credits,
                                'niveau': niveau,
                                'session': session
                            }
                        )
                        if not created:
                            updated = False
                            for attr, val in {
                                'nom': nom_c,
                                'credits': credits,
                                'niveau': niveau,
                                'session': session
                            }.items():
                                if getattr(cours, attr) != val:
                                    setattr(cours, attr, val)
                                    updated = True
                            if updated:
                                cours.save()
                        # Création / récupération du professeur
                        prof, _ = Professeur.objects.get_or_create(prenom=prenom, nom=nom)
                        # Création de l'horaire
                        hoc, hcreated = HoraireCours.objects.get_or_create(
                            jour=jour,
                            heure_debut=heure_debut,
                            heure_fin=heure_fin,
                            cours=cours,
                            professeur=prof,
                            defaults={'capacite_max': 30}
                        )

                    # Logs
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"✅ Cours créé : {cours}"))
                    if hcreated:
                        self.stdout.write(self.style.SUCCESS(
                            f"🕒 Horaire ajouté : {cours.nom} le {jour} {heure_debut}-{heure_fin}"
                        ))
                    else:
                        self.stdout.write(self.style.WARNING(
                            f"⚠️ Doublon horaire ignoré : {cours.nom} {jour} {heure_debut}-{heure_fin}"
                        ))

                self.stdout.write(self.style.SUCCESS("✅ Importation terminée."))

        except FileNotFoundError:
            raise CommandError(f"Fichier introuvable : {csv_file}")

    def convertir_heure(self, s):
        s = re.sub(r'[–—−]', '-', s.replace(' ', ''))
        if not re.match(r'^\d{1,2}:\d{2}-\d{1,2}:\d{2}$', s):
            raise ValueError("format attendu HH:MM-HH:MM")
        d, f = s.split('-')
        return time.fromisoformat(d), time.fromisoformat(f)

    def parse_credits(self, val):
        try:
            return int(val.replace(',', '.'))
        except Exception:
            self.stdout.write(self.style.WARNING(
                f"⚠️ Crédit invalide « {val} », valeur par défaut 3 utilisée."
            ))
            return 3

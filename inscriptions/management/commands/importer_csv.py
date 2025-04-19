import csv
from django.core.management.base import BaseCommand
from datetime import time
from inscriptions.models import Cours, Professeur, HoraireCours, Etudiant, Inscription

class Command(BaseCommand):
    help = "Importer les inscriptions à partir d'un fichier CSV"

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help="Chemin vers le fichier CSV")

    def handle(self, *args, **options):  # ✅ Bien indenté maintenant
        csv_file = options['csv_file']

        try:
            with open(csv_file, newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                # Nettoyage des noms de colonnes
                reader.fieldnames = [field.strip() for field in reader.fieldnames]
                print("Colonnes trouvées dans le fichier CSV :", reader.fieldnames)

                for row in reader:
                    jour = row.get("Jour", "").strip()
                    heure_debut, heure_fin = self.convertir_heure(row.get("Heure", "").strip())
                    nom_cours = row.get("Cours", "").strip()
                    prenom = row.get("prenom", "").strip()
                    nom = row.get("nom", "").strip()

                    if not (jour and heure_debut and heure_fin and nom_cours and prenom and nom):
                        self.stdout.write(self.style.ERROR(f"⚠️ Données manquantes dans la ligne: {row}"))
                        continue

                    cours, _ = Cours.objects.get_or_create(nom=nom_cours)
                    prof, _ = Professeur.objects.get_or_create(prenom=prenom, nom=nom)

                    horaire, created = HoraireCours.objects.get_or_create(
                        jour=jour,
                        heure_debut=heure_debut,
                        heure_fin=heure_fin,
                        cours=cours,
                        professeur=prof,
                        defaults={"capacite_max": 30}
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(
                            f"{prof} assigné à {cours.nom} ({jour} {heure_debut}-{heure_fin})"
                        ))
                    else:
                        self.stdout.write(f"⚠️ Horaire déjà existant pour {cours.nom} ({jour} {heure_debut}-{heure_fin})")

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"Fichier introuvable : {csv_file}"))

    def convertir_heure(self, heure_str):
        import re
        heure_str = heure_str.replace("–", "-").replace("—", "-").replace("−", "-")
        heure_str = heure_str.replace("h", "").replace("H", "")
        heure_str = re.sub(r'\s+', '', heure_str)

        try:
            debut_str, fin_str = heure_str.split("-")

            def convertir_en_time(h):
                h = h.zfill(2)
                return time.fromisoformat(f"{h}:00:00")

            return convertir_en_time(debut_str), convertir_en_time(fin_str)

        except Exception as e:
            raise ValueError(f"Erreur lors de la conversion de l'heure '{heure_str}': {e}")

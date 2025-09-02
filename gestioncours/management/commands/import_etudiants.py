import csv
from django.core.management.base import BaseCommand
from gestioncours.models import Etudiant, Departement  # adapte selon ton app

class Command(BaseCommand):
    help = "Importe les étudiants depuis etudiants.csv"

    def handle(self, *args, **kwargs):
        with open("etudiants.csv", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # Récupère ou crée le département
                departement, _ = Departement.objects.get_or_create(nom=row["departement"])

                etudiant, created = Etudiant.objects.get_or_create(
                    email=row["email"],
                    defaults={
                        "nom": row["nom"],
                        "prenom": row["prenom"],
                        "telephone": row["telephone"],
                        "niveau": row["niveau"],
                        "departement": departement,  # <-- ICI on met l’instance
                    },
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Ajouté: {etudiant}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Déjà existant: {etudiant}"))

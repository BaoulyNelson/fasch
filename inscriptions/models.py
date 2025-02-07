from django.db import models
from django.utils import timezone  # Ajouter cette ligne
from django.contrib.auth.models import User

class Professeur(models.Model):
    NOM_PROFESSEUR_CHOICES = [
    ("Charles Vorbe", "Charles Vorbe"),
    ("Dominique Muscadin", "Dominique MUSCADIN"),
    ("Emmanuel Milord", "Emmanuel Milord"),
    ("Etienne Oremil", "Etienne Oremil"),
    ("Georges Legagneur", "Georges LEGAGNEUR"),
    ("Hancy Pierre", "Hancy Pierre"),
    ("Hubermane Ciguino", "Hubermane Ciguino"),
    ("Janes Louis", "Janes LOUIS"),
    ("Jean Evrard Jean Charles", "Jean Evrard Jean Charles"),
    ("Jean Luc Tondreau", "Jean Luc Tondreau"),
    ("Jean Pierre Ciguino", "Jean Pierre CIGUINO"),
    ("Jean Ronel Sistanis", "Jean Ronel Sistanis"),
    ("Jean Roy FAUSTIN", "Jean Roy FAUSTIN"),
    ("Jerome M", "Jerome M"),
    ("Job Silver", "Job SILVER"),
    ("Julio Elisna", "Julio Elisna"),
    ("Kenaz Brunis", "Kénaz BRUNIS"),
    ("Kenley Brutus", "Kenley Brutus"),
    ("Max Lubin", "Max Lubin"),
    ("Murielle Antoine", "Murielle ANTOINE"),
    ("Roosevelt Millard", "Roosevelt Millard"),
    ("Schmied Saint Fleur", "Schmied Saint Fleur"),
    ("Simeon Francois", "Siméon FRANCOIS"),
    ("Vosh Dathus", "Vosh Dathus"),
]


    SPECIALISATION_CHOICES = [
        ("Mathematiques", "Mathématiques"),
        ("Philosophie", "Philosophie"),
        ("Histoire", "Histoire"),
        ("Droit", "Droit"),
        ("Economie", "Économie"),
        ("Francais", "Français"),
        ("Creole", "Créole"),
        ("OTI", "Organisation du Travail"),
        ("Caraibe", "Monde Caraïbe"),
        ("Intro Aux Sc Hum", "Intro Aux Sc Hum"),
        ("HIPS", "Histoire Des Idees Politiques et Sociales"),
    ]

    nom = models.CharField(max_length=100, choices=NOM_PROFESSEUR_CHOICES)
    specialisation = models.CharField(max_length=100, choices=SPECIALISATION_CHOICES)

    def __str__(self):
        return f"{self.nom} ({self.specialisation})"


class Cours(models.Model):
    NOM_COURS_CHOICES = [
        ("HIPS", "Histoire des Idées Politiques et Sociales (HIPS)"),
        ("CREOLE", "Créole: Expression Écrite et Orale"),
        ("MATHS", "Mathématiques"),
        ("ECONOMIE", "Introduction à l'Économie"),
        ("Intro Aux SC HUM", "Introduction aux Sciences Humaines"),
        ("PHILO", "Introduction à la Philosophie"),
        ("OTI", "Organisation du Travail Intellectuel"),
        ("DROIT", "Introduction au Droit"),
        ("FRANCAIS", "Français: Expression Écrite et Orale"),
        ("CARAIBE", "Monde Caraïbe"),
        ("HISTOIRE D'HAITI", "Histoire d'Haïti"),
    ]

    SPECIALISATION_CHOICES = [
        ("Mathematiques", "Mathématiques"),
        ("Philosophie", "Philosophie"),
        ("Histoire", "Histoire"),
        ("Droit", "Droit"),
        ("Economie", "Économie"),
        ("Francais", "Français"),
        ("Creole", "Créole"),
        ("OTI", "Organisation du Travail Intellectuel"),
        ("Caraibe", "Monde Caraïbe"),
        ("Intro Aux SC Hum", "Intro Aux SC Hum"),
        ("HIPS", "Histoire des idées Politiques et Sociales"),
    ]

    HORAIRE_CHOICES = [
        ("Lundi 7H-10H", "Lundi 7H:00 - 10H:00"),
        ("Lundi 10H-1H", "Lundi 10H:00 - 1H:00"),
        ("Lundi 1H-4H", "Lundi 1H:00 - 4H:00"),
        ("Mardi 7H-10H", "Mardi 7H:00 - 10H:00"),
        ("Mardi 10H-1H", "Mardi 10H:00 - 1H:00"),
        ("Mardi 1H-4H", "Mardi 1H:00 - 4H:00"),
        ("Mercredi 7H-10H", "Mercredi 7H:00 - 10H:00"),
        ("Mercredi 10H-1H", "Mercredi 10H:00 - 1H:00"),
        ("Mercredi 1H-4H", "Mercredi 1H:00 - 4H:00"),
        ("Jeudi 7H-10H", "Jeudi 7H:00 - 10H:00"),
        ("Jeudi 10H-1H", "Jeudi 10H:00 - 1H:00"),
        ("Jeudi 1H-4H", "Jeudi 1H:00 - 4H:00"),
        ("Vendredi 7H-10H", "Vendredi 7H:00 - 10H:00"),
        ("Vendredi 10H-1H", "Vendredi 10H:00 - 1H:00"),
        ("Vendredi 1H-4H", "Vendredi 1H:00 - 4H:00"),
        ("Samedi 7H-10H", "Samedi 7H:00 - 10H:00"),
        ("Samedi 10H-1H", "Samedi 10H:00 - 1H:00"),
        ("Samedi 1H-4H", "Samedi 1H:00 - 4H:00"),
    ]

    nom = models.CharField(max_length=200, choices=NOM_COURS_CHOICES)
    specialisation = models.CharField(max_length=100, choices=SPECIALISATION_CHOICES)
    professeurs = models.ManyToManyField(Professeur, related_name="cours")
    capacite_maximale = models.PositiveIntegerField()
    horaire = models.CharField(max_length=50, choices=HORAIRE_CHOICES)
    est_ferme = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} ({self.specialisation}) - {self.horaire}"

    def get_nombre_inscrits(self):
        return self.inscriptions.count()

    def est_sature(self):
        """Vérifie si le cours est saturé."""
        return self.inscriptions.count() >= self.capacite_maximale

    def ajouter_professeur(self, professeur):
        """Ajoute un professeur au cours, en validant la spécialisation."""
        if professeur.specialisation != self.specialisation:
            raise ValueError(
                f"Le professeur {professeur.nom} ne peut pas enseigner ce cours ({self.nom}) : spécialisation incompatible."
            )
        self.professeurs.add(professeur)






class Etudiant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='etudiants')  # Un utilisateur peut avoir plusieurs étudiants
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='etudiants')  # Un utilisateur peut avoir plusieurs étudiants

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    niveau = models.CharField(
        max_length=50,
        choices=[
            ("Preparatoire", "Préparatoire"),
            ("Premiere Annee", "Première Année"),
            ("Deuxieme Annee", "Deuxième Année"),
            ("Troisieme Annee", "Troisième Année"),
            ("Quatrieme Annee", "Quatrième Année"),
        ],
        default="Preparatoire",
    )
    email = models.EmailField(unique=True)  # Email unique
    telephone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.niveau}"


class Inscription(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name="inscriptions")
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, related_name="inscriptions")
    date_inscription = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('etudiant', 'cours')  # Empêche l'inscription multiple à un même cours

    def save(self, *args, **kwargs):
        """Validation avant de sauvegarder une inscription."""
        if self.cours.est_ferme:
            raise ValueError(f"Le cours '{self.cours.nom}' est fermé aux inscriptions.")
        if self.cours.est_sature():
            raise ValueError(f"Le cours '{self.cours.nom}' est saturé.")
        if Inscription.objects.filter(etudiant=self.etudiant, cours=self.cours).exists():
            raise ValueError(f"L'étudiant '{self.etudiant.nom}' est déjà inscrit à ce cours.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.etudiant.nom} inscrit à {self.cours.nom}"



class Evenement(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField()
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    image = models.ImageField(upload_to='evenements/', null=True, blank=True)  # Champ pour les images
    lieu = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.titre

    def is_coming_up(self):
        """Retourne True si l'événement est à venir."""
        return self.date_debut > timezone.now()
    

class Annonce(models.Model):
    titre = models.CharField(max_length=255)
    contenu = models.TextField()  # Correspond à "description" dans le template
    date_publication = models.DateTimeField(auto_now_add=True)
    est_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='annonces/', null=True, blank=True)  # Champ pour les images
    organisateur = models.CharField(max_length=255, null=True, blank=True, default="FASCH")
    lieu = models.CharField(max_length=255, null=True, blank=True)  # Lieu
    date_evenement = models.DateTimeField(null=True, blank=True)  # Date et heure de l'événement

    def __str__(self):
        return self.titre

    def is_active(self):
        """Retourne True si l'annonce est active."""
        return self.est_active



class Article(models.Model):
    titre = models.CharField(max_length=200, help_text="Le titre de l'article")
    contenu = models.TextField(help_text="Le contenu de l'article")
    auteur = models.CharField(max_length=100, default="FASCH")  # Auteur par défaut

    date_publication = models.DateTimeField(default=timezone.now,)
    image = models.ImageField(upload_to='articles/', null=True, blank=True, help_text="Image associée à l'article")
    est_active = models.BooleanField(default=True, help_text="Indique si l'article est actif ou non")

    def __str__(self):
        return self.titre

    def resume(self):
        """Retourne un extrait de l'article limité à 200 caractères"""
        return self.contenu[:200] + "..." if len(self.contenu) > 200 else self.contenu
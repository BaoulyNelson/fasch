from django.db import models
from django.utils import timezone  # Ajouter cette ligne
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Etudiant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, blank=True)

    NIVEAU_CHOICES = [
        ("Preparatoire", "Préparatoire"),
        ("Premiere Annee", "Première Année"),
        ("Deuxieme Annee", "Deuxième Année"),
        ("Troisieme Annee", "Troisième Année"),
        ("Quatrieme Annee", "Quatrième Année"),
    ]
    niveau = models.CharField(max_length=50, choices=NIVEAU_CHOICES, default="Preparatoire")

    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
class Cours(models.Model):
    nom = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nom

class Professeur(models.Model):
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

class HoraireCours(models.Model):
    JOUR_CHOICES = [
        ("LUNDI", "Lundi"),
        ("MARDI", "Mardi"),
        ("MERCREDI", "Mercredi"),
        ("JEUDI", "Jeudi"),
        ("VENDREDI", "Vendredi"),
        ("SAMEDI", "Samedi"),
    ]

    jour = models.CharField(max_length=10, choices=JOUR_CHOICES)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)
    professeur = models.ForeignKey(Professeur, on_delete=models.CASCADE)
    capacite_max = models.PositiveIntegerField(default=30)  # <- capacité maximale du créneau
    est_ferme = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.jour} {self.heure_debut}-{self.heure_fin}: {self.cours.nom}"

    
    def est_sature(self):
        return self.est_ferme or self.inscription_set.count() >= self.capacite_max



class Inscription(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    horaire_cours = models.ForeignKey(HoraireCours, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('etudiant', 'horaire_cours')

    def clean(self):
        # Max 7 cours
        if Inscription.objects.filter(etudiant=self.etudiant).count() >= 7:
            raise ValidationError("Un étudiant ne peut pas s'inscrire à plus de 7 cours.")

        # Cours déjà suivi
        if Inscription.objects.filter(
            etudiant=self.etudiant,
            horaire_cours__cours=self.horaire_cours.cours
        ).exists():
            raise ValidationError("L'étudiant est déjà inscrit à ce cours.")

        # Conflit d'horaires
        conflit = Inscription.objects.filter(
            etudiant=self.etudiant,
            horaire_cours__jour=self.horaire_cours.jour,
            horaire_cours__heure_debut__lt=self.horaire_cours.heure_fin,
            horaire_cours__heure_fin__gt=self.horaire_cours.heure_debut
        ).exists()
        if conflit:
            raise ValidationError("Conflit d’horaire avec un autre cours.")

        # Capacité max atteinte
        if self.horaire_cours.est_sature():
            raise ValidationError("Ce cours est complet (capacité atteinte).")

    def __str__(self):
        return f"{self.etudiant} inscrit à {self.horaire_cours}"


class DemandeAdmission(models.Model):
    nom = models.CharField(max_length=255)
    email = models.EmailField()
    telephone = models.CharField(max_length=15)
    programme = models.CharField(max_length=255)
    message = models.TextField()

    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} - {self.programme}"
   
    
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
    
# models.py
class Programme(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField()
    niveau = models.CharField(max_length=100, choices=[('Licence', 'Licence'), ('Maîtrise', 'Maîtrise')])

    def __str__(self):
        return self.titre


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
    
    
    
class AxeRecherche(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.titre


class PublicationRecherche(models.Model):
    titre = models.CharField(max_length=255)
    auteurs = models.CharField(max_length=255)
    description = models.TextField()
    date_publication = models.DateField()
    domaines = models.CharField(max_length=255, help_text="Séparer les domaines par des virgules")
    lien = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.titre
    
    
class Livre(models.Model):
    titre = models.CharField(max_length=200)
    auteur = models.CharField(max_length=100)
    annee = models.IntegerField()
    resume = models.TextField()
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.titre


class Personnel(models.Model):
    POSTE_CHOICES = [
        ('doyen', 'Doyen'),
        ('vice_doyen_acad', 'Vice-Doyen Académique'),
        ('vice_doyen_admin', 'Vice-Doyen Administratif'),
        ('secretaire', 'Secrétaire Général'),
        ('agent_admin', 'Agent Administratif'),
        ('rap', 'Responsable Année Préparatoire'),
        ('chef_dept_socio', 'Chef de Département de Sociologie'),
        ('chef_dept_psy', 'Chef de Département de Psychologie'),
        ('chef_dept_com', 'Chef de Département de Communication Sociale'),
        ('chef_dept_ss', 'Chef de Département de Service Social'),
    ]

    poste = models.CharField(max_length=50, choices=POSTE_CHOICES)
    nom = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.ImageField(upload_to='personnel/', blank=True, null=True)
    description = models.TextField()

    class Meta:
        verbose_name = "Membre du personnel"
        verbose_name_plural = "Personnel administratif"
        ordering = ['poste']

    def __str__(self):
        return f"{self.nom} - {self.get_poste_display()}"

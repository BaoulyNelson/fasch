from django.db import models
from django.utils import timezone  # Ajouter cette ligne
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.text import slugify


class Departement(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom
    
    
class Etudiant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True,  error_messages={'unique': "Cet email appartient déjà à un autre étudiant."}
)
    telephone = models.CharField(max_length=20, unique=True,  error_messages={'unique': "Ce numero appartient déjà à un autre étudiant."}
)



    NIVEAU_CHOICES = [
        ("Preparatoire", "Préparatoire"),
        ("Premiere Annee", "Première Année"),
        ("Deuxieme Annee", "Deuxième Année"),
        ("Troisieme Annee", "Troisième Année"),
        ("Quatrieme Annee", "Quatrième Année"),
    ]
    niveau = models.CharField(max_length=50, choices=NIVEAU_CHOICES, default="Preparatoire")
    departement = models.ForeignKey(Departement, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
class Cours(models.Model):
    code = models.CharField(max_length=20, unique=True, null=True, blank=True)
    nom = models.CharField(max_length=255, unique=True)
    credits = models.PositiveIntegerField(default=3)

    NIVEAU_CHOICES = [
        ("Preparatoire", "Préparatoire"),
        ("Premiere Annee", "Première Année"),
        ("Deuxieme Annee", "Deuxième Année"),
        ("Troisieme Annee", "Troisième Année"),
        ("Quatrieme Annee", "Quatrième Année"),
    ]
    niveau = models.CharField(max_length=50, choices=NIVEAU_CHOICES, default="Preparatoire")

    SESSION_CHOICES = [
        ("session1", "Session 1"),
        ("session2", "Session 2"),
    ]
    session = models.CharField(max_length=20, choices=SESSION_CHOICES, default="session1")

    def __str__(self):
        return f"{self.code} - {self.nom}"


class Professeur(models.Model):
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=True, error_messages={'unique': "Cet email appartient déjà à un autre professeur."}
                              )
    telephone = models.CharField(max_length=20, null=True, unique=True,  error_messages={'unique': "Ce numero appartient déjà à un autre professeur."}
)
    specialite = models.CharField(max_length=255, blank=True, null=True)  # Champ stocké

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    def cours_enseignes(self):
        cours = Cours.objects.filter(horairecours__professeur=self).distinct()
        return ", ".join(c.nom for c in cours)  # Calculé dynamiquement



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



class EtapeAdmission(models.Model):
    nom = models.CharField(max_length=255)
    date_debut = models.DateField(null=True, blank=True)
    date_limite = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.nom
    
    
    
class DemandeAdmission(models.Model):
    nom = models.CharField(max_length=255)
    email = models.EmailField(unique=True,  error_messages={'unique': "Cet email appartient déjà à une autre personne."}
)
    telephone = models.CharField(max_length=15,unique=True,  error_messages={'unique': "Ce numero appartient déjà à une autre personne."}
)
    programme = models.CharField(max_length=255)
    message = models.TextField()

    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} - {self.programme}"
   
    

class Programme(models.Model):
    NIVEAU_CHOICES = [
        ("Preparatoire",     "Préparatoire"),
        ("Premiere Annee",   "Première Année"),
        ("Deuxieme Annee",   "Deuxième Année"),
        ("Troisieme Annee",  "Troisième Année"),
        ("Quatrieme Annee",  "Quatrième Année"),
    ]

    titre = models.CharField(max_length=255)
    description = models.TextField()
    niveau = models.CharField(
        max_length=20,
        choices=NIVEAU_CHOICES,
        default="Preparatoire",
    )

    def __str__(self):
        return self.titre




def generate_unique_slug(instance, model, slug_field='slug'):
    slug = slugify(instance.titre)[:200]
    unique_slug = slug
    num = 1
    ModelClass = model.__class__ if isinstance(model, models.Model) else model

    while ModelClass.objects.filter(**{slug_field: unique_slug}).exclude(pk=instance.pk).exists():
        unique_slug = f"{slug[:200 - len(str(num)) - 1]}-{num}"
        num += 1
    return unique_slug



class Article(models.Model):
    titre = models.CharField(max_length=200, help_text="Le titre de l'article")
    contenu = models.TextField(help_text="Le contenu de l'article")
    auteur = models.CharField(max_length=100, default="FASCH")
    date_publication = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='articles/', null=True, blank=True, help_text="Image associée à l'article")
    est_active = models.BooleanField(default=True, help_text="Indique si l'article est actif ou non")
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug or self._state.adding:
            self.slug = generate_unique_slug(self, Article)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titre

    def resume(self):
        return self.contenu[:200] + "..." if len(self.contenu) > 200 else self.contenu


class Evenement(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField()
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    image = models.ImageField(upload_to='evenements/', null=True, blank=True)
    lieu = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug or self._state.adding:
            self.slug = generate_unique_slug(self, Evenement)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titre

    def is_coming_up(self):
        return self.date_debut > timezone.now()


class Annonce(models.Model):
    titre = models.CharField(max_length=255)
    contenu = models.TextField()
    date_publication = models.DateTimeField(auto_now_add=True)
    est_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='annonces/', null=True, blank=True)
    organisateur = models.CharField(max_length=255, null=True, blank=True, default="FASCH")
    lieu = models.CharField(max_length=255, null=True, blank=True)
    date_evenement = models.DateTimeField(null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug or self._state.adding:
            self.slug = generate_unique_slug(self, Annonce)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titre

    def is_active(self):
        return self.est_active

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
    domaines = models.CharField(
        max_length=255,
        help_text="Séparer les domaines par des virgules",
        blank=True,
    )
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

    class Meta:
        verbose_name = "Membre du personnel"
        verbose_name_plural = "Personnel administratif"
        ordering = ['poste']

    def __str__(self):
        return f"{self.nom} - {self.get_poste_display()}"




class Examen(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Terminé'),
        ('active',    'En cours'),
        ('upcoming',  'À venir'),
    ]

    titre       = models.CharField("Intitulé de l'examen", max_length=255)
    date        = models.DateField("Date de l'examen")
    description = models.TextField("Description", blank=True)
    status      = models.CharField(
        "Statut",
        max_length=20,
        choices=STATUS_CHOICES,
        default='upcoming'
    )

    class Meta:
        ordering = ['date']
        verbose_name        = "Examen"
        verbose_name_plural = "Examens"

    def __str__(self):
        return f"{self.titre} le {self.date:%d %B %Y}"

    def save(self, *args, **kwargs):
        """
        Recalcule automatiquement `status` en fonction de `date` :
        - date < aujourd'hui  → 'completed'
        - date == aujourd'hui → 'active'
        - date > aujourd'hui  → 'upcoming'
        """
        today = timezone.localdate()
        if self.date < today:
            self.status = 'completed'
        elif self.date == today:
            self.status = 'active'
        else:
            self.status = 'upcoming'
        super().save(*args, **kwargs)



class SearchableMixin:
    @classmethod
    def search(cls, query):
        fields = getattr(cls, 'search_fields', [])
        filters = Q()
        for field in fields:
            filters |= Q(**{f"{field}__icontains": query})
        return cls.objects.filter(filters)

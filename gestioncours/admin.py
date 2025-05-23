from django.contrib import admin
from .models import Etudiant, Cours, Professeur, HoraireCours, Inscription,DemandeAdmission,Article,Annonce,Evenement,Programme,AxeRecherche, PublicationRecherche,Livre,Personnel,EtapeAdmission,Departement,Examen


@admin.register(Examen)
class ExamenAdmin(admin.ModelAdmin):
    list_display  = ('titre', 'date', 'status')
    list_filter   = ('date', 'status')
    search_fields = ('titre',)
    
@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ("prenom", "nom", "email", "telephone", "niveau", "departement")
    search_fields = ("prenom", "nom", "email")
    list_filter = ("niveau",)


admin.site.register(Departement)
@admin.register(Cours)
class CoursAdmin(admin.ModelAdmin):
    list_display = ("nom",)
    search_fields = ("nom",)

@admin.register(Professeur)
class ProfesseurAdmin(admin.ModelAdmin):
    list_display = ("prenom", "nom", "email", "telephone", "get_cours_enseignes")
    search_fields = ("prenom", "nom", "email", "telephone")

    @admin.display(description="Cours enseignés")
    def get_cours_enseignes(self, obj):
        return obj.cours_enseignes()


@admin.register(HoraireCours)
class HoraireCoursAdmin(admin.ModelAdmin):
    list_display = ("cours", "professeur", "jour", "heure_debut", "heure_fin", "capacite_max", "est_ferme")
    list_editable = ("est_ferme",)
    list_filter = ("jour", "cours", "professeur", "est_ferme")
    search_fields = ("cours__nom", "professeur__prenom", "professeur__nom")


@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    list_display = ("etudiant", "horaire_cours")
    list_filter = ("horaire_cours__cours", "etudiant__niveau")
    search_fields = ("etudiant__prenom", "etudiant__nom", "horaire_cours__cours__nom")
    
    

@admin.register(DemandeAdmission)
class DemandeAdmissionAdmin(admin.ModelAdmin):
    list_display = ("nom", "email", "programme", "date_envoi")
    search_fields = ("nom", "email", "programme")
    list_filter = ("programme", "date_envoi")


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur', 'date_publication', 'est_active')
    search_fields = ('titre', 'contenu')
    list_filter = ('est_active', 'date_publication')
    readonly_fields = ('date_publication', 'slug')  # + slug


@admin.register(Annonce)
class AnnonceAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date_publication', 'est_active', 'organisateur')
    search_fields = ('titre', 'contenu')
    list_filter = ('est_active', 'organisateur')
    readonly_fields = ('date_publication', 'slug')  # <- Ici


@admin.register(Evenement)
class EvenementAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date_debut', 'date_fin', 'lieu')
    search_fields = ('titre', 'description')
    list_filter = ('date_debut', 'lieu')
    readonly_fields = ('slug',)  # <- Si tu veux verrouiller le slug




@admin.register(AxeRecherche)
class AxeRechercheAdmin(admin.ModelAdmin):
    list_display = ("titre",)

@admin.register(PublicationRecherche)
class PublicationRechercheAdmin(admin.ModelAdmin):
    list_display = ("titre", "auteurs", "date_publication")
    search_fields = ("titre", "auteurs")
    list_filter = ("date_publication",)


@admin.register(Personnel)
class PersonnelAdmin(admin.ModelAdmin):
    list_display = ('nom', 'poste')
    list_filter = ('poste',)
    search_fields = ('nom',)




admin.site.register(EtapeAdmission)
admin.site.register(Livre)
admin.site.register(Programme)


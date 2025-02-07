from django.contrib import admin
from .models import Professeur, Cours, Etudiant, Inscription,Annonce,Evenement,Article

admin.site.register(Annonce)
admin.site.register(Evenement)
admin.site.register(Article)




@admin.register(Professeur)
class ProfesseurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'specialisation')
    list_filter = ('specialisation',)
    search_fields = ('nom', 'specialisation')



@admin.register(Cours)
class CoursAdmin(admin.ModelAdmin):
    list_display = ('nom', 'specialisation', 'capacite_maximale', 'horaire', 'est_ferme', 'est_sature', 'nombre_inscrits')
    list_filter = ('specialisation', 'horaire', 'est_ferme')
    search_fields = ('nom', 'specialisation')
    filter_horizontal = ('professeurs',)
    ordering = ('specialisation', 'nom')
    actions = ['ouvrir_cours', 'fermer_cours']

    def est_sature(self, obj):
        return obj.get_nombre_inscrits() >= obj.capacite_maximale
    est_sature.boolean = True
    est_sature.short_description = "Saturé ?"

    def nombre_inscrits(self, obj):
        return obj.get_nombre_inscrits()
    nombre_inscrits.short_description = "Inscriptions"

    @admin.action(description="Ouvrir les cours sélectionnés")
    def ouvrir_cours(self, request, queryset):
        queryset.update(est_ferme=False)
        self.message_user(request, f"{queryset.count()} cours ont été ouverts.")

    @admin.action(description="Fermer les cours sélectionnés")
    def fermer_cours(self, request, queryset):
        queryset.update(est_ferme=True)
        self.message_user(request, f"{queryset.count()} cours ont été fermés.")


@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'niveau', 'email', 'telephone')
    list_filter = ('niveau',)
    search_fields = ('nom', 'prenom', 'email', 'telephone')


@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'cours', 'date_inscription')
    list_filter = ('date_inscription', 'cours__nom')
    search_fields = ('etudiant__nom', 'cours__nom')

    def save_model(self, request, obj, form, change):
        # Vérifier si le cours est saturé avant de valider l'inscription
        if obj.cours.est_sature():
            self.message_user(
                request,
                f"Le cours {obj.cours.nom} est saturé et ne peut plus accepter d'inscriptions.",
                level="error"
            )
        else:
            super().save_model(request, obj, form, change)

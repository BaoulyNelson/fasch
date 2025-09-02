# forms.py
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import (
    Departement, Etudiant, Cours, Professeur, HoraireCours, Inscription,
    EtapeAdmission, Programme, Article, Evenement, Annonce, AxeRecherche,
    PublicationRecherche, Livre, Personnel, DemandeAdmission, Examen
)


# ---------------------------
# BaseStyledForm (style Tailwind automatique)
# ---------------------------
def _add_class(widget, classes):
    """Ajoute une classe au widget sans écraser celles existantes."""
    existing = widget.attrs.get("class", "").strip()
    widget.attrs["class"] = f"{existing} {classes}".strip() if existing else classes


class BaseStyledForm(forms.ModelForm):
    """
    Applique automatiquement un style Tailwind cohérent à tous les champs.
    - Checkboxes : classe simple (pas w-full).
    - File inputs : style adapté.
    - Textarea : rows et style.
    - Autres : w-full + padding + bord + focus ring.
    - Placeholder par défaut = label du champ (si absent).
    """

    default_text_class = "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
    default_file_class = "w-full p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
    default_checkbox_class = "mr-2"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            widget = field.widget

            # Checkbox
            if isinstance(widget, forms.CheckboxInput):
                _add_class(widget, self.default_checkbox_class)
                # pas de placeholder pour checkbox
                continue

            # File input
            if isinstance(widget, forms.ClearableFileInput):
                _add_class(widget, self.default_file_class)
                widget.attrs.setdefault("placeholder", field.label or "")
                continue

            # Textarea
            if isinstance(widget, forms.Textarea):
                _add_class(widget, self.default_text_class)
                widget.attrs.setdefault("rows", 4)
                widget.attrs.setdefault("placeholder", field.label or "")
                continue

            # Inputs (TextInput, EmailInput, NumberInput, DateInput, Select, etc.)
            # Si widget a déjà des classes (ex. widget personnalisé), on ne remplace pas — on concatène
            if widget.attrs.get("class"):
                # On conserve la classe fournie et ajoute rien par défaut pour éviter conflits.
                pass
            else:
                _add_class(widget, self.default_text_class)

            widget.attrs.setdefault("placeholder", field.label or "")
            # accessibilité minimale
            widget.attrs.setdefault("aria-label", field.label or name)


# ---------------------------
# Forms
# ---------------------------

class CustomUserChangeForm(BaseStyledForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
        labels = {
            "username": "Nom d'utilisateur",
            "first_name": "Prénom",
            "last_name": "Nom",
            "email": "Adresse e-mail",
        }
        widgets = {
            # On laisse le BaseStyledForm ajouter la classe; on conserve les types.
            "username": forms.TextInput(),
            "first_name": forms.TextInput(),
            "last_name": forms.TextInput(),
            "email": forms.EmailInput(),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Cet email est déjà utilisé par un autre utilisateur.")
        return email


class EtudiantForm(BaseStyledForm):
    class Meta:
        model = Etudiant
        fields = ["prenom", "nom", "email", "telephone", "niveau", "departement"]
        widgets = {
            # on laisse BaseStyledForm ajouter les classes ; préciser les types utiles
            "prenom": forms.TextInput(),
            "nom": forms.TextInput(),
            "email": forms.EmailInput(),
            "telephone": forms.TextInput(),
            "niveau": forms.Select(),
            "departement": forms.Select(),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Etudiant.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Cet email est déjà utilisé par un autre étudiant.")
        return email

    def clean_telephone(self):
        telephone = self.cleaned_data.get("telephone")
        if Etudiant.objects.filter(telephone=telephone).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ce numéro de téléphone est déjà utilisé par un autre étudiant.")
        return telephone


class ContactForm(forms.Form):
    nom = forms.CharField(max_length=100, label="Nom complet", widget=forms.TextInput())
    email = forms.EmailField(label="Email", widget=forms.EmailInput())
    sujet = forms.CharField(max_length=150, label="Sujet", widget=forms.TextInput())
    message = forms.CharField(widget=forms.Textarea(attrs={"rows": 5}), label="Message")


class DemandeAdmissionForm(BaseStyledForm):
    class Meta:
        model = DemandeAdmission
        fields = ["nom", "email", "telephone", "programme", "message"]
        widgets = {
            "nom": forms.TextInput(attrs={"placeholder": "Votre nom complet"}),
            "email": forms.EmailInput(attrs={"placeholder": "votre@email.com"}),
            "telephone": forms.TextInput(attrs={"placeholder": "+229 90 00 00 00"}),
            "programme": forms.TextInput(),  # si tu as select, remplace par Select()
            "message": forms.Textarea(attrs={"rows": 4}),
        }


class CoursForm(BaseStyledForm):
    class Meta:
        model = Cours
        fields = ["code", "nom", "credits", "niveau", "session"]
        widgets = {
            "code": forms.TextInput(attrs={"placeholder": "Code du cours (ex: INF101)"}),
            "nom": forms.TextInput(attrs={"placeholder": "Nom du cours"}),
            "credits": forms.NumberInput(attrs={"min": 1}),
            "niveau": forms.Select(),
            "session": forms.Select(),
        }


class ProfesseurForm(BaseStyledForm):
    cours_enseignes_display = forms.CharField(
        label="Cours enseignés",
        required=False,
        widget=forms.Textarea(attrs={"readonly": "readonly", "rows": 2})
    )

    class Meta:
        model = Professeur
        # si tu veux éviter d'afficher user liée etc. ajuste ici
        fields = ["prenom", "nom", "email", "telephone", "specialite"]
        widgets = {
            "prenom": forms.TextInput(),
            "nom": forms.TextInput(),
            "email": forms.EmailInput(),
            "telephone": forms.TextInput(),
            "specialite": forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            cours = self.instance.cours_enseignes()
            self.fields["cours_enseignes_display"].initial = cours


class HoraireCoursForm(BaseStyledForm):
    class Meta:
        model = HoraireCours
        fields = ["jour", "heure_debut", "heure_fin", "cours", "professeur", "capacite_max", "est_ferme"]
        widgets = {
            "jour": forms.Select(),
            "heure_debut": forms.TimeInput(attrs={"type": "time"}),
            "heure_fin": forms.TimeInput(attrs={"type": "time"}),
            "cours": forms.Select(),
            "professeur": forms.Select(),
            "capacite_max": forms.NumberInput(attrs={"min": 1}),
            "est_ferme": forms.CheckboxInput(),
        }


class InscriptionForm(BaseStyledForm):
    class Meta:
        model = Inscription
        fields = ["etudiant", "horaire_cours"]
        widgets = {
            "etudiant": forms.Select(),
            "horaire_cours": forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Amélioration UX : afficher une description lisible pour horaire_cours
        self.fields["horaire_cours"].queryset = HoraireCours.objects.select_related("cours").all()
        # on ne peut pas définir label_from_instance directement sur queryset dans ModelChoiceField,
        # mais on peut remplacer le widget choices (ou utiliser ModelChoiceField subclass). Simplicité :
        self.fields["horaire_cours"].label_from_instance = lambda obj: f"{obj.jour} {obj.heure_debut.strftime('%H:%M')}–{obj.heure_fin.strftime('%H:%M')} ({obj.cours.nom})"


class EtapeAdmissionForm(BaseStyledForm):
    class Meta:
        model = EtapeAdmission
        fields = ["nom", "date_debut", "date_limite"]
        widgets = {
            "nom": forms.TextInput(),
            "date_debut": forms.DateInput(attrs={"type": "date"}),
            "date_limite": forms.DateInput(attrs={"type": "date"}),
        }


class ProgrammeForm(BaseStyledForm):
    class Meta:
        model = Programme
        fields = ["titre", "description", "niveau"]
        widgets = {
            "titre": forms.TextInput(),
            "description": forms.Textarea(attrs={"rows": 5}),
            "niveau": forms.Select(),
        }


class ArticleForm(BaseStyledForm):
    class Meta:
        model = Article
        fields = ['titre', 'contenu', 'auteur', 'date_publication', 'image', 'est_active', 'slug']
        widgets = {
            "titre": forms.TextInput(),
            "contenu": forms.Textarea(attrs={"rows": 6}),
            "auteur": forms.TextInput(),
            "date_publication": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "image": forms.ClearableFileInput(),
            "est_active": forms.CheckboxInput(),
            "slug": forms.TextInput(attrs={"readonly": "readonly"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # date_publication facultative
        self.fields["date_publication"].required = False

    def clean_slug(self):
        slug = self.cleaned_data.get("slug")
        if slug and Article.objects.filter(slug=slug).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ce slug est déjà utilisé par un autre article.")
        return slug


class EvenementForm(BaseStyledForm):
    class Meta:
        model = Evenement
        fields = ['titre', 'description', 'date_debut', 'date_fin', 'image', 'lieu', 'slug']
        widgets = {
            "titre": forms.TextInput(),
            "description": forms.Textarea(attrs={"rows": 5}),
            "date_debut": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "date_fin": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "image": forms.ClearableFileInput(),
            "lieu": forms.TextInput(),
            "slug": forms.TextInput(attrs={"readonly": "readonly"}),
        }

    def clean_slug(self):
        slug = self.cleaned_data.get("slug")
        if slug and Evenement.objects.filter(slug=slug).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ce slug est déjà utilisé pour un autre événement.")
        return slug


class AnnonceForm(BaseStyledForm):
    class Meta:
        model = Annonce
        fields = ['titre', 'contenu', 'est_active', 'image', 'organisateur', 'lieu', 'date_evenement', 'slug']
        widgets = {
            "titre": forms.TextInput(),
            "contenu": forms.Textarea(attrs={"rows": 5}),
            "est_active": forms.CheckboxInput(),
            "image": forms.ClearableFileInput(),
            "organisateur": forms.TextInput(),
            "lieu": forms.TextInput(),
            "date_evenement": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "slug": forms.TextInput(attrs={"readonly": "readonly"}),
        }

    def clean_slug(self):
        slug = self.cleaned_data.get("slug")
        if slug and Annonce.objects.filter(slug=slug).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ce slug est déjà utilisé pour une autre annonce.")
        return slug


class AxeRechercheForm(BaseStyledForm):
    class Meta:
        model = AxeRecherche
        fields = ['titre', 'description']
        widgets = {
            "titre": forms.TextInput(),
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class ExamenForm(BaseStyledForm):
    class Meta:
        model = Examen
        fields = ['titre', 'date', 'description']   # ✅
        widgets = {
            "titre": forms.TextInput(),
            "date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class PublicationRechercheForm(BaseStyledForm):
    class Meta:
        model = PublicationRecherche
        fields = ['titre', 'auteurs', 'description', 'date_publication', 'domaines', 'lien']
        widgets = {
            "titre": forms.TextInput(),
            "auteurs": forms.TextInput(),
            "description": forms.Textarea(attrs={"rows": 5}),
            "date_publication": forms.DateInput(attrs={"type": "date"}),
            "domaines": forms.TextInput(),
            "lien": forms.URLInput(),
        }


class LivreForm(BaseStyledForm):
    class Meta:
        model = Livre
        fields = ['titre', 'auteur', 'annee', 'resume', 'disponible']
        widgets = {
            "titre": forms.TextInput(),
            "auteur": forms.TextInput(),
            "annee": forms.NumberInput(),
            "resume": forms.Textarea(attrs={"rows": 4}),
            "disponible": forms.CheckboxInput(),
        }


class PersonnelForm(BaseStyledForm):
    class Meta:
        model = Personnel
        fields = ['poste', 'nom', 'description', 'photo']
        widgets = {
            "poste": forms.Select(),
            "nom": forms.TextInput(),
            "description": forms.Textarea(attrs={"rows": 4}),
            "photo": forms.ClearableFileInput(),
        }

    # Pas d'actions spéciales ici, mais tu peux ajouter un clean_* si nécessaire.

from django import forms
from django.contrib.auth.models import User
from .models import Etudiant,DemandeAdmission
from django import forms
from .models import (
    Cours, Professeur, HoraireCours, Inscription,
    EtapeAdmission, Programme, Evenement,
    Annonce, Article, AxeRecherche, PublicationRecherche,
    Livre, Personnel
)


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Nom d\'utilisateur',
            'first_name': 'Prénom',
            'last_name': 'Nom',
            'email': 'Adresse e-mail',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("Cet email est déjà utilisé par un autre utilisateur.")
        return email

        
        
class EtudiantForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = ['nom', 'prenom', 'email', 'telephone', 'niveau']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Etudiant.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("Cet email est déjà utilisé par un autre étudiant.")
        return email

    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        if Etudiant.objects.filter(telephone=telephone).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("Ce numéro de téléphone est déjà utilisé par un autre étudiant.")
        return telephone



class ContactForm(forms.Form):
    nom = forms.CharField(max_length=100, label="Nom complet")
    email = forms.EmailField(label="Email")
    sujet = forms.CharField(max_length=150, label="Sujet")
    message = forms.CharField(widget=forms.Textarea, label="Message")
    


class DemandeAdmissionForm(forms.ModelForm):
    class Meta:
        model = DemandeAdmission
        fields = ['nom', 'email', 'telephone', 'programme', 'message']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md text-base',
                'style': 'border-color: var(--border-color); background-color: var(--bg-primary); color: var(--text-primary);'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md text-base',
                'style': 'border-color: var(--border-color); background-color: var(--bg-primary); color: var(--text-primary);'
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md text-base',
                'style': 'border-color: var(--border-color); background-color: var(--bg-primary); color: var(--text-primary);'
            }),
            'programme': forms.Select(
                choices=[
                    ('', 'Sélectionnez un programme'),
                    ('sociologie-l', 'Sociologie (Licence)'),
                    ('sociologie-m', 'Sociologie (Maîtrise)'),
                    ('psychologie-l', 'Psychologie (Licence)'),
                    ('psychologie-m', 'Psychologie (Maîtrise)'),
                    ('communication-l', 'Communication Sociale (Licence)'),
                    ('servicesocial-l', 'Service Social (Licence)')
                ],
                attrs={
                    'class': 'w-full px-3 py-2 border rounded-md text-base',
                    'style': 'border-color: var(--border-color); background-color: var(--bg-primary); color: var(--text-primary);'
                }
            ),
            'message': forms.Textarea(attrs={
                'rows': 3,
                'class': 'w-full px-3 py-2 border rounded-md text-base',
                'style': 'border-color: var(--border-color); background-color: var(--bg-primary); color: var(--text-primary);'
            }),
        }
        
        
        
class CoursForm(forms.ModelForm):
    class Meta:
        model = Cours
        fields = ['code', 'nom', 'credits', 'niveau']
        widgets = {
            'code': forms.TextInput(attrs={
                'class': 'block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Code du cours (ex: INF101)'
            }),
            'nom': forms.TextInput(attrs={
                'class': 'block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Nom du cours'
            }),
            'credits': forms.NumberInput(attrs={
                'class': 'block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500',
                'min': 1,
                'placeholder': 'Nombre de crédits'
            }),
            'niveau': forms.Select(attrs={
                'class': 'block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500',
            }),
        }

      
class ProfesseurForm(forms.ModelForm):
    cours_enseignes_display = forms.CharField(
        label="Cours enseignés",
        required=False,
        widget=forms.Textarea(attrs={'readonly': 'readonly', 'rows': 2})
    )

    class Meta:
        model = Professeur
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:  # édition uniquement
            cours = self.instance.cours_enseignes()
            self.fields['cours_enseignes_display'].initial = cours


class HoraireCoursForm(forms.ModelForm):
    jour = forms.ChoiceField(
        choices=HoraireCours.JOUR_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select mt-1 block w-full rounded-md border-gray-300'})
    )

    class Meta:
        model = HoraireCours
        fields = ['jour', 'heure_debut', 'heure_fin', 'cours', 'professeur', 'capacite_max', 'est_ferme']



class InscriptionForm(forms.ModelForm):
    class Meta:
        model = Inscription
        fields = ['etudiant', 'horaire_cours']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Pour personnaliser l'affichage des horaires dans le select
        self.fields['horaire_cours'].queryset = HoraireCours.objects.select_related('cours').all()
        self.fields['horaire_cours'].label_from_instance = lambda obj: f"{obj.jour} {obj.heure_debut.strftime('%H:%M')}–{obj.heure_fin.strftime('%H:%M')} ({obj.cours.nom})"
        
        
class EtapeAdmissionForm(forms.ModelForm):
    class Meta:
        model = EtapeAdmission
        fields = '__all__'



class ProgrammeForm(forms.ModelForm):
    class Meta:
        model = Programme
        fields = '__all__'
        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-primary focus:border-primary sm:text-sm'
            }),
            'niveau': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-primary focus:border-primary sm:text-sm'
            }),
            'description': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-primary focus:border-primary sm:text-sm',
                'rows': 5
            }),
        }


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_publication'].required = False
        self.fields['slug'].widget.attrs['readonly'] = True  # facultatif : le rendre non modifiable

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        # ⚠️ On ignore l'objet actuel (self.instance.pk) pour éviter les faux positifs
        if Article.objects.filter(slug=slug).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ce slug est déjà utilisé par un autre article.")
        return slug


class EvenementForm(forms.ModelForm):
    class Meta:
        model = Evenement
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].widget.attrs['readonly'] = True  # Rendre le champ slug en lecture seule

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if Evenement.objects.filter(slug=slug).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ce slug est déjà utilisé pour un autre événement.")
        return slug


class AnnonceForm(forms.ModelForm):
    class Meta:
        model = Annonce
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].widget.attrs['readonly'] = True  # Rendre le champ slug en lecture seule

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if Annonce.objects.filter(slug=slug).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ce slug est déjà utilisé pour une autre annonce.")
        return slug


class AxeRechercheForm(forms.ModelForm):
    class Meta:
        model = AxeRecherche
        fields = '__all__'

class PublicationRechercheForm(forms.ModelForm):
    class Meta:
        model = PublicationRecherche
        fields = '__all__'

class LivreForm(forms.ModelForm):
    class Meta:
        model = Livre
        fields = '__all__'

class PersonnelForm(forms.ModelForm):
    class Meta:
        model = Personnel
        fields = '__all__'

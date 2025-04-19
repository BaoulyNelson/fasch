from django import forms
from django.contrib.auth.models import User
from .models import Etudiant,DemandeAdmission


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
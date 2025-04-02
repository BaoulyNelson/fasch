from django import forms
from django.contrib.auth.models import User
from .models import Etudiant


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
    name = forms.CharField(label="Nom", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    message = forms.CharField(label="Message", widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))

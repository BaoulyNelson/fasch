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

class EtudiantForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = ['nom', 'prenom', 'email', 'telephone', 'niveau']

class ContactForm(forms.Form):
    name = forms.CharField(label="Nom", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    message = forms.CharField(label="Message", widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))

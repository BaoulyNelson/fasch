from django.shortcuts import render, redirect
from .models import Inscription, Etudiant,Evenement,Article,HoraireCours, Inscription, Etudiant,Annonce,Programme,PublicationRecherche,AxeRecherche,Livre,Personnel
from .forms import CustomUserChangeForm,DemandeAdmissionForm,EtudiantForm,ContactForm
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone  # Ajouter cette ligne
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages
from django.utils.timezone import now
from django.db import transaction
from django.db.models import Q
from django.utils.html import mark_safe
import re
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.contrib.messages import get_messages
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import logout
from inscriptions.utils import ajouter_message
from django.core.exceptions import PermissionDenied




def login_view(request):
    # Supprime les anciens messages avant d'afficher un nouveau
    storage = get_messages(request)
    for _ in storage:
        pass  # Cette boucle vide supprime tous les anciens messages

    next_url = request.GET.get("next", "profile")  # Récupérer 'next' ou rediriger vers 'profile' par défaut

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenue {username} ! 😊 Vous êtes connecté.")

                if request.POST.get("remember_me"):
                    request.session.set_expiry(1209600)  # 2 semaines

                return redirect(request.POST.get("next", next_url))  # Redirige vers next
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        else:
            messages.error(request, "Veuillez vérifier vos informations.")
    else:
        form = AuthenticationForm()

    return render(request, "registration/login.html", {"form": form, "next": next_url})


def signup_view(request):
    next_url = request.GET.get("next", "home")  # Récupérer la page demandée ou rediriger vers 'home' par défaut

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Connecter directement après l'inscription
            messages.success(request, "Inscription réussie ! 🎉 Bienvenue sur notre plateforme.")

            return redirect(request.POST.get("next", next_url))  # Rediriger vers la page prévue
        else:
            messages.error(request, "Une erreur est survenue lors de l'inscription. Vérifiez les informations.")
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form, "next": next_url})



@login_required
def profile_view(request):
    return render(request, 'registration/profile.html', {'user': request.user})


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            ajouter_message(request, 'success', '✅ Votre profil a été mis à jour avec succès.')
            return redirect('profile')  # Redirection vers la page du profil
    
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    return render(request, 'registration/edit_profile.html', {'form': form})


def logout_view(request):
    print("🔥 logout_view appelée")  # ← Test console
    logout(request)
    messages.info(request, "🔒 Vous avez été déconnecté avec succès.")
    return redirect('home')


def confirmer_deconnexion(request):
    return render(request, 'registration/confirmer_deconnexion.html')


def home(request):
    # Articles actifs avec pagination
    articles_list = Article.objects.filter(est_active=True).order_by('-date_publication')
    paginator = Paginator(articles_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Événements à venir (prochains événements)
    evenements = Evenement.objects.filter(date_debut__gte=timezone.now()).order_by('date_debut')

    # Annonces actives (peut aussi filtrer par date_evenement si nécessaire)
    annonces = Annonce.objects.filter(est_active=True).order_by('-date_publication')  # ou '-date_evenement'

    context = {
        'articles': page_obj,
        'evenements': evenements,
        'annonces': annonces,
        'now': timezone.now(),
    }

    return render(request, 'index.html', context)

    
    


@login_required
def create_profile(request):
    # Vérifier si l'étudiant a déjà un profil
    try:
        etudiant = Etudiant.objects.get(user=request.user)
        return redirect("profile")  # Si le profil existe, rediriger vers la page de profil
    except Etudiant.DoesNotExist:
        pass

    if request.method == "POST":
        form = EtudiantForm(request.POST)
        if form.is_valid():
            # Créer le profil étudiant et l'associer à l'utilisateur
            etudiant = form.save(commit=False)
            etudiant.user = request.user  # Lier l'utilisateur à ce profil étudiant
            etudiant.save()
            messages.success(request, "Votre profil étudiant a été créé avec succès ! 🎉")
            return redirect("etudiant_profil")  # Rediriger vers la page de profil
        else:
            messages.error(request, "Il y a eu une erreur dans la création de votre profil.")
    else:
        form = EtudiantForm()

    return render(request, "etudiants/create_profile.html", {"form": form})


@login_required
def etudiant_profil(request):
    # On suppose que l'utilisateur est lié à un étudiant via la relation OneToOne
    try:
        etudiant = request.user.etudiant
    except Etudiant.DoesNotExist:
        return redirect('edit_info_etudiant', etudiant_id=0)  # ou une autre gestion d'erreur
    
    return render(request, 'etudiants/etudiant_profil.html', {'etudiant': etudiant})


@login_required
def edit_info_etudiant(request, etudiant_id):
    etudiant = get_object_or_404(Etudiant, id=etudiant_id)

    # Vérifie que l'utilisateur connecté est bien celui associé à l'étudiant
    if request.user != etudiant.user:
        raise PermissionDenied("Vous n'avez pas la permission de modifier ce profil.")

    if request.method == 'POST':
        form = EtudiantForm(request.POST, instance=etudiant)
        if form.is_valid():
            form.save()
            ajouter_message(request, 'success', '✅ Votre profil a été mis à jour avec succès.')
            return redirect('etudiant_profil')  # Redirection vers la page du profil
    else:
        form = EtudiantForm(instance=etudiant)

    return render(request, 'etudiants/edit_info_etudiant.html', {'form': form})



@login_required
def cours_list(request):
    horaires = HoraireCours.objects.select_related('cours', 'professeur')
    paginator = Paginator(horaires, 9)  # 10 cours par page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "cours/liste.html", {"page_obj": page_obj})



@login_required
def cours_detail(request, horaire_id):
    horaire = get_object_or_404(HoraireCours, id=horaire_id)
    inscrit = Inscription.objects.filter(etudiant__user=request.user, horaire_cours=horaire).exists()
    return render(request, "cours/detail.html", {"horaire": horaire, "inscrit": inscrit})



@login_required
def mes_cours(request):
    try:
        etudiant = Etudiant.objects.get(user=request.user)
    except Etudiant.DoesNotExist:
        ajouter_message(request, 'error', "Aucun profil étudiant lié à ce compte.")
        return redirect("create_profile")

    inscriptions = Inscription.objects.filter(etudiant=etudiant).select_related("horaire_cours", "horaire_cours__cours", "horaire_cours__professeur")
    return render(request, "cours/mes_cours.html", {"etudiant": etudiant, "inscriptions": inscriptions})




@login_required
def inscription_create(request, horaire_id):
    horaire = get_object_or_404(HoraireCours, id=horaire_id)

    # Vérifier que l'utilisateur est lié à un étudiant
    try:
        etudiant = Etudiant.objects.get(user=request.user)
    except Etudiant.DoesNotExist:
        ajouter_message(request, 'error', "Aucun profil étudiant lié à ce compte.")
        return redirect("create_profile")

    inscription = Inscription(etudiant=etudiant, horaire_cours=horaire)

    try:
        inscription.clean()
        inscription.save()
        ajouter_message(request, 'success', "Inscription réussie ! 🎉")
        return redirect("mes_cours")  # ✅ redirection vers la liste des cours inscrits
    except Exception as e:
        ajouter_message(request, 'error', f"Erreur : {e}")
        return redirect("cours_detail", horaire_id=horaire_id)


def programmes(request):
    programmes = Programme.objects.all()  # Récupérer tous les programmes
    return render(request, 'programmes/programmes.html', {'programmes': programmes})  # Rendre le template 'programmes.html'

def programme_detail(request, pk):
    programme = get_object_or_404(Programme, pk=pk)
    return render(request, 'programmes/program_detail.html', {'programme': programme})


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    autres_articles = Article.objects.exclude(pk=pk).order_by('-date_publication')[:3]  # les 3 plus récents sauf celui-ci
    return render(request, 'articles/article_detail.html', {
        'article': article,
        'autres_articles': autres_articles
    })

def annonce_detail(request, pk):
    annonce = get_object_or_404(Annonce, pk=pk)
    return render(request, 'annonces/annonces_details.html', {'annonce': annonce})

def evenement_detail(request, pk):
    evenement = get_object_or_404(Evenement, pk=pk)
    return render(request, 'evenements/evenement_detail.html', {'evenement': evenement})



def success_page(request):
    try:
        etudiant = request.user.etudiant  # Si l'utilisateur a un profil 'etudiant'
    except AttributeError:
        # Si l'utilisateur n'a pas de profil étudiant, rediriger ou gérer ce cas
        return redirect('cours')  # Ou une autre page qui indique que l'étudiant n'est pas trouvé
    
    return render(request, 'success_page.html', {'etudiant': etudiant})



def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Traitement ici (ex : envoi d'email)
            return render(request, "contact/contact_success.html")  # ← page de confirmation
    else:
        form = ContactForm()

    return render(request, "contact/contact.html", {"form": form})


def contact_success_view(request):
    return render(request, "contact/contact_success.html")




def catalogue(request):
    livres = Livre.objects.all()
    return render(request, 'bibliotheque/catalogue.html', {'livres': livres})


def apropos(request):
    personnel = Personnel.objects.all()
    return render(request, 'apropos.html', {'personnel': personnel})


def demande_admission(request):
    if request.method == "POST":
        form = DemandeAdmissionForm(request.POST)
        if form.is_valid():
            form.save()
            # Ajoutez 'request' dans l'appel de render pour la page de confirmation
            return render(request, 'admissions/confirmation_admission.html')  # redirige vers une page de remerciement
    else:
        form = DemandeAdmissionForm()

    return render(request, 'admissions/demande_admission.html', {'form': form})


def recherche_view(request):
    axes_recherche = AxeRecherche.objects.all()
    publications = PublicationRecherche.objects.order_by('-date_publication')[:5]
    
    # Préparer les domaines pour chaque publication
    for pub in publications:
        pub.domaines_list = pub.domaines.split(",")  # Diviser les domaines en une liste

    return render(request, 'search/centre_recherche.html', {
        'axes_recherche': axes_recherche,
        'publications': publications
    })

    
def publications_list(request):
    publications = PublicationRecherche.objects.all()
    
    # Préparer les domaines pour chaque publication
    for pub in publications:
        pub.domaines_list = pub.domaines.split(",")  # Diviser les domaines en une liste

    return render(request, 'search/publications.html', {'publications': publications})


def recherche(request):
    return render(request, 'search/recherche.html')






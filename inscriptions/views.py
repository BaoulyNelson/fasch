from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.messages import get_messages
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.utils import timezone
from django.apps import apps

from .models import (
    Inscription, Etudiant, Evenement, Article, HoraireCours,
    Annonce, Programme, PublicationRecherche, AxeRecherche,
    Livre, Personnel, EtapeAdmission
)
from .forms import CustomUserChangeForm, DemandeAdmissionForm, EtudiantForm, ContactForm
from .search_config import search_config
from inscriptions.utils import ajouter_message



def login_view(request):
    # Supprime les anciens messages avant d'afficher un nouveau
    storage = get_messages(request)
    for _ in storage:
        pass  # Cette boucle vide supprime tous les anciens messages

    # Récupérer 'next' ou rediriger vers 'profile' par défaut
    next_url = request.GET.get("next", "profile")

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(
                    request, f"Bienvenue {username} ! 😊 Vous êtes connecté.")

                if request.POST.get("remember_me"):
                    request.session.set_expiry(1209600)  # 2 semaines

                # Redirige vers next
                return redirect(request.POST.get("next", next_url))
            else:
                messages.error(
                    request, "Nom d'utilisateur ou mot de passe incorrect.")
        else:
            messages.error(request, "Veuillez vérifier vos informations.")
    else:
        form = AuthenticationForm()

    return render(request, "registration/login.html", {"form": form, "next": next_url})


def signup_view(request):
    # Récupérer la page demandée ou rediriger vers 'home' par défaut
    next_url = request.GET.get("next", "home")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Connecter directement après l'inscription
            messages.success(
                request, "Inscription réussie ! 🎉 Bienvenue sur notre plateforme.")

            # Rediriger vers la page prévue
            return redirect(request.POST.get("next", next_url))
        else:
            messages.error(
                request, "Une erreur est survenue lors de l'inscription. Vérifiez les informations.")
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
            ajouter_message(request, 'success',
                            '✅ Votre profil a été mis à jour avec succès.')
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
    articles_list = Article.objects.filter(
        est_active=True).order_by('-date_publication')
    paginator = Paginator(articles_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Événements à venir (prochains événements)
    evenements = Evenement.objects.filter(
        date_debut__gte=timezone.now()).order_by('date_debut')

    # Annonces actives (peut aussi filtrer par date_evenement si nécessaire)
    annonces = Annonce.objects.filter(est_active=True).order_by(
        '-date_publication')  # ou '-date_evenement'

    context = {
        'articles': page_obj,
        'evenements': evenements,
        'annonces': annonces,
        'now': timezone.now(),
    }

    return render(request, 'index.html', context)


@login_required
def create_profile(request):
    try:
        # Si le profil existe déjà, on retourne où on devait aller
        Etudiant.objects.get(user=request.user)
        next_url = request.session.get("next_url", None)
        if next_url:
            return redirect(next_url)
        return redirect("profile")
    except Etudiant.DoesNotExist:
        pass

    if request.method == "POST":
        form = EtudiantForm(request.POST)
        if form.is_valid():
            etudiant = form.save(commit=False)
            etudiant.user = request.user
            etudiant.save()

            # Récupérer l’URL de retour
            next_url = request.session.pop("next_url", None)
            if next_url:
                return redirect(next_url)
            return redirect("etudiant_profil")
        else:
            messages.error(
                request, "Il y a eu une erreur dans la création de votre profil.")
    else:
        form = EtudiantForm()

    return render(request, "etudiants/create_profile.html", {"form": form})


@login_required
def etudiant_profil(request):
    # On suppose que l'utilisateur est lié à un étudiant via la relation OneToOne
    try:
        etudiant = request.user.etudiant
    except Etudiant.DoesNotExist:
        # ou une autre gestion d'erreur
        return redirect('edit_info_etudiant', etudiant_id=0)

    return render(request, 'etudiants/etudiant_profil.html', {'etudiant': etudiant})


@login_required
def edit_info_etudiant(request, etudiant_id):
    etudiant = get_object_or_404(Etudiant, id=etudiant_id)

    # Vérifie que l'utilisateur connecté est bien celui associé à l'étudiant
    if request.user != etudiant.user:
        raise PermissionDenied(
            "Vous n'avez pas la permission de modifier ce profil.")

    if request.method == 'POST':
        form = EtudiantForm(request.POST, instance=etudiant)
        if form.is_valid():
            form.save()
            ajouter_message(request, 'success',
                            '✅ Votre profil a été mis à jour avec succès.')
            # Redirection vers la page du profil
            return redirect('etudiant_profil')
    else:
        form = EtudiantForm(instance=etudiant)

    return render(request, 'etudiants/edit_info_etudiant.html', {'form': form})


@login_required
def cours_list(request):
    horaires = HoraireCours.objects.select_related('cours', 'professeur').order_by('jour', 'heure_debut')
    paginator = Paginator(horaires, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "cours/liste.html", {"page_obj": page_obj})




@login_required
def cours_detail(request, horaire_id):
    horaire = get_object_or_404(HoraireCours, id=horaire_id)
    inscrit = Inscription.objects.filter(
        etudiant__user=request.user, horaire_cours=horaire).exists()
    return render(request, "cours/detail.html", {"horaire": horaire, "inscrit": inscrit})


@login_required
def mes_cours(request):
    try:
        etudiant = Etudiant.objects.get(user=request.user)
    except Etudiant.DoesNotExist:
        ajouter_message(request, 'error',
                        "Aucun profil étudiant lié à ce compte.")
        return redirect("create_profile")

    inscriptions = Inscription.objects.filter(etudiant=etudiant).select_related(
        "horaire_cours", "horaire_cours__cours", "horaire_cours__professeur")
    return render(request, "cours/mes_cours.html", {"etudiant": etudiant, "inscriptions": inscriptions})


@login_required
def inscription_create(request, horaire_id):
    horaire = get_object_or_404(HoraireCours, id=horaire_id)

    try:
        etudiant = Etudiant.objects.get(user=request.user)
    except Etudiant.DoesNotExist:
        # Sauvegarder l'URL actuelle pour revenir après création du profil
        request.session["next_url"] = request.path
        ajouter_message(
            request, 'error', "Aucun profil étudiant lié à ce compte. Veuillez compléter votre profil.")
        return redirect("create_profile")

    # Continuer avec l'inscription
    inscription = Inscription(etudiant=etudiant, horaire_cours=horaire)

    try:
        inscription.clean()
        inscription.save()
        ajouter_message(request, 'success', "Inscription réussie ! 🎉")
        return redirect("mes_cours")
    except Exception as e:
        ajouter_message(request, 'error', f"Erreur : {e}")
        return redirect("cours_detail", horaire_id=horaire_id)


def programmes(request):
    programmes = Programme.objects.all()  # Récupérer tous les programmes
    # Rendre le template 'programmes.html'
    return render(request, 'programmes/programmes.html', {'programmes': programmes})





def programme_view(request, programme):
    templates = {
        'sociologie': 'programmes/sociologie.html',
        'psychologie': 'programmes/psychologie.html',
        'communication': 'programmes/communication.html',
        'service_social': 'programmes/service_social.html',
    }

    template_name = templates.get(programme)

    if template_name:
        titre_map = {
            'sociologie': 'Sociologie',
            'psychologie': 'Psychologie',
            'communication': 'Communication Sociale',
            'service_social': 'Service Social',
        }
        prog_obj = Programme.objects.filter(titre__iexact=titre_map[programme]).first()
        return render(request, template_name, {'programme': prog_obj})
    else:
        return render(request, '404.html')


def programme_detail(request, pk):
    # La logique de type dynamique peut être utilisée ici
    programme = get_object_or_404(Programme, pk=pk)
    
    # Ici, on renvoie le programme comme détail
    return render(request, 'programmes/program_detail.html', {'programme': programme})


def detail_view(request, type_detail, pk):
    if type_detail == 'article':
        detail = get_object_or_404(Article, pk=pk)
        template_name = 'articles/article_detail.html'
        autres = Article.objects.exclude(pk=pk).order_by('-date_publication')[:3]
        context = {
            'article': detail,
            'autres_articles': autres
        }
    elif type_detail == 'annonce':
        detail = get_object_or_404(Annonce, pk=pk)
        template_name = 'annonces/annonces_details.html'
        context = {'detail': detail}
    elif type_detail == 'evenement':
        detail = get_object_or_404(Evenement, pk=pk)
        template_name = 'evenements/evenement_detail.html'
        context = {'detail': detail}
    else:
        return render(request, '404.html')

    return render(request, template_name, context)


def success_page(request):
    try:
        etudiant = request.user.etudiant  # Si l'utilisateur a un profil 'etudiant'
    except AttributeError:
        # Si l'utilisateur n'a pas de profil étudiant, rediriger ou gérer ce cas
        # Ou une autre page qui indique que l'étudiant n'est pas trouvé
        return redirect('cours')

    return render(request, 'success_page.html', {'etudiant': etudiant})


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Traitement ici (ex : envoi d'email)
            # ← page de confirmation
            return render(request, "contact/contact_success.html")
    else:
        form = ContactForm()

    return render(request, "contact/contact.html", {"form": form})


def contact_success_view(request):
    return render(request, "contact/contact_success.html")


def catalogue(request):
    livres = Livre.objects.all()
    return render(request, 'bibliotheque/catalogue.html', {'livres': livres})


def admission(request, section="demande"):
    etapes = EtapeAdmission.objects.all().order_by('date_debut', 'date_limite')
    section_templates = {
        "demande": "admissions/admission_form.html",
        "conditions": "admissions/conditions.html",
        "calendrier": "admissions/calendrier.html"
    }

    form = DemandeAdmissionForm(request.POST or None)

    if request.method == "POST" and section in ["demande", "all"]:
        if form.is_valid():
            form.save()
            ajouter_message(request, 'success',
                            "Votre demande a bien été envoyée ✅.")
            return redirect('admission_section', section=section)
        else:
            ajouter_message(
                request, 'error', "Veuillez corriger les erreurs dans le formulaire ❌.")

    if section == "all":
        return render(request, 'admissions/admission_all.html', {
            'form': form,
            'etapes': etapes,
        })

    return render(request, 'admissions/admission_base.html', {
        'section_template': section_templates.get(section, "admissions/table_faculte.html"),
        'form': form,
        'etapes': etapes
    })


def recherche_view(request):
    axes_recherche = AxeRecherche.objects.all()
    publications = PublicationRecherche.objects.order_by(
        '-date_publication')[:5]

    # Préparer les domaines pour chaque publication
    for pub in publications:
        pub.domaines_list = pub.domaines.split(
            ",")  # Diviser les domaines en une liste

    return render(request, 'publications/centre_recherche.html', {
        'axes_recherche': axes_recherche,
        'publications': publications
    })


def publications_list(request):
    publications = PublicationRecherche.objects.all()

    # Préparer les domaines pour chaque publication
    for pub in publications:
        pub.domaines_list = pub.domaines.split(
            ",")  # Diviser les domaines en une liste

    return render(request, 'publications/publications.html', {'publications': publications})


def publications_view(request, type_publication):
    # Dictionnaire pour mapper les types de publications aux templates
    templates = {
        'revues_scientifiques': 'publications/revues_scientifiques.html',
        'projets_en_cours': 'publications/projets_en_cours.html',
    }

    template_name = templates.get(type_publication)

    if template_name:  # Vérifie si le type de publication est valide
        return render(request, template_name)
    else:
        # Affiche une page 404 si le type n'est pas trouvé
        return render(request, '404.html')


def recherche(request):
    return render(request, 'search/recherche.html')


def recherche_globale(request):
    query = request.GET.get('q', '')
    resultats = []

    if query:
        for nom_modele, champs in search_config.items():
            try:
                # Remplace 'inscriptions' par le nom de ton app
                modele = apps.get_model('inscriptions', nom_modele)
                filtres = Q()
                for champ in champs:
                    filtres |= Q(**{f"{champ}__icontains": query})
                objets = modele.objects.filter(filtres)

                # Ajouter les objets au résultat global
                # Utilise extend pour ne pas créer une liste de listes
                resultats.extend(objets)
            except Exception as e:
                # Si un modèle ou un champ est invalide, on l'ignore
                print(f"Erreur avec {nom_modele}: {e}")
                continue

    return render(request, 'search/recherche.html', {
        'query': query,
        'resultats': resultats
    })


def apropos_view(request, section):
    # Dictionnaire pour mapper les sections aux templates
    templates = {
        'apropos': 'apropos/apropos.html',
        'histoire': 'apropos/histoire.html',
        'mission_vision': 'apropos/mission_vision.html',
        'administration': 'apropos/administration.html',
        'mot_doyen': 'apropos/mot_doyen.html',
        'galerie': 'apropos/galerie.html',
    }

    template_name = templates.get(section)

    # Vérification si la section nécessite des données supplémentaires
    context = {}
    if section in ['apropos', 'administration']:
        context['personnel'] = Personnel.objects.all()

    if template_name:  # Vérifie si la section est valide
        return render(request, template_name, context)
    else:
        # Affiche une page 404 si la section n'est pas trouvée
        return render(request, '404.html')


def formation_view(request, niveau):
    # Dictionnaire pour mapper les niveaux aux templates
    templates = {
        'licence': 'formations/licence.html',
        'master': 'formations/master.html',
        'formation_continue': 'formations/formation_continue.html',
    }

    template_name = templates.get(niveau)

    if template_name:  # Vérification si le niveau est valide
        return render(request, template_name)
    else:
        # Affiche une page 404 si le niveau n'est pas trouvé
        return render(request, '404.html')


def etudiant_view(request, section):
    # Dictionnaire pour mapper les sections aux templates
    templates = {
        'associations': 'etudiants/association.html',
        'activites': 'etudiants/activite.html',
        'services': 'etudiants/services.html',
        'bourses': 'etudiants/bourse.html',
    }

    template_name = templates.get(section)

    if template_name:  # Vérifie si la section est valide
        return render(request, template_name)
    else:
        # Affiche une page 404 si la section n'est pas trouvée
        return render(request, '404.html')

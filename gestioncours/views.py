from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.utils import timezone
from django.utils.timezone import now
from django.apps import apps
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView,ListView,UpdateView,DeleteView,DetailView
from django.core.exceptions import ImproperlyConfigured
import calendar
from datetime import date
from datetime import datetime, time as dt_time
from django.utils import timezone
from .models import (
    Inscription, Etudiant, Evenement, Article, HoraireCours,
    Annonce, Programme, PublicationRecherche, AxeRecherche,
    Livre, Personnel, EtapeAdmission, Cours, Professeur,EtapeAdmission, DemandeAdmission,Examen,Departement
)
from .forms import (
    CustomUserChangeForm, DemandeAdmissionForm, EtudiantForm,
    ContactForm, CoursForm, ProfesseurForm,
    EvenementForm, AnnonceForm, ArticleForm, InscriptionForm,HoraireCoursForm,EtapeAdmissionForm,PublicationRechercheForm,AxeRechercheForm,PersonnelForm,LivreForm,ProgrammeForm,ExamenForm
)
from .search_config import search_config
from gestioncours.utils import ajouter_message
from django.contrib.messages import get_messages  
from django.contrib.auth.decorators import login_required, user_passes_test



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

    now = timezone.now()

    # Événements à venir
    evenements = Evenement.objects.filter(date_debut__gte=now).order_by('date_debut')

    # Événements passés
    evenements_passes = Evenement.objects.filter(date_debut__lt=now).order_by('-date_debut')

    # Annonces actives
    annonces = Annonce.objects.filter(est_active=True).order_by('-date_publication')

    context = {
        'articles': page_obj,
        'evenements': evenements,
        'evenements_passes': evenements_passes,
        'annonces': annonces,
        'now': now,
    }

    return render(request, 'index.html', context)


@login_required
def create_profile(request):
    # 1) Si un Etudiant existe déjà en base AVEC le même email que l'utilisateur
    #    et que son champ `user` est encore NULL, on l'affecte automatiquement.
    try:
        etu = Etudiant.objects.get(email=request.user.email, user__isnull=True)
        etu.user = request.user
        etu.save()
    except Etudiant.DoesNotExist:
        pass

    # 2) Si le profil est déjà lié à ce user, on le redirige directement
    try:
        Etudiant.objects.get(user=request.user)
        next_url = request.session.get("next_url")
        if next_url:
            return redirect(next_url)
        return redirect("profile")
    except Etudiant.DoesNotExist:
        pass

    # 3) Sinon, on affiche le formulaire de création comme avant
    if request.method == "POST":
        form = EtudiantForm(request.POST)
        if form.is_valid():
            etudiant = form.save(commit=False)
            etudiant.user = request.user
            etudiant.save()
            next_url = request.session.pop("next_url", None)
            if next_url:
                return redirect(next_url)
            return redirect("etudiant_profil")
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
def list_cours(request, session=None):
    # 1) on récupère tout
    qs = HoraireCours.objects.select_related('cours', 'professeur') \
    .order_by('cours__session', 'jour', 'heure_debut')

    # 2) si `session` est "session1" ou "session2", on filtre
    if session in ("session1", "session2"):
        qs = qs.filter(cours__session=session)

    # 3) pagination
    paginator  = Paginator(qs, 9)
    page_obj   = paginator.get_page(request.GET.get("page"))

    # 4) préparer un libellé pour le template
    if session == "session1":
        label = "Session 1"
    elif session == "session2":
        label = "Session 2"
    else:
        label = "Toutes les sessions"

    return render(request, "cours/liste.html", {
        "page_obj":    page_obj,
        "session":     session,   # None, "session1" ou "session2"
        "session_label": label,   # libellé lisible
    })




@login_required
def cours_detail(request, horaire_id):
    horaire = get_object_or_404(HoraireCours, id=horaire_id)
    inscrit = Inscription.objects.filter(
        etudiant__user=request.user, horaire_cours=horaire).exists()
    return render(request, "cours/detail.html", {"horaire": horaire, "inscrit": inscrit})


@login_required
def cours_par_session(request, session):
    horaires = HoraireCours.objects.select_related('cours', 'professeur') \
        .filter(cours__session=session) \
        .order_by('jour', 'heure_debut')

    paginator = Paginator(horaires, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "cours/liste.html", {
        "page_obj": page_obj,
        "session": session  # optionnel pour afficher le titre de la session dans le template
    })



@login_required
def mes_cours(request):
    # Récupération du profil Étudiant
    try:
        etudiant = Etudiant.objects.get(user=request.user)
    except Etudiant.DoesNotExist:
        ajouter_message(request, 'error', "Aucun profil étudiant lié à ce compte")
        return redirect("create_profile")

    # On récupère toutes les inscriptions associées, avec join pour optimiser
    inscriptions = (
        Inscription.objects.filter(etudiant=etudiant)
        .select_related("horaire_cours", "horaire_cours__cours", "horaire_cours__professeur")
    )

    return render(request, "cours/mes_cours.html", {
        "etudiant": etudiant,
        "inscriptions": inscriptions,
    })



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
    programmes = Programme.objects.all()  # 
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
    return render(request, 'programmes/detail_programme.html', {'programme': programme})






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
    publications = PublicationRecherche.objects.order_by('-date_publication')[:5]

    return render(request, 'publications/centre_recherche.html', {
        'axes_recherche': axes_recherche,
        'publications': publications
    })


def publications_list(request):
    publications = PublicationRecherche.objects.all()

    return render(request, 'publications/publications.html', {
        'publications': publications
    })


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
                # Remplace 'gestioncours' par le nom de ton app
                modele = apps.get_model('gestioncours', nom_modele)
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




from django.utils import timezone
from django.db.models import Count

# 1. Vérification du staff
def is_staff_user(user):
    return user.is_staff

# 2. Vue dashboard
@login_required
@user_passes_test(is_staff_user)
def dashboard_admin(request):

    # Comptages globaux
    context = {
        'nombre_etudiants': Etudiant.objects.count(),
        'nombre_cours': Cours.objects.count(),
        'nombre_professeurs': Professeur.objects.count(),
        'nombre_horaires': HoraireCours.objects.count(), 
        'nombre_inscriptions': Inscription.objects.count(),
        'nombre_programmes': Programme.objects.count(),
        'nombre_axes': AxeRecherche.objects.count(),
        'nombre_publications': PublicationRecherche.objects.count(),
        'nombre_livres': Livre.objects.count(),
        'nombre_personnel': Personnel.objects.count(),
        'nombre_etapes_admission': EtapeAdmission.objects.count(),
        'nombre_demandes_admission': DemandeAdmission.objects.count(),
        'nombre_evenements': Evenement.objects.count(),
        'nombre_annonces': Annonce.objects.count(),
        'nombre_articles': Article.objects.count(),
        'nombre_examens': Examen.objects.count(),
    }

    # Listes récentes / à venir
    context.update({
        'evenements_a_venir': Evenement.objects
            .filter(date_debut__gte=timezone.now())
            .order_by('date_debut')[:5],
        'dernieres_annonces': Annonce.objects
            .order_by('-date_publication')[:5],
        'derniers_articles': Article.objects
            .order_by('-date_publication')[:5],
    })

    # Listes détaillées pour onglets “Gestion”
    context.update({
        'etudiants': Etudiant.objects.all().order_by('nom', 'prenom'),
        'cours_list': Cours.objects.all().order_by('nom'),
        'professeurs': Professeur.objects.all().order_by('nom', 'prenom'),
        'horaires': HoraireCours.objects.all().order_by('jour', 'heure_debut'),

        'programmes': Programme.objects.all().order_by('titre'),
        'axes': AxeRecherche.objects.all().order_by('titre'),
        'publications': PublicationRecherche.objects.all().order_by('-date_publication'),
        'livres': Livre.objects.all().order_by('titre'),
        'personnel': Personnel.objects.all().order_by('poste', 'nom'),
        'etapes_admission': EtapeAdmission.objects.all().order_by('date_debut'),
        'demandes_admission': DemandeAdmission.objects.all().order_by('-date_envoi'),
        'examens': Examen.objects.all().order_by('date'),
    })

    # Formulaires pour modals
    context['inscription_form'] = InscriptionForm()
    context['horaire_form']    = HoraireCoursForm()
    context['programme_form']  = ProgrammeForm()

    # Départements pour selects
    context['departements']= Departement.objects.all().order_by('nom')
    
    # Inscriptions (pour tableau)
    context['inscriptions'] = Inscription.objects.select_related('etudiant', 'horaire_cours').all().order_by('-pk')

    # Poste choices
    context['poste_choices'] = Personnel.POSTE_CHOICES

    # 1️⃣ Graphique des inscriptions par mois (inchangé)
    current_year = timezone.now().year
    inscriptions = Inscription.objects.filter(date_inscription__year=current_year)

    inscriptions_by_month = (
        inscriptions
        .values_list('date_inscription__month')
        .annotate(total=Count('id'))
        .order_by('date_inscription__month')
    )

    months = list(range(1, 13))
    inscriptions_data = {month: 0 for month in months}
    for month, total in inscriptions_by_month:
        inscriptions_data[month] = total

    context['inscriptions_chart_data'] = list(inscriptions_data.values())

    # 2️⃣ Activité récente (normalisation des dates pour éviter le TypeError)
    recent_activities = []

    # Helper : rendre un objet date/datetime en tz-aware datetime
    def as_datetime(value):
        """
        value peut être:
        - un datetime (aware ou naive)
        - une date (datetime.date)
        Retourne un datetime tz-aware.
        """
        if value is None:
            return timezone.make_aware(datetime.min.replace(year=1970))
        if isinstance(value, datetime):
            # si naive -> rendre aware avec timezone courant
            if timezone.is_naive(value):
                return timezone.make_aware(value, timezone.get_current_timezone())
            return value
        # si c'est une date (datetime.date)
        # on prend min time (00:00) et on rend aware
        return timezone.make_aware(datetime.combine(value, dt_time.min), timezone.get_current_timezone())

    # Inscription récentes (utilise date_inscription, qui est DateTimeField)
    for ins in Inscription.objects.select_related('etudiant', 'horaire_cours').order_by('-date_inscription')[:8]:
        etu = ins.etudiant
        recent_activities.append({
            'type': 'student',
            'title': 'Nouvel étudiant inscrit',
            'description': f"{etu.prenom} {etu.nom} a été inscrit à {ins.horaire_cours.cours.nom}",
            'created_at': as_datetime(ins.date_inscription)
        })

    # Événements récents (date_debut est DateTimeField)
    for event in Evenement.objects.order_by('-date_debut')[:8]:
        recent_activities.append({
            'type': 'event',
            'title': 'Événement publié',
            'description': event.titre,
            'created_at': as_datetime(event.date_debut)
        })

    # Publications récentes (date_publication est DateField) -> normaliser en datetime aware
    for pub in PublicationRecherche.objects.order_by('-date_publication')[:8]:
        recent_activities.append({
            'type': 'publication',
            'title': 'Nouvelle publication',
            'description': pub.titre,
            'created_at': as_datetime(pub.date_publication)
        })

    # Trier toutes activités par date décroissante et garder top 5
    recent_activities.sort(key=lambda x: x['created_at'], reverse=True)
    context['recent_activities'] = recent_activities[:5]

    return render(request, 'admin/dashboard.html', context)




# Classe générique
class CreateWithMessage(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Vue générique pour créer un objet,
    afficher un message de succès et rediriger vers la liste.
    """
    success_url_name = None  # Nom de l'URL de la liste
    success_message = None   # Message de succès

    def get_success_url(self):
        if not self.success_url_name:
            raise ImproperlyConfigured(
                "Vous devez définir success_url_name dans la sous-classe"
            )
        return reverse_lazy(self.success_url_name)


# Sous-classes pour chaque modèle

class EtudiantCreate(CreateWithMessage):
    model = Etudiant
    form_class = EtudiantForm
    template_name = 'admin/etudiant/etudiant_form.html'
    success_message = "L'étudiant a été ajouté avec succès."
    success_url_name = "etudiants_list"


class CoursCreate(CreateWithMessage):
    model = Cours
    form_class = CoursForm
    template_name = 'admin/cours/cours_form.html'
    success_message = "Le cours a été ajouté avec succès."
    success_url_name = "cours_list"


class ProfesseurCreate(CreateWithMessage):
    model = Professeur
    form_class = ProfesseurForm
    template_name = 'admin/professeur/professeur_form.html'
    success_message = "Le professeur a été ajouté avec succès."
    success_url_name = "professeurs_list"


class InscriptionCreate(CreateWithMessage):
    model = Inscription
    form_class = InscriptionForm
    template_name = 'admin/inscription/inscription_form.html'
    success_message = "Inscription créée."
    success_url_name = "inscriptions_list"


class HoraireCoursCreate(CreateWithMessage):
    model = HoraireCours
    form_class = HoraireCoursForm
    template_name = 'admin/horaire/horaire_form.html'
    success_message = "Horaire ajouté."
    success_url_name = "horaires_list"


class ArticleCreate(CreateWithMessage):
    model = Article
    form_class = ArticleForm
    template_name = 'admin/article/article_form.html'
    success_message = "Article ajouté."
    success_url_name = "articles_list"


class EvenementCreate(CreateWithMessage):
    model = Evenement
    form_class = EvenementForm
    template_name = 'admin/evenement/evenement_form.html'
    success_message = "Événement ajouté."
    success_url_name = "evenements_list"


class AnnonceCreate(CreateWithMessage):
    model = Annonce
    form_class = AnnonceForm
    template_name = 'admin/annonce/annonce_form.html'
    success_message = "Annonce ajoutée."
    success_url_name = "annonces_list"


class ProgrammeCreate(CreateWithMessage):
    model = Programme
    form_class = ProgrammeForm
    template_name = 'admin/programme/programme_form.html'
    success_message = "Programme ajouté."
    success_url_name = "programmes_list"


class AxeRechercheCreate(CreateWithMessage):
    model = AxeRecherche
    form_class = AxeRechercheForm
    template_name = 'admin/axe/axe_form.html'
    success_message = "Axe de recherche ajouté."
    success_url_name = "axes_list"


class PublicationRechercheCreate(CreateWithMessage):
    model = PublicationRecherche
    form_class = PublicationRechercheForm
    template_name = 'admin/publication/publication_form.html'
    success_message = "Publication ajoutée."
    success_url_name = "publications_list"


class LivreCreate(CreateWithMessage):
    model = Livre
    form_class = LivreForm
    template_name = 'admin/livre/livre_form.html'
    success_message = "Livre ajouté."
    success_url_name = "livres_list"


class PersonnelCreate(CreateWithMessage):
    model = Personnel
    form_class = PersonnelForm
    template_name = 'admin/personnel/personnel_form.html'
    success_message = "Membre du personnel ajouté."
    success_url_name = "personnels_list"


class EtapeAdmissionCreate(CreateWithMessage):
    model = EtapeAdmission
    form_class = EtapeAdmissionForm
    template_name = 'admin/etape/etape_admission_form.html'
    success_message = "Étape d'admission ajoutée."
    success_url_name = "etapes_admission_list"


class DemandeAdmissionCreate(CreateWithMessage):
    model = DemandeAdmission
    form_class = DemandeAdmissionForm
    template_name = 'admin/demande/demande_admission_form.html'
    success_message = "Demande d'admission ajoutée."
    success_url_name = "demandes_admission_list"

class ExamenCreate(CreateWithMessage):
    model = Examen
    form_class = ExamenForm
    template_name = 'admin/examen/examen_form.html'
    success_message = "L'examen « %(titre)s » a été créé avec succès."
    success_url_name = "examens_list"
    
# ------------------ Étudiants ------------------
class EtudiantListView(ListView):
    model = Etudiant
    template_name = "admin/etudiant/list.html"
    context_object_name = "etudiants"
    ordering = ['-date_creation']  # tri décroissant
    paginate_by = 20  # <-- 10 étudiants par page


# ------------------ Cours ------------------
class CoursListView(ListView):
    model = Cours
    template_name = "admin/cours/list.html"
    context_object_name = "cours"
    ordering = ['-date_creation']  # <- tri décroissant, du plus récent au plus ancien
    paginate_by = 20  # <-- 10 étudiants par page
    

# ------------------ Professeurs ------------------
class ProfesseurListView(ListView):
    model = Professeur
    template_name = "admin/professeur/list.html"
    context_object_name = "professeurs"
    ordering = ['-date_creation']  # <- tri décroissant, du plus récent au plus ancien
    paginate_by = 20  # <-- 10 étudiants par page
    

# ------------------ Inscriptions ------------------
class InscriptionListView(ListView):
    model = Inscription
    template_name = "admin/inscription/list.html"
    context_object_name = "inscriptions"
    ordering = ['-date_inscription']  # <- tri décroissant, du plus récent au plus ancien
    paginate_by = 20  # <-- 10 étudiants par page
    

# ------------------ Horaires ------------------
class HoraireCoursListView(ListView):
    model = HoraireCours
    template_name = "admin/horaire/list.html"
    context_object_name = "horaires"
    ordering = ['-date_creation']  # <- tri décroissant, du plus récent au plus ancien
    paginate_by = 20  # <-- 10 étudiants par page

# ------------------ Articles ------------------
class ArticleListView(ListView):
    model = Article
    template_name = "admin/article/list.html"
    context_object_name = "articles"
    ordering = ['-date_publication']  # <- tri décroissant, du plus récent au plus ancien
    paginate_by = 10  # <-- 10 étudiants par page
    

# ------------------ Événements ------------------
class EvenementListView(ListView):
    model = Evenement
    template_name = "admin/evenement/list.html"
    context_object_name = "evenements"
    ordering = ['-date_creation']  # <- tri décroissant, du plus récent au plus ancien
    paginate_by = 10  # <-- 10 étudiants par page
    

# ------------------ Annonces ------------------
class AnnonceListView(ListView):
    model = Annonce
    template_name = "admin/annonce/list.html"
    context_object_name = "annonces"
    ordering = ['-date_publication']  # <- tri décroissant, du plus récent au plus ancien
    paginate_by = 10  # <-- 10 étudiants par page
    

# ------------------ Programmes ------------------
class ProgrammeListView(ListView):
    model = Programme
    template_name = "admin/programme/list.html"
    context_object_name = "programmes"
    ordering = ['-date_creation']  # <- tri décroissant, du plus récent au plus ancien
    paginate_by = 10  # <-- 10 étudiants par page
    

# ------------------ Axes de recherche ------------------
class AxeRechercheListView(ListView):
    model = AxeRecherche
    template_name = "admin/axe/list.html"
    context_object_name = "axes"
    paginate_by = 10  # <-- 10 étudiants par page

# ------------------ Publications ------------------
class PublicationRechercheListView(ListView):
    model = PublicationRecherche
    template_name = "admin/publication/list.html"
    context_object_name = "publications"
    paginate_by = 10  # <-- 10 étudiants par page
    ordering = ['-date_publication']  # <- tri décroissant, du plus récent au plus ancien
    

# ------------------ Livres ------------------
class LivreListView(ListView):
    model = Livre
    template_name = "admin/livre/list.html"
    context_object_name = "livres"
    ordering = ['-date_creation']  # <- tri décroissant, du plus récent au plus ancien
    paginate_by = 10  # <-- 10 étudiants par page
    

# ------------------ Personnel ------------------
class PersonnelListView(ListView):
    model = Personnel
    template_name = "admin/personnel/list.html"
    context_object_name = "personnels"
    ordering = ['-date_creation']  # <- tri décroissant, du plus récent au plus ancien
    paginate_by = 10  # <-- 10 étudiants par page
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departements'] = Departement.objects.all()
        context['postes'] = Personnel.POSTE_CHOICES
        return context
# ------------------ Étapes d'admission ------------------
class EtapeAdmissionListView(ListView):
    model = EtapeAdmission
    template_name = "admin/etape/list.html"
    context_object_name = "etapes_admission"
    ordering = ['-date_creation']  # <- tri décroissant, du plus récent au plus ancien
    paginate_by = 10  # <-- 10 étudiants par page
    

# ------------------ Demandes d'admission ------------------
class DemandeAdmissionListView(ListView):
    model = DemandeAdmission
    template_name = "admin/demande/list.html"
    context_object_name = "demandes_admission"
    ordering = ['-date_creation']  # <- tri décroissant, du plus récent au plus ancien
    paginate_by = 10  # <-- 10 étudiants par page
    

# ------------------ Examens ------------------
class ExamenListView(ListView):
    model = Examen
    template_name = "admin/examen/list.html"
    context_object_name = "examens"
    paginate_by = 10  # <-- 10 étudiants par page
    

# Classe générique pour UpdateView
class UpdateWithMessage(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Vue générique pour modifier un objet,
    afficher un message de succès et rediriger vers la liste.
    """
    success_url_name = None  # Nom de l'URL de la liste
    success_message = None   # Message de succès

    def get_success_url(self):
        if not self.success_url_name:
            raise ImproperlyConfigured(
                "Vous devez définir success_url_name dans la sous-classe"
            )
        return reverse_lazy(self.success_url_name)


# Sous-classes pour chaque modèle
class ExamenUpdate(UpdateWithMessage):
    model = Examen
    form_class = ExamenForm
    template_name = 'admin/examen/examen_form.html'
    success_message = "L'examen « %(titre)s » a été mis à jour."
    success_url_name = "examens_list"


class EtudiantUpdate(UpdateWithMessage):
    model = Etudiant
    form_class = EtudiantForm
    template_name = 'admin/etudiant/etudiant_form.html'
    success_message = "Les informations de l'étudiant ont été modifiées avec succès."
    success_url_name = "etudiants_list"


class CoursUpdate(UpdateWithMessage):
    model = Cours
    form_class = CoursForm
    template_name = 'admin/cours/cours_form.html'
    success_message = "Les informations du cours ont été modifiées avec succès."
    success_url_name = "cours_list"


class ProfesseurUpdate(UpdateWithMessage):
    model = Professeur
    form_class = ProfesseurForm
    template_name = 'admin/professeur/professeur_form.html'
    success_message = "Le professeur a été mis à jour avec succès."
    success_url_name = "professeurs_list"


class InscriptionUpdate(UpdateWithMessage):
    model = Inscription
    form_class = InscriptionForm
    template_name = 'admin/inscription/inscription_form.html'
    success_message = "Inscription modifiée."
    success_url_name = "inscriptions_list"


class HoraireCoursUpdate(UpdateWithMessage):
    model = HoraireCours
    form_class = HoraireCoursForm
    template_name = 'admin/horaire/horaire_form.html'
    success_message = "Horaire modifié."
    success_url_name = "horaires_list"


class ArticleUpdate(UpdateWithMessage):
    model = Article
    form_class = ArticleForm
    template_name = 'admin/article/article_form.html'
    success_message = "Article modifié."
    success_url_name = "articles_list"


class EvenementUpdate(UpdateWithMessage):
    model = Evenement
    form_class = EvenementForm
    template_name = 'admin/evenement/evenement_form.html'
    success_message = "Événement modifié."
    success_url_name = "evenements_list"


class AnnonceUpdate(UpdateWithMessage):
    model = Annonce
    form_class = AnnonceForm
    template_name = 'admin/annonce/annonce_form.html'
    success_message = "Annonce modifiée."
    success_url_name = "annonces_list"


class ProgrammeUpdate(UpdateWithMessage):
    model = Programme
    form_class = ProgrammeForm
    template_name = 'admin/programme/programme_form.html'
    success_message = "Programme modifié."
    success_url_name = "programmes_list"


class AxeRechercheUpdate(UpdateWithMessage):
    model = AxeRecherche
    form_class = AxeRechercheForm
    template_name = 'admin/axe/axe_form.html'
    success_message = "Axe de recherche modifié."
    success_url_name = "axes_list"


class PublicationRechercheUpdate(UpdateWithMessage):
    model = PublicationRecherche
    form_class = PublicationRechercheForm
    template_name = 'admin/publication/publication_form.html'
    success_message = "Publication modifiée."
    success_url_name = "publications_list"


class LivreUpdate(UpdateWithMessage):
    model = Livre
    form_class = LivreForm
    template_name = 'admin/livre/livre_form.html'
    success_message = "Livre modifié."
    success_url_name = "livres_list"


class PersonnelUpdate(UpdateWithMessage):
    model = Personnel
    form_class = PersonnelForm
    template_name = 'admin/personnel/personnel_form.html'
    success_message = "Membre du personnel modifié."
    success_url_name = "personnels_list"


class EtapeAdmissionUpdate(UpdateWithMessage):
    model = EtapeAdmission
    form_class = EtapeAdmissionForm
    template_name = 'admin/etape/etape_admission_form.html'
    success_message = "Étape d'admission modifiée."
    success_url_name = "etapes_admission_list"


class DemandeAdmissionUpdate(UpdateWithMessage):
    model = DemandeAdmission
    form_class = DemandeAdmissionForm
    template_name = 'admin/demande/demande_admission_form.html'
    success_message = "Demande d'admission modifiée."
    success_url_name = "demandes_admission_list"
#detail
class DetailWithLogin(LoginRequiredMixin, DetailView):
    """
    Vue générique pour afficher le détail d'un objet.
    """

# Sous-classes pour chaque modèle
class ExamenDetail(DetailWithLogin):
    model = Examen
    template_name = 'admin/examen/examen_detail.html'
    context_object_name = 'examen'
    
class EtudiantDetail(DetailWithLogin):
    model = Etudiant
    template_name = 'admin/etudiant/etudiant_detail.html'
    context_object_name = 'etudiant'

class CoursDetail(DetailWithLogin):
    model = Cours
    template_name = 'admin/cours/cours_detail.html'
    context_object_name = 'cours'

class ProfesseurDetail(DetailWithLogin):
    model = Professeur
    template_name = 'admin/professeur/professeur_detail.html'
    context_object_name = 'professeur'

class InscriptionDetail(DetailWithLogin):
    model = Inscription
    template_name = 'admin/inscription/inscription_detail.html'
    context_object_name = 'inscription'

class HoraireCoursDetail(DetailWithLogin):
    model = HoraireCours
    template_name = 'admin/horaire/horaire_detail.html'
    context_object_name = 'horaire'

class ArticleDetail(DetailWithLogin):
    model = Article
    template_name = 'admin/article/article_detail.html'
    context_object_name = 'article'

class EvenementDetail(DetailWithLogin):
    model = Evenement
    template_name = 'admin/evenement/evenement_detail.html'
    context_object_name = 'evenement'

class AnnonceDetail(DetailWithLogin):
    model = Annonce
    template_name = 'admin/annonce/annonce_detail.html'
    context_object_name = 'annonce'
    

class ProgrammeDetail(DetailWithLogin):
    model = Programme
    template_name = 'admin/programme/programme_detail.html'
    context_object_name = 'programme'

class AxeRechercheDetail(DetailWithLogin):
    model = AxeRecherche
    template_name = 'admin/axe/axe_detail.html'
    context_object_name = 'axe'

class PublicationRechercheDetail(DetailWithLogin):
    model = PublicationRecherche
    template_name = 'admin/publication/publication_detail.html'
    context_object_name = 'publication'

class LivreDetail(DetailWithLogin):
    model = Livre
    template_name = 'admin/livre/livre_detail.html'
    context_object_name = 'livre'

class PersonnelDetail(DetailWithLogin):
    model = Personnel
    template_name = 'admin/personnel/personnel_detail.html'
    context_object_name = 'personnel'

class EtapeAdmissionDetail(DetailWithLogin):
    model = EtapeAdmission
    template_name = 'admin/etape/etape_admission_detail.html'
    context_object_name = 'etape_admission'

class DemandeAdmissionDetail(DetailWithLogin):
    model = DemandeAdmission
    template_name = 'admin/demande/demande_admission_detail.html'
    context_object_name = 'demande_admission'
    
    
#pour supprimer
# Classe générique pour DeleteView
class DeleteWithMessage(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    """
    Vue générique pour supprimer un objet,
    afficher un message de succès et rediriger vers la liste.
    """
    success_url_name = None  # Nom de l'URL de la liste
    success_message = None   # Message de succès

    def get_success_url(self):
        if not self.success_url_name:
            raise ImproperlyConfigured(
                "Vous devez définir success_url_name dans la sous-classe"
            )
        return reverse_lazy(self.success_url_name)


# Sous-classes pour chaque modèle
class ExamenDelete(DeleteWithMessage):
    model = Examen
    template_name = 'admin/examen/examen_confirm_delete.html'
    success_message = "L'examen a bien été supprimé."
    success_url_name = "examens_list"


class EtudiantDelete(DeleteWithMessage):
    model = Etudiant
    template_name = 'admin/etudiant/etudiant_confirm_delete.html'
    success_message = "L'étudiant a été supprimé avec succès."
    success_url_name = "etudiants_list"


class CoursDelete(DeleteWithMessage):
    model = Cours
    template_name = 'admin/cours/cours_confirm_delete.html'
    success_message = "Le cours a été supprimé avec succès."
    success_url_name = "cours_list"


class ProfesseurDelete(DeleteWithMessage):
    model = Professeur
    template_name = 'admin/professeur/professeur_confirm_delete.html'
    success_message = "Le professeur a été supprimé avec succès."
    success_url_name = "professeurs_list"


class InscriptionDelete(DeleteWithMessage):
    model = Inscription
    template_name = 'admin/inscription/inscription_confirm_delete.html'
    success_message = "Inscription supprimée."
    success_url_name = "inscriptions_list"


class HoraireCoursDelete(DeleteWithMessage):
    model = HoraireCours
    template_name = 'admin/horaire/horaire_confirm_delete.html'
    success_message = "Horaire supprimé."
    success_url_name = "horaires_list"


class ArticleDelete(DeleteWithMessage):
    model = Article
    template_name = 'admin/article/article_confirm_delete.html'
    success_message = "Article supprimé."
    success_url_name = "articles_list"


class EvenementDelete(DeleteWithMessage):
    model = Evenement
    template_name = 'admin/evenement/evenement_confirm_delete.html'
    success_message = "Événement supprimé."
    success_url_name = "evenements_list"


class AnnonceDelete(DeleteWithMessage):
    model = Annonce
    template_name = 'admin/annonce/annonce_confirm_delete.html'
    success_message = "Annonce supprimée."
    success_url_name = "annonces_list"


class ProgrammeDelete(DeleteWithMessage):
    model = Programme
    template_name = 'admin/programme/programme_confirm_delete.html'
    success_message = "Programme supprimé."
    success_url_name = "programmes_list"


class AxeRechercheDelete(DeleteWithMessage):
    model = AxeRecherche
    template_name = 'admin/axe/axe_confirm_delete.html'
    success_message = "Axe de recherche supprimé."
    success_url_name = "axes_list"


class PublicationRechercheDelete(DeleteWithMessage):
    model = PublicationRecherche
    template_name = 'admin/publication/publication_confirm_delete.html'
    success_message = "Publication supprimée."
    success_url_name = "publications_list"


class LivreDelete(DeleteWithMessage):
    model = Livre
    template_name = 'admin/livre/livre_confirm_delete.html'
    success_message = "Livre supprimé."
    success_url_name = "livres_list"


class PersonnelDelete(DeleteWithMessage):
    model = Personnel
    template_name = 'admin/personnel/personnel_confirm_delete.html'
    success_message = "Membre du personnel supprimé."
    success_url_name = "personnels_list"


class EtapeAdmissionDelete(DeleteWithMessage):
    model = EtapeAdmission
    template_name = 'admin/etape/etape_admission_confirm_delete.html'
    success_message = "Étape d'admission supprimée."
    success_url_name = "etapes_admission_list"


class DemandeAdmissionDelete(DeleteWithMessage):
    model = DemandeAdmission
    template_name = 'admin/demande/demande_admission_confirm_delete.html'
    success_message = "Demande d'admission supprimée."
    success_url_name = "demandes_admission_list"
    



def calendrier_examen(request, annee=None):
    """
    Affiche une vue annuelle (12 mois) des examens.
    Variables en français : annee, mois, mois_donnees, evenements_par_date, aujourd
    """
    aujourd = timezone.localdate()
    annee = int(annee) if annee else aujourd.year

    cal = calendar.Calendar(firstweekday=0)  # lundi = 0

    # Récupère tous les examens de l'année (une seule requête)
    examens_annee = Examen.objects.filter(date__year=annee).order_by('date')

    # Groupe les examens par date (clé: datetime.date)
    evenements_par_date = {}
    for ex in examens_annee:
        evenements_par_date.setdefault(ex.date, []).append(ex)

    # noms des mois en français courts (tu peux les modifier)
    mois_noms = ['janv.', 'févr.', 'mars', 'avr.', 'mai', 'juin',
                 'juil.', 'août', 'sept.', 'oct.', 'nov.', 'déc.']

    # Construire la structure des 12 mois
    mois_donnees = []
    for m in range(1, 13):
        semaines = cal.monthdatescalendar(annee, m)
        # semaines : liste de semaines, chaque semaine = liste de 7 objets date
        semaines_cells = []
        for semaine in semaines:
            jours = []
            # dans la boucle construisant les jours (remplace ton code actuel de construction de jours)
            for d in semaine:
                jours.append({
                    'date': d,
                    'day': d.day,
                    'est_mois_courant': d.month == m,
                    'evenements': evenements_par_date.get(d, []),
                    'est_aujourd': d == aujourd,
                    'weekday': d.weekday(),  # 0=Lun ... 6=Dim -> utile pour colorer le dimanche
                })

            semaines_cells.append(jours)
        mois_donnees.append({
            'numero': m,
            'nom': mois_noms[m - 1],
            'semaines': semaines_cells,
        })

    contexte = {
        'annee': annee,
        'mois_donnees': mois_donnees,
        'aujourd': aujourd,
        'jours_noms': ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'],
        'annee_precedente': annee - 1,
        'annee_suivante': annee + 1,
        # examens à venir globaux (optionnel)
        'examens_a_venir': Examen.objects.filter(date__gt=aujourd).order_by('date')[:10],
    }

    return render(request, 'calendrier/annee.html', contexte)



# Articles
def detail_article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    
    # Récupérer les autres articles, sauf l'article actuel
    autres_articles = Article.objects.exclude(id=article.id).order_by('-date_publication')[:5]  # Tu peux ajuster le nombre

    return render(request, 'articles/article_detail.html', {
        'article': article,
        'autres_articles': autres_articles
    })


def liste_evenements(request):
    evenements = Evenement.objects.all().order_by('-date_debut')  # du plus récent au plus ancien
    return render(request, 'evenements/evenements_list.html', {'evenements': evenements})


# Evenements
def detail_evenement(request, slug):
    evenement = get_object_or_404(Evenement, slug=slug)
    return render(request, 'evenements/evenement_detail.html', {'evenement': evenement})


# Annonces
def detail_annonce(request, slug):
    annonce = get_object_or_404(Annonce, slug=slug)
    return render(request, 'annonces/annonces_details.html', {'annonce': annonce})



def global_search(request):
    q = request.GET.get('q', '').strip()
    limit_per_model = 10  # ajustable

    results = {}
    total_counts = {}

    if q:
        # Étudiants
        qs = Etudiant.objects.select_related('departement').filter(
            Q(prenom__icontains=q) |
            Q(nom__icontains=q) |
            Q(email__icontains=q) |
            Q(telephone__icontains=q)
        )
        total_counts['etudiants'] = qs.count()
        results['etudiants'] = qs[:limit_per_model]

        # Cours
        qs = Cours.objects.filter(
            Q(code__icontains=q) |
            Q(nom__icontains=q)
        )
        total_counts['cours'] = qs.count()
        results['cours'] = qs[:limit_per_model]

        # Professeurs
        qs = Professeur.objects.filter(
            Q(prenom__icontains=q) |
            Q(nom__icontains=q) |
            Q(email__icontains=q) |
            Q(specialite__icontains=q)
        )
        total_counts['professeurs'] = qs.count()
        results['professeurs'] = qs[:limit_per_model]

        # Programmes
        qs = Programme.objects.filter(
            Q(titre__icontains=q) |
            Q(description__icontains=q)
        )
        total_counts['programmes'] = qs.count()
        results['programmes'] = qs[:limit_per_model]

        # Articles
        qs = Article.objects.filter(
            Q(titre__icontains=q) |
            Q(contenu__icontains=q) |
            Q(auteur__icontains=q)
        )
        total_counts['articles'] = qs.count()
        results['articles'] = qs[:limit_per_model]

        # Evenements
        qs = Evenement.objects.filter(
            Q(titre__icontains=q) |
            Q(description__icontains=q) |
            Q(lieu__icontains=q)
        )
        total_counts['evenements'] = qs.count()
        results['evenements'] = qs[:limit_per_model]

        # Annonces
        qs = Annonce.objects.filter(
            Q(titre__icontains=q) |
            Q(contenu__icontains=q) |
            Q(organisateur__icontains=q) |
            Q(lieu__icontains=q)
        )
        total_counts['annonces'] = qs.count()
        results['annonces'] = qs[:limit_per_model]

        # Publications de recherche
        qs = PublicationRecherche.objects.filter(
            Q(titre__icontains=q) |
            Q(auteurs__icontains=q) |
            Q(description__icontains=q) |
            Q(domaines__icontains=q)
        )
        total_counts['publications'] = qs.count()
        results['publications'] = qs[:limit_per_model]

        # Livres
        qs = Livre.objects.filter(
            Q(titre__icontains=q) |
            Q(auteur__icontains=q) |
            Q(resume__icontains=q)
        )
        total_counts['livres'] = qs.count()
        results['livres'] = qs[:limit_per_model]

        # Personnel
        qs = Personnel.objects.filter(
            Q(nom__icontains=q) |
            Q(description__icontains=q) |
            Q(poste__icontains=q)
        )
        total_counts['personnel'] = qs.count()
        results['personnel'] = qs[:limit_per_model]

        # Examens
        qs = Examen.objects.filter(
            Q(titre__icontains=q) |
            Q(description__icontains=q)
        )
        total_counts['examens'] = qs.count()
        results['examens'] = qs[:limit_per_model]

        # Horaires & Inscriptions (si tu veux les inclure)
        qs = HoraireCours.objects.filter(
            Q(jour__icontains=q) |
            Q(cours__nom__icontains=q) |
            Q(professeur__prenom__icontains=q) |
            Q(professeur__nom__icontains=q)
        ).select_related('cours', 'professeur')
        total_counts['horaires'] = qs.count()
        results['horaires'] = qs[:limit_per_model]

        qs = Inscription.objects.filter(
            Q(etudiant__prenom__icontains=q) |
            Q(etudiant__nom__icontains=q) |
            Q(horaire_cours__cours__nom__icontains=q)
        ).select_related('etudiant', 'horaire_cours')
        total_counts['inscriptions'] = qs.count()
        results['inscriptions'] = qs[:limit_per_model]



    context = {
        'query': q,
        'results': results,
        'total_counts': total_counts,
        'limit_per_model': limit_per_model,
    }
    return render(request, 'search/global_search.html', context)

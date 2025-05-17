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
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
import calendar
from datetime import date

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
def cours_list(request, session=None):
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

    # **Ajout du formulaire d'inscription pour le modal**
    context['inscription_form'] = InscriptionForm()
    context['horaire_form']    = HoraireCoursForm()
    
    context['inscriptions'] = Inscription.objects.select_related('etudiant', 'horaire_cours').all().order_by('-pk')
    
    context['poste_choices'] = Personnel.POSTE_CHOICES
    context['programme_form'] = ProgrammeForm() 
    # AJOUT : charger les départements pour le select
    context['departements']= Departement.objects.all().order_by('nom')
    
    return render(request, 'admin/dashboard.html', context)


class CreateWithMessage(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Vue générique pour créer un objet,
    afficher un message de succès et revenir au dashboard.
    """
    success_url = reverse_lazy('dashboard')




class ExamenCreate(CreateWithMessage, SuccessMessageMixin, CreateView):
    model = Examen
    form_class = ExamenForm
    template_name = 'admin/examen_form.html'
    success_message = "L'examen « %(titre)s » a été créé avec succès."
    
    

# Sous-classes pour chaque formulaire
class EtudiantCreate(CreateWithMessage):
    form_class = EtudiantForm
    template_name = 'admin/etudiant_form.html'
    success_message = "L'étudiant a été ajouté avec succès."

class CoursCreate(CreateWithMessage):
    form_class = CoursForm
    template_name = 'admin/cours_form.html'
    success_message = "Le cours a été ajouté avec succès."

class ProfesseurCreate(CreateWithMessage):
    form_class = ProfesseurForm
    template_name = 'admin/professeur_form.html'
    success_message = "Le professeur a été ajouté avec succès."

class InscriptionCreate(CreateWithMessage):
    form_class = InscriptionForm
    template_name = 'admin/inscription_form.html'
    success_message = "Inscription créée."

class HoraireCoursCreate(CreateWithMessage):
    form_class = HoraireCoursForm
    template_name = 'admin/horaire_form.html'
    success_message = "Horaire ajouté."

class ArticleCreate(CreateWithMessage):
    form_class = ArticleForm
    template_name = 'admin/article_form.html'
    success_message = "Article ajouté."

class EvenementCreate(CreateWithMessage):
    form_class = EvenementForm
    template_name = 'admin/evenement_form.html'
    success_message = "Événement ajouté."

class AnnonceCreate(CreateWithMessage):
    form_class = AnnonceForm
    template_name = 'admin/annonce_form.html'
    success_message = "Annonce ajoutée."

class ProgrammeCreate(CreateWithMessage):
    form_class = ProgrammeForm
    template_name = 'admin/programme_form.html'
    success_message = "Programme ajouté."

class AxeRechercheCreate(CreateWithMessage):
    form_class = AxeRechercheForm
    template_name = 'admin/axe_form.html'
    success_message = "Axe de recherche ajouté."

class PublicationRechercheCreate(CreateWithMessage):
    form_class = PublicationRechercheForm
    template_name = 'admin/publication_form.html'
    success_message = "Publication ajoutée."

class LivreCreate(CreateWithMessage):
    form_class = LivreForm
    template_name = 'admin/livre_form.html'
    success_message = "Livre ajouté."

class PersonnelCreate(CreateWithMessage):
    form_class = PersonnelForm
    template_name = 'admin/personnel_form.html'
    success_message = "Membre du personnel ajouté."

class EtapeAdmissionCreate(CreateWithMessage):
    form_class = EtapeAdmissionForm
    template_name = 'admin/etape_admission_form.html'
    success_message = "Étape d'admission ajoutée."

class DemandeAdmissionCreate(CreateWithMessage):
    form_class = DemandeAdmissionForm
    template_name = 'admin/demande_admission_form.html'
    success_message = "Demande d'admission ajoutée."

    #modifier

class UpdateWithMessage(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Vue générique pour modifier un objet,
    afficher un message de succès et revenir au dashboard.
    """
    success_url = reverse_lazy('dashboard')

# Sous-classes pour chaque modèle
class ExamenUpdate(UpdateWithMessage, SuccessMessageMixin, UpdateView):
    model = Examen
    form_class = ExamenForm
    template_name = 'admin/examen_form.html'
    success_message = "L'examen « %(titre)s » a été mis à jour."

class EtudiantUpdate(UpdateWithMessage):
    model = Etudiant
    form_class = EtudiantForm
    template_name = 'admin/etudiant_form.html'
    success_message = "Les informations de l'étudiant ont été modifiées avec succès."

class CoursUpdate(UpdateWithMessage):
    model = Cours
    form_class = CoursForm
    template_name = 'admin/cours_form.html'
    success_message = "Les informations du cours ont été modifiées avec succès."

class ProfesseurUpdate(UpdateWithMessage):
    model = Professeur
    form_class = ProfesseurForm
    template_name = 'admin/professeur_form.html'
    success_message = "Le professeur a été mis à jour avec succès."

class InscriptionUpdate(UpdateWithMessage):
    model = Inscription
    form_class = InscriptionForm
    template_name = 'admin/inscription_form.html'
    success_message = "Inscription modifiée."

class HoraireCoursUpdate(UpdateWithMessage):
    model = HoraireCours
    form_class = HoraireCoursForm
    template_name = 'admin/horaire_form.html'
    success_message = "Horaire modifié."

class ArticleUpdate(UpdateWithMessage):
    model = Article
    form_class = ArticleForm
    template_name = 'admin/article_form.html'
    success_message = "Article modifié."

class EvenementUpdate(UpdateWithMessage):
    model = Evenement
    form_class = EvenementForm
    template_name = 'admin/evenement_form.html'
    success_message = "Événement modifié."

class AnnonceUpdate(UpdateWithMessage):
    model = Annonce
    form_class = AnnonceForm
    template_name = 'admin/annonce_form.html'
    success_message = "Annonce modifiée."

class ProgrammeUpdate(UpdateWithMessage):
    model = Programme
    form_class = ProgrammeForm
    template_name = 'admin/programme_form.html'
    success_message = "Programme modifié."

class AxeRechercheUpdate(UpdateWithMessage):
    model = AxeRecherche
    form_class = AxeRechercheForm
    template_name = 'admin/axe_form.html'
    success_message = "Axe de recherche modifié."

class PublicationRechercheUpdate(UpdateWithMessage):
    model = PublicationRecherche
    form_class = PublicationRechercheForm
    template_name = 'admin/publication_form.html'
    success_message = "Publication modifiée."

class LivreUpdate(UpdateWithMessage):
    model = Livre
    form_class = LivreForm
    template_name = 'admin/livre_form.html'
    success_message = "Livre modifié."

class PersonnelUpdate(UpdateWithMessage):
    model = Personnel
    form_class = PersonnelForm
    template_name = 'admin/personnel_form.html'
    success_message = "Membre du personnel modifié."

class EtapeAdmissionUpdate(UpdateWithMessage):
    model = EtapeAdmission
    form_class = EtapeAdmissionForm
    template_name = 'admin/etape_admission_form.html'
    success_message = "Étape d'admission modifiée."

class DemandeAdmissionUpdate(UpdateWithMessage):
    model = DemandeAdmission
    form_class = DemandeAdmissionForm
    template_name = 'admin/demande_admission_form.html'
    success_message = "Demande d'admission modifiée."


#detail
class DetailWithLogin(LoginRequiredMixin, DetailView):
    """
    Vue générique pour afficher le détail d'un objet.
    """
    # par défaut, context_object_name = '<model>'

# Sous-classes pour chaque modèle
class ExamenDetail(DetailWithLogin):
    model = Examen
    template_name = 'admin/examen_detail.html'
    context_object_name = 'examen'
    
class EtudiantDetail(DetailWithLogin):
    model = Etudiant
    template_name = 'admin/etudiant_detail.html'
    context_object_name = 'etudiant'

class CoursDetail(DetailWithLogin):
    model = Cours
    template_name = 'admin/cours_detail.html'
    context_object_name = 'cours'

class ProfesseurDetail(DetailWithLogin):
    model = Professeur
    template_name = 'admin/professeur_detail.html'
    context_object_name = 'professeur'

class InscriptionDetail(DetailWithLogin):
    model = Inscription
    template_name = 'admin/inscription_detail.html'
    context_object_name = 'inscription'

class HoraireCoursDetail(DetailWithLogin):
    model = HoraireCours
    template_name = 'admin/horaire_detail.html'
    context_object_name = 'horaire'

class ArticleDetail(DetailWithLogin):
    model = Article
    template_name = 'admin/article_detail.html'
    context_object_name = 'article'

class EvenementDetail(DetailWithLogin):
    model = Evenement
    template_name = 'admin/evenement_detail.html'
    context_object_name = 'evenement'

class AnnonceDetail(DetailWithLogin):
    model = Annonce
    template_name = 'admin/annonce_detail.html'
    context_object_name = 'annonce'
    

class ProgrammeDetail(DetailWithLogin):
    model = Programme
    template_name = 'admin/programme_detail.html'
    context_object_name = 'programme'

class AxeRechercheDetail(DetailWithLogin):
    model = AxeRecherche
    template_name = 'admin/axe_detail.html'
    context_object_name = 'axe'

class PublicationRechercheDetail(DetailWithLogin):
    model = PublicationRecherche
    template_name = 'admin/publication_detail.html'
    context_object_name = 'publication'

class LivreDetail(DetailWithLogin):
    model = Livre
    template_name = 'admin/livre_detail.html'
    context_object_name = 'livre'

class PersonnelDetail(DetailWithLogin):
    model = Personnel
    template_name = 'admin/personnel_detail.html'
    context_object_name = 'personnel'

class EtapeAdmissionDetail(DetailWithLogin):
    model = EtapeAdmission
    template_name = 'admin/etape_admission_detail.html'
    context_object_name = 'etape_admission'

class DemandeAdmissionDetail(DetailWithLogin):
    model = DemandeAdmission
    template_name = 'admin/demande_admission_detail.html'
    context_object_name = 'demande_admission'
    
    
#pour supprimer
class DeleteWithMessage(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    """
    Vue générique pour supprimer un objet,
    afficher un message de succès et revenir au dashboard.
    """
    success_url = reverse_lazy('dashboard')

# Sous-classes pour chaque modèle

class ExamenDelete(DeleteWithMessage, SuccessMessageMixin, DeleteView):
    model = Examen
    template_name = 'admin/examen_confirm_delete.html'
    success_message = "L'examen a bien été supprimé."
    
    
class EtudiantDelete(DeleteWithMessage):
    model = Etudiant
    template_name = 'admin/etudiant_confirm_delete.html'
    success_message = "L'étudiant a été supprimé avec succès."

class CoursDelete(DeleteWithMessage):
    model = Cours
    template_name = 'admin/cours_confirm_delete.html'
    success_message = "Le cours a été supprimé avec succès."

class ProfesseurDelete(DeleteWithMessage):
    model = Professeur
    template_name = 'admin/professeur_confirm_delete.html'
    success_message = "Le professeur a été supprimé avec succès."

class InscriptionDelete(DeleteWithMessage):
    model = Inscription
    template_name = 'admin/inscription_confirm_delete.html'
    success_message = "Inscription supprimée."

class HoraireCoursDelete(DeleteWithMessage):
    model = HoraireCours
    template_name = 'admin/horaire_confirm_delete.html'
    success_message = "Horaire supprimé."

class ArticleDelete(DeleteWithMessage):
    model = Article
    template_name = 'admin/article_confirm_delete.html'
    success_message = "Article supprimé."

class EvenementDelete(DeleteWithMessage):
    model = Evenement
    template_name = 'admin/evenement_confirm_delete.html'
    success_message = "Événement supprimé."

class AnnonceDelete(DeleteWithMessage):
    model = Annonce
    template_name = 'admin/annonce_confirm_delete.html'
    success_message = "Annonce supprimée."

class ProgrammeDelete(DeleteWithMessage):
    model = Programme
    template_name = 'admin/programme_confirm_delete.html'
    success_message = "Programme supprimé."

class AxeRechercheDelete(DeleteWithMessage):
    model = AxeRecherche
    template_name = 'admin/axe_confirm_delete.html'
    success_message = "Axe de recherche supprimé."

class PublicationRechercheDelete(DeleteWithMessage):
    model = PublicationRecherche
    template_name = 'admin/publication_confirm_delete.html'
    success_message = "Publication supprimée."

class LivreDelete(DeleteWithMessage):
    model = Livre
    template_name = 'admin/livre_confirm_delete.html'
    success_message = "Livre supprimé."

class PersonnelDelete(DeleteWithMessage):
    model = Personnel
    template_name = 'admin/personnel_confirm_delete.html'
    success_message = "Membre du personnel supprimé."

class EtapeAdmissionDelete(DeleteWithMessage):
    model = EtapeAdmission
    template_name = 'admin/etape_admission_confirm_delete.html'
    success_message = "Étape d'admission supprimée."

class DemandeAdmissionDelete(DeleteWithMessage):
    model = DemandeAdmission
    template_name = 'admin/demande_admission_confirm_delete.html'
    success_message = "Demande d'admission supprimée."




def exam_calendar(request, year=None, month=None):
    """
    Affiche un calendrier mensuel des examens pour le staff.
    """
    # 1) Détermination de l'année et du mois
    today = date.today()
    year = int(year) if year else today.year
    month = int(month) if month else today.month

    # 2) Construction des dates du mois
    cal = calendar.Calendar(firstweekday=0)  # lundi=0
    month_dates = cal.monthdatescalendar(year, month)

    # 3) Récupération et groupement des examens
    events = Examen.objects.filter(date__year=year, date__month=month)
    events_by_day = {}
    for ev in events:
        events_by_day.setdefault(ev.date.day, []).append(ev)

    # 4) Calcul du mois précédent
    if month == 1:
        prev_month, prev_year = 12, year - 1
    else:
        prev_month, prev_year = month - 1, year

    # 5) Calcul du mois suivant
    if month == 12:
        next_month, next_year = 1, year + 1
    else:
        next_month, next_year = month + 1, year

    # 6) Contexte pour le template
    context = {
        'month_name': date(year, month, 1).strftime('%B %Y'),
        'month_dates': month_dates,
        'events_by_day': events_by_day,
        'current_month': month,
        'current_year': year,
        'day_names': ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'],
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
        'today': date.today(),  # ← ajoute ceci
        
    }
    
       
    # 7) Examens à venir (au-delà d'aujourd'hui)
    upcoming_exams = Examen.objects.filter(date__gt=now()).order_by('date')

    # Ajout au contexte
    context['upcoming_exams'] = upcoming_exams

    return render(request, 'calendrier/calendrier.html', context)

 



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


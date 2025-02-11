from django.shortcuts import render, redirect
from .models import Cours, Inscription, Etudiant,Professeur,Evenement, Annonce,Article
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserChangeForm
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
from .forms import EtudiantForm,ContactForm
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.contrib.messages import get_messages
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm


def home(request):
    # Récupérer tous les articles triés par date décroissante
    articles_list = Article.objects.all().order_by('-date_publication')

    # Initialiser la pagination (5 articles par page)
    paginator = Paginator(articles_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'evenements': Evenement.objects.filter(date_debut__gte=timezone.now()).order_by('date_debut')[:10],
        'annonces': Annonce.objects.filter(est_active=True).order_by('-date_publication'),
        'cours': Cours.objects.all(),
        'articles': page_obj,  # On remplace la liste brute par l'objet paginé
        'professeurs': Professeur.objects.all(),
        'cours_list': Cours.objects.all(),
        'now': timezone.now(),
    }

    return render(request, 'index.html', context)



def annonces_list(request):
    annonces = Annonce.objects.filter(est_active=True)  # Utiliser est_active au lieu de is_active
    return render(request, 'annonces/annonces_list.html', {'annonces': annonces})


def annonce_detail(request, id):
    # Récupérer l'annonce spécifique en fonction de l'id
    annonce = get_object_or_404(Annonce, id=id)
    
    # Récupérer toutes les annonces actives, sauf celle qui est déjà affichée
    annonces_actives = Annonce.objects.filter(est_active=True).exclude(id=annonce.id)
    
    # Passer l'annonce et les autres annonces au template
    return render(request, 'annonces/annonces_detail.html', {
        'annonce': annonce,
        'annonces': annonces_actives
    })
    
def evenements_list(request):
    now = timezone.now()  # Récupère l'heure actuelle
    evenements = Evenement.objects.filter(date_debut__gte=now)  # Récupère les événements à venir
    return render(request, 'evenements/evenements_list.html', {'evenements': evenements})
   

def evenement_detail(request, id):
    # Récupérer l'événement spécifique en fonction de l'id
    evenement = get_object_or_404(Evenement, id=id)
    
    # Récupérer tous les événements à venir, sauf celui qui est déjà affiché
    evenements_a_venir = Evenement.objects.filter(date_debut__gt=timezone.now()).exclude(id=evenement.id)
    
    # Passer l'événement et les autres événements à venir au template
    return render(request, 'evenements/evenement_detail.html', {
        'evenement': evenement,
        'evenements': evenements_a_venir
    })

def programmes(request):
    return render(request, 'programmes/programmes.html')



def apropos(request):
    return render(request, 'apropos.html')



def login_view(request):
    # Supprime les anciens messages avant d'afficher un nouveau
    storage = get_messages(request)
    for _ in storage:
        pass  # Cette boucle vide supprime tous les anciens messages

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

                return redirect("profile")
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        else:
            messages.error(request, "Veuillez vérifier vos informations.")
    else:
        form = AuthenticationForm()

    return render(request, "registration/login.html", {"form": form})


def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Inscription réussie ! 🎉 Bienvenue sur notre plateforme.")
            return redirect("home")  # Redirection après succès
        else:
            messages.error(request, "Une erreur est survenue lors de l'inscription. Vérifiez les informations.")
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})


@login_required
def profile_view(request):
    return render(request, 'registration/profile.html', {'user': request.user})


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirigez vers la page du profil après modification
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'registration/edit_profile.html', {'form': form})



@login_required
def etudiant_profil(request):
    # Récupère tous les étudiants liés à l'utilisateur connecté
    etudiants = Etudiant.objects.filter(user=request.user)

    if etudiants.exists():
        # Si plusieurs étudiants existent, vous pouvez choisir le premier ou gérer le cas
        etudiant = etudiants.first()
    else:
        # Gérer le cas où aucun étudiant n'est trouvé
        etudiant = None

    return render(request, 'etudiants/etudiant_profil.html', {'etudiant': etudiant})


@login_required
def edit_info_etudiant(request, etudiant_id):
    etudiant = get_object_or_404(Etudiant, id=etudiant_id)
    if request.method == 'POST':
        form = EtudiantForm(request.POST, instance=etudiant)
        if form.is_valid():
            form.save()
            return redirect('etudiant_profil')  # Redirige vers le profil après modification
    else:
        form = EtudiantForm(instance=etudiant)
    return render(request, 'etudiants/edit_info_etudiant.html', {'form': form})



def cours(request):
    cours_list = Cours.objects.all().order_by('-date_creation')  # Récupère tous les cours
    paginator = Paginator(cours_list, 6)  # 6 cours par page

    page_number = request.GET.get('page')  # Récupérer le numéro de la page
    page_obj = paginator.get_page(page_number)  # Obtenir la page demandée

    return render(request, 'cours/cours.html', {'page_obj': page_obj})


@login_required
def inscription_etudiant(request, cours_id):
    cours = get_object_or_404(Cours, id=cours_id)
    etudiant = Etudiant.objects.filter(user=request.user).first()

    # Vérification de la capacité du cours
    if cours.get_nombre_inscrits() >= cours.capacite_maximale:
        messages.error(request, "Ce cours est déjà complet.")
        return redirect('cours_professeurs')

    # Si l'étudiant existe déjà, éviter de lui demander ses infos à nouveau
    if etudiant:
        # Vérifier s'il est déjà inscrit à ce cours
        if Inscription.objects.filter(etudiant=etudiant, cours=cours).exists():
            messages.warning(request, "Vous êtes déjà inscrit à ce cours.")
            return redirect('cours_detail', cours_id=cours.id)

        # Vérifier la limite de 7 cours
        if Inscription.objects.filter(etudiant=etudiant).count() >= 7:
            messages.error(request, "Vous ne pouvez pas vous inscrire à plus de 7 cours pour cette session.")
            return redirect('cours_professeurs')

        # Inscription directe sans demander d'infos supplémentaires
        try:
            with transaction.atomic():
                Inscription.objects.create(etudiant=etudiant, cours=cours)
                messages.success(request, f"Inscription réussie au cours {cours.nom}.")
        except IntegrityError:
            messages.error(request, "Erreur d'inscription. Veuillez réessayer.")

        return redirect('cours_detail', cours_id=cours.id)  # Redirection vers le détail du cours après inscription

    # Si l'étudiant n'existe pas, afficher le formulaire pour qu'il complète ses infos
    form = EtudiantForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        etudiant = form.save(commit=False)
        etudiant.user = request.user  # Associer l'étudiant à l'utilisateur connecté
        etudiant.save()

        try:
            with transaction.atomic():
                Inscription.objects.create(etudiant=etudiant, cours=cours)
                messages.success(request, f"Inscription réussie au cours {cours.nom}.")
        except IntegrityError:
            messages.error(request, "Erreur d'inscription. Veuillez réessayer.")
            return render(request, 'inscription.html', {'cours': cours, 'form': form})

        return redirect('cours_detail', cours_id=cours.id)  # Redirige vers le détail du cours

    return render(request, 'inscription.html', {'cours': cours, 'form': form})



@login_required
def list_etudiants(request):
    etudiants = Etudiant.objects.prefetch_related('inscriptions__cours').all()  # Récupérer tous les étudiants
    return render(request, 'etudiants/list_etudiants.html', {'etudiants': etudiants})



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
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            # 📩 Envoyer un email (optionnel)
            send_mail(
                f"Nouveau message de {name}",
                message,
                email,
                ["admin@example.com"],  # Remplace avec l'email de ton admin
                fail_silently=False,
            )

            return redirect("contact_success")  # Redirige vers une page de succès
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})


def contact_success_view(request):
    return render(request, "contact_success.html")



def cours_et_professeurs(request):
    cours_list = Cours.objects.all().order_by('-date_creation')
    professeurs_list = Professeur.objects.all()

    return render(request, 'cours/cours_professeurs.html', {
        'cours_list': cours_list,
        'professeurs_list': professeurs_list
    })



def liste_professeurs(request):
    professeurs_list = Professeur.objects.all()  # Récupérer tous les professeurs
    paginator = Paginator(professeurs_list, 6)  # 6 professeurs par page

    page_number = request.GET.get('page')  # Obtenir le numéro de la page
    page_obj = paginator.get_page(page_number)  # Récupérer la page actuelle

    return render(request, "professeurs/professeurs.html", {"page_obj": page_obj})


@login_required
def cours_detail(request, cours_id):
    # Récupérer le cours par son ID
    cours = get_object_or_404(Cours, id=cours_id)
    # Récupérer l'étudiant actuellement connecté
    etudiant = Etudiant.objects.filter(user=request.user).first()

    inscrit = False  # Indiquer si l'étudiant est inscrit ou pas

    # Vérifier si l'étudiant est déjà inscrit à ce cours
    if etudiant and Inscription.objects.filter(etudiant=etudiant, cours=cours).exists():
        inscrit = True

    # Si l'étudiant clique pour s'inscrire
    if not inscrit and request.method == 'POST':
        if cours.est_ferme:
            messages.error(request, "Les inscriptions sont fermées pour ce cours.")
        else:
            # Inscrire l'étudiant au cours
            Inscription.objects.create(etudiant=etudiant, cours=cours)
            messages.success(request, f"Vous êtes inscrit avec succès au cours {cours.nom}.")
            inscrit = True  # L'étudiant est maintenant inscrit

    context = {
        'cours': cours,
        'inscrit': inscrit,  # Passer l'état d'inscription de l'étudiant
    }

    return render(request, 'cours/cours_detail.html', context)


def program_detail(request, program_name):
    # Logique pour récupérer les données spécifiques du programme
    program_data = {
        'sociologie': {
            'title': 'Sociologie',
            'description': 'Explorer les structures sociales et les comportements collectifs.'
        },
        'psychologie': {
            'title': 'Psychologie',
            'description': 'Préparation à comprendre et intervenir sur les comportements humains.'
        },
        'service_social': {
            'title': 'Service Social',
            'description': 'Comprendre les grandes questions existentielles et éthiques.'
        },
        'communication_sociale': {
            'title': 'Communication Sociale',
            'description': 'Comprendre les grandes questions existentielles et éthiques.'
        }
    }

    # Obtenir les informations du programme à partir de la variable program_name
    program = program_data.get(program_name)

    if not program:
        # Si le programme n'existe pas, on affiche une erreur
        return render(request, '404.html')

    return render(request, 'programmes/program_detail.html', {'program': program})




def article_detail(request, id):
    # Récupérer l'article principal
    article = Article.objects.get(id=id)

    # Ajouter une liste d'articles récents/recommandés
    recommended_articles = Article.objects.exclude(id=id).order_by('-date_publication')[:6]

    # Passer les deux informations au template
    context = {
        'article': article,
        'recommended_articles': recommended_articles
    }
    return render(request, 'articles/article_detail.html', context)



def articles_list(request):
    articles = Article.objects.all().order_by('-date_publication')  # Trier les articles par date (du plus récent au plus ancien)
    
    # Appliquer la pagination (6 articles par page)
    paginator = Paginator(articles, 6)
    page_number = request.GET.get('page')  # Récupérer le numéro de la page depuis l'URL
    page_obj = paginator.get_page(page_number)

    return render(request, 'articles/articles_list.html', {'page_obj': page_obj})



def highlight_keyword(text, keyword):
    """Retourne le texte avec le mot-clé en surbrillance."""
    if not keyword:
        return text
    highlighted = re.sub(
        f'({re.escape(keyword)})',
        r'<span class="highlight">\1</span>',
        text,
        flags=re.IGNORECASE
    )
    return mark_safe(highlighted)



def search(request):
    query = request.GET.get('q', '')
    results = {}

    if query:
        results['articles'] = Article.objects.filter(
            Q(titre__icontains=query) | Q(contenu__icontains=query) | Q(auteur__icontains=query)
        )
        results['annonces'] = Annonce.objects.filter(
            Q(titre__icontains=query) | Q(contenu__icontains=query) | Q(organisateur__icontains=query) | Q(lieu__icontains=query)
        )
        results['evenements'] = Evenement.objects.filter(
            Q(titre__icontains=query) | Q(description__icontains=query) | Q(lieu__icontains=query)
        )
        results['cours'] = Cours.objects.filter(
            Q(nom__icontains=query) | Q(specialisation__icontains=query)
        )
        results['professeurs'] = Professeur.objects.filter(
            Q(nom__icontains=query) | Q(specialisation__icontains=query)
        )
        results['etudiants'] = Etudiant.objects.filter(
            Q(nom__icontains=query) | Q(prenom__icontains=query) | Q(email__icontains=query)
        )

        # Ajouter la surbrillance
        for category, items in results.items():
            for item in items:
                if hasattr(item, 'titre'):
                    item.titre = highlight_keyword(item.titre, query)
                if hasattr(item, 'contenu'):
                    item.contenu = highlight_keyword(item.contenu, query)
                if hasattr(item, 'description'):
                    item.description = highlight_keyword(item.description, query)
    
    return render(request, 'search/search_results.html', {'query': query, 'results': results})






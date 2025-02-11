from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Accueil
    path('', views.home, name='home'),

    # Ajoute cette ligne dans ton `urls.py`
    path('signup/', views.signup_view, name='signup'),
    # Page de connexion
    path('login/', views.login_view, name='login'),
    
    # Page de déconnexion
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    
    # Changer de mot de passe
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # Réinitialisation de mot de passe
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html'
    ), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),

    # Profil utilisateur
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    
    # Profil étudiant
    path('etudiant/profil/', views.etudiant_profil, name='etudiant_profil'),
    path('edit_etudiant/<int:etudiant_id>/', views.edit_info_etudiant, name='edit_info_etudiant'),

    # Inscription aux cours
    path('inscription/<int:cours_id>/', views.inscription_etudiant, name='inscription_etudiant'),

    # Liste et détails des étudiants
    path('etudiants/', views.list_etudiants, name='list_etudiants'),

    # Gestion des cours
    path('cours_professeurs/', views.cours_et_professeurs, name='cours_professeurs'),


    path('cours/<int:cours_id>/', views.cours_detail, name='cours_detail'),  # Détails d’un cours

    # Programmes
    path('programmes/', views.programmes, name='programmes'),
    path('programmes/<str:program_name>/', views.program_detail, name='program_detail'),

    # Pages diverses
    path('apropos/', views.apropos, name='apropos'),
    # Page Contact
    path("contact/", views.contact_view, name="contact"),
    # Page Témoignages
    path("contact/success/", views.contact_success_view, name="contact_success"),
    # Recherche
    path('search/', views.search, name='search'),

    # Annonces et événements
    path('annonces/', views.annonces_list, name='annonces_list'),
    path('annonce/<int:id>/', views.annonce_detail, name='annonce_detail'),

    path('evenements/', views.evenements_list, name='evenements_list'),
    path('evenement/<int:id>/', views.evenement_detail, name='evenement_detail'),

    # Articles
    path('articles/', views.articles_list, name='articles_list'),
    path('article/<int:id>/', views.article_detail, name='article_detail'),
    
    path('cours/', views.cours, name='cours'),  # Nouvelle URL pour afficher tous les cours
    path("professeurs/", views.liste_professeurs, name="liste_professeurs"),  # URL pour la liste des profs


]

# Gestion des fichiers médias en mode développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

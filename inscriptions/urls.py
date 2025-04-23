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
    path('logout/', views.logout_view, name='logout'),

  # Déconnexion avec confirmation
    path('confirmer-deconnexion/', views.confirmer_deconnexion, name='confirmer_deconnexion'),

    
    path('demande-admission/', views.demande_admission, name='demande_admission'),

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
    path('create_profile/', views.create_profile, name='create_profile'),
    path('profil/', views.etudiant_profil, name='etudiant_profil'),
    path('profil/modifier/<int:etudiant_id>/', views.edit_info_etudiant, name='edit_info_etudiant'),
  

    path('cours/', views.cours_list, name='cours_list'),
    path('cours/<int:horaire_id>/', views.cours_detail, name='cours_detail'),
    path('cours/<int:horaire_id>/inscription/', views.inscription_create, name='inscription_create'),

    path("mes-cours/", views.mes_cours, name="mes_cours"),


    # Programmes
    path('programme/<int:pk>/', views.programme_detail, name='programme_detail'),

    path('programmes/', views.programmes, name='programmes'),
    path('bibliotheques/', views.catalogue, name='catalogue'),

    path('sociologie/', views.sociologie, name='sociologie'),
    path('psychologie/', views.psychologie, name='psychologie'),
    path('communication/', views.communication, name='communication'),
    path('service-social/', views.service_social, name='service_social'),
    
    # Pages diverses
    path('apropos/', views.apropos, name='apropos'),
    path('histoire/', views.histoire, name='histoire'),
    path('mission-vision/', views.mission_vision, name='mission_vision'),
    path('administration/', views.administration, name='administration'),
    path('mot-du-doyen/', views.mot_doyen, name='mot_doyen'),
    path('galerie/', views.galerie, name='galerie'),

  
    # Page Contact
    path("contact/", views.contact_view, name="contact"),
    # Page Témoignages
    path("contact/success/", views.contact_success_view, name="contact_success"),
    # publiactions
    path("publication/", views.recherche_view, name="recherche"),

    path('publications/', views.publications_list, name='publications'),
    path('revues-scientifiques/', views.revues_scientifiques, name='revues_scientifiques'),
    path('projets-en-cours/', views.projets_en_cours, name='projets_en_cours'),


    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('annonce/<int:pk>/', views.annonce_detail, name='annonce_detail'),
    path('evenement/<int:pk>/', views.evenement_detail, name='evenement_detail'),
    
    #formations
    path('licence/', views.licence, name='licence'),
    path('master/', views.master, name='master'),
    path('formation-continue/', views.formation_continue, name='formation_continue'),
    
    path('associations/', views.associations_etudiantes, name='associations_etudiantes'),
    path('activites/', views.activites_culturelles, name='activites_culturelles'),
    path('services/', views.services_etudiants, name='services_etudiants'),
    path('bourses/', views.bourses_et_aides, name='bourses_et_aides'),


]

# Gestion des fichiers médias en mode développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

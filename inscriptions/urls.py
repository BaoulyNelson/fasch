from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    # ------------------- Accueil -------------------
    path('', views.home, name='home'),

    # ------------------- Authentification -------------------
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('confirmer-deconnexion/', views.confirmer_deconnexion, name='confirmer_deconnexion'),

    # ------------------- Gestion du mot de passe -------------------
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

    # ------------------- Profil Utilisateur -------------------
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),

    # ------------------- Profil Étudiant -------------------
    path('create_profile/', views.create_profile, name='create_profile'),
    path('profil/', views.etudiant_profil, name='etudiant_profil'),
    path('profil/modifier/<int:etudiant_id>/', views.edit_info_etudiant, name='edit_info_etudiant'),

    # ------------------- Cours -------------------
    path('cours/', views.cours_list, name='cours_list'),
    path('cours/<int:horaire_id>/', views.cours_detail, name='cours_detail'),
    path('cours/<int:horaire_id>/inscription/', views.inscription_create, name='inscription_create'),
    path('mes-cours/', views.mes_cours, name='mes_cours'),

    # ------------------- Admissions -------------------
    path('admissions/', views.admission, name='demande_admission'),
    path('admissions/<str:section>/', views.admission, name='admission_section'),

    # ------------------- Programmes -------------------
    path('programmes/', views.programmes, name='programmes'),
    path('programmes/<str:programme>/', views.programme_view, name='programme_view'),
    path('programme/<int:pk>/', views.programme_detail, name='programme_detail'),

    # ------------------- Formations -------------------
    path('formations/<str:niveau>/', views.formation_view, name='formation_view'),

    # ------------------- Publications -------------------
    path('publication/', views.recherche_view, name='recherche'),
    path('publications/', views.publications_list, name='publications'),
    path('publications/<str:type_publication>/', views.publications_view, name='publications_view'),

    # ------------------- Bibliothèque -------------------
    path('bibliotheques/', views.catalogue, name='catalogue'),

    # ------------------- Pages diverses -------------------
    path('apropos/<str:section>/', views.apropos_view, name='apropos_view'),
    path('contact/', views.contact_view, name='contact'),
    path('contact/success/', views.contact_success_view, name='contact_success'),

    # ------------------- Recherche Globale -------------------
    path('recherche/', views.recherche_globale, name='recherche_globale'),

    # ------------------- Étudiants -------------------
    path('etudiants/<str:section>/', views.etudiant_view, name='etudiant_view'),

    # ------------------- Détail générique -------------------
    path('<str:type_detail>/<int:pk>/', views.detail_view, name='detail_view'),
]

# ------------------- Fichiers médias en développement -------------------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

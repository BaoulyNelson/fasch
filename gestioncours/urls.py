from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import re_path
from .views import calendrier_examen


urlpatterns = [
    # ------------------- Accueil -------------------
    path('', views.home, name='home'),
   
    # ------------------- Authentification -------------------
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_admin, name='dashboard'),

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

    #pour creer
    path('staff/etudiant/add/', views.EtudiantCreate.as_view(), name='add_etudiant'),
    path('staff/cours/add/', views.CoursCreate.as_view(), name='add_cours'),
    path('staff/professeur/add/', views.ProfesseurCreate.as_view(), name='add_professeur'),
    path('staff/inscription/add/', views.InscriptionCreate.as_view(), name='add_inscription'),
    path('staff/horaire/add/', views.HoraireCoursCreate.as_view(), name='add_horaire'),
    path('staff/article/add/', views.ArticleCreate.as_view(), name='add_article'),
    path('staff/evenement/add/', views.EvenementCreate.as_view(), name='add_evenement'),
    path('annonce/add/', views.AnnonceCreate.as_view(), name='add_annonce'),
    path('staff/programme/add/', views.ProgrammeCreate.as_view(), name='add_programme'),
    path('staff/axe-recherche/add/', views.AxeRechercheCreate.as_view(), name='add_axe'),
    path('staff/publication/add/', views.PublicationRechercheCreate.as_view(), name='add_publication'),
    path('staff/livre/add/', views.LivreCreate.as_view(), name='add_livre'),
    path('staff/personnel/add/', views.PersonnelCreate.as_view(), name='add_personnel'),
    path('staff/etape-admission/add/', views.EtapeAdmissionCreate.as_view(), name='add_etape_admission'),
    path('staff/demande-admission/add/', views.DemandeAdmissionCreate.as_view(), name='add_demande_admission'),
    path('staff/examens/ajouter/', views.ExamenCreate.as_view(), name='add_examen'),

        
    # ------------------ Étudiants ------------------
    path('staff/etudiant/', views.EtudiantListView.as_view(), name='etudiants_list'),

    # ------------------ Cours ------------------
    path('staff/cours/', views.CoursListView.as_view(), name='cours_list'),

    # ------------------ Professeurs ------------------
    path('staff/professeur/', views.ProfesseurListView.as_view(), name='professeurs_list'),

    # ------------------ Inscriptions ------------------
    path('staff/inscription/', views.InscriptionListView.as_view(), name='inscriptions_list'),

    # ------------------ Horaires ------------------
    path('staff/horaire/', views.HoraireCoursListView.as_view(), name='horaires_list'),

    # ------------------ Articles ------------------
    path('staff/article/', views.ArticleListView.as_view(), name='articles_list'),

    # ------------------ Événements ------------------
    path('staff/evenement/', views.EvenementListView.as_view(), name='evenements_list'),

    # ------------------ Annonces ------------------
    path('staff/annonce/', views.AnnonceListView.as_view(), name='annonces_list'),

    # ------------------ Programmes ------------------
    path('staff/programme/', views.ProgrammeListView.as_view(), name='programmes_list'),

    # ------------------ Axes de recherche ------------------
    path('staff/axe-recherche/', views.AxeRechercheListView.as_view(), name='axes_list'),

    # ------------------ Publications ------------------
    path('staff/publication/', views.PublicationRechercheListView.as_view(), name='publications_list'),

    # ------------------ Livres ------------------
    path('staff/livre/', views.LivreListView.as_view(), name='livres_list'),

    # ------------------ Personnel ------------------
    path('staff/personnel/', views.PersonnelListView.as_view(), name='personnels_list'),

    # ------------------ Étapes d'admission ------------------
    path('staff/etape-admission/', views.EtapeAdmissionListView.as_view(), name='etapes_admission_list'),

    # ------------------ Demandes d'admission ------------------
    path('staff/demande-admission/', views.DemandeAdmissionListView.as_view(), name='demandes_admission_list'),

    # ------------------ Examens ------------------
    path('staff/examens/', views.ExamenListView.as_view(), name='examens_list'),

    #pour modifier
    path('staff/etudiant/<int:pk>/edit/', views.EtudiantUpdate.as_view(), name='modifier_etudiant'),
    path('staff/cours/<int:pk>/edit/', views.CoursUpdate.as_view(), name='modifier_cours'),
    path('staff/professeur/<int:pk>/edit/', views.ProfesseurUpdate.as_view(), name='modifier_professeur'),
    path('staff/inscription/<int:pk>/edit/', views.InscriptionUpdate.as_view(), name='modifier_inscription'),
    path('staff/horaire/<int:pk>/edit/', views.HoraireCoursUpdate.as_view(), name='modifier_horaire'),
    path('staff/article/<int:pk>/edit/', views.ArticleUpdate.as_view(), name='modifier_article'),
    path('staff/evenement/<int:pk>/edit/', views.EvenementUpdate.as_view(), name='modifier_evenement'),
    path('staff/annonce/<int:pk>/edit/', views.AnnonceUpdate.as_view(), name='modifier_annonce'),
    path('programme/<int:pk>/edit/', views.ProgrammeUpdate.as_view(), name='modifier_programme'),
    path('staff/axe-recherche/<int:pk>/edit/', views.AxeRechercheUpdate.as_view(), name='modifier_axe'),
    path('staff/publication/<int:pk>/edit/', views.PublicationRechercheUpdate.as_view(), name='modifier_publication'),
    path('staff//<int:pk>/edit/', views.LivreUpdate.as_view(), name='modifier_livre'),
    path('personnel/<int:pk>/edit/', views.PersonnelUpdate.as_view(), name='modifier_personnel'),
    path('staff/etape-admission/<int:pk>/edit/', views.EtapeAdmissionUpdate.as_view(), name='modifier_etape_admission'),
    path('staff/demande-admission/<int:pk>/edit/', views.DemandeAdmissionUpdate.as_view(), name='modifier_demande_admission'),
    path('staff/examens/<int:pk>/modifier/', views.ExamenUpdate.as_view(), name='modifier_examen'),

    #details
    path('staff/etudiant/<int:pk>/', views.EtudiantDetail.as_view(), name='detail_etudiant'),
    path('staff/cours/<int:pk>/', views.CoursDetail.as_view(), name='detail_cours'),
    path('staff/professeur/<int:pk>/', views.ProfesseurDetail.as_view(), name='detail_professeur'),
    path('staff/inscription/<int:pk>/', views.InscriptionDetail.as_view(), name='detail_inscription'),
    path('staff/horaire/<int:pk>/', views.HoraireCoursDetail.as_view(), name='detail_horaire'),
    path('staff/cours/<int:pk>/', views.CoursDetail.as_view(), name='detail_cours'),  
    path('staff/article/<int:pk>/', views.ArticleDetail.as_view(), name='detail_article'),
    path('staff/evenement/<int:pk>/', views.EvenementDetail.as_view(), name='detail_evenement'),
    path('staff/annonce/<int:pk>/', views.AnnonceDetail.as_view(), name='detail_annonce'),
    path('staff/programme/<int:pk>/', views.ProgrammeDetail.as_view(), name='detail_programme'),
    path('staff/axe-recherche/<int:pk>/', views.AxeRechercheDetail.as_view(), name='detail_axe'),
    path('staff/publication/<int:pk>/', views.PublicationRechercheDetail.as_view(), name='detail_publication'),
    path('staff/livre/<int:pk>/', views.LivreDetail.as_view(), name='detail_livre'),
    path('staff/personnel/<int:pk>/', views.PersonnelDetail.as_view(), name='detail_personnel'),
    path('staff/etape-admission/<int:pk>/', views.EtapeAdmissionDetail.as_view(), name='detail_etape_admission'),
    path('staff/-admission/<int:pk>/', views.DemandeAdmissionDetail.as_view(), name='detail_demande_admission'),
    path('staff/examens/<int:pk>/', views.ExamenDetail.as_view(), name='detail_examen'),
    
    # ------------------- confirmation de suppression -------------------
    path('staff/etudiant/<int:pk>/delete/', views.EtudiantDelete.as_view(), name='supprimer_etudiant'),
    path('staff/cours/<int:pk>/delete/', views.CoursDelete.as_view(), name='supprimer_cours'),
    path('staff/professeur/<int:pk>/delete/', views.ProfesseurDelete.as_view(), name='supprimer_professeur'),
    path('staff/inscription/<int:pk>/delete/', views.InscriptionDelete.as_view(), name='supprimer_inscription'),
    path('staff/horaire/<int:pk>/delete/', views.HoraireCoursDelete.as_view(), name='supprimer_horaire'),
    path('staff/article/<int:pk>/delete/', views.ArticleDelete.as_view(), name='supprimer_article'),
    path('staff/evenement/<int:pk>/delete/', views.EvenementDelete.as_view(), name='supprimer_evenement'),
    path('staff/annonce/<int:pk>/delete/', views.AnnonceDelete.as_view(), name='supprimer_annonce'),
    path('staff/programme/<int:pk>/delete/', views.ProgrammeDelete.as_view(), name='supprimer_programme'),
    path('staff/axe-recherche/<int:pk>/delete/', views.AxeRechercheDelete.as_view(), name='supprimer_axe'),
    path('staff/publication/<int:pk>/delete/', views.PublicationRechercheDelete.as_view(), name='supprimer_publication'),
    path('staff/livre/<int:pk>/delete/', views.LivreDelete.as_view(), name='supprimer_livre'),
    path('staff/personnel/<int:pk>/delete/', views.PersonnelDelete.as_view(), name='supprimer_personnel'),
    path('staff/etape-admission/<int:pk>/delete/', views.EtapeAdmissionDelete.as_view(), name='supprimer_etape_admission'),
    path('staff/demande-admission/<int:pk>/delete/', views.DemandeAdmissionDelete.as_view(), name='supprimer_demande_admission'),
    path('staff/examens/<int:pk>/supprimer/', views.ExamenDelete.as_view(), name='supprimer_examen'),

    # ------------------- Admissions -------------------
    path('admissions/', views.admission, name='demande_admission'),
    path('admissions/<str:section>/', views.admission, name='admission_section'),

    # ------------------- Formations -------------------
    path('formations/<str:niveau>/', views.formation_view, name='formation_view'),

    # ------------------- Bibliothèque -------------------
    path('bibliotheques/', views.catalogue, name='catalogue'),

    # ------------------- Pages diverses -------------------
    path('apropos/<str:section>/', views.apropos_view, name='apropos_view'),
    path('contact/', views.contact_view, name='contact'),
    path('contact/success/', views.contact_success_view, name='contact_success'),

    # ------------------- Recherche Globale -------------------
    path('recherche/', views.recherche_globale, name='recherche_globale'),
    # urls.py
    path('search/', views.global_search, name='global_search'),

    # accepte /calendrier/  et /calendrier/2025/
    re_path(r'^calendrier(?:/(?P<annee>\d{4}))?/$', calendrier_examen, name='calendrier_examen'),

    # ------------------- Événements -------------------
    path('evenement/<slug:slug>/', views.detail_evenement, name='evenement_detail'),

    path('evenements/', views.liste_evenements, name='liste_evenements'),

    # ------------------- Annonces -------------------
    path('annonce/<slug:slug>/', views.detail_annonce, name='annonce_detail'),

    # ------------------- Articles -------------------

    path('article/<slug:slug>/', views.detail_article, name='article_detail'),

    path('etudiants/<str:section>/', views.etudiant_view, name='etudiant_view'),

    path('programmes/', views.programmes, name='programmes'),
    path('programmes/<str:programme>/', views.programme_view, name='programme_view'),
    # Pour les utilisateurs ordinaires
    path('programme/<int:pk>/', views.programme_detail, name='programme_detail'),
    
    # ------------------- Publications -------------------
    path('publication/', views.recherche_view, name='recherche'),
    path('publications/', views.publications_list, name='publications'),
    path('publications/<str:type_publication>/', views.publications_view, name='publications_view'),
    path('cours/', views.list_cours, name='list_cours'),
    path('cours/', views.list_cours, name='cours_tous'),
    path('horaire/<int:horaire_id>/cours/',views.cours_detail,name='cours_detail'
),
    path('cours/<str:session>/', views.cours_par_session, name='cours_par_session'),

    path('cours/<int:horaire_id>/inscription/', views.inscription_create, name='inscription_create'),
    path('mes-cours/', views.mes_cours, name='mes_cours'),

]

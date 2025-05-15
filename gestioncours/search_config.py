# search_config.py

search_config = {
    'Etudiant': ['prenom', 'nom', 'email', 'telephone', 'niveau'],
    'Cours': ['nom'],
    'Professeur': ['prenom', 'nom'],
    'HoraireCours': ['jour', 'heure_debut', 'heure_fin', 'capacite_max', 'est_ferme'],
    'Inscription': ['etudiant', 'horaire_cours'],
    'EtapeAdmission': ['nom', 'date_debut', 'date_limite'],
    'DemandeAdmission': ['nom', 'email', 'telephone', 'programme', 'message', 'date_envoi'],
    'Evenement': ['titre', 'description', 'date_debut', 'date_fin', 'image', 'lieu'],
    'Programme': ['titre', 'description', 'niveau'],
    'Annonce': ['titre', 'contenu', 'date_publication', 'est_active', 'image', 'organisateur', 'lieu', 'date_evenement'],
    'Article': ['titre', 'contenu', 'auteur', 'date_publication', 'image', 'est_active'],
    'AxeRecherche': ['titre', 'description'],
    'PublicationRecherche': ['titre', 'auteurs', 'description', 'date_publication', 'domaines', 'lien'],
    'Livre': ['titre', 'auteur', 'annee', 'resume', 'disponible'],
    'Personnel': ['poste', 'nom', 'description', 'photo'],
}
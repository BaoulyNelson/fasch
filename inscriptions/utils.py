from django.contrib import messages

def ajouter_message(request, niveau, texte):
    """Ajoute un message avec le niveau spécifié (succès, erreur, info, avertissement)."""
    niveaux_valides = {
        'success': messages.SUCCESS,
        'error': messages.ERROR,
        'warning': messages.WARNING,
        'info': messages.INFO
    }

    niveau_message = niveaux_valides.get(niveau, messages.INFO)  # Par défaut, niveau INFO
    messages.add_message(request, niveau_message, texte)

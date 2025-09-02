from django import template
register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Permet d'accéder à dictionary[key] dans les templates"""
    return dictionary.get(key)

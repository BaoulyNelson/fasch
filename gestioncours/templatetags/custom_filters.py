from django import template

register = template.Library()

@register.filter
def split(value, sep=","):
    return value.split(sep)


@register.filter
def trim(value):
    if isinstance(value, str):
        return value.strip()
    return value

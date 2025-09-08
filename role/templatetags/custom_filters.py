from django import template

register = template.Library()

@register.filter
def dict_get(d, key):
    """Récupère une valeur dans un dict avec une clé donnée"""
    if not d:
        return None
    return d.get(key)

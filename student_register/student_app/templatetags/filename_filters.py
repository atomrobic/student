from django import template
import os

register = template.Library()

@register.filter
def filename(value):
    """Returns only the base filename of a path."""
    return os.path.basename(value)

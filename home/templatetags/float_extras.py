from distutils.command import register

from django import template

register = template.Library()

@register.filter
def addf(value, arg):
    """Adds the arg to the value."""
    return float(value) + float(arg)

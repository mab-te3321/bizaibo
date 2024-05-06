from django import template

register = template.Library()

@register.filter(name='get_attr')
def get_attr(obj, attr_name):
    """ Retrieve attribute by name from an object. """
    return getattr(obj, attr_name, "")

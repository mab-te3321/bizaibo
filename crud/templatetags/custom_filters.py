from django import template

register = template.Library()

@register.filter(name='get_attr')
def get_attr(obj, attr_name):
    """ Retrieve attribute by name from an object. """
    res = getattr(obj, attr_name, "")
    print('type is --> ',type(res))
    return res
@register.filter
def is_queryset(item):
    if 'object' in str(item):
        return True
    else:
        return False
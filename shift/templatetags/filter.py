from django import template

register = template.Library()

# tag
@register.filter
def key(dict, key):    
    return dict[key]
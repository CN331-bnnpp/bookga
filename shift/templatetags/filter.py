from django import template

register = template.Library()

# tag
@register.filter
def key(dict, key):    
    return dict[key]

@register.filter
def getvalue(queryset):
    return queryset.values_list('user_id__username', flat=True)

@register.filter
def is_user(queryset, user):
    return queryset.filter(user_id=user).exists()
from django import template

register = template.Library()

@register.filter
def return_item(l, i):
    try:
        return l[i]
    except:
        return None

@register.filter
def next(value, arg):
    try:
        return value[int(arg)+1]
    except:
        return None

@register.filter
def prev(value, arg):
    try:
        return value[int(arg)-1]
    except:
        return None
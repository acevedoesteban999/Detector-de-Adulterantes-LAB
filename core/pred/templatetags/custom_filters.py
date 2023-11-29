from django import template

register = template.Library()

@register.filter
def mul(var,val):
    return f"{var*val:.2f}"


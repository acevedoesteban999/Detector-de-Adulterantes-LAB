from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def media_url(file_path):
    return f"{settings.MEDIA_URL}{file_path}"

@register.simple_tag
def media_url_index(file_path,index1,index2):
    return f"{settings.MEDIA_URL}{file_path}{index1}{index2}"
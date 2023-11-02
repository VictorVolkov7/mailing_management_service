from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def path_tag(format_string):
    return settings.MEDIA_URL + str(format_string)

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.conf import settings
import re

register = template.Library()

@register.filter
@stringfilter
def mailhtml(value):
    replacements = getattr(settings,'MAILING_HTML_REPLACE', None)
    if replacements:
        for r in replacements:
            value = re.sub(r[0], r[1], value)
    return mark_safe(value)

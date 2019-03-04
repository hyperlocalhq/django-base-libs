# -*- coding: UTF-8 -*-
from django import template
from django.utils.html import mark_safe
from django.conf import settings

register = template.Library()

### FILTERS ###


@register.filter
def force_full_urls(html):
    html = html.replace(' src="/', ' src="%s/' % settings.WEBSITE_URL)
    html = html.replace(' src=\'/', ' src=\'%s/' % settings.WEBSITE_URL)
    html = html.replace(' href="/', ' href="%s/' % settings.WEBSITE_URL)
    html = html.replace(' href=\'/', ' href=\'%s/' % settings.WEBSITE_URL)
    return mark_safe(html)

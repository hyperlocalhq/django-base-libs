# -*- coding: UTF-8 -*-
from django import template
from django.utils.html import mark_safe

from base_libs.utils.misc import get_website_url

register = template.Library()

### FILTERS ###


@register.filter
def force_full_urls(html):
    html = html.replace('src="/', 'src="%s' % get_website_url())
    html = html.replace('src=\'/', 'src=\'%s' % get_website_url())
    html = html.replace('href="/', 'href="%s' % get_website_url())
    html = html.replace('href=\'/', 'href=\'%s' % get_website_url())
    return mark_safe(html)

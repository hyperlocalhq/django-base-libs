# -*- coding: utf-8 -*-
from django import template

register = template.Library()

@register.inclusion_tag('theater_of_the_week/includes/theater_of_the_week.html', takes_context=True)
def theater_of_the_week(context):
    from base_libs.models.base_libs_settings import STATUS_CODE_PUBLISHED
    from ruhrbuehnen.apps.theater_of_the_week.views import get_theaters
    
    queryset = get_theaters('all', STATUS_CODE_PUBLISHED)
    article = queryset.order_by('-published_from')
    
    if article:
        article = article[0]

    return {
        'article': article,
        'MEDIA_URL': context['MEDIA_URL'],
        'STATIC_URL': context['STATIC_URL'],
        'UPLOADS_URL': context['UPLOADS_URL'],
    }
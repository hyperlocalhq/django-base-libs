# -*- coding: UTF-8 -*-
from django import template
from django.conf import settings

register = template.Library()

def absolute_url(value, arg):
    return value.get_absolute_url2(arg)

register.filter('absolute_url', absolute_url)

@register.inclusion_tag('articles/includes/other_articles.html', takes_context=True)
def other_articles(context, current_article, amount=5):
    from ruhrbuehnen.apps.articles.views import get_articles
    other_articles = get_articles().exclude(id=current_article.id)[:amount]
    return {
        'other_articles': other_articles,
        'MEDIA_URL': context['MEDIA_URL'],
        'STATIC_URL': context['STATIC_URL'],
        }

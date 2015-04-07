# -*- coding: utf-8 -*-
from jetson.apps.articles.templatetags.articles import *

@register.inclusion_tag('articles/includes/other_articles.html', takes_context=True)
def other_articles(context, current_article, amount=5):
    from berlinbuehnen.apps.articles.views import get_articles
    other_articles = get_articles().exclude(id=current_article.id)[:amount]
    return {
        'other_articles': other_articles,
        'MEDIA_URL': context['MEDIA_URL'],
        'STATIC_URL': context['STATIC_URL'],
        }

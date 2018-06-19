# -*- coding: UTF-8 -*-
from jetson.apps.articles.templatetags.articles_tags import *


@register.inclusion_tag('articles/includes/magazine_overview_slider.html', takes_context=True)
def show_magazine_overview(context):
    from ..views import get_articles
    context.update({
        'articles_under_player_of_the_week': get_articles().filter(
            featured_in_magazine=True,
            article_type__slug="player-of-the-week",
        ).order_by("-importance_in_magazine"),
        'articles_under_when_i_moved_to_berlin': get_articles().filter(
            featured_in_magazine=True,
            article_type__slug="when-i-moved-to-berlin",
        ).order_by("-importance_in_magazine"),
        'articles_under_innovation_and_vision': get_articles().filter(
            featured_in_magazine=True,
            article_type__slug="innovation-and-vision",
        ).order_by("-importance_in_magazine"),
        'articles_under_at_home_with': get_articles().filter(
            featured_in_magazine=True,
            article_type__slug="at-home-with",
        ).order_by("-importance_in_magazine"),
        'articles_under_knowledge_and_analysis': get_articles().filter(
            featured_in_magazine=True,
            article_type__slug="knowledge-and-analysis",
        ).order_by("-importance_in_magazine"),
        'articles_under_specials': get_articles().filter(
            featured_in_magazine=True,
            article_type__slug="specials",
        ).order_by("-importance_in_magazine"),
        'articles_under_articles_from_our_network_partners': get_articles().filter(
            featured_in_magazine=True,
            article_type__slug="articles-from-our-network-partners",
        ).order_by("-importance_in_magazine"),
    })
    return context

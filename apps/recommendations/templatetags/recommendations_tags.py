# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django import template
from ..models import Recommendation

register = template.Library()

@register.inclusion_tag('recommendations/includes/recommended_items.html', takes_context=True)
def show_recommended_items(context, sysname):
    if Recommendation.WIDGET_TEMPLATE_CHOICES:
        default_widget_template = Recommendation.WIDGET_TEMPLATE_CHOICES[0][0]
        recommendation, _created = Recommendation.objects.get_or_create(
            sysname=sysname,
            defaults={
                'widget_template': default_widget_template,
            }
        )
        if recommendation.status == recommendation.STATUS_CHOICE_PUBLISHED:
            context['recommendation'] = recommendation
    return context

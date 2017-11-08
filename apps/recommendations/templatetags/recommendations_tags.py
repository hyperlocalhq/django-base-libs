# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django import template
from ..models import Recommendation, WIDGET_TEMPLATE_CHOICES

register = template.Library()

@register.inclusion_tag('recommendations/includes/recommended_items.html', takes_context=True)
def show_recommended_items(context, sysname):
    recommendation, _created = Recommendation.objects.get_or_create(
        sysname=sysname,
        defaults={
            'widget_template': WIDGET_TEMPLATE_CHOICES[0][0],
        }
    )
    context['recommendation'] = recommendation
    return context

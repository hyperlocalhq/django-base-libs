# -*- coding: utf-8 -*-
from django import template
from django.db import models

register = template.Library()

@register.inclusion_tag('productions/includes/other_productions.html', takes_context=True)
def other_productions(context, current_event, amount=24):
    from berlinbuehnen.apps.productions.models import Production
    locations = list(current_event.production.in_program_of.all()) + list(current_event.ev_or_prod_play_locations())
    other_production_set = Production.objects.filter(
        models.Q(in_program_of__in=locations) | models.Q(play_locations__in=locations),
        show_among_others=True,
        #status="published",
    ).exclude(id=current_event.production.id)[:amount]
    return {
        'current_event': current_event,
        'other_productions': other_production_set,
        'MEDIA_URL': context['MEDIA_URL'],
        'STATIC_URL': context['STATIC_URL'],
    }
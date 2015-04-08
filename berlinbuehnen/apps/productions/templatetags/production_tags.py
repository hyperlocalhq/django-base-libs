# -*- coding: utf-8 -*-
from django import template
from django.db import models
from datetime import datetime, date

register = template.Library()

@register.inclusion_tag('productions/includes/other_productions.html', takes_context=True)
def other_productions(context, current_event=False, current_location=False, amount=24):
    from berlinbuehnen.apps.productions.models import Production
    
    if current_location:
        locations = [current_location]
    elif current_event:
        locations = list(current_event.production.in_program_of.all()) + list(current_event.ev_or_prod_play_locations())
    else:
        locations = []
        
    other_production_set = Production.objects.filter(
        models.Q(in_program_of__in=locations) | models.Q(play_locations__in=locations),
        show_among_others=True,
        #status="published",
    )
    if current_event:
        other_production_set = other_production_set.exclude(id=current_event.production.id)
        
    other_production_set = other_production_set[:amount]
        
    return {
        'current_event': current_event,
        'current_location': current_location,
        'other_productions': other_production_set,
        'MEDIA_URL': context['MEDIA_URL'],
        'STATIC_URL': context['STATIC_URL'],
    }
    
@register.inclusion_tag('productions/includes/date_slider.html', takes_context=True)
def date_slider(context, page, active=0):
    
    today = datetime.today()

    days = [];
    for i in range(0, 7):
        days += [date(2015, 4, 5 + i)]
    
    months = [];
    for i in range(1, 13):
        months += [date(2015, i, 1)]
    
    return {
        'today': today,
        'active': active,
        'days': days,
        'months': months,
        'page': page,
        'STATIC_URL': context['STATIC_URL'],
    }
    
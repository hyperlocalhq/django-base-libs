# -*- coding: utf-8 -*-
from django import template
from django.db import models
from datetime import datetime, date, timedelta
from django.utils.timezone import now as tz_now

register = template.Library()

@register.inclusion_tag('productions/includes/other_productions.html', takes_context=True)
def other_productions(context, current_event=False, current_location=False, amount=24):
    from berlinbuehnen.apps.productions.models import Production
    
    if current_location:
        locations = [current_location]
    elif current_event:
        locations = list(current_event.production.in_program_of.all()) # + list(current_event.ev_or_prod_play_locations())
    else:
        locations = []
        
    timestamp = tz_now()
    other_production_set = Production.objects.filter(
        models.Q(in_program_of__in=locations) | models.Q(play_locations__in=locations),
        show_among_others=True,
        status="published",
    ).exclude(start_date__lt=timestamp.date()).order_by('start_date', 'start_time')
    
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
def date_slider(context, page, active=0, id=''):
    
    today = datetime.today()

    days = []
    for i in range(0, 7):
        days += [date(2015, 4, 5 + i)]
    
    months = []
    for i in range(1, 13):
        months += [date(2015, i, 1)]
    
    return {
        'today': today,
        'active': active,
        'id': id,
        'days': days,
        'months': months,
        'page': page,
        'STATIC_URL': context['STATIC_URL'],
    }
    
    
@register.inclusion_tag('productions/includes/bvg.html', takes_context=True)
def bvg(context, address="", address_2=False, postal_code=False, city=False, event_date=False, event_time=False, delta=0, timesel="depart"):

    to = address
    if address_2:
        to += "\n" + address_2
    if postal_code:
        to += "\n" + postal_code
    if city:
        if postal_code:
            to += " "
        else:
            to += "\n"
        to += city
        
        

    today = datetime.now()
    
    if event_date and event_time:
        event_datetime = datetime(year=event_date.year, month=event_date.month, day=event_date.day, hour=event_time.hour, minute=event_time.minute)
        if (event_datetime < today):
            event_date = False
            event_time = False
            delta = 0
            timesel = "depart"
    
    if event_date:
        today = datetime(year=event_date.year, month=event_date.month, day=event_date.day, hour=today.hour, minute=today.minute)
    if event_time:
        today = datetime(year=today.year, month=today.month, day=today.day, hour=event_time.hour, minute=event_time.minute)
    
    if (delta < 0):
        delta *= -1;
        today -= timedelta(minutes=delta)
    else:
        today += timedelta(minutes=delta)
        
    
    return {
        'to': to,
        'date': today.strftime('%d.%m.%Y'),
        'time': today.strftime('%H:%M'),
        'timesel': timesel,
    }

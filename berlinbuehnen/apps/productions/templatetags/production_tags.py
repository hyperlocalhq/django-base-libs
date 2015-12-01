# -*- coding: utf-8 -*-
from django import template
from django.db import models
from datetime import datetime, date, timedelta, time
from django.utils.timezone import now as tz_now
from urllib import urlencode
from filebrowser.models import FileDescription
from django.utils.translation import ugettext as _

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
    ).exclude(start_date__lt=timestamp.date()).order_by('start_date', 'start_time').distinct()
    
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
    
    if delta < 0:
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


@register.inclusion_tag('productions/includes/pin.html', takes_context=True)
def pin(context, image, description=""):

    file_description = None
    file_descriptions = FileDescription.objects.filter(file_path=image).order_by("pk")
    if file_descriptions:
        file_description = file_descriptions[0]

    protected = image.copyright_restrictions == "protected"

    description = description.encode('utf-8')
    if file_description and file_description.author:
        if not description == "":
            description += ", "
        description = description + _('Photo').encode('utf-8') + ': ' + file_description.author.encode('utf-8')

    param = {
        'url': context['request'].build_absolute_uri(context['request'].get_full_path()),
        'media': context['request'].build_absolute_uri(context['MEDIA_URL']+image.path.path),
        'description': description
    }
    href = "https://www.pinterest.com/pin/create/button/?"+urlencode(param)
        
    return {
        'href': href,
        'protected': protected
    }


@register.inclusion_tag('productions/includes/add_to_calender.html', takes_context=True)
def add_to_calender(context, event):

    start_datetime = None
    if event.start_date and event.start_time:
        start_datetime = datetime(year=event.start_date.year, month=event.start_date.month, day=event.start_date.day, hour=event.start_time.hour, minute=event.start_time.minute)
    end_datetime = None

    end_date = event.end_date
    end_time = event.end_time

    two_hours = timedelta(hours=2)
    
    if start_datetime and not end_time:
        end_datetime = start_datetime + two_hours

    if end_datetime:
        end_date = date(year=end_datetime.year, month=end_datetime.month, day=end_datetime.day)
        end_time = time(hour=end_datetime.hour, minute=end_datetime.minute)

    description = event.ev_or_prod_teaser()
    if description:
        description += "\n\n"
    description += context['request'].build_absolute_uri(event.get_url_path())
        
    return {
        'event': event,
        'end_date': end_date,
        'end_time': end_time,
        'description': description
    }
# -*- coding: utf-8 -*-
from django import template
from datetime import datetime, date, timedelta, time
from django.utils.timezone import now as tz_now

register = template.Library()

@register.inclusion_tag('festivals/includes/month_slider.html', takes_context=True)
def month_slider(context, id=''):
    
    today = datetime.today()
    
    months = []
    for i in range(1, 13):
        months += [date(2015, i, 1)]
    
    return {
        'today': today,
        'id': id,
        'months': months,
        'STATIC_URL': context['STATIC_URL'],
    }
    

@register.inclusion_tag('festivals/includes/festivals_slider.html', takes_context=True)
def festivals_slider(context):
    from berlinbuehnen.apps.festivals.models import Festival
    
    today = datetime.today()
    
    festivals = Festival.objects.filter(
        slideshow = True,
        end__gte = today,
    )
        
    return {
        'festivals': festivals,
        'MEDIA_URL': context['MEDIA_URL'],
        'STATIC_URL': context['STATIC_URL'],
    }
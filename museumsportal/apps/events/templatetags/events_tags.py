# -*- coding: UTF-8 -*-
from django import template

register = template.Library()

@register.filter
def get_selected_date(event, selected_date):
    return event.get_closest_event_time(selected_date)
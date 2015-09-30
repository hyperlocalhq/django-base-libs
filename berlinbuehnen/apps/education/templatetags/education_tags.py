# -*- coding: utf-8 -*-
from django import template
from django.db import models
from datetime import datetime, date, timedelta, time
from django.utils.timezone import now as tz_now
from urllib import urlencode
from filebrowser.models import FileDescription
from django.utils.translation import ugettext as _
from berlinbuehnen.apps.education.models import Project

register = template.Library()


@register.inclusion_tag('education/includes/add_to_calender.html', takes_context=True)
def add_to_calender_education(context, department, event):

    project = event.project
    
    end_datetime = None

    two_hours = timedelta(hours=2)
    
    if not event.end:
        end_datetime = event.start + two_hours
    else:
        end_datetime = event.end

    description = project.description
    if description:
        description += "\n\n"
    description += context['request'].build_absolute_uri(project.get_url_path(event))
        
    return {
        'department': department,
        'project': project,
        'event': event,
        'end_datetime': end_datetime,
        'description': description
    }
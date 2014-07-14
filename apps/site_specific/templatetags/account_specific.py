# -*- coding: UTF-8 -*-
from django.conf import settings
from django.db.models import get_model
from django.template import loader, Template, Context
from django import template

from ccb.apps.people.models import Person

register = template.Library()

### FILTERS ###

def get_unconfirmed_contact_count(request):
    return Person.objects.filter(
        user__individualrelation__to_user=request.user,
        user__individualrelation__status="inviting",
        ).count()
    
def get_new_job_count(request):
    return 0
    
register.filter('get_unconfirmed_contact_count', get_unconfirmed_contact_count)
register.filter('get_new_job_count', get_new_job_count)


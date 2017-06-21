# -*- coding: UTF-8 -*-
from django import template

from kb.apps.people.models import Person

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

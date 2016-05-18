# -*- coding: UTF-8 -*-
from django.db import models
from django.shortcuts import render

from ccb.apps.events.models import Event
from ccb.apps.institutions.models import Institution


def event_list(request):
    institutions = Institution.objects.filter(slug__in=[
        "kulturforderpunkt_berlin",
        "crowdfunding_berlin",
        "creative_city_berlin",
        "kreativ_kultur_berlin",
        "kreativwirtschaftsberatung_berlin",
    ])
    events = Event.objects.filter(
        models.Q(organizing_institution__in=institutions) | models.Q(venue__in=institutions),
        status="published",
    ).order_by("start")[:20]

    return render(request, "kreativkultur/event_list.html", {'object_list': events})
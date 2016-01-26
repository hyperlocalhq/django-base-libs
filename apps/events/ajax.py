# -*- coding: UTF-8 -*-
import json

from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.db import models

Institution = models.get_model("institutions", "Institution")
Person = models.get_model("people", "Person")
Event = models.get_model("events", "Event")

from base_libs.middleware import get_current_user
from base_libs.middleware import get_current_language
from base_libs.utils.misc import ExtendedJSONEncoder


def get_all_events(search):
    language = get_current_language()

    if not search or len(search) < 1:
        return Event.objects.none()

    queryset = Event.objects.filter()
    if search != "all":
        queryset = queryset.filter(**{
            'title_%s__istartswith' % language: search,
        })

    return queryset
    

def get_related_events(search):
    language = get_current_language()
    
    if not search or len(search) < 1:
        return Event.objects.none()
        
    model = Event
    field_name = "related_events"
    f = model._meta.get_field(field_name)
    queryset = f.rel.to._default_manager.complex_filter(f.rel.limit_choices_to)
    
    if search != "all":
        queryset = queryset.filter(**{
            'title_%s__istartswith' % language: search,
            })
        
    return queryset


if Institution:

    def get_venues(search):

        if not get_current_user() and search != "all":
            return Institution.objects.none()

        if not search or len(search) < 1:
            return Institution.objects.none()

        queryset = Institution.objects.all()
        if search != "all":
            queryset = queryset.filter(title__istartswith=search)

        return queryset

    def get_organizing_institutions(search):
        return get_venues(search)

    def json_get_institution_attrs(request, institution_id):
        """
        Gets attributes from a given institution, such as address, phone numbers, etc...
        """
        json_data = "false"

        institution = Institution.objects.get(id=institution_id)
        contacts = institution.get_primary_contact()
        for day in ("mon", "tue", "wed", "thu", "fri", "sat", "sun"):
            for field in ("open", "break_close", "break_open", "close"):
                if getattr(institution, "%s_%s" % (day, field)):
                    contacts["%s_%s" % (day, field)] = getattr(institution, "%s_%s" % (day, field)).strftime("%H:%M")
        contacts['title'] = institution.get_title()
        json_data = json.dumps(contacts, ensure_ascii=False, cls=ExtendedJSONEncoder)

        return HttpResponse(json_data, content_type='text/javascript; charset=utf-8')

    json_get_institution_attrs = never_cache(json_get_institution_attrs)

if Person:

    def get_organizing_people(search):

        if not get_current_user() and search != "all":
            return Person.objects.none()

        if not search or len(search) < 1:
            return Person.objects.none()

        queryset = Person.objects.all()

        if search != "all":
            queryset = queryset.filter(user__username__istartswith=search)

        return queryset

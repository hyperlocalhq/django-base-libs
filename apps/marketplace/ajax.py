# -*- coding: UTF-8 -*-
import json

from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.cache import never_cache
from django.db import models
from django.contrib.auth.models import User

Institution = models.get_model("institutions", "Institution")
Person = models.get_model("people", "Person")

from base_libs.middleware import get_current_user
from base_libs.utils.misc import ExtendedJSONEncoder

def get_institutions(search):
    
    if not get_current_user() and search != "all":
        return Institution.objects.none()
    
    if not search or len(search) < 1:
        return Institution.objects.none()
    
    queryset = Institution.objects.filter(
        status__in=("published", "published_commercial"),
        )
    if search != "all":
        queryset = queryset.filter(title__istartswith=search)
        
    return queryset

def get_users(search):
    
    if not get_current_user() and search != "all":
        return User.objects.none()
    
    if not search or len(search) < 1:
        return User.objects.none()
    
    queryset = User.objects.filter()
    
    if search != "all":
        queryset = queryset.filter(username__istartswith=search)
        
    return queryset

def get_people(search):
    
    if not get_current_user() and search != "all":
        return Person.objects.none()
    
    if not search or len(search) < 1:
        return Person.objects.none()
    
    queryset = Person.objects.filter(
        status="published",
        )
    if search != "all":
        queryset = queryset.filter(user__username__istartswith=search)
        
    return queryset


def json_get_institution_attrs(request, institution_id):
    """
    Gets attributes from a given institution, such as address, phone numbers, etc...
    """
    institution = Institution.objects.get(id=institution_id)
    contacts = institution.get_primary_contact()
    for day in ("mon", "tue", "wed", "thu", "fri", "sat", "sun"):
        for field in ("open", "break_close", "break_open", "close"):
            if getattr(institution, "%s_%s" % (day, field)):
                contacts["%s_%s" % (day, field)] = getattr(institution, "%s_%s" % (day, field)).strftime("%H:%M")
    contacts['title'] = institution.get_title()
    json_str = json.dumps(contacts, ensure_ascii=False, cls=ExtendedJSONEncoder)
    
    return HttpResponse(json_str, content_type='text/javascript; charset=utf-8')

json_get_institution_attrs = never_cache(json_get_institution_attrs)



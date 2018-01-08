# -*- coding: UTF-8 -*-
import json

from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.cache import never_cache
from django.db import models

from base_libs.middleware import get_current_user
from base_libs.utils.misc import ExtendedJSONEncoder, get_related_queryset

app = models.get_app("institutions")
Institution, InstitutionalContact = (
    app.Institution, app.InstitutionalContact,
    )

def get_published_institutions(search):
    
    if not get_current_user():
        return []
    
    if not search or len(search) < 1:
        return []
    
    queryset = Institution.objects.filter(
        status__in=("published", "published_commercial"),
        )
    if search != "all":
        queryset = queryset.filter(title__istartswith=search)
        
    return queryset

def get_all_institutions(search):
    
    if not get_current_user():
        return []
    
    if not search or len(search) < 1:
        return []
    
    queryset = Institution.objects.all()
    if search != "all":
        queryset = queryset.filter(title__istartswith=search)
        
    return queryset

def json_get_institution_attrs(request, institution_id):
    """
    Gets attributes from a given institution, such as address, phone numbers, etc...
    """
    institution = Institution.objects.get(id=institution_id)
    contact = institution.get_primary_contact()
    contact['title'] = institution.get_title()
    contact['location_type'] = get_related_queryset(
        InstitutionalContact,
        "location_type",
        ).get(slug="main")
    json_str = json.dumps(contact, ensure_ascii=False, cls=ExtendedJSONEncoder)
    
    return HttpResponse(json_str, content_type='text/javascript; charset=utf-8')

json_get_institution_attrs = never_cache(json_get_institution_attrs)

# -*- coding: UTF-8 -*-

from django.db import models
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.cache import never_cache
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from base_libs.views import access_denied

from jetson.apps.structure.models import Category
from jetson.apps.utils.views import object_list, object_detail
from jetson.apps.utils.views import get_abc_list
from jetson.apps.utils.views import filter_abc

from ccb.apps.people.models import Person
from ccb.apps.institutions.models import Institution
from ccb.apps.site_specific.models import ContextItem
from ccb.apps.events.views import event_list

from actstream.models import following



@never_cache
def counselling_events_list(request, slug, **kwargs):
    """
    Lists the institution's events
    """
    item = get_object_or_404(
        ContextItem,
        content_type__model__in=("person", "institution"),
        slug=slug,
    )
    if item.is_person():
        if not request.user.has_perm("people.change_person", item.content_object) and item.status not in ("published", "published_commercial"):
            return access_denied(request)
        person = item.content_object
        kwargs['queryset'] = kwargs['queryset'].filter(
            models.Q(organizing_person=person)
        ).order_by('-creation_date')
        kwargs['template_name'] = 'counselling/events_list.html'
    else:
        if not request.user.has_perm("institutions.change_institution", item.content_object) and item.status not in ("published", "published_commercial"):
            return access_denied(request)
        institution = item.content_object
        kwargs['queryset'] = kwargs['queryset'].filter(
            models.Q(organizing_institution=institution) |
            models.Q(venue=institution),
        ).order_by('-creation_date')
        kwargs['template_name'] = 'counselling/events_list.html'

    kwargs.setdefault("extra_context", {})
    kwargs['extra_context']['object'] = item.content_object
    kwargs['title'] = _("Events by/at %s") % item.content_object.get_title()
    return event_list(request, show="related", **kwargs)
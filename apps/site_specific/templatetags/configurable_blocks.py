# -*- coding: UTF-8 -*-
import re

from django.conf import settings
from django import template

from jetson.apps.structure.models import Term
from base_libs.utils.misc import get_related_queryset
from ccb.apps.people.models import Person
from ccb.apps.institutions.models import Institution
from ccb.apps.resources.models import Document
from ccb.apps.events.models import Event
from ccb.apps.groups_networks.models import PersonGroup

register = template.Library()

### FILTERS ###

def get_sector_info(path):
    class AdditionalInfo(object):
        def __init__(self, sector_slug=""):
            self.sector_slug = sector_slug

        def get_new_people(self, count=3):
            try:
                cs = get_related_queryset(Person, "creative_sectors").get(
                    slug=self.sector_slug
                )
                return Person.objects.filter(
                    status="published",
                    creative_sectors__lft__gte=cs.lft,
                    creative_sectors__rght__lte=cs.rght,
                    creative_sectors__tree_id=cs.tree_id,
                ).select_related().order_by('-auth_user.date_joined', 'auth_user.username').distinct()[:count]
            except Exception:
                return Person.objects.filter(
                    status="published",
                ).select_related().order_by('-auth_user.date_joined', 'auth_user.username').distinct()[:count]

        def get_new_institutions(self, count=3):
            try:
                cs = get_related_queryset(Institution, "creative_sectors").get(
                    slug=self.sector_slug
                )
                return Institution.objects.filter(
                    status__in=("published", "published_commercial"),
                    creative_sectors__slug=self.sector_slug
                ).order_by('-creation_date', 'title').distinct()[:count]
            except Exception:
                return Institution.objects.filter(
                    status__in=("published", "published_commercial"),
                ).order_by('-creation_date', 'title').distinct()[:count]

        def get_new_events(self, count=3):
            try:
                cs = get_related_queryset(Institution, "creative_sectors").get(
                    slug=self.sector_slug
                )
                return Event.objects.filter(
                    status="published",
                    creative_sectors__slug=self.sector_slug
                ).order_by('-creation_date', 'title').distinct()[:count]
            except Exception:
                return Event.objects.filter(
                    status="published",
                ).order_by('-creation_date', 'title').distinct()[:count]

        def get_new_documents(self, count=3):
            try:
                cs = get_related_queryset(Institution, "creative_sectors").get(
                    slug=self.sector_slug
                )
                return Document.objects.filter(
                    status__in=("published", "published_commercial"),
                    creative_sectors__slug=self.sector_slug
                ).order_by('-creation_date', 'title').distinct()[:count]
            except Exception:
                return Document.objects.filter(
                    status__in=("published", "published_commercial"),
                ).order_by('-creation_date', 'title').distinct()[:count]

        def get_new_groups(self, count=3):
            try:
                cs = get_related_queryset(Institution, "creative_sectors").get(
                    slug=self.sector_slug
                )
                return PersonGroup.objects.order_by('-creation_date', 'title').distinct()[:count]
            except Exception:
                return PersonGroup.objects.order_by('-creation_date', 'title').distinct()[:count]

        def get_new_lists(self, count=3):
            return []

    sector_slug = ""
    if hasattr(settings, "CREATIVE_SECTOR"):
        sector_slug = Term.objects.get(
            vocabulary__sysname="categories_creativesectors",
            sysname=settings.CREATIVE_SECTOR,
        ).slug
    path_re = re.compile('^/creative-sector/(?P<slug>[^/]+)/$')
    m = re.match(path_re, path)
    if m:
        sector_slug = m.groupdict()["slug"]

    return AdditionalInfo(sector_slug)


register.filter('get_sector_info', get_sector_info)

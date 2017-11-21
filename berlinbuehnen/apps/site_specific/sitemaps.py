# -*- coding: UTF-8 -*-
from django.contrib.sitemaps import Sitemap
from cms.sitemaps import CMSSitemap as CMSSitemapBase


class CMSSitemap(CMSSitemapBase):
    limit = 100

    def items(self):
        from cms.utils.page_resolver import get_page_queryset
        page_queryset = get_page_queryset(None)
        all_pages = page_queryset.published().filter(login_required=False, in_navigation=True)
        return all_pages


class LocationSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    limit = 100

    def items(self):
        from berlinbuehnen.apps.locations.models import Location
        qs = Location.objects.filter(status="published")
        return qs

    def lastmod(self, obj):
        return obj.modified_date


class EventSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5
    limit = 100

    def items(self):
        from datetime import datetime
        from berlinbuehnen.apps.productions.models import Event
        qs = Event.objects.filter(production__status="published").exclude(event_status="trashed")
        qs = qs.filter(production__part=None)
        now = datetime.now()
        qs = qs.exclude(
            start_date__lte=now,
            start_time__lt=now,
        ).distinct()
        qs = qs.only('pk', 'start_date', 'start_time', 'production', 'event_status')

        return qs

    def lastmod(self, obj):
        return obj.modified_date


sitemaps = {
    'pages': CMSSitemap,
    'locations': LocationSitemap,
    'events': EventSitemap,
}

# -*- coding: UTF-8 -*-
from django.contrib.sitemaps import Sitemap
from cms.sitemaps import CMSSitemap as CMSSitemapBase


class CMSSitemap(CMSSitemapBase):
    limit = 100

    def items(self):
        all_pages = super(CMSSitemap, self).items().filter(page__in_navigation=True)
        return all_pages


class LocationSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    limit = 100

    def items(self):
        from ruhrbuehnen.apps.locations.models import Location
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
        from ruhrbuehnen.apps.productions.models import Event
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


class FestivalSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5
    limit = 100

    def items(self):
        from ruhrbuehnen.apps.festivals.models import Festival
        qs = Festival.objects.filter(status="published")
        return qs

    def lastmod(self, obj):
        return obj.modified_date


sitemaps = {
    'pages': CMSSitemap,
    'locations': LocationSitemap,
    'events': EventSitemap,
    'festivals': FestivalSitemap,
}

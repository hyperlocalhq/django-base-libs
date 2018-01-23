# -*- coding: UTF-8 -*-

from django.contrib.sitemaps import Sitemap

from cms.sitemaps import CMSSitemap as CMSSitemapBase

from museumsportal.apps.museums.models import Museum
from museumsportal.apps.exhibitions.models import Exhibition
from museumsportal.apps.events.models import Event
from museumsportal.apps.workshops.models import Workshop


class CMSSitemap(CMSSitemapBase):
    def items(self):
        from cms.utils.page_resolver import get_page_queryset
        page_queryset = get_page_queryset(None)
        all_pages = page_queryset.published().filter(login_required=False, in_navigation=True)
        return all_pages


class MuseumSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Museum.objects.filter(status="published")

    def lastmod(self, obj):
        return obj.modified_date


class ExhibitionSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Exhibition.objects.filter(status="published")

    def lastmod(self, obj):
        return obj.modified_date


class EventSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Event.objects.filter(status="published")

    def lastmod(self, obj):
        return obj.modified_date


class WorkshopSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Workshop.objects.filter(status="published")

    def lastmod(self, obj):
        return obj.modified_date


sitemaps = {
    'cms_pages': CMSSitemap,
    'museums': MuseumSitemap,
    'exhibitions': ExhibitionSitemap,
    'events': EventSitemap,
    'workshops': WorkshopSitemap,
}

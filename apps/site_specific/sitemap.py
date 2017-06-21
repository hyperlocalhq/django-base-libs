# -*- coding: UTF-8 -*-
from django.contrib.sitemaps import Sitemap

from base_libs.middleware import get_current_language
from kb.apps.site_specific.models import ContextItem


class ContextItemSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return ContextItem.objects.filter(
            status__in=("published", "published_commercial"),
        ).distinct()

    def location(self, obj):
        return "/%s%s" % (
            get_current_language(),
            obj.get_url_path()
        )

    def lastmod(self, obj):
        return obj.modified_date

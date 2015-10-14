# -*- coding: UTF-8 -*-
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.utils.translation import ugettext
from django.db import models


class MediaGalleryRssFeed(Feed):
    link = ""

    # title and description templates for displaying the feeds
    title_template = "media_gallery/feeds/feed_title.html"
    description_template = "media_gallery/feeds/feed_description.html"

    def get_object(self, request, *args, **kwargs):
        self.request = request
        self.kwargs = kwargs
        return None

    def title(self):
        Site = models.get_model("sites", "Site")
        title = ugettext("%(site)s projects") % {
            'site': Site.objects.get_current().name,
        }
        return title

    def description(self, obj):
        return ugettext("Latest projects")

    def items(self, obj):
        return self.kwargs['queryset']

    def item_link(self, obj):
        try:
            return obj.get_url()
        except Exception:
            return ""

    def item_pubdate(self, obj):
        """
        Takes an item, as returned by items(), and returns the item's
        pubdate.
        """
        return obj.published_from


class MediaGalleryAtomFeed(MediaGalleryRssFeed):
    feed_type = Atom1Feed

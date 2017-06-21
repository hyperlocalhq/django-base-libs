# -*- coding: UTF-8 -*-
import re

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils.encoding import force_unicode
from django.contrib.sites.models import Site
from django.db import models

from kb.apps.site_specific.views import get_browse_queryset

app = models.get_app("people")
Person, URL_ID_PERSON, URL_ID_PEOPLE = (
    app.Person, app.URL_ID_PERSON, app.URL_ID_PEOPLE,
)

app = models.get_app("institutions")
Institution, URL_ID_INSTITUTION, URL_ID_INSTITUTIONS = (
    app.Institution, app.URL_ID_INSTITUTION, app.URL_ID_INSTITUTIONS,
)

app = models.get_app("resources")
Document, URL_ID_DOCUMENT, URL_ID_DOCUMENTS = (
    app.Document, app.URL_ID_DOCUMENT, app.URL_ID_DOCUMENTS,
)

app = models.get_app("events")
Event, URL_ID_EVENT, URL_ID_EVENTS = (
    app.Event, app.URL_ID_EVENT, app.URL_ID_EVENTS,
)

app = models.get_app("groups_networks")
PersonGroup, URL_ID_PERSONGROUP, URL_ID_PERSONGROUPS = (
    app.PersonGroup, app.URL_ID_PERSONGROUP, app.URL_ID_PERSONGROUPS,
)


class BrowseRssFeed(Feed):
    link = "/browse/feeds/rss/"

    title_template = "site_specific/feeds/feed_title.html"
    description_template = "site_specific/feeds/feed_description.html"

    def __init__(self, feed_slug, request, **kwargs):
        Feed.__init__(self, feed_slug, request)
        self.request = request
        self.kwargs = kwargs

    def title(self, obj):
        result = _("Browse Feeds @ %(site)s") % {
            'site': Site.objects.get_current().name,
        }
        return force_unicode(result)

    def description(self, obj):
        return force_unicode(_("Browse result feeds"))

    def items(self, obj):
        return get_browse_queryset(self.request, **self.kwargs)['queryset']

    def item_pubdate(self, obj):
        """
        Takes an item, as returned by items(), and returns the item's
        pubdate.
        """
        return obj.creation_date


class BrowseAtomFeed(BrowseRssFeed):
    link = "/"

    title_template = "site_specific/feeds/feed_title.html"
    description_template = "site_specific/feeds/feed_description.html"

    feed_type = Atom1Feed


class LatestPublishedObjectsRssFeed(Feed):
    link = "/"
    title_template = "site_specific/feeds/feed_title.html"
    description_template = "site_specific/feeds/feed_description.html"

    def get_object(self, request, *args, **kwargs):
        self.request = request

        self.ot = kwargs['ot_url_part']
        if self.ot == URL_ID_DOCUMENTS:
            self.model = Document
            self.object_title = _("Documents")
        elif self.ot == URL_ID_EVENTS:
            self.model = Event
            self.object_title = _("Events")
        elif self.ot == URL_ID_PERSONGROUPS:
            self.model = PersonGroup
            self.object_title = _("Groups")
        elif self.ot == URL_ID_INSTITUTIONS:
            self.model = Institution
            self.object_title = _("Institutions")
        elif self.ot == URL_ID_PEOPLE:
            self.model = Person
            self.object_title = _("Persons")
        self.kwargs = kwargs
        try:
            self.amount = request.GET['amount']
        except Exception:
            self.amount = 5

    def title(self, obj):
        result = _("Latest published %(object)s @ %(site)s") % {
            'object': self.object_title,
            'site': Site.objects.get_current().name,
        }
        return force_unicode(result)

    def items(self, obj):

        sector_slug = getattr(settings, "CREATIVE_SECTOR", "")
        path_re = re.compile('^/creative-sector/(?P<slug>[^/]+)/$')
        m = re.match(path_re, self.request.path)
        if m:
            sector_slug = m.groupdict()["slug"]
        if hasattr(self.model.objects, "latest_published"):
            qs = self.model.objects.latest_published()
        else:
            qs = self.model.objects.all()
        if sector_slug:
            qs = qs.filter(creative_sectors__slug=sector_slug)
        if qs.model.__name__ == "Event":
            qs = qs.order_by("start")

        return qs[:self.amount]

    def item_pubdate(self, obj):
        """
        Takes an item, as returned by items(), and returns the item's
        pubdate.
        """
        return obj.creation_date


class LatestPublishedObjectsAtomFeed(LatestPublishedObjectsRssFeed):
    link = "/"
    title_template = "site_specific/feeds/feed_title.html"
    description_template = "site_specific/feeds/feed_description.html"
    feed_type = Atom1Feed

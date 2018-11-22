# -*- coding: UTF-8 -*-
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.utils.translation import ugettext
from django.utils.encoding import force_unicode
from django.db import models


class ArticleRssFeed(Feed):
    link = ""

    # title and description templates for displaying the feeds
    title_template = "articles/feeds/feed_title.html"
    description_template = "articles/feeds/feed_description.html"

    def get_object(self, request, *args, **kwargs):
        self.request = request
        self.kwargs = kwargs
        return None

    def title(self):
        Site = models.get_model("sites", "Site")

        if 'article_type' in self.kwargs:
            if 'category' in self.kwargs:
                title = ugettext("%(category)s %(article_type)s at %(site)s") % {
                    'site': Site.objects.get_current().name,
                    'article_type': force_unicode(self.kwargs['article_type'].title),
                    'category': force_unicode(self.kwargs['category'].title),
                }
            else:
                title = ugettext("%(site)s %(article_type)s") % {
                    'site': Site.objects.get_current().name,
                    'article_type': force_unicode(self.kwargs['article_type'].title),
                }
        else:
            if 'category' in self.kwargs:
                title = ugettext("%(category)s News at %(site)s") % {
                    'site': Site.objects.get_current().name,
                    'category': force_unicode(self.kwargs['category'].title),
                }
            else:
                title = ugettext("%(site)s News") % {
                    'site': Site.objects.get_current().name,
                }
        return title

    def description(self, obj):
        desc = ""
        if 'article_type' in self.kwargs:
            desc = ugettext("Latest %(article_type)s") % {
                'article_type': self.kwargs['article_type'].title,
            }
        return desc

    def items(self, obj):
        return self.kwargs['queryset']

    def item_link(self, obj):
        if obj.is_excerpt:
            return obj.external_url
        return obj.get_absolute_url()

    def item_pubdate(self, obj):
        """
        Takes an item, as returned by items(), and returns the item's
        pubdate.
        """
        return obj.published_from


class ArticleAtomFeed(ArticleRssFeed):
    link = ""

    # title and description templates for displaying the feeds
    title_template = "articles/feeds/feed_title.html"
    description_template = "articles/feeds/feed_description.html"

    feed_type = Atom1Feed

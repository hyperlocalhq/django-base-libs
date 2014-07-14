# -*- coding: UTF-8 -*-
from django.db.models.loading import load_app
from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed
from django.utils.translation import ugettext, ugettext_lazy as _
from django.conf import settings
from django.utils.encoding import force_unicode
from django.db import models

class ArticleRssFeed(Feed):
    
    link = ""

    # title and description templates for displaying the feeds
    title_template = "articles/feeds/feed_title.html"
    description_template = "articles/feeds/feed_description.html"
    
    def __init__(self, feed_slug, request, **kwargs):
        Feed.__init__(self, feed_slug, request)
        self.request = request
        self.kwargs = kwargs
        
    def title(self):
        Site = models.get_model("sites", "Site")
        
        if not self.kwargs.has_key("type"):
            title = ugettext("%(site)s News") % {
                'site': Site.objects.get_current().name,
                }
        else:
            title = ugettext("%(site)s %(article_type)s") % {
                'site': Site.objects.get_current().name,
                'article_type': force_unicode(self.kwargs['type'].get_title()),
                }
        return title
            
    def description(self, obj):
        desc = ""
        if self.kwargs.has_key("type"):
            if self.kwargs.has_key("creative_sector"):
                desc = ugettext("Latest %(article_type)s at %(creative_sector)s") % {
                    'article_type': self.kwargs['type'].get_title(),
                    'creative_sector': self.kwargs['creative_sector'].get_title(),
                    }
            else:
                desc = ugettext("Latest %(article_type)s") % {
                    'article_type': self.kwargs['type'].get_title(),
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

# -*- coding: UTF-8 -*-
from django.db.models.loading import load_app
from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils.encoding import force_unicode

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
        
        if not self.kwargs.has_key("type"):
            title = force_unicode(_("Article feeds"))
        else:
            title = "%s %s" % (
                force_unicode(self.kwargs['type'].get_title()),
                force_unicode(_("feeds")),
                )
        
        if self.kwargs.has_key("creative_sector"):
            return "%s @ %s" % (
                title,
                self.kwargs['creative_sector'].get_title(),
                )
        else:
            return title
            
    def description(self, obj):
        if not self.kwargs.has_key("type"):
            return force_unicode(_("Latest articles"))
        else:
            return "%s %s" % (force_unicode(_("Latest")), self.kwargs['type'].get_title())

    def items(self, obj):
        return self.kwargs['queryset']
                 
    def item_link(self, obj):
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
    

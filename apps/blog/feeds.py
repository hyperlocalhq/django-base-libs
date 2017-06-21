# -*- coding: UTF-8 -*-
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode
from django.contrib.sites.models import Site

from kb.apps.blog.models import Post

class RssFeed(Feed):
    
    link = ""

    # title and description templates for displaying the feeds
    title_template = "blog/feeds/feed_title.html"
    description_template = "blog/feeds/feed_description.html"

    def __init__(self, **kwargs):
        Feed.__init__(self)
        self.kwargs = kwargs

    def title(self):
        obj = self.kwargs.get('object', None)
        if obj:
            result = _(u"Feeds for '%(obj)s' @ %(site)s") % {
                'obj': obj,
                'site': Site.objects.get_current().name,
                } 
        else:
            result = _(u"Blog @ %(site)s") % {
                'site': Site.objects.get_current().name,
                }
        return force_unicode(result)

    def description(self, obj):
        return force_unicode(_("Latest posts"))

    def items(self, obj):
        container = self.kwargs.get('container', None)
        return Post.published_objects.filter(blog=container).order_by('-published_from')[:5]
                 
    def item_link(self, obj):
        return obj.get_url()
    
    def item_pubdate(self, obj):
        return obj.published_from
    
class AtomFeed(RssFeed):
    link = "/blog/feeds/atom/"
    
    # title and description templates for displaying the feeds
    title_template = "blog/feeds/feed_title.html"
    description_template = "blog/feeds/feed_description.html"
    
    feed_type = Atom1Feed
    

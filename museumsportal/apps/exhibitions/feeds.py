# -*- coding: UTF-8 -*-
from django.contrib.syndication.views import Feed
from django.utils.translation import ugettext, ugettext_lazy as _
from django.conf import settings
from django.db import models

from models import Exhibition

class ExhibitionRssFeed(Feed):
    
    link = ""
    title = _("Exhibitions in the Museums of Berlin")

    # title and description templates for displaying the feeds
    description_template = "exhibitions/feeds/feed_description.html"
    
    def items(self, obj):
        return Exhibition.objects.filter(status="published").order_by("-creation_date")[:50]
        
    def item_title(self, item):
        return item.title
        
    def item_link(self, obj):
        return obj.get_url()
    
    def item_pubdate(self, obj):
        return obj.creation_date
    

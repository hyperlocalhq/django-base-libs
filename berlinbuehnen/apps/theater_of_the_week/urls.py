# -*- coding: UTF-8 -*-
from django.conf.urls import *

from .feeds import TheaterOfTheWeekRssFeed, TheaterOfTheWeekAtomFeed
from . import views

theater_of_the_week_feeds = {
    'rss': TheaterOfTheWeekRssFeed,
    'atom': TheaterOfTheWeekAtomFeed,
}


urlpatterns = [
    url(r'^$',
        views.theater_of_the_week,
        name="theater_of_the_week",
    ),
    
    # articles aggregated syndication feeds
    url(r'^feeds/(?P<feed_type>.*)/$', 
        views.theater_of_the_week_feed,
        dict(type_sysname='all', **theater_of_the_week_feeds),
        name="theater_of_the_week_feed",
    ), 
 
    # article details
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<theater_of_the_week_slug>[^/]+)/$',
        views.theater_of_the_week_object_detail, name='theater_of_the_week_object_detail'
    ),
]



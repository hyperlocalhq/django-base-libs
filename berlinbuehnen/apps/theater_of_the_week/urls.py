# -*- coding: UTF-8 -*-

from django.conf.urls import *
from base_libs.utils.misc import get_installed, path_in_installed_app

TheaterOfTheWeekRssFeed = get_installed("theater_of_the_week.feeds.TheaterOfTheWeekRssFeed")
TheaterOfTheWeekAtomFeed = get_installed("theater_of_the_week.feeds.TheaterOfTheWeekAtomFeed")

theater_of_the_week_feeds = {
    'rss': TheaterOfTheWeekRssFeed,
    'atom': TheaterOfTheWeekAtomFeed,
}


urlpatterns = patterns(path_in_installed_app('theater_of_the_week.views'),
    # articles aggregated overview
    url(r'^$', 
        'theater_of_the_week_archive_index',
        dict(num_latest=5, 
            type_sysname='all'),
        name="theater_of_the_week_archive",
    ),
    
    # articles aggregated syndication feeds
    url(r'^feeds/(?P<feed_type>.*)/$', 
        'theater_of_the_week_feed', 
        dict(theater_of_the_week_feeds, type_sysname='all'),
        name="theater_of_the_week_feed",
    ), 
 
    # article details
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<theater_of_the_week_slug>[^/]+)/$',
        'theater_of_the_week_object_detail', name='theater_of_the_week_object_detail'
    ),
    
)



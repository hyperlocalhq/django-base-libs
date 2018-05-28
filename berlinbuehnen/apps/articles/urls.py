# -*- coding: UTF-8 -*-

from django.conf.urls import *
from base_libs.utils.misc import get_installed, path_in_installed_app

ArticleRssFeed = get_installed("articles.feeds.ArticleRssFeed")
ArticleAtomFeed = get_installed("articles.feeds.ArticleAtomFeed")

article_feeds = {
    'rss': ArticleRssFeed,
    'atom': ArticleAtomFeed,
}


urlpatterns = patterns(path_in_installed_app('articles.views'),
    # articles aggregated overview
    url(r'^$', 
        'article_archive_index',
        dict(paginate_by=50,
            num_latest=2000,
            type_sysname='all',
            template_name="articles/articles_overview.html"),
        name="article_archive",
    ),
    
    # articles aggregated syndication feeds
    url(r'^feeds/(?P<feed_type>.*)/$', 
        'article_feed', 
        dict(article_feeds, type_sysname='all'),
        name="article_feed",
    ), 

    # articles aggregated date-based by year
    url(r'^(?P<year>\d{4})/$',
        'article_archive_year', 
        dict(paginate_by=5)
    ), 

    # articles aggregated date-based by month
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$', 
        'article_archive_month', 
        dict(paginate_by=5)
    ),

    # articles aggregated date-based by day
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', 
        'article_archive_day',
        dict(paginate_by=5)
    ),
 
    # article details
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<article_slug>[^/]+)/$',
        'article_object_detail', name='article_object_detail'
    ),
)

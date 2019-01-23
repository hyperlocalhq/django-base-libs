# -*- coding: UTF-8 -*-

from django.conf.urls import *
from base_libs.utils.misc import get_installed

ArticleRssFeed = get_installed("articles.feeds.ArticleRssFeed")
ArticleAtomFeed = get_installed("articles.feeds.ArticleAtomFeed")

article_feeds = {
    'rss': ArticleRssFeed,
    'atom': ArticleAtomFeed,
}

from . import views

urlpatterns = [
    # articles aggregated overview
    url(r'^$', 
        views.article_archive_index,
        dict(num_latest=5, 
            type_sysname='all',
            template_name="articles/articles_overview.html"),
        name="article_archive",
    ),
    
    # articles aggregated syndication feeds
    url(r'^feeds/(?P<feed_type>.*)/$', 
        views.article_feed,
        dict(article_feeds, type_sysname='all'),
        name="article_feed",
    ), 

    # articles aggregated date-based by year
    url(r'^(?P<year>\d{4})/$',
        views.article_archive_year,
        dict(paginate_by=5)
    ), 

    # articles aggregated date-based by month
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$', 
        views.article_archive_month,
        dict(paginate_by=5)
    ),

    # articles aggregated date-based by day
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', 
        views.article_archive_day,
        dict(paginate_by=5)
    ),
 
    # article details
    url(r'^(?P<article_slug>[^/]+)/$', 
        views.article_object_detail, name='article_object_detail'
    ),

]
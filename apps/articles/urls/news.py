from django.conf.urls import *

from ccb.apps.articles.feeds import ArticleRssFeed, ArticleAtomFeed

article_feeds = {
    'rss': ArticleRssFeed(),
    'atom': ArticleAtomFeed(),
}

from .. import views


urlpatterns = [
    url(
        r'^$',
        views.article_archive_news,
        dict(creative_sector_slug='all', paginate_by=24, num_latest=None, type_sysname='news'),
        name="article_archive_for_news",
    ),

    url(
        r'^favorites/$',
        views.article_archive_news,
        dict(creative_sector_slug='all', paginate_by=24, num_latest=None, type_sysname='news', show="favorites"),
        name="article_archive_favoorites_for_news",
    ),

    url(
        r'^category/(?P<type_sysname>[^/]+)/$',
        views.article_archive_news,
        dict(creative_sector_slug='all', paginate_by=24, num_latest=None),
        name="article_archive_for_news_by_type",
    ),

    # articles aggregated syndication feeds
    url(
        r'^category/(?P<type_sysname>[^/]+)/feeds/(?P<feed_type>rss|atom)/$',
        views.article_feed,
        dict(article_feeds, creative_sector_slug='all'),
        name="article_feed_for_news",
    ),

    # articles aggregated syndication feeds
    url(
        r'^feeds/(?P<feed_type>rss|atom)/$',
        views.article_feed,
        dict(article_feeds, creative_sector_slug='all', type_sysname='news'),
        name="article_feed_for_news",
    ),

    # articles aggregated date-based by year
    url(
        r'^(?P<year>\d{4})/$',
        views.article_archive_year,
        dict(creative_sector_slug='all', paginate_by=24, type_sysname='news'),
        name="article_archive_year_for_news",
    ),

    # articles aggregated date-based by month
    url(
        r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        views.article_archive_month,
        dict(creative_sector_slug='all', paginate_by=24, type_sysname='news'),
        name="article_archive_month_for_news",
    ),

    # articles aggregated date-based by day
    url(
        r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
        views.article_archive_day,
        dict(creative_sector_slug='all', paginate_by=24, type_sysname='news'),
        name="article_archive_day_for_news",
    ),

    # articles without any creative sector details
    url(
        r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<article_slug>[^/]+)/$',
        views.article_object_detail,
        dict(creative_sector_slug='all', type_sysname='news'),
        name="article_object_detail_for_news",
    ),
]

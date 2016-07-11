from django.conf.urls import *

from ccb.apps.articles.feeds import ArticleRssFeed, ArticleAtomFeed

article_feeds = {
    'rss': ArticleRssFeed(),
    'atom': ArticleAtomFeed(),
}

urlpatterns = patterns(
    'ccb.apps.articles.views',
    url(
        r'^$',
        'article_archive_interviews',
        dict(creative_sector_slug='all', paginate_by=24, num_latest=None, type_sysname='interviews'),
        name="article_archive_for_interviews",
    ),
    url(
        r'^overview/$',
        'magazine_overview',
        name="magazine_overview",
    ),
    url(
        r'^favorites/$',
        'article_archive_interviews',
        dict(creative_sector_slug='all', paginate_by=24, num_latest=None, type_sysname='interviews', show="favorites"),
        name="article_archive_favoorites_for_interviews",
    ),

    url(
        r'^category/(?P<type_sysname>[^/]+)/$',
        'article_archive_interviews',
        dict(creative_sector_slug='all', paginate_by=24, num_latest=None),
        name="article_archive_for_interviews_by_type",
    ),
    # articles aggregated syndication feeds
    url(
        r'^feeds/(?P<feed_type>.*)/$',
        'article_feed',
        dict(article_feeds, creative_sector_slug='all', type_sysname='interviews'),
        name="article_feed_for_interviews",
    ),

    # articles aggregated date-based by year
    url(
        r'^(?P<year>\d{4})/$',
        'article_archive_year',
        dict(creative_sector_slug='all', paginate_by=24, type_sysname='interviews'),
        name="article_archive_year_for_interviews",
    ),

    # articles aggregated date-based by month
    url(
        r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        'article_archive_month',
        dict(creative_sector_slug='all', paginate_by=24, type_sysname='interviews'),
        name="article_archive_month_for_interviews",
    ),

    # articles aggregated date-based by day
    url(
        r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
        'article_archive_day',
        dict(creative_sector_slug='all', paginate_by=24, type_sysname='interviews'),
        name="article_archive_day_for_interviews",
    ),

    # articles without any creative sector details
    url(
        r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<article_slug>[^/]+)/$',
        'article_object_detail',
        dict(creative_sector_slug='all', type_sysname='interviews'),
        name='article_object_detail_for_interviews',
    ),
)

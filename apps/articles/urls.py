from django.conf.urls import *

from ccb.apps.articles.feeds import ArticleRssFeed, ArticleAtomFeed

article_feeds = {
    'rss': ArticleRssFeed,
    'atom': ArticleAtomFeed,
}

urlpatterns = patterns(
    'ccb.apps.articles.views',

    # url(r'^articles/$', lambda request: redirect("/"), name="article_archive"),
    url(r'^articles/$',
        'article_archive_non_interviews',
        dict(creative_sector_slug='all', paginate_by=10, num_latest=None),
        name="article_archive",
        ),
    url(r'^interviews/$',
        'article_archive_interviews',
        dict(creative_sector_slug='all', paginate_by=10, num_latest=None),
        name="interviews_archive",
        ),
    url(r'^$',
        'article_archive_index',
        dict(creative_sector_slug='all', paginate_by=10, num_latest=None)
        ),

    # articles aggregated syndication feeds
    # FIXME
    # url(r'^feeds/(?P<feed_type>.*)/$',
    #     'article_feed',
    #     dict(article_feeds, creative_sector_slug='all', type_sysname='all'),
    #     name="article_feed",
    #     ),

    # articles aggregated by type
    url(r'^$',
        'article_archive_index',
        dict(creative_sector_slug='all', paginate_by=10, num_latest=None)
        ),

    # articles aggregated date-based by year
    url(r'^(?P<year>\d{4})/$',
        'article_archive_year',
        dict(creative_sector_slug='all', paginate_by=10)
        ),

    # articles aggregated date-based by month
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        'article_archive_month',
        dict(creative_sector_slug='all', paginate_by=10)
        ),

    # articles aggregated date-based by day
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
        'article_archive_day',
        dict(creative_sector_slug='all', paginate_by=10)
        ),

    # articles without any creative sector details
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<article_slug>[^/]+)/$',
        'article_object_detail',
        dict(creative_sector_slug='all'),
        name='article_object_detail',
        ),
    # articles for creative sector overview
    url(r'^creative-sector/(?P<creative_sector_slug>[^/]+)/$',
        'article_archive_index',
        dict(num_latest=None,
             type_sysname='all',
             template_name="articles/articles_archive.html")
        ),

    # featured articles for creative sector overview
    url(r'^creative-sector/(?P<creative_sector_slug>[^/]+)/features/$',
        'article_archive_index',
        dict(only_features=True,
             num_latest=None,
             type_sysname='all',
             template_name="articles/articles_archive.html")
        ),

    # articles for creative sector date-based by year
    url(r'^creative-sector/(?P<creative_sector_slug>[^/]+)/(?P<year>\d{4})/$',
        'article_archive_year',
        dict(paginate_by=10)
        ),

    # articles for creative sector date-based by month
    url(r'^creative-sector/(?P<creative_sector_slug>[^/]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        'article_archive_month',
        dict(paginate_by=10)
        ),

    # articles for creative sector date-based by day
    url(
        r'^creative-sector/(?P<creative_sector_slug>[^/]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
        'article_archive_day',
        dict(paginate_by=10)
    ),

    # articles for creative sector details
    url(
        r'^creative-sector/(?P<creative_sector_slug>[^/]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<article_slug>[^/]+)/$',
        'article_object_detail',
    ),

    # FIXME
    # url(r'^creative-sector/(?P<creative_sector_slug>[^/]+)/feeds/(?P<feed_type>.*)/$',
    #     'article_feed', article_feeds
    #     ),

)

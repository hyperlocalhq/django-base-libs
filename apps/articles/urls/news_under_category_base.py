# -*- coding: UTF-8 -*-
def news_under_category_urlpatterns(category_slug):
    from django.conf.urls import url, patterns
    from ccb.apps.articles.feeds import ArticleRssFeed, ArticleAtomFeed

    article_feeds = {
        'rss': ArticleRssFeed(),
        'atom': ArticleAtomFeed(),
    }

    urlpatterns = patterns(
        'ccb.apps.articles.views',
        url(r'^$',
            'article_archive_news',
            dict(
                creative_sector_slug='all',
                paginate_by=24,
                num_latest=None,
                type_sysname='news',
                category_slug=category_slug,
                template_name="articles/news_under_category.html"
            ),
        ),

        # articles aggregated syndication feeds
        url(r'^feeds/(?P<feed_type>.*)/$',
            'article_feed',
            dict(article_feeds, creative_sector_slug='all', type_sysname='news', category_slug=category_slug),
        ),
    )
    return urlpatterns
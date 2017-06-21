# -*- coding: UTF-8 -*-

def media_galleries_under_category_urlpatterns(category_slug):
    from django.conf.urls import patterns, url

    from kb.apps.media_gallery.feeds import MediaGalleryRssFeed, MediaGalleryAtomFeed
    from kb.apps.media_gallery.models import MediaGallery

    gallery_list_info = {
        'queryset': MediaGallery.objects.all(),
        'template_name': 'media_gallery/gallery_list_under_category.html',
        'paginate_by': 24,
        'allow_empty': True,
        'category_slug': category_slug,
    }

    latest_media_galleries = {
        'rss': MediaGalleryRssFeed(),
        'atom': MediaGalleryAtomFeed(),
        'queryset': MediaGallery.objects.filter(categories__slug=category_slug).order_by("-creation_date")[:50],
    }

    urlpatterns = [
        url(
            r'^$',
            'kb.apps.media_gallery.views.gallery_list',
            gallery_list_info,
        ),
        url(
            r'^feeds/(?P<feed_type>.*)/$',
            'jetson.apps.utils.views.feed',
            latest_media_galleries,
        ),
    ]
    return urlpatterns
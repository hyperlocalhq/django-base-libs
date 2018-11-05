# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, url

from ccb.apps.media_gallery.feeds import MediaGalleryRssFeed, MediaGalleryAtomFeed
from ccb.apps.media_gallery.models import MediaGallery

gallery_list_info = {
    'queryset': MediaGallery.objects.all(),
    'template_name': 'media_gallery/gallery_list.html',
    'paginate_by': 24,
    'allow_empty': True,
}

latest_media_galleries = {
    'rss': MediaGalleryRssFeed(),
    'atom': MediaGalleryAtomFeed(),
    'queryset': MediaGallery.objects.order_by("-creation_date")[:50],
}

urlpatterns = (
    url(
        r'^$',
        'ccb.apps.media_gallery.views.gallery_list',
        gallery_list_info,
    ),
    url(
        r'^(?P<show>favorites)/$',
        'ccb.apps.media_gallery.views.gallery_list',
        gallery_list_info,
    ),
    url(
        r'^(?P<show>memos)/$',
        'ccb.apps.media_gallery.views.gallery_list',
        gallery_list_info,
    ),
    url(
        r'^(?P<show>all)/$',
        'ccb.apps.media_gallery.views.gallery_list',
        gallery_list_info,
    ),
    url(
        r'^feeds/(?P<feed_type>rss|atom)/$',
        'jetson.apps.utils.views.feed',
        latest_media_galleries,
    ),
)

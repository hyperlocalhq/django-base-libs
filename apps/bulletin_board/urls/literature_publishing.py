# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, url

from ccb.apps.bulletin_board.feeds import BulletinFeed

CATEGORY_SLUG = "literatur-verlage"

bulletin_list_info = {
    'template_name': "bulletin_board/bulletin_list_under_category.html",
    'category_slug': CATEGORY_SLUG,
}

urlpatterns = patterns('ccb.apps.bulletin_board.views',
    url(r'^$', 'bulletin_list', bulletin_list_info, name='bulletin_list'),
    url(r'^rss/$', BulletinFeed(category_slug=CATEGORY_SLUG), name='bulletin_rss'),
)

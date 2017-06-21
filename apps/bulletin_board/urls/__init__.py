# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, url

from kb.apps.bulletin_board.feeds import BulletinFeed

urlpatterns = patterns('kb.apps.bulletin_board.views',
    url(r'^$', 'bulletin_list', name='bulletin_list'),
    url(r'^(?P<show>favorites)/$',
        'bulletin_list',
        name="bulletin_list",
        ),
    url(r'^my-bulletins/$', 'my_bulletin_list', name='my_bulletin_list'),
    url(r'^rss/$', BulletinFeed(), name='bulletin_rss'),
    url(r'^add/$', 'add_bulletin', name='add_bulletin'),
    url(r'^bulletin/(?P<token>\d+)/$', 'bulletin_detail', name='bulletin_detail'),
    url(r'^bulletin/(?P<token>\d+)/change/$', 'change_bulletin', name='change_bulletin'),
    url(r'^bulletin/(?P<token>\d+)/delete/$', 'delete_bulletin', name='delete_bulletin'),
    url(r'^bulletin/(?P<token>\d+)/status/$', 'change_bulletin_status', name='change_bulletin_status'),
)

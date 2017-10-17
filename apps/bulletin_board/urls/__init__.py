# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from ccb.apps.bulletin_board.feeds import BulletinFeed

urlpatterns = patterns('ccb.apps.bulletin_board.views',
    url(r'^$', 'bulletin_list', name='bulletin_list'),
    url(r'^(?P<show>favorites)/$', 'bulletin_list', name="bulletin_list"),
    url(r'^my-bulletins/$', 'my_bulletin_list', name='my_bulletin_list'),
    url(r'^rss/$', BulletinFeed(), name='bulletin_rss'),
    url(r'^add/$', 'add_bulletin', name='add_bulletin'),
    # success pages
    url(r'^created/$', TemplateView.as_view(template_name='bulletin_board/bulletin_created.html'), name='bulletin_created'),
    url(r'^deleted/$', TemplateView.as_view(template_name='bulletin_board/bulletin_deleted.html'), name='bulletin_deleted'),
    # detail pages
    url(r'^bulletin/(?P<token>\d+)/$', 'bulletin_detail', name='bulletin_detail'),
    url(r'^bulletin/(?P<token>\d+)/change/$', 'change_bulletin', name='change_bulletin'),
    url(r'^bulletin/(?P<token>\d+)/delete/$', 'delete_bulletin', name='delete_bulletin'),
    url(r'^bulletin/(?P<token>\d+)/status/$', 'change_bulletin_status', name='change_bulletin_status'),
)

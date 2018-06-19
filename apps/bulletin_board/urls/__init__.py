# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from jetson.apps.utils.decorators import login_required
from ccb.apps.bulletin_board.feeds import BulletinFeed
from ccb.apps.bulletin_board import views as bulletin_board_views

urlpatterns = [
    url(r'^$', bulletin_board_views.bulletin_list, name='bulletin_list'),
    url(r'^(?P<show>favorites)/$', login_required(bulletin_board_views.bulletin_list), name="bulletin_list"),
    url(r'^my-bulletins/$', bulletin_board_views.my_bulletin_list, name='my_bulletin_list'),
    url(r'^rss/$', BulletinFeed(), name='bulletin_rss'),
    url(r'^add/$', bulletin_board_views.add_bulletin, name='add_bulletin'),
    # success pages
    url(r'^created/$', TemplateView.as_view(template_name='bulletin_board/bulletin_created.html'), name='bulletin_created'),
    url(r'^deleted/$', TemplateView.as_view(template_name='bulletin_board/bulletin_deleted.html'), name='bulletin_deleted'),
    # detail pages
    url(r'^bulletin/(?P<token>\d+)/$', bulletin_board_views.bulletin_detail, name='bulletin_detail'),
    url(r'^bulletin/(?P<token>\d+)/change/$', bulletin_board_views.change_bulletin, name='change_bulletin'),
    url(r'^bulletin/(?P<token>\d+)/delete/$', bulletin_board_views.delete_bulletin, name='delete_bulletin'),
    url(r'^bulletin/(?P<token>\d+)/status/$', bulletin_board_views.change_bulletin_status, name='change_bulletin_status'),
]
# -*- coding: UTF-8 -*-

from django.conf.urls import *

urlpatterns = patterns('berlinbuehnen.apps.festivals.views',
    url(r'^$', 'festival_list', name='festival_list'),
    url(r'^add/$', 'add_festival', name='add_festival'),
    url(r'^(?P<slug>[^/]+)/$', 'festival_detail', name='festival_detail'),
    url(r'^(?P<slug>[^/]+)/change/$', 'change_festival', name='change_festival'),
    url(r'^(?P<slug>[^/]+)/delete/$', 'delete_festival', name='delete_festival'),
    url(r'^(?P<slug>[^/]+)/status/$', 'change_festival_status', name='change_festival_status'),
    # gallery
    url(r'^(?P<slug>[^/]+)/gallery/$', 'image_overview', name='festival_image_overview'),
    url(r'^(?P<slug>[^/]+)/gallery/add/$', 'create_update_image', name='festival_add_image'),
    url(r'^(?P<slug>[^/]+)/gallery/file_(?P<mediafile_token>[^/]+)/$', 'create_update_image', name='festival_change_image'),
    url(r'^(?P<slug>[^/]+)/gallery/file_(?P<mediafile_token>[^/]+)/delete/$', 'delete_image', name='festival_delete_image'),
)

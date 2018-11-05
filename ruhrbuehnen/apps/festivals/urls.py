# -*- coding: UTF-8 -*-

from django.conf.urls import *

urlpatterns = patterns('ruhrbuehnen.apps.festivals.views',
    url(r'^$', 'festival_list', name='festival_list'),
    url(r'^add/$', 'add_festival', name='add_festival'),
    url(r'^(?P<slug>[^/]+)/$', 'festival_detail', name='festival_detail'),
    url(r'^(?P<slug>[^/]+)/events/$', 'festival_events', name='festival_events'),
    url(r'^(?P<slug>[^/]+)/change/$', 'change_festival', name='change_festival'),
    url(r'^(?P<slug>[^/]+)/delete/$', 'delete_festival', name='delete_festival'),
    url(r'^(?P<slug>[^/]+)/status/$', 'change_festival_status', name='change_festival_status'),
    url(r'^(?P<slug>[^/]+)/duplicate/$', 'duplicate_festival', name='duplicate_festival'),
    # gallery
    url(r'^(?P<slug>[^/]+)/gallery/$', 'image_overview', name='festival_image_overview'),
    url(r'^(?P<slug>[^/]+)/gallery/add/$', 'create_update_image', name='festival_add_image'),
    url(r'^(?P<slug>[^/]+)/gallery/file_(?P<mediafile_token>[^/]+)/$', 'create_update_image', name='festival_change_image'),
    url(r'^(?P<slug>[^/]+)/change/gallery/file_(?P<mediafile_token>[^/]+)/delete/$', 'delete_image', name='festival_delete_image'),
    # pdfs
    url(r'^(?P<slug>[^/]+)/pdf/$', 'pdf_overview', name='festival_pdf_overview'),
    url(r'^(?P<slug>[^/]+)/pdf/add/$', 'create_update_pdf', name='festival_add_pdf'),
    url(r'^(?P<slug>[^/]+)/pdf/file_(?P<mediafile_token>[^/]+)/$', 'create_update_pdf', name='festival_change_pdf'),
    url(r'^(?P<slug>[^/]+)/pdf/file_(?P<mediafile_token>[^/]+)/delete/$', 'delete_pdf', name='festival_delete_pdf'),
)

# -*- coding: UTF-8 -*-

from django.conf.urls import *

from .feeds import ExhibitionRssFeed

from . import views

urlpatterns = [
    url(r'^$', views.exhibition_list, name='exhibition_list'),
    url(r'^map/$', views.exhibition_list_map, name='exhibition_list_map'),
    # url(r'^vernissages/$', views.vernissage_list, name='vernissage_list'),  # TODO: eliminate or fix - not functional at the moment
    url(r'^export-json-exhibitions/$', views.export_json_exhibitions, name='export_json_exhibitions'),
    url(r'^add/$', views.add_exhibition, name='add_exhibition'),
    url(r'^rss/$', ExhibitionRssFeed(), name='exhibitions_rss'),
    url(r'^(?P<slug>[^/]+)/$', views.exhibition_detail, name='exhibition_detail'),
    url(r'^(?P<slug>[^/]+)/ajax/$', views.exhibition_detail_ajax, name='exhibition_detail_ajax'),
    url(r'^(?P<slug>[^/]+)/ajax/map/$', views.exhibition_detail_ajax, {'template_name': 'exhibitions/exhibition_detail_ajax_map.html'}, name='exhibition_detail_ajax_map'),
    url(r'^(?P<slug>[^/]+)/slideshow/$', views.exhibition_detail_slideshow, name='exhibition_detail_slideshow'),
    url(r'^(?P<slug>[^/]+)/change/$', views.change_exhibition, name='change_exhibition'),
    url(r'^(?P<slug>[^/]+)/delete/$', views.delete_exhibition, name='delete_exhibition'),
    url(r'^(?P<slug>[^/]+)/status/$', views.change_exhibition_status, name='change_exhibition_status'),
    url(r'^(?P<slug>[^/]+)/products/$', views.exhibition_products, name='exhibition_products'),
    # gallery
    url(r'^(?P<slug>[^/]+)/gallery/$', views.gallery_overview, name='exhibition_gallery_overview'),
    url(r'^(?P<slug>[^/]+)/gallery/add/$', views.create_update_mediafile, name='exhibition_add_mediafile'),
    url(r'^(?P<slug>[^/]+)/gallery/file_(?P<mediafile_token>[^/]+)/$', views.create_update_mediafile, name='exhibition_change_mediafile'),
    url(r'^(?P<slug>[^/]+)/gallery/file_(?P<mediafile_token>[^/]+)/delete/$', views.delete_mediafile, name='exhibition_delete_mediafile'),
]
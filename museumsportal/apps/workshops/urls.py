# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

from feeds import WorkshopRssFeed

urlpatterns = patterns('museumsportal.apps.workshops.views',
    url(r'^$', 'workshop_list', name='workshop_list'),
    url(r'^map/$', 'workshop_list_map', name='workshop_list_map'),
    url(r'^add/$', 'add_workshop', name='add_workshop'),
    url(r'^rss/$', WorkshopRssFeed()),
    url(r'^(?P<slug>[^/]+)/$', 'workshop_detail', name='workshop_detail'),
    url(r'^(?P<slug>[^/]+)/ajax/$', 'workshop_detail_ajax', name='workshop_detail_ajax'),
    url(r'^(?P<slug>[^/]+)/ajax/map/$', 'workshop_detail_ajax', {'template_name': 'workshops/workshop_detail_ajax_map.html'}, name='workshop_detail_ajax_map'),
    url(r'^(?P<slug>[^/]+)/slideshow/$', 'workshop_detail_slideshow', name='workshop_detail_slideshow'),
    url(r'^(?P<slug>[^/]+)/change/$', 'change_workshop', name='change_workshop'),
    url(r'^(?P<slug>[^/]+)/delete/$', 'delete_workshop', name='delete_workshop'),    
    url(r'^(?P<slug>[^/]+)/status/$', 'change_workshop_status', name='change_workshop_status'),    
    url(r'^(?P<slug>[^/]+)/batch-workshop-times/$', 'batch_workshop_times', name='batch_workshop_times'),    
    url(r'^(?P<slug>[^/]+)/products/$', 'workshop_products', name='workshop_products'),
    # gallery
    url(r'^(?P<slug>[^/]+)/gallery/$', 'gallery_overview', name='workshop_gallery_overview'),    
    url(r'^(?P<slug>[^/]+)/gallery/add/$', 'create_update_mediafile', name='workshop_add_mediafile'),    
    url(r'^(?P<slug>[^/]+)/gallery/file_(?P<mediafile_token>[^/]+)/$', 'create_update_mediafile', name='workshop_change_mediafile'),    
    url(r'^(?P<slug>[^/]+)/gallery/file_(?P<mediafile_token>[^/]+)/delete/$', 'delete_mediafile', name='workshop_delete_mediafile'),    
)

# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

from feeds import WorkshopRssFeed

urlpatterns = patterns('museumsportal.apps.workshops.views',
    url(r'^$', 'workshop_list', name='workshop_list'),
    url(r'^add/$', 'add_workshop', name='add_workshop'),    
    url(r'^rss/$', WorkshopRssFeed()),
    url(r'^(?P<slug>[^/]+)/$', 'workshop_detail', name='workshop_detail'),
    url(r'^(?P<slug>[^/]+)/change/$', 'change_workshop', name='change_workshop'),    
    url(r'^(?P<slug>[^/]+)/delete/$', 'delete_workshop', name='delete_workshop'),    
    url(r'^(?P<slug>[^/]+)/status/$', 'change_workshop_status', name='change_workshop_status'),    
    url(r'^(?P<slug>[^/]+)/batch-workshop-times/$', 'batch_workshop_times', name='batch_workshop_times'),    
    # gallery
    url(r'^(?P<slug>[^/]+)/gallery/$', 'gallery_overview', name='workshop_gallery_overview'),    
    url(r'^(?P<slug>[^/]+)/gallery/add/$', 'create_update_mediafile', name='workshop_add_mediafile'),    
    url(r'^(?P<slug>[^/]+)/gallery/file_(?P<mediafile_token>[^/]+)/$', 'create_update_mediafile', name='workshop_change_mediafile'),    
    url(r'^(?P<slug>[^/]+)/gallery/file_(?P<mediafile_token>[^/]+)/delete/$', 'delete_mediafile', name='workshop_delete_mediafile'),    
)

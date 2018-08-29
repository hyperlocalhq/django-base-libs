# -*- coding: utf-8 -*-
from django.conf.urls import *

urlpatterns = patterns('museumsportal.apps.media_gallery.views.cms',
    url(r'^$', 'gallery_detail', ),
    url(r'^add/((?P<media_file_type>[^/]+)/)?$', 'create_update_mediafile', ),
    url(r'^file_(?P<token>[^/]+)/$', 'create_update_mediafile', ),
    url(r'^file_(?P<token>[^/]+)/delete/$', 'delete_mediafile', ),
    url(r'^file_(?P<token>[^/]+)/popup_delete/$', 'delete_mediafile_popup', ),
    url(r'^file_(?P<token>[^/]+)/json/$', 'json_show_file',),
)


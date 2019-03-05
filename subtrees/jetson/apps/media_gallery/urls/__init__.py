# -*- coding: utf-8 -*-
from django.conf.urls import *

from base_libs.utils.misc import path_in_installed_app

urlpatterns = patterns(
    path_in_installed_app("media_gallery.views"),
    url(
        r'^$',
        'gallery_detail',
    ),
    url(
        r'^add/((?P<media_file_type>[^/]+)/)?$',
        'create_update_mediafile',
    ),
    url(
        r'^file_(?P<token>[^/]+)/$',
        'create_update_mediafile',
    ),
    url(
        r'^file_(?P<token>[^/]+)/delete/$',
        'delete_mediafile',
    ),
    url(
        r'^file_(?P<token>[^/]+)/popup_delete/$',
        'delete_mediafile_popup',
    ),
    url(
        r'^file_(?P<token>[^/]+)/json/$',
        'json_show_file',
    ),
)

# -*- coding: UTF-8 -*-

from django.conf.urls import *
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

urlpatterns = patterns('jetson.apps.public_filebrowser.views',
    # public filebrowser urls
    url(r'^$', lambda request: redirect(reverse("pfb_browse"))),    
    url(r'^browse/$', 'browse', name="pfb_browse"),
    url(r'^mkdir/', 'mkdir', name="pfb_mkdir"),
    url(r'^upload/', 'upload', name="pfb_upload"),
    url(r'^download/', 'download', name="pfb_download"),
    url(r'^rename/$', 'rename', name="pfb_rename"),
    url(r'^delete/$', 'delete', name="pfb_delete"),
    url(r'^versions/$', 'versions', name="pfb_versions"),
    
    url(r'^check_file/$', '_check_file', name="pfb_check"),
    url(r'^upload_file/$', '_upload_file', name="pfb_do_upload"),
)

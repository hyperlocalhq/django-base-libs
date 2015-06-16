# -*- coding: UTF-8 -*-
import os

import django
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib.auth.models import User
from django.contrib import admin
from django.db import models
from django.views.generic import TemplateView

from filebrowser.settings import MEDIA_ROOT as UPLOADS_ROOT
from filebrowser.settings import MEDIA_URL as UPLOADS_URL

admin.autodiscover()

urlpatterns = []

urlpatterns += patterns('django.views.static',
    # media
    url(r'^uploads/(?P<path>.*)$', 'serve', {'document_root': UPLOADS_ROOT}),
    url(r'^media/\d+/(?P<path>.*)$', 'serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^jetson-media/\d+/(?P<path>.*)$', 'serve', {'document_root': settings.JETSON_MEDIA_ROOT}),
    url(
        r'^admin-media/(?P<path>.*)$',
        'serve',
        {
            'document_root': settings.GRAPPELLI_MEDIA_ROOT
            },
        name="admin_media_url"
        ),
    )    

### HELPERS (system urls not visible directly for the users) ###
urlpatterns += patterns('',
    # i18n
    #url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', {'packages': 'jetson'}),

    # gmap
    url(r'^gmap/$', TemplateView.as_view(template_name='gmap/index.html')),

    url(r'^admin/', include('jetson.apps.extendedadmin.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
)

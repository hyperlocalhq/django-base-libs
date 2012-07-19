# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from filebrowser.sites import site

from base_libs.utils.misc import path_in_installed_app

admin.autodiscover()

handler404 = "jetson.apps.error_handler.views.page_not_found"
handler500 = "jetson.apps.error_handler.views.server_error"

urlpatterns = patterns(path_in_installed_app('image_mods.views'),
    url(r'^admin/filebrowser/versions/$', 'versions', name="fb_versions"),
    url(r'^filebrowser/get-version/$', 'get_or_create_modified_path', name="fb_get_version"),
    url(r'^admin/filebrowser/adjust-version/$', 'adjust_version', name="fb_adjust_version"),
    url(r'^admin/filebrowser/delete-version/$', 'delete_version', name="fb_delete_version"),
    )

urlpatterns += patterns('',
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^recrop/', include('jetson.apps.image_mods.urls')),
)

urlpatterns += staticfiles_urlpatterns()

urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^jetson-media/\d+/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.JETSON_MEDIA_ROOT}),
) + urlpatterns

urlpatterns += patterns('',    
    # i18n
    (r'^i18n/', 'jetson.apps.utils.views.set_language'),
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', {'packages': 'jetson.apps.utils'}),
    
    url(r'^gmap/$', 'django.views.generic.simple.direct_to_template', {'template': 'gmap/index.html'}),    
    url(r'^jssettings/$', 'jetson.apps.utils.views.direct_to_js_template', {'template': 'settings.js'}, name="jssettings"),
    
    url(r'^grappelli/', include('grappelli.urls')),    
    url(r'^tagging_autocomplete/', include('tagging_autocomplete.urls')),
    
    url(r'^twitterwall/', include('museumsportal.apps.twitterwall.urls')),
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('cms.urls')),
)


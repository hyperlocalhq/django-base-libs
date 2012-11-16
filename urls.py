# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from filebrowser.sites import site

from tastypie.api import Api
from museumsportal.apps.museums.api.resources import MuseumCategoryResource
from museumsportal.apps.museums.api.resources import MuseumResource
from museumsportal.apps.exhibitions.api.resources import ExhibitionCategoryResource
from museumsportal.apps.exhibitions.api.resources import ExhibitionResource

from base_libs.utils.misc import path_in_installed_app

admin.autodiscover()

handler404 = "jetson.apps.error_handler.views.page_not_found"
handler500 = "jetson.apps.error_handler.views.server_error"

v1_api = Api(api_name='v1')
v1_api.register(MuseumCategoryResource())
v1_api.register(MuseumResource())
v1_api.register(ExhibitionCategoryResource())
v1_api.register(ExhibitionResource())

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
    url(r'^api/', include(v1_api.urls)),
    url(r'^tagging_autocomplete/', include('tagging_autocomplete.urls')),
    
    # i18n
    (r'^i18n/', 'jetson.apps.utils.views.set_language'),
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', {'packages': 'jetson.apps.utils'}),
    
    url(r'^gmap/$', 'django.views.generic.simple.direct_to_template', {'template': 'gmap/index.html'}),
    url(r'^jssettings/$', 'jetson.apps.utils.views.direct_to_js_template', {'template': 'settings.js'}, name="jssettings"),
    
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^tagging_autocomplete/', include('tagging_autocomplete.urls')),
    
    url(r'^twitterwall/', include('museumsportal.apps.twitterwall.urls')),
    url(r'^tweets/$', 'museumsportal.apps.twitter.views.latest_tweets', {
        'twitter_username': settings.TWITTER_USERNAME,
        'number_of_tweets': settings.TWITTER_NUMBER_OF_TWEETS,
        }),
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('cms.urls')),
    
    
)


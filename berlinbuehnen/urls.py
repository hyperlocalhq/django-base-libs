# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from django.conf import settings

from base_libs.utils.misc import path_in_installed_app
from filebrowser.sites import site as filebrowser_site

from berlinbuehnen.apps.site_specific.sitemaps import sitemaps

import autocomplete_light

from tastypie.api import Api

# API v1
from berlinbuehnen.apps.locations.api.resources import v1 as locations_api_v1
from berlinbuehnen.apps.productions.api.resources import v1 as productions_api_v1

v1_api = Api(api_name='v1')

v1_api.register(locations_api_v1.ServiceResource())
v1_api.register(locations_api_v1.AccessibilityOptionResource())
v1_api.register(locations_api_v1.LocationResource())
v1_api.register(locations_api_v1.StageResource())

v1_api.register(productions_api_v1.LanguageAndSubtitlesResource())
v1_api.register(productions_api_v1.ProductionCategoryResource())
v1_api.register(productions_api_v1.ProductionCharacteristicsResource())
v1_api.register(productions_api_v1.ProductionResource())
v1_api.register(productions_api_v1.EventCharacteristicsResource())

autocomplete_light.autodiscover()

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}, name="media_url"),
    url(r'^jetson-media/\d+/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.JETSON_MEDIA_ROOT}, name="jetson_media_url"),

    url(r'^tweets/$', 'berlinbuehnen.apps.twitter.views.latest_tweets', {
        'twitter_username': settings.TWITTER_USERNAME,
        'number_of_tweets': settings.TWITTER_NUMBER_OF_TWEETS,
    }),
    url(r'^tweets/(?P<twitter_username>.+)/$', 'berlinbuehnen.apps.twitter.views.latest_tweets', {
        'number_of_tweets': settings.TWITTER_NUMBER_OF_TWEETS,
    }),

)
urlpatterns += staticfiles_urlpatterns()

import debug_toolbar
urlpatterns += patterns('',
    url(r'^debug/673657483929/', include(debug_toolbar.urls)),
)

urlpatterns += i18n_patterns(path_in_installed_app('image_mods.views'),
    url(r'^admin/filebrowser/versions/$', 'versions', name="fb_versions"),
    url(r'^filebrowser/get-version/$', 'get_or_create_modified_path', name="fb_get_version"),
    url(r'^admin/filebrowser/adjust-version/$', 'adjust_version', name="fb_adjust_version"),
    url(r'^admin/filebrowser/delete-version/$', 'delete_version', name="fb_delete_version"),
)

urlpatterns += i18n_patterns('',
    url(r'^admin/filebrowser/', include(filebrowser_site.urls)),
    url(r'^recrop/', include('jetson.apps.image_mods.urls')),
)

urlpatterns += i18n_patterns('',
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^api/', include(v1_api.urls)),
    url(r'^culturebase-export/locations/(?P<location_slug>[^/]+)/productions/$', 'berlinbuehnen.apps.site_specific.views.culturebase_export_productions', name="culturebase_export_productions"),

    url(r'^tagging_autocomplete/', include('tagging_autocomplete.urls')),
    url(r'^helper/autocomplete/(?P<app>[^/]+)/(?P<qs_function>[^/]+)/(?P<display_attr>[^/]+)/(?P<add_display_attr>[^/]+)/$', 'base_libs.views.ajax_autocomplete'),
    url(r'^helper/ajax-upload/$', 'berlinbuehnen.apps.site_specific.views.uploader', name="ajax_uploader"),
    url(r'^helper/modified-path/$', 'jetson.apps.image_mods.views.get_or_create_modified_path', name="modified_path"),
    url(r'^helper/menu/$', 'berlinbuehnen.apps.mega_menu.views.mega_drop_down_menu', name="mega_drop_down_menu"),
    url(r'^helper/favorite/(?P<content_type_id>[0-9]+)/(?P<object_id>[0-9]+)/$', 'jetson.apps.favorites.views.json_set_favorite'),
    url(r'^autocomplete/', include('autocomplete_light.urls')),

    # i18n
    url(r'^i18n/', 'jetson.apps.utils.views.set_language', name="set_language"),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', {'packages': 'jetson.apps.utils'}),

    url(r'^jssettings/$', 'jetson.apps.utils.views.direct_to_js_template', {'template_name': 'settings.js'}, name="jssettings"),

    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^tagging_autocomplete/', include('tagging_autocomplete.urls')),

    url(r'^styleguide/', include('jetson.apps.styleguide.urls')),

    url(r'^', include('berlinbuehnen.apps.accounts.urls')),

    url(r'^dashboard/$', 'berlinbuehnen.apps.site_specific.views.dashboard', name="dashboard"),
    url(r'^dashboard/locations/$', 'berlinbuehnen.apps.site_specific.views.dashboard_locations', name="dashboard_locations"),
    url(r'^dashboard/productions/$', 'berlinbuehnen.apps.site_specific.views.dashboard_productions', name="dashboard_productions"),
    url(r'^dashboard/multiparts/$', 'berlinbuehnen.apps.site_specific.views.dashboard_multiparts', name="dashboard_multiparts"),
    url(r'^claiming-invitation/$', 'berlinbuehnen.apps.site_specific.views.invite_to_claim_location', name="invite_to_claim_location"),
    url(r'^claiming-invitation/done/$', TemplateView.as_view(template_name='site_specific/claiming_invitation_done.html'), name="invite_to_claim_location_done"),
    url(r'^claiming-confirmation/(?P<invitation_code>[a-zA-Z0-9_\-=]+)/$', 'berlinbuehnen.apps.site_specific.views.register_and_claim_location', name="register_and_claim_location"),
    url(r'^favorites/(?P<user_token>[^/]+)/$', 'berlinbuehnen.apps.site_specific.views.user_favorites', {'template_name': 'favorites/all_favorites.html'}, name="user_favorites"),
    url(r'^my-profile/favorites/$', 'berlinbuehnen.apps.site_specific.views.redirect_to_user_favorites', name="favorites"),    # url(r'^my-profile/favorites/$', 'berlinbuehnen.apps.site_specific.views.favorites', name="favorites"),
    # url(r'^my-profile/favorites/locations/$', 'berlinbuehnen.apps.site_specific.views.favorite_locations', name="favorite_locations"),
    # url(r'^my-profile/favorites/exhibitions/$', 'berlinbuehnen.apps.site_specific.views.favorite_exhibitions', name="favorite_exhibitions"),
    # url(r'^my-profile/favorites/events/$', 'berlinbuehnen.apps.site_specific.views.favorite_events', name="favorite_events"),
    # url(r'^my-profile/favorites/guided-tours/$', 'berlinbuehnen.apps.site_specific.views.favorite_workshops', name="favorite_workshops"),

    url(r'^rosetta/', include('rosetta.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('cms.urls')),
)

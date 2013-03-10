# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import direct_to_template

from filebrowser.sites import site

from tastypie.api import Api
from museumsportal.apps.museums.api.resources import MuseumCategoryResource
from museumsportal.apps.museums.api.resources import MuseumResource
from museumsportal.apps.exhibitions.api.resources import ExhibitionCategoryResource
from museumsportal.apps.exhibitions.api.resources import ExhibitionResource

from jetson.apps.utils.decorators import login_required
from base_libs.utils.misc import path_in_installed_app

from museumsportal.apps.site_specific.forms import password_change_form_helper
from museumsportal.apps.site_specific.forms import password_reset_form_helper
from museumsportal.apps.site_specific.forms import password_reset_change_form_helper

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
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}, name="media_url"),
    url(r'^jetson-media/\d+/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.JETSON_MEDIA_ROOT}, name="jetson_media_url"),
) + urlpatterns

urlpatterns += patterns('',
    url(r'^api/', include(v1_api.urls)),
    url(r'^tagging_autocomplete/', include('tagging_autocomplete.urls')),
    url(r'^helper/autocomplete/(?P<app>[^/]+)/(?P<qs_function>[^/]+)/(?P<display_attr>[^/]+)/(?P<add_display_attr>[^/]+)/$', 'base_libs.views.ajax_autocomplete'),
    url(r'^helper/favorite/(?P<content_type_id>[0-9]+)/(?P<object_id>[0-9]+)/$', 'jetson.apps.favorites.views.json_set_favorite'),
    url(r'^helper/museum_attrs/(?P<museum_id>[0-9]+)/$', 'museumsportal.apps.museums.views.json_museum_attrs'),
    
    # i18n
    (r'^i18n/', 'jetson.apps.utils.views.set_language'),
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', {'packages': 'jetson.apps.utils'}),
    
    url(r'^gmap/$', 'django.views.generic.simple.direct_to_template', {'template': 'gmap/index.html'}),
    url(r'^jssettings/$', 'jetson.apps.utils.views.direct_to_js_template', {'template': 'settings.js'}, name="jssettings"),
    
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^tagging_autocomplete/', include('tagging_autocomplete.urls')),

    url(r'^styleguide/', include('jetson.apps.styleguide.urls')),

    url(r'^twitterwall/', include('museumsportal.apps.twitterwall.urls')),
    url(r'^tweets/$', 'museumsportal.apps.twitter.views.latest_tweets', {
        'twitter_username': settings.TWITTER_USERNAME,
        'number_of_tweets': settings.TWITTER_NUMBER_OF_TWEETS,
        }),
    url(r'^tweets/(?P<twitter_username>.+)/$', 'museumsportal.apps.twitter.views.latest_tweets', {
        'number_of_tweets': settings.TWITTER_NUMBER_OF_TWEETS,
        }),
    
    url(r'^login/$', 'museumsportal.apps.site_specific.views.login', {'template_name': 'accounts/login.html', 'redirect_to': '/dashboard/'}, name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': "/"}, name="logout"),
    url(r'^signup/$', 'museumsportal.apps.site_specific.views.register' ),
    url(r'^signup/almost-done/$', 'django.views.generic.simple.direct_to_template', {'template': 'accounts/register_verify_required.html'}),
    url(r'^signup/welcome/$', login_required(direct_to_template), {'template': 'accounts/register_done.html'}),
    url(r'^signup/(?P<encrypted_email>[a-zA-Z0-9\+\/_\-=]+)/$', 'museumsportal.apps.site_specific.views.confirm_registration'),
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset', {'template_name': 'accounts/password_reset_form.html', 'email_template_name': 'accounts/password_reset_email.html', 'extra_context': {'form_helper': password_reset_form_helper}}),
    url(r'^password_reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name': 'accounts/password_reset_confirm.html', 'extra_context': {'form_helper': password_reset_change_form_helper}}),
    url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'accounts/password_reset_done.html'}),
    url(r'^password_reset/complete/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'accounts/password_reset_complete.html'}),
    url(r'^password_change/$', 'django.contrib.auth.views.password_change', {'template_name': 'accounts/password_change_form.html', 'extra_context': {'form_helper': password_change_form_helper}}),
    url(r'^password_change/done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'accounts/password_change_done.html'}),
    url(r'^dashboard/$', 'museumsportal.apps.site_specific.views.dashboard', name="dashboard"),
    url(r'^dashboard/museums/$', 'museumsportal.apps.site_specific.views.dashboard_museums', name="dashboard_museums"),
    url(r'^dashboard/exhibitions/$', 'museumsportal.apps.site_specific.views.dashboard_exhibitions', name="dashboard_exhibitions"),
    url(r'^dashboard/events/$', 'museumsportal.apps.site_specific.views.dashboard_events', name="dashboard_events"),
    url(r'^dashboard/guided-tours/$', 'museumsportal.apps.site_specific.views.dashboard_workshops', name="dashboard_workshops"),
    url(r'^claiming-invitation/$', 'museumsportal.apps.site_specific.views.invite_to_claim_museum', name="invite_to_claim_museum"),
    url(r'^claiming-invitation/done/$', 'django.views.generic.simple.direct_to_template', {'template': 'site_specific/claiming_invitation_done.html'}, name="invite_to_claim_museum_done"),
    url(r'^claiming-confirmation/(?P<invitation_code>[a-zA-Z0-9_\-=]+)/$', 'museumsportal.apps.site_specific.views.register_and_claim_museum', name="register_and_claim_museum"),
    url(r'^my-profile/favorites/$', 'jetson.apps.favorites.views.favorites', {'template_name': 'favorites/favorites.html'}),
    
    url(r'^rosetta/', include('rosetta.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('cms.urls')),
    
    
)


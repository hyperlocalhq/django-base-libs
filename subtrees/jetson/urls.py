# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from django.conf.urls.i18n import i18n_patterns

from filebrowser.sites import site

from tastypie.api import Api
# API v1
from museumsportal.apps.museums.api.resources import v1 as museums_api_v1
from museumsportal.apps.exhibitions.api.resources import v1 as exhibitions_api_v1
# API v2
from museumsportal.apps.museums.api.resources import v2 as museums_api_v2
from museumsportal.apps.exhibitions.api.resources import v2 as exhibitions_api_v2
from museumsportal.apps.events.api.resources import v2 as events_api_v2
from museumsportal.apps.workshops.api.resources import v2 as workshops_api_v2

from jetson.apps.utils.decorators import login_required
from base_libs.utils.misc import path_in_installed_app

from museumsportal.apps.site_specific.forms import password_change_form_helper
from museumsportal.apps.site_specific.forms import password_reset_form_helper
from museumsportal.apps.site_specific.forms import password_reset_change_form_helper

from museumsportal.apps.search.views import SearchView

admin.autodiscover()

handler404 = "jetson.apps.error_handler.views.page_not_found"
handler500 = "jetson.apps.error_handler.views.server_error"

v1_api = Api(api_name='v1')
v1_api.register(museums_api_v1.MuseumCategoryResource())
v1_api.register(museums_api_v1.MuseumResource())
v1_api.register(exhibitions_api_v1.ExhibitionCategoryResource())
v1_api.register(exhibitions_api_v1.ExhibitionResource())

v2_api = Api(api_name='v2')
v2_api.register(museums_api_v2.MuseumCategoryResource())
v2_api.register(museums_api_v2.AccessibilityOptionResource())
v2_api.register(museums_api_v2.MuseumResource())
v2_api.register(museums_api_v2.SeasonResource())
v2_api.register(museums_api_v2.SpecialOpeningTimeResource())
v2_api.register(museums_api_v2.MediaFileResource())
v2_api.register(museums_api_v2.SocialMediaChannelResource())
v2_api.register(exhibitions_api_v2.ExhibitionCategoryResource())
v2_api.register(exhibitions_api_v2.ExhibitionResource())
v2_api.register(exhibitions_api_v2.SeasonResource())
v2_api.register(exhibitions_api_v2.OrganizerResource())
v2_api.register(exhibitions_api_v2.MediaFileResource())
v2_api.register(events_api_v2.EventCategoryResource())
v2_api.register(events_api_v2.OrganizerResource())
v2_api.register(events_api_v2.EventTimeResource())
v2_api.register(events_api_v2.MediaFileResource())
v2_api.register(events_api_v2.EventResource())
v2_api.register(workshops_api_v2.OrganizerResource())
v2_api.register(workshops_api_v2.WorkshopTimeResource())
v2_api.register(workshops_api_v2.MediaFileResource())
v2_api.register(workshops_api_v2.WorkshopResource())

urlpatterns = i18n_patterns(path_in_installed_app('image_mods.views'),
    url(r'^admin/filebrowser/versions/$', 'versions', name="fb_versions"),
    url(r'^filebrowser/get-version/$', 'get_or_create_modified_path', name="fb_get_version"),
    url(r'^admin/filebrowser/adjust-version/$', 'adjust_version', name="fb_adjust_version"),
    url(r'^admin/filebrowser/delete-version/$', 'delete_version', name="fb_delete_version"),
)

urlpatterns += i18n_patterns('',
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^recrop/', include('jetson.apps.image_mods.urls')),
)

urlpatterns += staticfiles_urlpatterns()

urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}, name="media_url"),
    url(r'^jetson-media/\d+/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.JETSON_MEDIA_ROOT}, name="jetson_media_url"),
) + urlpatterns

urlpatterns += i18n_patterns('',
    url(r'^api/', include(v1_api.urls)),
    url(r'^api/', include(v2_api.urls)),
    url(r'^tagging_autocomplete/', include('tagging_autocomplete.urls')),
    url(r'^helper/autocomplete/(?P<app>[^/]+)/(?P<qs_function>[^/]+)/(?P<display_attr>[^/]+)/(?P<add_display_attr>[^/]+)/$', 'base_libs.views.ajax_autocomplete'),
    url(r'^helper/favorite/(?P<content_type_id>[0-9]+)/(?P<object_id>[0-9]+)/$', 'jetson.apps.favorites.views.json_set_favorite'),
    url(r'^helper/museum_attrs/(?P<museum_id>[0-9]+)/$', 'museumsportal.apps.museums.views.json_museum_attrs'),
    url(r'^helper/ajax-upload/$', 'museumsportal.apps.site_specific.views.uploader', name="ajax_uploader"),
    url(r'^helper/modified-path/$', 'jetson.apps.image_mods.views.get_or_create_modified_path', name="modified_path"),
    url(r'^helper/menu/$', 'museumsportal.apps.mega_menu.views.mega_drop_down_menu', name="mega_drop_down_menu"),

    # i18n
    url(r'^i18n/', 'jetson.apps.utils.views.set_language', name="set_language"),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', {'packages': 'jetson.apps.utils'}),
    
    url(r'^gmap/$', TemplateView.as_view(template_name='gmap/index.html')),
    url(r'^jssettings/$', 'jetson.apps.utils.views.direct_to_js_template', {'template_name': 'settings.js'}, name="jssettings"),
    
    url(r'^ads/', include('museumsportal.apps.advertising.urls')),

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
    
    url(r'^login/$', 'museumsportal.apps.site_specific.views.login', {'template_name': 'accounts/login.html', 'redirect_to': '/'}, name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': "/"}, name="logout"),
    url(r'^signup/$', 'museumsportal.apps.site_specific.views.register' ),
    url(r'^signup/almost-done/$', TemplateView.as_view(template_name='accounts/register_verify_required.html')),
    url(r'^signup/welcome/$', login_required(TemplateView.as_view(template_name='accounts/register_done.html'))),
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
    url(r'^claiming-invitation/done/$', TemplateView.as_view(template_name='site_specific/claiming_invitation_done.html'), name="invite_to_claim_museum_done"),
    url(r'^claiming-confirmation/(?P<invitation_code>[a-zA-Z0-9_\-=]+)/$', 'museumsportal.apps.site_specific.views.register_and_claim_museum', name="register_and_claim_museum"),
    url(r'^my-profile/favorites/$', 'jetson.apps.favorites.views.favorites', {'template_name': 'favorites/favorites.html'}),
    
    url(r'^rosetta/', include('rosetta.urls')),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^search/', include("museumsportal.apps.search.urls")),
    url(r'^', include('cms.urls')),
)
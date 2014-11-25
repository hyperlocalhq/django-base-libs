# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from django.conf import settings

from base_libs.utils.misc import path_in_installed_app
from filebrowser.sites import site as filebrowser_site

from berlinbuehnen.apps.site_specific.sitemaps import sitemaps
from jetson.apps.utils.decorators import login_required

from berlinbuehnen.apps.site_specific.forms import password_change_form_helper
from berlinbuehnen.apps.site_specific.forms import password_reset_form_helper
from berlinbuehnen.apps.site_specific.forms import password_reset_change_form_helper

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}, name="media_url"),
    url(r'^jetson-media/\d+/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.JETSON_MEDIA_ROOT}, name="jetson_media_url"),
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

    url(r'^tagging_autocomplete/', include('tagging_autocomplete.urls')),
    url(r'^helper/autocomplete/(?P<app>[^/]+)/(?P<qs_function>[^/]+)/(?P<display_attr>[^/]+)/(?P<add_display_attr>[^/]+)/$', 'base_libs.views.ajax_autocomplete'),
    url(r'^helper/ajax-upload/$', 'berlinbuehnen.apps.site_specific.views.uploader', name="ajax_uploader"),
    url(r'^helper/modified-path/$', 'jetson.apps.image_mods.views.get_or_create_modified_path', name="modified_path"),
    url(r'^helper/menu/$', 'berlinbuehnen.apps.mega_menu.views.mega_drop_down_menu', name="mega_drop_down_menu"),

    # i18n
    url(r'^i18n/', 'jetson.apps.utils.views.set_language', name="set_language"),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', {'packages': 'jetson.apps.utils'}),

    url(r'^jssettings/$', 'jetson.apps.utils.views.direct_to_js_template', {'template_name': 'settings.js'}, name="jssettings"),

    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^tagging_autocomplete/', include('tagging_autocomplete.urls')),

    url(r'^styleguide/', include('jetson.apps.styleguide.urls')),

    url(r'^login/$', 'berlinbuehnen.apps.site_specific.views.login', {'template_name': 'accounts/login.html', 'redirect_to': '/'}, name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': "/"}, name="logout"),
    url(r'^signup/$', 'berlinbuehnen.apps.site_specific.views.register' ),
    url(r'^signup/almost-done/$', TemplateView.as_view(template_name='accounts/register_verify_required.html')),
    url(r'^signup/welcome/$', login_required(TemplateView.as_view(template_name='accounts/register_done.html'))),
    url(r'^signup/(?P<encrypted_email>[a-zA-Z0-9\+\/_\-=]+)/$', 'berlinbuehnen.apps.site_specific.views.confirm_registration'),
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset', {'template_name': 'accounts/password_reset_form.html', 'email_template_name': 'accounts/password_reset_email.html', 'extra_context': {'form_helper': password_reset_form_helper}}),
    url(r'^password_reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name': 'accounts/password_reset_confirm.html', 'extra_context': {'form_helper': password_reset_change_form_helper}}),
    url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'accounts/password_reset_done.html'}),
    url(r'^password_reset/complete/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'accounts/password_reset_complete.html'}),
    url(r'^password_change/$', 'django.contrib.auth.views.password_change', {'template_name': 'accounts/password_change_form.html', 'extra_context': {'form_helper': password_change_form_helper}}),
    url(r'^password_change/done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'accounts/password_change_done.html'}),
    # url(r'^dashboard/$', 'berlinbuehnen.apps.site_specific.views.dashboard', name="dashboard"),
    # url(r'^dashboard/museums/$', 'berlinbuehnen.apps.site_specific.views.dashboard_museums', name="dashboard_museums"),
    # url(r'^dashboard/exhibitions/$', 'berlinbuehnen.apps.site_specific.views.dashboard_exhibitions', name="dashboard_exhibitions"),
    # url(r'^dashboard/events/$', 'berlinbuehnen.apps.site_specific.views.dashboard_events', name="dashboard_events"),
    # url(r'^dashboard/guided-tours/$', 'berlinbuehnen.apps.site_specific.views.dashboard_workshops', name="dashboard_workshops"),
    # url(r'^dashboard/shop/$', 'berlinbuehnen.apps.site_specific.views.dashboard_shopproducts', name="dashboard_shopproducts"),
    # url(r'^claiming-invitation/$', 'berlinbuehnen.apps.site_specific.views.invite_to_claim_museum', name="invite_to_claim_museum"),
    # url(r'^claiming-invitation/done/$', TemplateView.as_view(template_name='site_specific/claiming_invitation_done.html'), name="invite_to_claim_museum_done"),
    # url(r'^claiming-confirmation/(?P<invitation_code>[a-zA-Z0-9_\-=]+)/$', 'berlinbuehnen.apps.site_specific.views.register_and_claim_museum', name="register_and_claim_museum"),
    # url(r'^my-profile/favorites/$', 'berlinbuehnen.apps.site_specific.views.favorites', name="favorites"),
    # url(r'^my-profile/favorites/museums/$', 'berlinbuehnen.apps.site_specific.views.favorite_museums', name="favorite_museums"),
    # url(r'^my-profile/favorites/exhibitions/$', 'berlinbuehnen.apps.site_specific.views.favorite_exhibitions', name="favorite_exhibitions"),
    # url(r'^my-profile/favorites/events/$', 'berlinbuehnen.apps.site_specific.views.favorite_events', name="favorite_events"),
    # url(r'^my-profile/favorites/guided-tours/$', 'berlinbuehnen.apps.site_specific.views.favorite_workshops', name="favorite_workshops"),

    url(r'^rosetta/', include('rosetta.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('cms.urls')),
)

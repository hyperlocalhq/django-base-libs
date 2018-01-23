# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from jetson.apps.utils.decorators import login_required

from museumsportal.apps.accounts.forms import password_change_form_helper
from museumsportal.apps.accounts.forms import password_reset_form_helper
from museumsportal.apps.accounts.forms import password_reset_change_form_helper

urlpatterns = patterns("",
    url(r'^login/$', 'museumsportal.apps.accounts.views.login', {'template_name': 'accounts/login.html'}, name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': "/"}, name="logout"),
    url(r'^signup/$', 'museumsportal.apps.accounts.views.register' ),
    url(r'^signup/almost-done/$', TemplateView.as_view(template_name='accounts/register_verify_required.html')),
    url(r'^signup/welcome/$', login_required(TemplateView.as_view(template_name='accounts/register_done.html'))),
    url(r'^signup/(?P<encrypted_email>[a-zA-Z0-9\+\/_\-=]+)/$', 'museumsportal.apps.accounts.views.confirm_registration'),
    url(r'^password-reset/$', 'django.contrib.auth.views.password_reset', {'template_name': 'accounts/password_reset_form.html', 'email_template_name': 'accounts/password_reset_email.html', 'extra_context': {'form_helper': password_reset_form_helper}}),
    url(r'^password-reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name': 'accounts/password_reset_confirm.html', 'extra_context': {'form_helper': password_reset_change_form_helper}}),
    url(r'^password-reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'accounts/password_reset_done.html'}),
    url(r'^password-reset/complete/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'accounts/password_reset_complete.html'}),
    url(r'^password-change/$', 'django.contrib.auth.views.password_change', {'template_name': 'accounts/password_change_form.html', 'extra_context': {'form_helper': password_change_form_helper}}),
    url(r'^password-change/done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'accounts/password_change_done.html'}),
    url(r'^privacy-settings/$', 'museumsportal.apps.accounts.views.change_privacy_settings', name="change_privacy_settings"),
    url(r'^my-profile/change/$', 'museumsportal.apps.accounts.views.change_profile', name="change_profile"),
)
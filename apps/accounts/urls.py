# -*- coding: UTF-8 -*-
from django.conf.urls import *
from django.views.generic import TemplateView
from jetson.apps.utils.decorators import login_required

from ccb.apps.accounts.forms import password_change_form_helper
from ccb.apps.accounts.forms import password_reset_form_helper
from ccb.apps.accounts.forms import password_reset_change_form_helper


urlpatterns = [
    url(r'^account/$', TemplateView.as_view(template_name='accounts/index.html')),
    url(
        r'^login',
        'ccb.apps.accounts.views.login',
        {'template_name': 'accounts/login.html'},
        name="login",
    ),
    url(
        r'^logout',
        'django.contrib.auth.views.logout',
        {'next_page': "/"},
        name="logout",
    ),
    url(r'^changeuser/', 'django.contrib.auth.views.logout_then_login'),
    url(
        r'^register/$',
        'ccb.apps.accounts.views.register',
        name="register"
    ),
    url(
        r'^register/done/$',
        TemplateView.as_view(template_name='accounts/register_verify_required.html'),
        name="register_done",
    ),
    url(
        r'^register/alldone/$',
        login_required(TemplateView.as_view(template_name='accounts/register_done.html')),
        name="register_all_done",
    ),
    url(
        r'^register/(?P<encrypted_email>[a-zA-Z0-9\+/_\-=]+)/$',
        'ccb.apps.accounts.views.confirm_registration',
        name="register_confirm",
    ),
    url(
        r'^password_reset/$',
        'django.contrib.auth.views.password_reset',
        {
            'template_name': 'accounts/password_reset_form.html',
            'email_template_name': 'accounts/password_reset_email.html',
            'extra_context': {'form_helper': password_reset_form_helper}
        },
        name="password_reset",
    ),
    url(
        r'^password_reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {
            'template_name': 'accounts/password_reset_confirm.html',
            'extra_context': {'form_helper': password_reset_change_form_helper}
        },
        name="password_reset_confirm",
    ),
    url(
        r'^password_reset/done/$',
        'django.contrib.auth.views.password_reset_done',
        {'template_name': 'accounts/password_reset_done.html'},
        name="password_reset_done",
    ),
    url(
        r'^password_reset/complete/$',
        'django.contrib.auth.views.password_reset_complete',
        {'template_name': 'accounts/password_reset_complete.html'},
        name="password_reset_complete",
    ),
    url(
        r'^password_change/$',
        'django.contrib.auth.views.password_change',
        {
            'template_name': 'accounts/password_change_form.html',
            'extra_context': {'form_helper': password_change_form_helper}
        },
        name="password_change"
    ),
    url(
        r'^password_change/done/$',
        'django.contrib.auth.views.password_change_done',
        {'template_name': 'accounts/password_change_done.html'},
        name='password_change_done',
    ),
]

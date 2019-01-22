# -*- coding: UTF-8 -*-
from django.conf.urls import *
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from base_libs.utils.misc import path_in_installed_app

urlpatterns = patterns(
    path_in_installed_app('facebook_app.views'),
    url(
        r'^$',
        lambda request: redirect(reverse("manage_facebook_connections")),
    ),
    url(
        r'^link/$',
        "login_and_link",
    ),
    url(
        r'^link/login/$',
        "login",
    ),
    url(
        r'^link/register/$',
        "register",
    ),
    url(
        r'^manage/$',
        "manage_facebook_connections",
        name="manage_facebook_connections",
    ),
    url(
        r'^pages/$',
        "manage_facebook_pages",
        name="manage_facebook_pages",
    ),
    url(
        r'^data-exchange/$',
        "data_exchange",
    ),
)

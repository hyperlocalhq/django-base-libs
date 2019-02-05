# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.views.generic import TemplateView

from .views import subscribe_for_info_simplified

urlpatterns = [
    url(
        r'^$',
        subscribe_for_info_simplified,
        name="subscribe_for_info_simplified"
    ),
    url(
        r'^done/$',
        TemplateView.as_view(
            template_name='mailchimp/subscription_simplified_done.html'
        ),
        name="subscribe_for_info_simplified_done"
    ),
]

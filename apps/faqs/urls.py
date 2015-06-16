# -*- coding: UTF-8 -*-
from django.conf.urls import patterns
from django.conf import settings

urlpatterns = patterns('ccb.apps.faqs.views',
    # category overview
    (r'^/?$', 'handle_request'),
    (r'^(?P<category_slug>[^/]+)/$', 'handle_request'),
)

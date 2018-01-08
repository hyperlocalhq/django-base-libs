# -*- coding: UTF-8 -*-

from django.conf.urls import *
from ccb.apps.curated_lists import views as app_views

urlpatterns = [
    url(r'^$', app_views.featured_curated_lists, name='featured_curated_lists'),
    url(r'^(?P<token>\S+)/$', app_views.curated_list_detail, name='curated_list_detail'),
]

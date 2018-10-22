# -*- coding: UTF-8 -*-

from django.conf.urls import *
from . import views as app_views

urlpatterns = [
    url(r'^$', app_views.featured_curated_lists, name='featured_curated_lists'),
    url(
        r'^register-curator/(?P<encrypted_email>[a-zA-Z0-9+/_\-=]+)/$',
        app_views.register_curator,
        name="register_curator",
    ),
    url(r'^(?P<token>[^/]+)/$', app_views.curated_list_detail, name='curated_list_detail'),
    url(r'^(?P<token>[^/]+)/change/$', app_views.change_curated_list, name='change_curated_list'),
    url(r'^(?P<token>[^/]+)/delete/$', app_views.delete_curated_list, name='delete_curated_list'),
    url(r'^(?P<token>[^/]+)/items/(?P<item_id>[^/]+)/change/$', app_views.change_curated_list_item, name='change_curated_list_item'),
    url(r'^(?P<token>[^/]+)/items/(?P<item_id>[^/]+)/remove/$', app_views.remove_curated_list_item, name='remove_curated_list_item'),
    url(r'^(?P<token>[^/]+)/owners/$', app_views.curated_list_owners, name='curated_list_owners'),
    url(r'^(?P<token>[^/]+)/owners/invite/$', app_views.invite_curated_list_owner, name='invite_curated_list_owner'),
    url(r'^(?P<token>[^/]+)/owners/(?P<owner_id>[^/]+)/remove/$', app_views.remove_curated_list_owner,
        name='remove_curated_list_owner'),
]

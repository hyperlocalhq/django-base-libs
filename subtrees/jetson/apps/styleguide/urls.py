# -*- coding: UTF-8 -*-
from django.conf.urls import url

from . import views
    
urlpatterns = [
    url(r'^/?$', views.page, name="styleguide"),
    url(r'^forms/$', views.dummy_form),
    url(r'^(?P<page>[^/]+)/$', views.page, name="styleguide"),
]

# -*- coding: UTF-8 -*-
from django.conf.urls import *
from django.conf import settings


    
urlpatterns = patterns("jetson.apps.styleguide.views",
    url(r'^/?$', "page", name="styleguide"),
    url(r'^(?P<page>[^/]+)/$', "page", name="styleguide"),
)

urlpatterns += patterns("jetson.apps.styleguide.views", 
    (
        r'^forms/$',
        "dummy_form",
        ),
    )

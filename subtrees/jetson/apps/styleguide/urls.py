# -*- coding: UTF-8 -*-
from django.conf.urls import *
from django.conf import settings

urlpatterns = patterns('django.shortcuts',
    (
        r'^$',
        "render",
        {'template_name': 'styleguide/grid.html'},
        ),
    (
        r'^grid/$',
        "render",
        {'template_name': 'styleguide/grid.html'},
        ),
    (
        r'^typography/$',
        "render",
        {'template_name': 'styleguide/typography.html'},
        ),
    (
        r'^colors/$',
        "render",
        {'template_name': 'styleguide/colors.html'},
        ),
    (
        r'^images/$',
        "render",
        {'template_name': 'styleguide/images.html'},
        ),
    )

urlpatterns += patterns("jetson.apps.styleguide.views", 
    (
        r'^forms/$',
        "dummy_form",
        ),
    )

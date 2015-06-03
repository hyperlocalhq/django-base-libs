# -*- coding: UTF-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('django.views.generic.simple',
    (
        r'^$',
        "direct_to_template",
        {'template': 'styleguide/grid.html'},
        ),
    (
        r'^grid/$',
        "direct_to_template",
        {'template': 'styleguide/grid.html'},
        ),
    (
        r'^forms/$',
        "direct_to_template",
        {'template': 'styleguide/forms.html'},
        ),
    (
        r'^typography/$',
        "direct_to_template",
        {'template': 'styleguide/typography.html'},
        ),
    (
        r'^colors/$',
        "direct_to_template",
        {'template': 'styleguide/colors.html'},
        ),
    (
        r'^images/$',
        "direct_to_template",
        {'template': 'styleguide/images.html'},
        ),
    )

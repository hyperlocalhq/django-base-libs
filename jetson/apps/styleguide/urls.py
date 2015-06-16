# -*- coding: UTF-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns = patterns('',
    (
        r'^$',
        TemplateView.as_view(template_name='styleguide/grid.html'),
    ),
    (
        r'^grid/$',
        TemplateView.as_view(template_name='styleguide/grid.html'),
    ),
    (
        r'^forms/$',
        TemplateView.as_view(template_name='styleguide/forms.html'),
    ),
    (
        r'^typography/$',
        TemplateView.as_view(template_name='styleguide/typography.html'),
    ),
    (
        r'^colors/$',
        TemplateView.as_view(template_name='styleguide/colors.html'),
    ),
    (
        r'^images/$',
        TemplateView.as_view(template_name='styleguide/images.html'),
    ),
)

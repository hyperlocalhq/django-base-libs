# -*- coding: UTF-8 -*-
from django.conf import settings
from django.conf.urls import *

from base_libs.utils.misc import path_in_installed_app

urlpatterns = patterns(path_in_installed_app('image_mods.views'),
    url(r'^$', "recrop", name="image_mods_recrop"),
    url(r'^cropping-preview/(?P<bgcolor>[A-Fa-f0-9]+)/$', 'cropping_preview', name="image_mods_cropping_preview"),
    )

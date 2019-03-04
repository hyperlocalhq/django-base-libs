# -*- coding: UTF-8 -*-
from django.conf import settings
from django.conf.urls import *

urlpatterns = patterns(
    'jetson.apps.flatpages.views',
    (r'^(?P<url>.*)$', "flatpage"),
)

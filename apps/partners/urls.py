# -*- coding: UTF-8 -*-
from django.conf.urls import *

urlpatterns = [
    url(r'^$', 'ccb.apps.partners.views.partner_list', name='partner_list'),
]

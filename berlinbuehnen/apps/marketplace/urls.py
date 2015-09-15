# -*- coding: UTF-8 -*-

from django.conf.urls import *

urlpatterns = patterns('berlinbuehnen.apps.marketplace.views',
    url(r'^$', 'job_offer_list', name='job_offer_list'),
    url(r'^add/$', 'add_job_offer', name='add_job_offer'),
    url(r'^(?P<secure_id>\d+)/$', 'job_offer_detail', name='job_offer_detail'),
    url(r'^(?P<secure_id>\d+)/change/$', 'change_job_offer', name='change_job_offer'),
    url(r'^(?P<secure_id>\d+)/delete/$', 'delete_job_offer', name='delete_job_offer'),
    url(r'^(?P<secure_id>\d+)/status/$', 'change_job_offer_status', name='change_job_offer_status'),
)

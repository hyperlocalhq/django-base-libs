# -*- coding: UTF-8 -*-

from django.conf.urls import *

urlpatterns = patterns('berlinbuehnen.apps.education.views',
    url(r'^$', 'project_list', name='project_list'),
    url(r'^(?P<slug>[^/]+)/$', 'project_detail', name='project_detail'),
    url(r'^(?P<slug>[^/]+)/events/(?P<event_id>\d+)/$', 'project_detail', name='project_event_detail'),

    # url(r'^add/$', 'add_project', name='add_project'),
    # url(r'^(?P<slug>[^/]+)/events/$', 'project_events', name='project_events'),
    # url(r'^(?P<slug>[^/]+)/change/$', 'change_project', name='change_project'),
    # url(r'^(?P<slug>[^/]+)/delete/$', 'delete_project', name='delete_project'),
    # url(r'^(?P<slug>[^/]+)/status/$', 'change_project_status', name='change_project_status'),
    # gallery
    # url(r'^(?P<slug>[^/]+)/gallery/$', 'image_overview', name='project_image_overview'),
    # url(r'^(?P<slug>[^/]+)/gallery/add/$', 'create_update_image', name='project_add_image'),
    # url(r'^(?P<slug>[^/]+)/gallery/file_(?P<mediafile_token>[^/]+)/$', 'create_update_image', name='project_change_image'),
    # url(r'^(?P<slug>[^/]+)/gallery/file_(?P<mediafile_token>[^/]+)/delete/$', 'delete_image', name='project_delete_image'),
)

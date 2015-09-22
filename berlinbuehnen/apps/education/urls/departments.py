# -*- coding: UTF-8 -*-

from django.conf.urls import *

urlpatterns = patterns('berlinbuehnen.apps.education.views',
    url(r'^$', 'department_list', name='department_list'),
    url(r'^(?P<slug>[^/]+)/$', 'department_detail', name='department_detail'),

    # url(r'^add/$', 'add_department', name='add_department'),
    # url(r'^(?P<slug>[^/]+)/change/$', 'change_project', name='change_project'),
    # url(r'^(?P<slug>[^/]+)/delete/$', 'delete_project', name='delete_project'),
    # url(r'^(?P<slug>[^/]+)/status/$', 'change_project_status', name='change_project_status'),

    # gallery
    # url(r'^(?P<slug>[^/]+)/gallery/$', 'image_overview', name='project_image_overview'),
    # url(r'^(?P<slug>[^/]+)/gallery/add/$', 'create_update_image', name='project_add_image'),
    # url(r'^(?P<slug>[^/]+)/gallery/file_(?P<mediafile_token>[^/]+)/$', 'create_update_image', name='project_change_image'),
    # url(r'^(?P<slug>[^/]+)/gallery/file_(?P<mediafile_token>[^/]+)/delete/$', 'delete_image', name='project_delete_image'),
)

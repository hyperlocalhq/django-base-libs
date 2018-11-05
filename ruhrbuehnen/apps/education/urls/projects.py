# -*- coding: UTF-8 -*-

from django.conf.urls import *

urlpatterns = patterns('ruhrbuehnen.apps.education.views.projects',
    url(r'^$', 'project_list', name='project_list'),
    url(r'^add/$', 'add_project', name='add_project'),

    url(r'^(?P<slug>[^/]+)/$', 'project_detail', name='project_detail'),
    url(r'^(?P<slug>[^/]+)/events/(?P<event_id>\d+)/$', 'project_detail', name='project_event_detail'),

    url(r'^(?P<slug>[^/]+)/change/$', 'change_project', name='change_project'),
    url(r'^(?P<slug>[^/]+)/delete/$', 'delete_project', name='delete_project'),
    url(r'^(?P<slug>[^/]+)/status/$', 'change_project_status', name='change_project_status'),
    url(r'^(?P<slug>[^/]+)/duplicate/$', 'duplicate_project', name='duplicate_project'),
)

urlpatterns += patterns('ruhrbuehnen.apps.education.views.project_gallery',
    # videos
    url(r'^(?P<slug>[^/]+)/video/$', 'video_overview', name='project_video_overview'),
    url(r'^(?P<slug>[^/]+)/video/add/$', 'create_update_video', name='project_add_video'),
    url(r'^(?P<slug>[^/]+)/video/file_(?P<mediafile_token>[^/]+)/$', 'create_update_video', name='project_change_video'),
    url(r'^(?P<slug>[^/]+)/video/file_(?P<mediafile_token>[^/]+)/delete/$', 'delete_video', name='project_delete_video'),
    # images
    url(r'^(?P<slug>[^/]+)/gallery/$', 'image_overview', name='project_image_overview'),
    url(r'^(?P<slug>[^/]+)/gallery/add/$', 'create_update_image', name='project_add_image'),
    url(r'^(?P<slug>[^/]+)/gallery/file_(?P<mediafile_token>[^/]+)/$', 'create_update_image', name='project_change_image'),
    url(r'^(?P<slug>[^/]+)/gallery/file_(?P<mediafile_token>[^/]+)/delete/$', 'delete_image', name='project_delete_image'),
    # pdfs
    url(r'^(?P<slug>[^/]+)/pdf/$', 'pdf_overview', name='project_pdf_overview'),
    url(r'^(?P<slug>[^/]+)/pdf/add/$', 'create_update_pdf', name='project_add_pdf'),
    url(r'^(?P<slug>[^/]+)/pdf/file_(?P<mediafile_token>[^/]+)/$', 'create_update_pdf', name='project_change_pdf'),
    url(r'^(?P<slug>[^/]+)/pdf/file_(?P<mediafile_token>[^/]+)/delete/$', 'delete_pdf', name='project_delete_pdf'),
)

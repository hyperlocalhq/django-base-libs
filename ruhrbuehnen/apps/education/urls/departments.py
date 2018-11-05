# -*- coding: UTF-8 -*-

from django.conf.urls import *

urlpatterns = patterns('ruhrbuehnen.apps.education.views.departments',
    url(r'^$', 'department_list', name='department_list'),
    url(r'^add/$', 'add_department', name='add_department'),

    url(r'^(?P<slug>[^/]+)/$', 'department_detail', name='department_detail'),

    url(r'^(?P<slug>[^/]+)/change/$', 'change_department', name='change_department'),
    url(r'^(?P<slug>[^/]+)/delete/$', 'delete_department', name='delete_department'),
    url(r'^(?P<slug>[^/]+)/status/$', 'change_department_status', name='change_department_status'),
)

urlpatterns += patterns('ruhrbuehnen.apps.education.views.department_gallery',
    # images
    url(r'^(?P<slug>[^/]+)/gallery/$', 'image_overview', name='department_image_overview'),
    url(r'^(?P<slug>[^/]+)/gallery/add/$', 'create_update_image', name='department_add_image'),
    url(r'^(?P<slug>[^/]+)/gallery/file_(?P<mediafile_token>[^/]+)/$', 'create_update_image', name='department_change_image'),
    url(r'^(?P<slug>[^/]+)/gallery/file_(?P<mediafile_token>[^/]+)/delete/$', 'delete_image', name='department_delete_image'),
    # pdfs
    url(r'^(?P<slug>[^/]+)/pdf/$', 'pdf_overview', name='department_pdf_overview'),
    url(r'^(?P<slug>[^/]+)/pdf/add/$', 'create_update_pdf', name='department_add_pdf'),
    url(r'^(?P<slug>[^/]+)/pdf/file_(?P<mediafile_token>[^/]+)/$', 'create_update_pdf', name='department_change_pdf'),
    url(r'^(?P<slug>[^/]+)/pdf/file_(?P<mediafile_token>[^/]+)/delete/$', 'delete_pdf', name='department_delete_pdf'),
)

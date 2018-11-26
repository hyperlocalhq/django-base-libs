# -*- coding: UTF-8 -*-

from django.conf.urls import *

urlpatterns = patterns(
    'ruhrbuehnen.apps.productions.views.productions',
    url(r'^$', 'event_list', name='event_list'),
    url(r'^add/$', 'add_production', name='add_production'),
    url(
        r'^(?P<year>\d\d\d\d)-(?P<month>\d\d)-(?P<day>\d\d)/$',
        'event_list',
        name='event_list_for_a_day'
    ),
    url(r'^(?P<slug>[^/]+)/$', 'event_detail', name='production_detail'),
    url(
        r'^(?P<slug>[^/]+)/change/$',
        'change_production',
        name='change_production'
    ),
    url(
        r'^(?P<slug>[^/]+)/delete/$',
        'delete_production',
        name='delete_production'
    ),
    url(
        r'^(?P<slug>[^/]+)/status/$',
        'change_production_status',
        name='change_production_status'
    ),
    url(
        r'^(?P<slug>[^/]+)/duplicate/$',
        'duplicate_production',
        name='duplicate_production'
    ),
)

urlpatterns += patterns(
    'ruhrbuehnen.apps.productions.views.production_gallery',
    # videos
    url(
        r'^(?P<slug>[^/]+)/video/$',
        'video_overview',
        name='production_video_overview'
    ),
    url(
        r'^(?P<slug>[^/]+)/video/add/$',
        'create_update_video',
        name='production_add_video'
    ),
    url(
        r'^(?P<slug>[^/]+)/video/file_(?P<mediafile_token>[^/]+)/$',
        'create_update_video',
        name='production_change_video'
    ),
    url(
        r'^(?P<slug>[^/]+)/video/file_(?P<mediafile_token>[^/]+)/delete/$',
        'delete_video',
        name='production_delete_video'
    ),
    # live streaming
    url(
        r'^(?P<slug>[^/]+)/live-streaming/$',
        'streaming_overview',
        name='production_streaming_overview'
    ),
    url(
        r'^(?P<slug>[^/]+)/live-streaming/add/$',
        'create_update_streaming',
        name='production_add_streaming'
    ),
    url(
        r'^(?P<slug>[^/]+)/live-streaming/file_(?P<mediafile_token>[^/]+)/$',
        'create_update_streaming',
        name='production_change_streaming'
    ),
    url(
        r'^(?P<slug>[^/]+)/live-streaming/file_(?P<mediafile_token>[^/]+)/delete/$',
        'delete_streaming',
        name='production_delete_streaming'
    ),
    # images
    url(
        r'^(?P<slug>[^/]+)/gallery/$',
        'image_overview',
        name='production_image_overview'
    ),
    url(
        r'^(?P<slug>[^/]+)/gallery/add/$',
        'create_update_image',
        name='production_add_image'
    ),
    url(
        r'^(?P<slug>[^/]+)/gallery/file_(?P<mediafile_token>[^/]+)/$',
        'create_update_image',
        name='production_change_image'
    ),
    url(
        r'^(?P<slug>[^/]+)/gallery/file_(?P<mediafile_token>[^/]+)/delete/$',
        'delete_image',
        name='production_delete_image'
    ),
    # pdfs
    url(
        r'^(?P<slug>[^/]+)/pdf/$',
        'pdf_overview',
        name='production_pdf_overview'
    ),
    url(
        r'^(?P<slug>[^/]+)/pdf/add/$',
        'create_update_pdf',
        name='production_add_pdf'
    ),
    url(
        r'^(?P<slug>[^/]+)/pdf/file_(?P<mediafile_token>[^/]+)/$',
        'create_update_pdf',
        name='production_change_pdf'
    ),
    url(
        r'^(?P<slug>[^/]+)/pdf/file_(?P<mediafile_token>[^/]+)/delete/$',
        'delete_pdf',
        name='production_delete_pdf'
    ),
)

urlpatterns += patterns(
    'ruhrbuehnen.apps.productions.views.productions',
    # events
    url(
        r'^(?P<slug>[^/]+)/events/$',
        'events_overview',
        name='production_events_overview'
    ),
    url(r'^(?P<slug>[^/]+)/events/add/$', 'add_events', name='add_events'),
    url(
        r'^(?P<slug>[^/]+)/events/(?P<event_id>\d+)/$',
        'event_detail',
        name='event_detail'
    ),
    url(
        r'^(?P<slug>[^/]+)/events/(?P<event_id>\d+)/change/basic-info/$',
        'change_event_basic_info',
        name='change_event_basic_info'
    ),
    url(
        r'^(?P<slug>[^/]+)/events/(?P<event_id>\d+)/change/description/$',
        'change_event_description',
        name='change_event_description'
    ),
    url(
        r'^(?P<slug>[^/]+)/events/(?P<event_id>\d+)/change/gallery/$',
        'change_event_gallery',
        name='change_event_gallery'
    ),
    url(
        r'^(?P<slug>[^/]+)/events/(?P<event_id>\d+)/delete/$',
        'delete_event',
        name='delete_event'
    ),
)

urlpatterns += patterns(
    'ruhrbuehnen.apps.productions.views.event_gallery',
    # videos
    url(
        r'^(?P<slug>[^/]+)/events/(?P<event_id>\d+)/change/video/$',
        'video_overview',
        name='event_video_overview'
    ),
    url(
        r'^(?P<slug>[^/]+)/events/(?P<event_id>\d+)/change/video/add/$',
        'create_update_video',
        name='event_add_video'
    ),
    url(
        r'^(?P<slug>[^/]+)/events/(?P<event_id>\d+)/change/video/file_(?P<mediafile_token>[^/]+)/$',
        'create_update_video',
        name='event_change_video'
    ),
    url(
        r'^(?P<slug>[^/]+)/events/(?P<event_id>\d+)/change/video/file_(?P<mediafile_token>[^/]+)/delete/$',
        'delete_video',
        name='event_delete_video'
    ),
    # live streaming
    url(
        r'^(?P<slug>[^/]+)/events/(?P<event_id>\d+)/change/live-streaming/$',
        'streaming_overview',
        name='event_streaming_overview'
    ),
    url(
        r'^(?P<slug>[^/]+)/events/(?P<event_id>\d+)/change/live-streaming/add/$',
        'create_update_streaming',
        name='event_add_streaming'
    ),
    url(
        r'^(?P<slug>[^/]+)/events/(?P<event_id>\d+)/change/live-streaming/file_(?P<mediafile_token>[^/]+)/$',
        'create_update_streaming',
        name='event_change_streaming'
    ),
    url(
        r'^(?P<slug>[^/]+)/events/(?P<event_id>\d+)/change/live-streaming/file_(?P<mediafile_token>[^/]+)/delete/$',
        'delete_streaming',
        name='event_delete_streaming'
    ),
    # images
    url(
        r'^(?P<slug>[^/]+)/events/(?P<event_id>\d+)/change/gallery/overview/$',
        'image_overview',
        name='event_image_overview'
    ),
    url(
        r'^(?P<slug>[^/]+)/events/(?P<event_id>\d+)/change/gallery/add/$',
        'create_update_image',
        name='event_add_image'
    ),
    url(
        r'^(?P<slug>[^/]+)/events/(?P<event_id>\d+)/change/gallery/file_(?P<mediafile_token>[^/]+)/$',
        'create_update_image',
        name='event_change_image'
    ),
    url(
        r'^(?P<slug>[^/]+)/events/(?P<event_id>\d+)/change/gallery/file_(?P<mediafile_token>[^/]+)/delete/$',
        'delete_image',
        name='event_delete_image'
    ),
    # pdfs
    url(
        r'^(?P<slug>[^/]+)/events/(?P<event_id>\d+)/change/pdf/$',
        'pdf_overview',
        name='event_pdf_overview'
    ),
    url(
        r'^(?P<slug>[^/]+)/events/(?P<event_id>\d+)/change/pdf/add/$',
        'create_update_pdf',
        name='event_add_pdf'
    ),
    url(
        r'^(?P<slug>[^/]+)/events/(?P<event_id>\d+)/change/pdf/file_(?P<mediafile_token>[^/]+)/$',
        'create_update_pdf',
        name='event_change_pdf'
    ),
    url(
        r'^(?P<slug>[^/]+)/events/(?P<event_id>\d+)/change/pdf/file_(?P<mediafile_token>[^/]+)/delete/$',
        'delete_pdf',
        name='event_delete_pdf'
    ),
)

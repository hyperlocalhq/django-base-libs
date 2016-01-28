# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, url

from ccb.apps.resources.models import Document
from jetson.apps.utils.views import object_detail
from jetson.apps.utils.context_processors import prev_next_processor
from ccb.apps.resources.views import _document_list_filter

document_list_info = {
    'queryset': Document.objects.filter(status__in=("published", "published_commercial")),
    'template_name': 'resources/documents/document_list.html',
    'paginate_by': 24,
    'allow_empty': True,
    'context_processors': (prev_next_processor,),
}

document_details_info = {
    'queryset': Document.objects.filter(status__in=("published", "published_commercial")),
    'slug_field': 'slug',
    'template_name': 'resources/documents/document_details.html',
    'context_processors': (prev_next_processor,),
    'context_item_type': 'document',
}

urlpatterns = (
    url(r'^$',
        'ccb.apps.resources.views.document_list',
        dict(list_filter=_document_list_filter, **document_list_info)
        ),
    url(r'^(?P<show>favorites)/$',
        'ccb.apps.resources.views.document_list',
        dict(list_filter=_document_list_filter, **document_list_info)
        ),
    url(r'^(?P<show>memos)/$',
        'ccb.apps.resources.views.document_list',
        dict(list_filter=_document_list_filter, **document_list_info)
        ),
    url(r'^(?P<show>cultural-funding)/$',
        'ccb.apps.resources.views.document_list',
        dict(list_filter=_document_list_filter, **document_list_info)
        ),
    url(r'^(?P<show>scholarship)/$',
        'ccb.apps.resources.views.document_list',
        dict(list_filter=_document_list_filter, **document_list_info)
        ),
    url(r'^(?P<show>support-programme)/$',
        'ccb.apps.resources.views.document_list',
        dict(list_filter=_document_list_filter, **document_list_info)
        ),
    url(r'^(?P<show>information-founders)/$',
        'ccb.apps.resources.views.document_list',
        dict(list_filter=_document_list_filter, **document_list_info)
        ),
    url(r'^(?P<show>other)/$',
        'ccb.apps.resources.views.document_list',
        dict(list_filter=_document_list_filter, **document_list_info)
        ),
    url(r'^document/(?P<slug>[^/]+)/$',
        object_detail,
        document_details_info
        ),
    url(r'^document/(?P<slug>[^/]+)/reviews/$',
        object_detail,
        dict(document_details_info, template_name="resources/documents/document_reviews.html")
        ),
    url(r'^document/(?P<slug>[^/]+)/network/$',
        object_detail,
        dict(document_details_info, template_name="resources/documents/document_network.html")
        ),
)

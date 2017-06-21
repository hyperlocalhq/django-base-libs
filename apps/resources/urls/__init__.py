# -*- coding: UTF-8 -*-
from django.conf.urls import url

from kb.apps.resources.models import Document
from jetson.apps.utils.views import object_detail
from jetson.apps.utils.context_processors import prev_next_processor
from kb.apps.resources.views import _document_list_filter

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
        'kb.apps.resources.views.document_list',
        dict(list_filter=_document_list_filter, **document_list_info),
        name="document_list_global",
        ),
    url(r'^(?P<show>favorites)/$',
        'kb.apps.resources.views.document_list',
        dict(list_filter=_document_list_filter, **document_list_info)
        ),
    url(r'^(?P<show>memos)/$',
        'kb.apps.resources.views.document_list',
        dict(list_filter=_document_list_filter, **document_list_info)
        ),
    url(r'^(?P<show>cultural-funding)/$',
        'kb.apps.resources.views.document_list',
        dict(list_filter=_document_list_filter, **document_list_info)
        ),
    url(r'^(?P<show>scholarship)/$',
        'kb.apps.resources.views.document_list',
        dict(list_filter=_document_list_filter, **document_list_info)
        ),
    url(r'^(?P<show>support-programme)/$',
        'kb.apps.resources.views.document_list',
        dict(list_filter=_document_list_filter, **document_list_info)
        ),
    url(r'^(?P<show>information-founders)/$',
        'kb.apps.resources.views.document_list',
        dict(list_filter=_document_list_filter, **document_list_info)
        ),
    url(r'^(?P<show>other)/$',
        'kb.apps.resources.views.document_list',
        dict(list_filter=_document_list_filter, **document_list_info)
        ),
    url(r'^document/(?P<slug>[^/]+)/$',
        object_detail,
        document_details_info,
        name="document_detail",
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

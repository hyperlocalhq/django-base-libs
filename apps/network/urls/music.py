# -*- coding: UTF-8 -*-
from django.conf.urls import *
from jetson.apps.utils.context_processors import prev_next_processor
from ccb.apps.site_specific.models import ContextItem

CATEGORY_SLUG = "musik"

member_list_info = {
    'queryset': ContextItem.objects.filter(
        content_type__model__in=["person", "institution"],
        ),
    'template_name': 'network/member_list_under_category.html',
    'paginate_by': 24,
    'allow_empty': True,
    'context_processors': (prev_next_processor,),
    'category_slug': CATEGORY_SLUG,
}

urlpatterns = [
    url(r'^$', 'ccb.apps.network.views.member_list', member_list_info),
]
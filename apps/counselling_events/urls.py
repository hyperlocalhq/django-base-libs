# -*- coding: UTF-8 -*-
from django.conf.urls import *
from jetson.apps.utils.context_processors import prev_next_processor
from ccb.apps.events.models import Event

event_list_info = {
    'allow_empty': True,
    'context_processors': (prev_next_processor,),
    # 'end_date': None,
    'paginate_by': 24,
    'queryset': Event.objects.all(),
    'slug': u'kreativwirtschaftsberatung_berlin',
    # 'start_date': None,
    'template_name': '',  # template name is defined in the view
    # 'unlimited': None,
}

urlpatterns = [
    url(
        r'^$',
        'ccb.apps.counselling_events.views.counselling_events_list',
        event_list_info,
        name="counselling_event_list"
    )
]

# -*- coding: UTF-8 -*-
def events_under_category_urlpatterns(category_slug):
    from django.conf.urls import url
    from ccb.apps.events.models import Event

    event_list_info = {
        'queryset': Event.objects.all(),
        'template_name': 'events/event_list_under_category.html',
        'paginate_by': 24,
        'allow_empty': True,
        'category_slug': category_slug,
    }

    urlpatterns = [
        url(
            r'^$',
            'ccb.apps.events.views.event_list',
            event_list_info,
        ),
        url(
            r'^ical/$',
            'ccb.apps.events.views.event_list_ical',
            event_list_info,
        ),
        url(
            r'^feeds/(?P<feed_type>[^/]+)/$',
            'ccb.apps.events.views.event_list_feed',
            event_list_info,
        ),
    ]
    return urlpatterns
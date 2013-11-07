# -*- coding: utf-8 -*-

from django import template
from django.contrib.contenttypes.models import ContentType
from museumsportal.apps.internal_links.models import LinkGroup

register = template.Library()


@register.inclusion_tag('internal_links/link_group.html', takes_context=True)
def link_group(context, obj):
    """
    Returns the latest link_group for a given Museum, Exhibition, Event, or Workshop.

    Tag usage:
    {% load internal_links_tags %}
    {% link_group object %}

    """
    to_return = {}
    lgs = None
    ct = ContentType.objects.get_for_model(obj)

    if ct.model == "museum":
        lgs = LinkGroup.objects.filter(museums=obj)
    elif ct.model == "exhibition":
        lgs = LinkGroup.objects.filter(exhibitions=obj)
    elif ct.model == "event":
        lgs = LinkGroup.objects.filter(events=obj)
    elif ct.model == "workshop":
        lgs = LinkGroup.objects.filter(workshops=obj)

    if lgs:
        to_return['lg'] = lgs.order_by("-creation_date")[0]

    return to_return

# -*- coding: UTF-8 -*-
from django import template

from ccb.apps.curated_lists.models import ListItem
from django.contrib.contenttypes.models import ContentType

register = template.Library()


@register.filter
def curated_list_count(instance):
    ct = ContentType.objects.get_for_model(instance)
    return ListItem.objects.filter(content_type=ct, object_id=instance.pk).count()

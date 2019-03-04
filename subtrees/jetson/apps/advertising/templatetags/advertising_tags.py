# -*- coding: utf-8 -*-

# © Copyright 2009 Andre Engelbrecht. All Rights Reserved.
# This script is licensed under the BSD Open Source Licence
# Please see the text file LICENCE for more information
# If this script is distributed, it must be accompanied by the Licence

from datetime import datetime
from django import template
from jetson.apps.advertising.models import AdBase, AdImpression

register = template.Library()

### FILTERS ###


@register.filter
def not_empty_ad_zone(ad_zone):
    return bool(AdBase.objects.get_random_ad(ad_zone))


### TAGS ###


@register.inclusion_tag('advertising/ad_tag.html', takes_context=True)
def random_zone_ad(context, ad_zone):
    """
    Returns a random advert for ``ad_zone``.
    The advert returned is independent of the category

    In order for the impression to be saved add the following
    to the TEMPLATE_CONTEXT_PROCESSORS:

    'jetson.apps.advertising.context_processors.get_source_features'

    Tag usage:
    {% load advertising_tags %}
    {% random_zone_ad 'zone_sysname' %}

    """
    to_return = {}

    # Retrieve a random ad for the zone
    ad = AdBase.objects.get_random_ad(ad_zone)
    to_return['ad'] = ad

    # Record a impression for the ad
    if context.has_key('from_ip'
                      ) and not context.get('is_crawler', False) and ad:
        from_ip = context.get('from_ip')
        try:
            impression = AdImpression(
                ad=ad, impression_date=datetime.now(), source_ip=from_ip
            )
            impression.save()
        except:
            pass
    return to_return


@register.inclusion_tag('advertising/ad_tag.html', takes_context=True)
def random_category_ad(context, ad_zone, ad_category):
    """
    Returns a random advert from the specified category.

    Usage:
    {% load advertizing_tags %}
    {% random_category_ad 'zone_sysname' 'my_category_sysname' %}

    """
    to_return = {}

    # Retrieve a random ad for the category and zone
    ad = AdBase.objects.get_random_ad(ad_zone, ad_category)
    to_return['ad'] = ad

    # Record a impression for the ad
    if context.has_key('from_ip'
                      ) and not context.get('is_crawler', False) and ad:
        from_ip = context.get('from_ip')
        try:
            impression = AdImpression(
                ad=ad, impression_date=datetime.now(), source_ip=from_ip
            )
            impression.save()
        except:
            pass
    return to_return

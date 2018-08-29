# -*- coding: utf-8 -*-

import datetime

from django.db import models

from base_libs.middleware.threadlocals import get_current_language

try:
    from django.utils.timezone import now
except ImportError:
    now = datetime.datetime.now


class AdManager(models.Manager):
    """ A Custom Manager for ads """

    def get_random_ad(self, ad_zone, ad_category=None):
        """
        Returns a random advert that belongs for the specified ``ad_category``
        and ``ad_zone``.
        If ``ad_category`` is None, the ad will be category independent.
        """
        language = get_current_language()
        time_now = now()
        qs = self.get_query_set().filter(
            start_showing__lte=time_now,
            stop_showing__gte=time_now,
            zone__sysname=ad_zone,
        ).filter(models.Q(language=language) | models.Q(language="")).select_related('textad', 'bannerad')

        if ad_category:
            qs = qs.filter(category__sysname=ad_category)

        try:
            ad = qs.order_by('?')[0]
        except IndexError:
            return None
        return ad

# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


class AdventCalendarApphook(CMSApp):
    name = _("Advent Calendar")
    urls = ["berlinbuehnen.apps.advent_calendar.urls"]


apphook_pool.register(AdventCalendarApphook)
# -*- coding: UTF-8 -*-

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class TheaterOfTheWeekApphook(CMSApp):
    name = _("Theater of the week")
    urls = ["ruhrbuehnen.apps.theater_of_the_week.urls"]


apphook_pool.register(TheaterOfTheWeekApphook)

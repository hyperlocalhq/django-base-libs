# -*- coding: UTF-8 -*-

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class FestivalsApphook(CMSApp):
    name = _("Festivals")
    urls = ["ruhrbuehnen.apps.festivals.urls"]


apphook_pool.register(FestivalsApphook)

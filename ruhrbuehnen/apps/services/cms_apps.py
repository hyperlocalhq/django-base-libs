# -*- coding: UTF-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class ServicesApphook(CMSApp):
    name = _("Services")
    urls = ["ruhrbuehnen.apps.services.urls"]


apphook_pool.register(ServicesApphook)

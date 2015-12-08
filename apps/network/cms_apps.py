# -*- coding: UTF-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class NetworkApphook(CMSApp):
    name = _("Network")
    urls = ["ccb.apps.network.urls"]

apphook_pool.register(NetworkApphook)
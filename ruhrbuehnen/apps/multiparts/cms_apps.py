# -*- coding: UTF-8 -*-

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class MultipartsApphook(CMSApp):
    name = _("Multipart productions")
    urls = ["ruhrbuehnen.apps.multiparts.urls"]

apphook_pool.register(MultipartsApphook)

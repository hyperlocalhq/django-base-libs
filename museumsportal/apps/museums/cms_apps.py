# -*- coding: UTF-8 -*-

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class MuseumsApphook(CMSApp):
    name = _("Museums")
    urls = ["museumsportal.apps.museums.urls"]

apphook_pool.register(MuseumsApphook)

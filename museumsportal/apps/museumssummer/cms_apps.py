# -*- coding: UTF-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class MuseumsSummerApphook(CMSApp):
    name = _("Museums' Summer Locations")
    urls = ["museumsportal.apps.museumssummer.urls"]

apphook_pool.register(MuseumsSummerApphook)

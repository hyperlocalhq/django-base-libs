# -*- coding: UTF-8 -*-

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class PartnersApphook(CMSApp):
    name = _("Partners")
    urls = ["kb.apps.partners.urls"]

apphook_pool.register(PartnersApphook)

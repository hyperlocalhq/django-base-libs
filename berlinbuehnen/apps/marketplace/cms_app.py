# -*- coding: UTF-8 -*-

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class MarketplaceApphook(CMSApp):
    name = _("Marketplace")
    urls = ["berlinbuehnen.apps.marketplace.urls"]

apphook_pool.register(MarketplaceApphook)

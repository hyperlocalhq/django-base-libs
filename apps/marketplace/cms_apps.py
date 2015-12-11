# -*- coding: UTF-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class MarketplaceAppHook(CMSApp):
    name = _("Job Offers")
    urls = ["ccb.apps.marketplace.urls"]

apphook_pool.register(MarketplaceAppHook)

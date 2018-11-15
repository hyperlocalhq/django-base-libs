# -*- coding: UTF-8 -*-

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class ShopApphook(CMSApp):
    name = _("Shop")
    urls = ["museumsportal.apps.shop.urls"]

apphook_pool.register(ShopApphook)

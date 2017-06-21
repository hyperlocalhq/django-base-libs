# -*- coding: UTF-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class ResourceAppHook(CMSApp):
    name = _("Documents")
    urls = ["kb.apps.resources.urls"]

apphook_pool.register(ResourceAppHook)

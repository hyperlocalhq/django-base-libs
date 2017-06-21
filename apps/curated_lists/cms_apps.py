# -*- coding: UTF-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class FeaturedCuratedListsApphook(CMSApp):
    name = _("Featured Curated Lists")
    urls = ["kb.apps.curated_lists.urls"]

apphook_pool.register(FeaturedCuratedListsApphook)

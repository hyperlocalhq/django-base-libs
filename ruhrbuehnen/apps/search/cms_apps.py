# -*- coding: UTF-8 -*-

from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


class SearchApphook(CMSApp):
    name = _("Search")
    urls = ["ruhrbuehnen.apps.search.urls"]


apphook_pool.register(SearchApphook)

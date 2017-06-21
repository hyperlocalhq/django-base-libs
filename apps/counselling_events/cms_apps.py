# -*- coding: UTF-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class CounsellingEventsApphook(CMSApp):
    name = _("Counselling Events")
    urls = ["kb.apps.counselling_events.urls"]

apphook_pool.register(CounsellingEventsApphook)

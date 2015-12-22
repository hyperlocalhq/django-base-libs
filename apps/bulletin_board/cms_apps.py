# -*- coding: UTF-8 -*-

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class BulletinBoardApphook(CMSApp):
    name = _("Bulletin Board")
    urls = ["ccb.apps.bulletin_board.urls"]

apphook_pool.register(BulletinBoardApphook)

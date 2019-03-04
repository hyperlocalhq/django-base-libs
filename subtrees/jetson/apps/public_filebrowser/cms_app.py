# -*- coding: UTF-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class PublicFilebrowserApphook(CMSApp):
    name = _("Public filebrowser")
    urls = ["jetson.apps.public_filebrowser.urls"]


apphook_pool.register(PublicFilebrowserApphook)

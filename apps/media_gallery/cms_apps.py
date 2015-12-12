# -*- coding: UTF-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class MediaGalleryAppHook(CMSApp):
    name = _("Media Gallery")
    urls = ["ccb.apps.media_gallery.urls"]

apphook_pool.register(MediaGalleryAppHook)

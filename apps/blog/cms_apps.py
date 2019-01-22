# -*- coding: UTF-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class BlogAppHook(CMSApp):
    name = _("Global Blog")
    urls = ["jetson.apps.blog.urls.cms"]


apphook_pool.register(BlogAppHook)

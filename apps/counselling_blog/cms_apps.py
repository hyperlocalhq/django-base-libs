# -*- coding: UTF-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class CounsellingBlogApphook(CMSApp):
    name = _("Counselling Blog")
    urls = ["ccb.apps.counselling_blog.urls"]

apphook_pool.register(CounsellingBlogApphook)
print 'registered counselling blog app'
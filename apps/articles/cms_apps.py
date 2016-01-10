# -*- coding: UTF-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class ArticleAppHook(CMSApp):
    name = _("Articles - Deprecated")
    urls = ["ccb.apps.articles.urls.news"]

apphook_pool.register(ArticleAppHook)

class NewsAppHook(CMSApp):
    name = _("Articles - News")
    urls = ["ccb.apps.articles.urls.news"]

apphook_pool.register(NewsAppHook)

class InterviewsAppHook(CMSApp):
    name = _("Articles - Interviews")
    urls = ["ccb.apps.articles.urls.interviews"]

apphook_pool.register(InterviewsAppHook)
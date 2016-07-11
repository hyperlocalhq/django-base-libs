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



class ArchitectureNewsApphook(CMSApp):
    name = _("Architecture - News")
    urls = ["ccb.apps.articles.urls.architecture"]

apphook_pool.register(ArchitectureNewsApphook)


class VisualArtsNewsApphook(CMSApp):
    name = _("Visual Arts - News")
    urls = ["ccb.apps.articles.urls.visual_arts"]

apphook_pool.register(VisualArtsNewsApphook)


class DesignNewsApphook(CMSApp):
    name = _("Design - News")
    urls = ["ccb.apps.articles.urls.design"]

apphook_pool.register(DesignNewsApphook)


class EventIndustryNewsApphook(CMSApp):
    name = _("Event Industry - News")
    urls = ["ccb.apps.articles.urls.event_industry"]

apphook_pool.register(EventIndustryNewsApphook)


class FilmBroadcastNewsApphook(CMSApp):
    name = _("Film & Broadcast - News")
    urls = ["ccb.apps.articles.urls.film_broadcast"]

apphook_pool.register(FilmBroadcastNewsApphook)


class PhotographyNewsApphook(CMSApp):
    name = _("Photography - News")
    urls = ["ccb.apps.articles.urls.photography"]

apphook_pool.register(PhotographyNewsApphook)


class GamesInteractiveNewsApphook(CMSApp):
    name = _("Games & Interactive - News")
    urls = ["ccb.apps.articles.urls.games_interactive"]

apphook_pool.register(GamesInteractiveNewsApphook)


class LiteraturePublishingNewsApphook(CMSApp):
    name = _("Literature & Publishing - News")
    urls = ["ccb.apps.articles.urls.literature_publishing"]

apphook_pool.register(LiteraturePublishingNewsApphook)


class FashionTextileNewsApphook(CMSApp):
    name = _("Fashion & Textile - News")
    urls = ["ccb.apps.articles.urls.fashion_textile"]

apphook_pool.register(FashionTextileNewsApphook)


class MusicNewsApphook(CMSApp):
    name = _("Music - News")
    urls = ["ccb.apps.articles.urls.music"]

apphook_pool.register(MusicNewsApphook)


class TheatreDanceNewsApphook(CMSApp):
    name = _("Theatre & Dance - News")
    urls = ["ccb.apps.articles.urls.theatre_dance"]

apphook_pool.register(TheatreDanceNewsApphook)


class AdvertisingPRNewsApphook(CMSApp):
    name = _("Advertising & PR - News")
    urls = ["ccb.apps.articles.urls.advertising_pr"]

apphook_pool.register(AdvertisingPRNewsApphook)

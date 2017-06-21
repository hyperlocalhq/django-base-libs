# -*- coding: UTF-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class EventAppHook(CMSApp):
    name = _("Events")
    urls = ["kb.apps.events.urls"]

apphook_pool.register(EventAppHook)


class ArchitectureEventsApphook(CMSApp):
    name = _("Architecture - Events")
    urls = ["kb.apps.events.urls.architecture"]

apphook_pool.register(ArchitectureEventsApphook)


class VisualArtsEventsApphook(CMSApp):
    name = _("Visual Arts - Events")
    urls = ["kb.apps.events.urls.visual_arts"]

apphook_pool.register(VisualArtsEventsApphook)


class DesignEventsApphook(CMSApp):
    name = _("Design - Events")
    urls = ["kb.apps.events.urls.design"]

apphook_pool.register(DesignEventsApphook)


class EventIndustryEventsApphook(CMSApp):
    name = _("Event Industry - Events")
    urls = ["kb.apps.events.urls.event_industry"]

apphook_pool.register(EventIndustryEventsApphook)


class FilmBroadcastEventsApphook(CMSApp):
    name = _("Film & Broadcast - Events")
    urls = ["kb.apps.events.urls.film_broadcast"]

apphook_pool.register(FilmBroadcastEventsApphook)


class PhotographyEventsApphook(CMSApp):
    name = _("Photography - Events")
    urls = ["kb.apps.events.urls.photography"]

apphook_pool.register(PhotographyEventsApphook)


class GamesInteractiveEventsApphook(CMSApp):
    name = _("Games & Interactive - Events")
    urls = ["kb.apps.events.urls.games_interactive"]

apphook_pool.register(GamesInteractiveEventsApphook)


class LiteraturePublishingEventsApphook(CMSApp):
    name = _("Literature & Publishing - Events")
    urls = ["kb.apps.events.urls.literature_publishing"]

apphook_pool.register(LiteraturePublishingEventsApphook)


class FashionTextileEventsApphook(CMSApp):
    name = _("Fashion & Textile - Events")
    urls = ["kb.apps.events.urls.fashion_textile"]

apphook_pool.register(FashionTextileEventsApphook)


class MusicEventsApphook(CMSApp):
    name = _("Music - Events")
    urls = ["kb.apps.events.urls.music"]

apphook_pool.register(MusicEventsApphook)


class TheatreDanceEventsApphook(CMSApp):
    name = _("Theatre & Dance - Events")
    urls = ["kb.apps.events.urls.theatre_dance"]

apphook_pool.register(TheatreDanceEventsApphook)


class AdvertisingPREventsApphook(CMSApp):
    name = _("Advertising & PR - Events")
    urls = ["kb.apps.events.urls.advertising_pr"]

apphook_pool.register(AdvertisingPREventsApphook)

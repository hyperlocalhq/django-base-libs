# -*- coding: UTF-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class NetworkApphook(CMSApp):
    name = _("Network")
    urls = ["ccb.apps.network.urls"]

apphook_pool.register(NetworkApphook)


class ArchitectureNetworkApphook(CMSApp):
    name = _("Architecture - Network")
    urls = ["ccb.apps.network.urls.architecture"]

apphook_pool.register(ArchitectureNetworkApphook)


class VisualArtsNetworkApphook(CMSApp):
    name = _("Visual Arts - Network")
    urls = ["ccb.apps.network.urls.visual_arts"]

apphook_pool.register(VisualArtsNetworkApphook)


class DesignNetworkApphook(CMSApp):
    name = _("Design - Network")
    urls = ["ccb.apps.network.urls.design"]

apphook_pool.register(DesignNetworkApphook)


class EventIndustryNetworkApphook(CMSApp):
    name = _("Event Industry - Network")
    urls = ["ccb.apps.network.urls.event_industry"]

apphook_pool.register(EventIndustryNetworkApphook)


class FilmBroadcastNetworkApphook(CMSApp):
    name = _("Film & Broadcast - Network")
    urls = ["ccb.apps.network.urls.film_broadcast"]

apphook_pool.register(FilmBroadcastNetworkApphook)


class PhotographyNetworkApphook(CMSApp):
    name = _("Photography - Network")
    urls = ["ccb.apps.network.urls.photography"]

apphook_pool.register(PhotographyNetworkApphook)


class GamesInteractiveNetworkApphook(CMSApp):
    name = _("Games & Interactive - Network")
    urls = ["ccb.apps.network.urls.games_interactive"]

apphook_pool.register(GamesInteractiveNetworkApphook)


class LiteraturePublishingNetworkApphook(CMSApp):
    name = _("Literature & Publishing - Network")
    urls = ["ccb.apps.network.urls.literature_publishing"]

apphook_pool.register(LiteraturePublishingNetworkApphook)


class FashionTextileNetworkApphook(CMSApp):
    name = _("Fashion & Textile - Network")
    urls = ["ccb.apps.network.urls.fashion_textile"]

apphook_pool.register(FashionTextileNetworkApphook)


class MusicNetworkApphook(CMSApp):
    name = _("Music - Network")
    urls = ["ccb.apps.network.urls.music"]

apphook_pool.register(MusicNetworkApphook)


class TheatreDanceNetworkApphook(CMSApp):
    name = _("Theatre & Dance - Network")
    urls = ["ccb.apps.network.urls.theatre_dance"]

apphook_pool.register(TheatreDanceNetworkApphook)


class AdvertisingPRNetworkApphook(CMSApp):
    name = _("Advertising & PR - Network")
    urls = ["ccb.apps.network.urls.advertising_pr"]

apphook_pool.register(AdvertisingPRNetworkApphook)

# -*- coding: UTF-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class MarketplaceAppHook(CMSApp):
    name = _("Job Offers")
    urls = ["ccb.apps.marketplace.urls"]

apphook_pool.register(MarketplaceAppHook)


class ArchitectureMarketplaceApphook(CMSApp):
    name = _("Architecture - Marketplace")
    urls = ["ccb.apps.marketplace.urls.architecture"]

apphook_pool.register(ArchitectureMarketplaceApphook)


class VisualArtsMarketplaceApphook(CMSApp):
    name = _("Visual Arts - Marketplace")
    urls = ["ccb.apps.marketplace.urls.visual_arts"]

apphook_pool.register(VisualArtsMarketplaceApphook)


class DesignMarketplaceApphook(CMSApp):
    name = _("Design - Marketplace")
    urls = ["ccb.apps.marketplace.urls.design"]

apphook_pool.register(DesignMarketplaceApphook)


class EventIndustryMarketplaceApphook(CMSApp):
    name = _("Event Industry - Marketplace")
    urls = ["ccb.apps.marketplace.urls.event_industry"]

apphook_pool.register(EventIndustryMarketplaceApphook)


class FilmBroadcastMarketplaceApphook(CMSApp):
    name = _("Film & Broadcast - Marketplace")
    urls = ["ccb.apps.marketplace.urls.film_broadcast"]

apphook_pool.register(FilmBroadcastMarketplaceApphook)


class PhotographyMarketplaceApphook(CMSApp):
    name = _("Photography - Marketplace")
    urls = ["ccb.apps.marketplace.urls.photography"]

apphook_pool.register(PhotographyMarketplaceApphook)


class GamesInteractiveMarketplaceApphook(CMSApp):
    name = _("Games & Interactive - Marketplace")
    urls = ["ccb.apps.marketplace.urls.games_interactive"]

apphook_pool.register(GamesInteractiveMarketplaceApphook)


class LiteraturePublishingMarketplaceApphook(CMSApp):
    name = _("Literature & Publishing - Marketplace")
    urls = ["ccb.apps.marketplace.urls.literature_publishing"]

apphook_pool.register(LiteraturePublishingMarketplaceApphook)


class FashionTextileMarketplaceApphook(CMSApp):
    name = _("Fashion & Textile - Marketplace")
    urls = ["ccb.apps.marketplace.urls.fashion_textile"]

apphook_pool.register(FashionTextileMarketplaceApphook)


class MusicMarketplaceApphook(CMSApp):
    name = _("Music - Marketplace")
    urls = ["ccb.apps.marketplace.urls.music"]

apphook_pool.register(MusicMarketplaceApphook)


class TheatreDanceMarketplaceApphook(CMSApp):
    name = _("Theatre & Dance - Marketplace")
    urls = ["ccb.apps.marketplace.urls.theatre_dance"]

apphook_pool.register(TheatreDanceMarketplaceApphook)


class AdvertisingPRMarketplaceApphook(CMSApp):
    name = _("Advertising & PR - Marketplace")
    urls = ["ccb.apps.marketplace.urls.advertising_pr"]

apphook_pool.register(AdvertisingPRMarketplaceApphook)

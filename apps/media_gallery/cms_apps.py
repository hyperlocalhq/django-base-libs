# -*- coding: UTF-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class MediaGalleryAppHook(CMSApp):
    name = _("Portfolios")
    urls = ["ccb.apps.media_gallery.urls"]

apphook_pool.register(MediaGalleryAppHook)



class ArchitectureMediaGalleryApphook(CMSApp):
    name = _("Architecture - Portfolios")
    urls = ["ccb.apps.media_gallery.urls.architecture"]

apphook_pool.register(ArchitectureMediaGalleryApphook)


class VisualArtsMediaGalleryApphook(CMSApp):
    name = _("Visual Arts - Portfolios")
    urls = ["ccb.apps.media_gallery.urls.visual_arts"]

apphook_pool.register(VisualArtsMediaGalleryApphook)


class DesignMediaGalleryApphook(CMSApp):
    name = _("Design - Portfolios")
    urls = ["ccb.apps.media_gallery.urls.design"]

apphook_pool.register(DesignMediaGalleryApphook)


class EventIndustryMediaGalleryApphook(CMSApp):
    name = _("Event Industry - Portfolios")
    urls = ["ccb.apps.media_gallery.urls.event_industry"]

apphook_pool.register(EventIndustryMediaGalleryApphook)


class FilmBroadcastMediaGalleryApphook(CMSApp):
    name = _("Film & Broadcast - Portfolios")
    urls = ["ccb.apps.media_gallery.urls.film_broadcast"]

apphook_pool.register(FilmBroadcastMediaGalleryApphook)


class PhotographyMediaGalleryApphook(CMSApp):
    name = _("Photography - Portfolios")
    urls = ["ccb.apps.media_gallery.urls.photography"]

apphook_pool.register(PhotographyMediaGalleryApphook)


class GamesInteractiveMediaGalleryApphook(CMSApp):
    name = _("Games & Interactive - Portfolios")
    urls = ["ccb.apps.media_gallery.urls.games_interactive"]

apphook_pool.register(GamesInteractiveMediaGalleryApphook)


class LiteraturePublishingMediaGalleryApphook(CMSApp):
    name = _("Literature & Publishing - Portfolios")
    urls = ["ccb.apps.media_gallery.urls.literature_publishing"]

apphook_pool.register(LiteraturePublishingMediaGalleryApphook)


class FashionTextileMediaGalleryApphook(CMSApp):
    name = _("Fashion & Textile - Portfolios")
    urls = ["ccb.apps.media_gallery.urls.fashion_textile"]

apphook_pool.register(FashionTextileMediaGalleryApphook)


class MusicMediaGalleryApphook(CMSApp):
    name = _("Music - Portfolios")
    urls = ["ccb.apps.media_gallery.urls.music"]

apphook_pool.register(MusicMediaGalleryApphook)


class TheatreDanceMediaGalleryApphook(CMSApp):
    name = _("Theatre & Dance - Portfolios")
    urls = ["ccb.apps.media_gallery.urls.theatre_dance"]

apphook_pool.register(TheatreDanceMediaGalleryApphook)


class AdvertisingPRMediaGalleryApphook(CMSApp):
    name = _("Advertising & PR - Portfolios")
    urls = ["ccb.apps.media_gallery.urls.advertising_pr"]

apphook_pool.register(AdvertisingPRMediaGalleryApphook)

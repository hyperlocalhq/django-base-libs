# -*- coding: UTF-8 -*-

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class BulletinBoardApphook(CMSApp):
    name = _("Bulletin Board")
    urls = ["ccb.apps.bulletin_board.urls"]

apphook_pool.register(BulletinBoardApphook)


class ArchitectureBulletinBoardApphook(CMSApp):
    name = _("Architecture - Bulletin Board")
    urls = ["ccb.apps.bulletin_board.urls.architecture"]

apphook_pool.register(ArchitectureBulletinBoardApphook)


class VisualArtsBulletinBoardApphook(CMSApp):
    name = _("Visual Arts - Bulletin Board")
    urls = ["ccb.apps.bulletin_board.urls.visual_arts"]

apphook_pool.register(VisualArtsBulletinBoardApphook)


class DesignBulletinBoardApphook(CMSApp):
    name = _("Design - Bulletin Board")
    urls = ["ccb.apps.bulletin_board.urls.design"]

apphook_pool.register(DesignBulletinBoardApphook)


class EventIndustryBulletinBoardApphook(CMSApp):
    name = _("Event Industry - Bulletin Board")
    urls = ["ccb.apps.bulletin_board.urls.event_industry"]

apphook_pool.register(EventIndustryBulletinBoardApphook)


class FilmBroadcastBulletinBoardApphook(CMSApp):
    name = _("Film & Broadcast - Bulletin Board")
    urls = ["ccb.apps.bulletin_board.urls.film_broadcast"]

apphook_pool.register(FilmBroadcastBulletinBoardApphook)


class PhotographyBulletinBoardApphook(CMSApp):
    name = _("Photography - Bulletin Board")
    urls = ["ccb.apps.bulletin_board.urls.photography"]

apphook_pool.register(PhotographyBulletinBoardApphook)


class GamesInteractiveBulletinBoardApphook(CMSApp):
    name = _("Games & Interactive - Bulletin Board")
    urls = ["ccb.apps.bulletin_board.urls.games_interactive"]

apphook_pool.register(GamesInteractiveBulletinBoardApphook)


class LiteraturePublishingBulletinBoardApphook(CMSApp):
    name = _("Literature & Publishing - Bulletin Board")
    urls = ["ccb.apps.bulletin_board.urls.literature_publishing"]

apphook_pool.register(LiteraturePublishingBulletinBoardApphook)


class FashionTextileBulletinBoardApphook(CMSApp):
    name = _("Fashion & Textile - Bulletin Board")
    urls = ["ccb.apps.bulletin_board.urls.fashion_textile"]

apphook_pool.register(FashionTextileBulletinBoardApphook)


class MusicBulletinBoardApphook(CMSApp):
    name = _("Music - Bulletin Board")
    urls = ["ccb.apps.bulletin_board.urls.music"]

apphook_pool.register(MusicBulletinBoardApphook)


class TheatreDanceBulletinBoardApphook(CMSApp):
    name = _("Theatre & Dance - Bulletin Board")
    urls = ["ccb.apps.bulletin_board.urls.theatre_dance"]

apphook_pool.register(TheatreDanceBulletinBoardApphook)


class AdvertisingPRBulletinBoardApphook(CMSApp):
    name = _("Advertising & PR - Bulletin Board")
    urls = ["ccb.apps.bulletin_board.urls.advertising_pr"]

apphook_pool.register(AdvertisingPRBulletinBoardApphook)

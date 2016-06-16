# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from cms.extensions import TitleExtension
from cms.extensions.extension_pool import extension_pool

from filebrowser.fields import FileBrowseField


OG_TYPE_CHOICES = (
    ("article", "article"),
    ("books.author", "books.author"),
    ("books.book", "books.book"),
    ("books.genre", "books.genre"),
    ("business.business", "business.business"),
    ("fitness.course", "fitness.course"),
    ("game.achievement", "game.achievement"),
    ("music.album", "music.album"),
    ("music.playlist", "music.playlist"),
    ("music.radio_station", "music.radio_station"),
    ("music.song", "music.song"),
    ("place", "place"),
    ("product", "product"),
    ("product.group", "product.group"),
    ("product.item", "product.item"),
    ("profile", "profile"),
    ("restaurant.menu", "restaurant.menu"),
    ("restaurant.menu_item", "restaurant.menu_item"),
    ("restaurant.menu_section", "restaurant.menu_section"),
    ("restaurant.restaurant", "restaurant.restaurant"),
    ("video.episode", "video.episode"),
    ("video.movie", "video.movie"),
    ("video.other", "video.other"),
    ("video.tv_show", "video.tv_show"),
    ("website", "website"),
)

OPEN_GRAPH_LOCALE_MAPPER = getattr(settings, "OPEN_GRAPH_LOCALE_MAPPER", {"en": "en_US"})


class OpenGraph(TitleExtension):
    og_title = models.CharField(_("Title"), blank=True, max_length=255)
    og_description = models.TextField(_("Description"), blank=True, help_text=_("No HTML and no new lines"))
    og_image = FileBrowseField(verbose_name=_("Image"), max_length=255, extensions=['.jpg', '.jpeg', '.gif', '.png'], blank=True)
    og_type = models.CharField(_("Type"), max_length=20, default="article", choices=OG_TYPE_CHOICES)

    class Meta:
        verbose_name = verbose_name_plural = _("Open Graph for Social Sharing")

    def __unicode__(self):
        return self.og_title or _("(untitled)")


extension_pool.register(OpenGraph)


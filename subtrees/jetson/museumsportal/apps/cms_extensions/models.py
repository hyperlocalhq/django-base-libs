# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from base_libs.middleware.threadlocals import get_current_language

from cms.models import Page
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


class CMSPageOpenGraph(models.Model):
    page = models.ForeignKey(Page, verbose_name=_("Page"), related_name='open_graph')
    og_title = models.CharField(_("Title"), blank=True, max_length=255)
    og_description = models.TextField(_("Description"), blank=True, help_text=_("No HTML and no new lines"))
    og_image = FileBrowseField(verbose_name=_("Image"), max_length=255, extensions=['.jpg', '.jpeg', '.gif', '.png'], blank=True)
    og_type = models.CharField(_("Type"), max_length=20, default="article", choices=OG_TYPE_CHOICES)
    language = models.CharField(_("Language"), max_length=5, default=settings.LANGUAGE_CODE, choices=settings.LANGUAGES)

    class Meta:
        verbose_name = verbose_name_plural = _("Open Graph for Social Sharing")

    def __unicode__(self):
        return self.og_title or _("(untitled)")

    def get_og_locale(self):
        return OPEN_GRAPH_LOCALE_MAPPER.get(self.language, "en_US")


def _get_open_graph_settings(self):
    lang_code = get_current_language()
    og_settings = self.publisher_draft.open_graph.filter(language=lang_code)
    if og_settings.count():
        return og_settings[0]
    return None

Page.open_graph_settings = _get_open_graph_settings
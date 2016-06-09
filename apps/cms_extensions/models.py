# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

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

OG_LOCALE_CHOICES = getattr(settings, "OPEN_GRAPH_LOCALE_CHOICES", (("en_US", "en_US"),))


class CMSPageOpenGraph(models.Model):
    page = models.OneToOneField("cms.Page", verbose_name=_("Page"), related_name='open_graph')
    og_title = models.CharField(_("Title"), blank=True, max_length=255)
    og_description = models.TextField(_("Description"), blank=True, help_text=_("No HTML and no new lines"))
    og_image = FileBrowseField(verbose_name=_("Image"), max_length=255, extensions=['.jpg', '.jpeg', '.gif', '.png'], blank=True)
    og_type = models.CharField(_("Type"), max_length=20, default="article", choices=OG_TYPE_CHOICES)
    og_locale = models.CharField(_("Locale"), max_length=5, default=OG_LOCALE_CHOICES[0][0], choices=OG_LOCALE_CHOICES)

    class Meta:
        verbose_name = verbose_name_plural = _("Open Graph for Social Sharing")

    def __unicode__(self):
        return self.og_title or _("(untitled)")


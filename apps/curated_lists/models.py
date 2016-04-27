# -*- coding: UTF-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import get_language, activate
from django.conf import settings

from base_libs.models.models import CreationModificationDateMixin, SlugMixin, ObjectRelationMixin, UrlMixin
from base_libs.models.fields import MultilingualCharField

verbose_name = _("Curated Lists")

PRIVACY_CHOICES = (
    ("private", _("Private")),
    ("public", _("Public")),
)


class CuratedList(CreationModificationDateMixin, SlugMixin(unique=False)):
    owner = models.ForeignKey("auth.User", verbose_name=_("Owner"), blank=True, null=True)
    title = MultilingualCharField(_("Title"), max_length=255)
    sort_order = models.IntegerField(_("Sort order"), blank=True, default=0)
    privacy = models.CharField(_("Privacy"), max_length=20, choices=PRIVACY_CHOICES, default="public")

    class Meta:
        verbose_name = _("Curated List")
        verbose_name_plural = _("Curated Lists")
        ordering = ["sort_order"]

    def __unicode__(self):
        return self.title


limit_content_type_choices_to = (
    models.Q(app_label="articles", model="article") |
    models.Q(app_label="blog", model="post") |
    models.Q(app_label="bulletin_board", model="bulletin") |
    models.Q(app_label="events", model="event") |
    models.Q(app_label="institutions", model="institution") |
    models.Q(app_label="marketplace", model="joboffer") |
    models.Q(app_label="people", model="person")
)

class ListItem(CreationModificationDateMixin, ObjectRelationMixin(limit_content_type_choices_to=limit_content_type_choices_to), UrlMixin):
    curated_list = models.ForeignKey(CuratedList, verbose_name=_("Curated list"))
    representation = MultilingualCharField(_("Representation"), max_length=255, blank=True)
    sort_order = models.IntegerField(_("Sort order"), blank=True, default=0)

    class Meta:
        verbose_name = _("List Item")
        verbose_name_plural = _("List Items")
        ordering = ["sort_order"]

    def __unicode__(self):
        return self.representation

    def get_url_path(self):
        if self.content_object:
            return self.content_object.get_url_path()
        return ""

    def save(self, *args, **kwargs):
        current_language = get_language()
        for lang_code, lang_name in settings.LANGUAGES:
            activate(lang_code)
            setattr(self, 'representation_{}'.format(lang_code), unicode(self.content_object))
        activate(current_language)
        super(ListItem, self).save(*args, **kwargs)

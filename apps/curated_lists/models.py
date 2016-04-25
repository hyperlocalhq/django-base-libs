# -*- coding: UTF-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from base_libs.models.models import CreationModificationDateMixin, SlugMixin, ObjectRelationMixin, UrlMixin
from base_libs.models.fields import MultilingualCharField


class CuratedList(CreationModificationDateMixin, SlugMixin(unique=False)):
    owner = models.ForeignKey("auth.User", verbose_name=_("Owner"), blank=True, null=True)
    title = MultilingualCharField(_("Title"), max_length=255)
    sort_order = models.IntegerField(_("Sort order"), blank=True, default=0)

    class Meta:
        verbose_name = _("curated list")
        verbose_name_plural = _("curated lists")
        ordering = ["sort_order"]

    def __unicode__(self):
        return self.title


class ListItem(CreationModificationDateMixin, ObjectRelationMixin(), UrlMixin):
    curated_list = models.ForeignKey(CuratedList, verbose_name=_("Curated list"))
    representation = MultilingualCharField(_("Representation"), max_length=255)
    sort_order = models.IntegerField(_("Sort order"), blank=True, default=0)

    class Meta:
        verbose_name = _("curated list")
        verbose_name_plural = _("curated lists")
        ordering = ["sort_order"]

    def __unicode__(self):
        return self.representation

    def get_url_path(self):
        if self.content_object:
            return self.content_object.get_url_path()
        return ""

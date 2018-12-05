# -*- coding: UTF-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from django.utils import timezone

from base_libs.models import SysnameMixin
from base_libs.models import PublishingMixin
from base_libs.models.fields import PositionField
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualTextField

from filebrowser.fields import FileBrowseField

verbose_name = _("Slideshows")


class Slideshow(SysnameMixin()):
    class Meta:
        verbose_name = _("slideshow")
        verbose_name_plural = _("slideshows")
        ordering = ['sysname']

    def __unicode__(self):
        return self.sysname


class Slide(PublishingMixin, models.Model):
    slideshow = models.ForeignKey(
        Slideshow, verbose_name=_("Slideshow"), default=0
    )
    path = FileBrowseField(
        _('File path'),
        max_length=255,
        blank=True,
        directory="slideshows/",
        help_text=_("A path to a locally stored image or video.")
    )
    link = models.CharField(_('Link'), max_length=255, blank=True)
    alt = MultilingualCharField(
        _("Alternative text"), max_length=100, blank=True
    )
    title = MultilingualTextField(_("Title"), blank=True)
    subtitle = MultilingualTextField(_("Subtitle"), blank=True)
    credits = MultilingualCharField(
        _("Photo credits"), max_length=255, blank=True
    )
    highlight = models.BooleanField(_("Highlight"), default=False)
    sort_order = PositionField(_("Sort order"), collection="slideshow")

    class Meta:
        verbose_name = _("slide")
        verbose_name_plural = _("slides")
        ordering = ['sort_order']

    def __unicode__(self):
        return u"{} ({})".format(
            unicode(self.path),
            ugettext("Shown now")
            if self.is_shown_now() else ugettext("Not shown now")
        )

    def is_shown_now(self):
        now = timezone.now()
        if self.published_from and now < self.published_from:
            return False
        if self.published_till and self.published_till < now:
            return False
        return True

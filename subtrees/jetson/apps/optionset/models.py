# -*- coding: UTF-8 -*-
import sys

from django.db import models

if "makemigrations" in sys.argv:
    from django.utils.translation import ugettext_noop as _
else:
    from django.utils.translation import ugettext_lazy as _

from base_libs.models.models import SlugMixin
from base_libs.models.fields import MultilingualCharField

verbose_name = _("Option Set")

GENDER_CHOICES = (('M', _('Male')), ('F', _('Female')))


class Prefix(SlugMixin()):

    title = MultilingualCharField(_('title'), max_length=255)
    sort_order = models.IntegerField(_("Sort order"), default=0)
    gender = models.CharField(
        _("Gender"), max_length=32, choices=GENDER_CHOICES, blank=True
    )

    class Meta:
        verbose_name = _("prefix")
        verbose_name_plural = _("prefixes")
        ordering = ['sort_order', 'title']

    def __unicode__(self):
        return self.title

    def get_title(self):
        return self.title


class Salutation(SlugMixin()):
    title = MultilingualCharField(_('title'), max_length=255)
    template = MultilingualCharField(
        _('template'),
        max_length=255,
        help_text=_("takes the person as {{ person }} variable")
    )
    sort_order = models.IntegerField(_("Sort Order"), default=0)

    class Meta:
        verbose_name = _("salutation")
        verbose_name_plural = _("salutations")
        ordering = ['sort_order', 'title']

    def __unicode__(self):
        return self.title

    def get_title(self):
        return self.title


class IndividualLocationType(SlugMixin()):
    title = MultilingualCharField(_('title'), max_length=255)
    sort_order = models.IntegerField(_("Sort order"), default=0)

    class Meta:
        verbose_name = _("individual location type")
        verbose_name_plural = _("individual location types")
        ordering = ['sort_order', 'title']

    def __unicode__(self):
        return self.title

    def get_title(self):
        return self.title


class InstitutionalLocationType(SlugMixin()):
    title = MultilingualCharField(_('title'), max_length=255)
    sort_order = models.IntegerField(_("Sort order"), default=0)

    class Meta:
        verbose_name = _("institutional location type")
        verbose_name_plural = _("institutional location types")
        ordering = ['sort_order', 'title']

    def __unicode__(self):
        return self.title

    def get_title(self):
        return self.title


class PhoneType(SlugMixin()):
    title = MultilingualCharField(_('title'), max_length=255)
    vcard_name = models.CharField(_("vCard Name"), blank=True, max_length=255)
    sort_order = models.IntegerField(_("Sort order"), default=0)

    class Meta:
        verbose_name = _("phone type")
        verbose_name_plural = _("phone types")
        ordering = ['sort_order', 'title']

    def __unicode__(self):
        return self.title

    def get_title(self):
        return self.title


def get_default_phonetype_for_phone():
    retval = None
    try:
        retval = PhoneType.objects.get(slug='phone').id
    except (PhoneType.DoesNotExist, PhoneType.MultipleObjectsReturned):
        pass
    return retval


def get_default_phonetype_for_fax():
    retval = None
    try:
        retval = PhoneType.objects.get(slug='fax').id
    except (PhoneType.DoesNotExist, PhoneType.MultipleObjectsReturned):
        pass
    return retval


def get_default_phonetype_for_mobile():
    retval = None
    try:
        retval = PhoneType.objects.get(slug='mobile').id
    except (PhoneType.DoesNotExist, PhoneType.MultipleObjectsReturned):
        pass
    return retval


class EmailType(SlugMixin()):
    title = MultilingualCharField(_('title'), max_length=255)
    sort_order = models.IntegerField(_("Sort order"), default=0)

    class Meta:
        verbose_name = _("email type")
        verbose_name_plural = _("email types")
        ordering = ['sort_order', 'title']

    def __unicode__(self):
        return self.title

    def get_title(self):
        return self.title


class URLType(SlugMixin()):
    title = MultilingualCharField(_('title'), max_length=255)
    sort_order = models.IntegerField(_("Sort order"), default=0)

    class Meta:
        verbose_name = _("url type")
        verbose_name_plural = _("url types")
        ordering = ['sort_order', 'title']

    def __unicode__(self):
        return self.title

    def get_title(self):
        return self.title


class IMType(SlugMixin()):
    title = MultilingualCharField(_('title'), max_length=255)
    sort_order = models.IntegerField(_("Sort order"), default=0)

    class Meta:
        verbose_name = _("instant messenger type")
        verbose_name_plural = _("instant messenger types")
        ordering = ['sort_order', 'title']

    def __unicode__(self):
        return self.title

    def get_title(self):
        return self.title

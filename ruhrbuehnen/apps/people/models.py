# -*- coding: UTF-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from base_libs.models.models import SlugMixin
from base_libs.models.models import CreationModificationMixin
from base_libs.models.models import CreationModificationDateMixin
from base_libs.models.fields import MultilingualCharField

from mptt.models import MPTTModel

STATUS_CHOICES = (
    ('draft', _("Draft")),
    ('published', _("Published")),
    ('not_listed', _("Not Listed")),
    ('import', _("Imported")),
    ('trashed', _("Trashed")),
)
GENDER_CHOICES = (('M', _('Male')), ('F', _('Female')))


class Prefix(SlugMixin()):

    title = MultilingualCharField(_('title'), max_length=255)
    sort_order = models.IntegerField(_("Sort order"), default=0)
    gender = models.CharField(
        _("Gender"), max_length=32, choices=GENDER_CHOICES, blank=True
    )

    class Meta:
        verbose_name = _("Prefix")
        verbose_name_plural = _("Prefixes")
        ordering = ['sort_order']

    def __unicode__(self):
        return self.title


class InvolvementType(SlugMixin()):
    title = MultilingualCharField(_('title'), max_length=255)
    sort_order = models.IntegerField(_("Sort order"), default=0)

    class Meta:
        verbose_name = _("Involvement type")
        verbose_name_plural = _("Involvement types")
        ordering = ['sort_order']

    def __unicode__(self):
        return self.title


class AuthorshipType(SlugMixin()):
    title = MultilingualCharField(_('title'), max_length=255)
    sort_order = models.IntegerField(_("Sort order"), default=0)

    class Meta:
        verbose_name = _("Authorship type")
        verbose_name_plural = _("Authorship types")
        ordering = ['sort_order']

    def __unicode__(self):
        return self.title


class PersonManager(models.Manager):
    def get_first_or_create(self, **kwargs):
        try:
            return self.get_or_create(**kwargs)
        except self.model.MultipleObjectsReturned:
            defaults = kwargs.pop('defaults', {})
            return self.filter(**kwargs)[0], False


class Person(
    CreationModificationMixin,
    SlugMixin(prepopulate_from=("first_name", "last_name"))
):
    prefix = models.ForeignKey(
        Prefix, verbose_name=_("Prefix"), null=True, blank=True
    )
    first_name = models.CharField(_('First name'), max_length=255, blank=True)
    last_name = models.CharField(_('Last name'), max_length=255, blank=True)

    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=STATUS_CHOICES,
        blank=True,
        default="draft"
    )

    objects = PersonManager()

    class Meta:
        verbose_name = _("person")
        verbose_name_plural = _("people")
        ordering = ['last_name', 'first_name']

    def __unicode__(self):
        return (self.first_name + ' ' + self.last_name).strip()

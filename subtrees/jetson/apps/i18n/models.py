# -*- coding: utf-8 -*-
# Copyright (c) 2006, Jonás Melián
# Licensed under New BSD. Read the LICENSE file
import sys

if "makemigrations" in sys.argv:
    from django.utils.translation import ugettext_noop as _
else:
    from django.utils.translation import ugettext_lazy as _

from django.db import models
from django.conf import settings
from django.utils.encoding import force_unicode

from base_libs.middleware import get_current_language

verbose_name = _("Internationalization")

CONTINENT = (
    ('af', _('Africa')),
    ('am', _('America')),
    ('e', _('Europe')),
    ('as', _('Asia')),
    ('o', _('Oceania')),
)

REGION = (
    ('af.e', _('Eastern Africa')),
    ('af.m', _('Middle Africa')),
    ('af.n', _('Northern Africa')),
    ('af.s', _('Southern Africa')),
    ('af.w', _('Western Africa')),
    ('am.ca', _('Caribbean')),
    ('am.c', _('Central America')),
    ('am.s', _('South America')),
    ('am.n', _('Northern America')),
    ('as.c', _('Central Asia')),
    ('as.e', _('Eastern Asia')),
    ('as.s', _('Southern Asia')),
    ('as.se', _('South-Eastern Asia')),
    ('as.w', _('Western Asia')),
    ('e.e', _('Eastern Europe')),
    ('e.n', _('Northern Europe')),
    ('e.s', _('Southern Europe')),
    ('e.w', _('Western Europe')),
    ('o.a', _('Australia and New Zealand')),
    ('o.me', _('Melanesia')),
    ('o.mi', _('Micronesia')),
    ('o.p', _('Polynesia')),
)

AREA = (
    ('a', _('Another')),
    ('i', _('Island')),
    ('ar', _('Arrondissement')),
    ('at', _('Atoll')),
    ('ai', _('Autonomous island')),
    ('ca', _('Canton')),
    ('cm', _('Commune')),
    ('co', _('County')),
    ('dp', _('Department')),
    ('de', _('Dependency')),
    ('dt', _('District')),
    ('dv', _('Division')),
    ('em', _('Emirate')),
    ('gv', _('Governorate')),
    ('ic', _('Island council')),
    ('ig', _('Island group')),
    ('ir', _('Island region')),
    ('kd', _('Kingdom')),
    ('mu', _('Municipality')),
    ('pa', _('Parish')),
    ('pf', _('Prefecture')),
    ('pr', _('Province')),
    ('rg', _('Region')),
    ('rp', _('Republic')),
    ('sh', _('Sheading')),
    ('st', _('State')),
    ('sd', _('Subdivision')),
    ('sj', _('Subject')),
    ('ty', _('Territory')),
)

LANGUAGE_TYPES = (
    ('o', _('official')),
    ('n', _('national')),
    ('r', _('regional')),
    ('f', _('de facto')),
    ('j', _('de jure')),
    ('l', _('legislative')),
    ('b', _('business')),
)


class Language(models.Model):
    """Languages more common.
    'synonym' field is used for some languages that are called with
    another name too.
    """
    iso3_code = models.CharField(_('Alpha-3 ISO Code'), max_length=3)
    name = models.CharField(
        _('Language Name (English)'), max_length=40, unique=True
    )
    name_de = models.CharField(
        _('Language Name (German)'), max_length=40, blank=True
    )
    iso2_code = models.CharField(
        _('Alpha-2 ISO Code'), max_length=2, blank=True
    )
    synonym = models.CharField(_('Language Synonym'), max_length=40, blank=True)
    display = models.BooleanField(
        _('Display'),
        default=False,
        help_text=_('Designates whether the language is shown.')
    )
    sort_order = models.PositiveIntegerField(_('Sort order'), default=20)

    class Meta:
        verbose_name = _('language')
        verbose_name_plural = _('languages')
        ordering = ['sort_order', 'name']

    def __unicode__(self):
        return self.get_name()

    def get_name(self, language=None):
        language = language or get_current_language()
        return getattr(self, "name_%s" % language, "") or self.name

    def get_title(self, language=None):
        language = language or get_current_language()
        return getattr(self, "name_%s" % language, "") or self.name


class Nationality(models.Model):
    name = models.CharField(
        _('Nationality Name (English)'), max_length=40, unique=True
    )
    name_de = models.CharField(
        _('Nationality Name (German)'), max_length=40, blank=True
    )
    display = models.BooleanField(
        _('Display'),
        default=False,
        help_text=_('Designates whether the language is shown.')
    )
    sort_order = models.PositiveIntegerField(_('Sort order'), default=20)

    class Meta:
        verbose_name = _('nationality')
        verbose_name_plural = _('nationalities')
        ordering = ['sort_order', 'name']

    def __unicode__(self):
        return self.get_name()

    def get_name(self, language=None):
        language = language or get_current_language()
        return getattr(self, "name_%s" % language, "") or self.name


class Country(models.Model):
    """Country or territory.

iso2_code and iso3_code are ISO 3166-1 codes.
    """
    name = models.CharField(
        _('Country Name (English)'), max_length=56, unique=True
    )
    name_de = models.CharField(
        _('Country Name (German)'), max_length=56, blank=True
    )
    iso3_code = models.CharField(_('Alpha-3 ISO Code'), max_length=3)
    iso2_code = models.CharField(
        _('Alpha-2 ISO Code'), max_length=2, unique=True, primary_key=True
    )
    region = models.CharField(
        _('Geographical Region'), max_length=5, choices=REGION
    )
    territory_of = models.CharField(_('Territory of'), max_length=3, blank=True)
    adm_area = models.CharField(
        _('Administrative Area'), max_length=2, choices=AREA, blank=True
    )
    display = models.BooleanField(
        _('Display'),
        default=True,
        help_text=_('Designates whether the country is shown.')
    )
    sort_order = models.PositiveIntegerField(_('Sort Order'), default=20)

    class Meta:
        verbose_name = _('country')
        verbose_name_plural = _('countries')
        ordering = ['sort_order', 'name']

    def __unicode__(self):
        return self.get_name()

    def get_name(self, language=None):
        language = language or get_current_language()
        return getattr(self, "name_%s" % language, "") or self.name

    def get_title(self, language=None):
        language = language or get_current_language()
        return getattr(self, "name_%s" % language, "") or self.name

    def _get_name(self):
        return "%s (%s)" % (self.name, self.iso3_code)

    country_id = property(_get_name)


class CountryLanguage(models.Model):
    """Countries with its languages.
    """
    country = models.ForeignKey(Country)
    language = models.ForeignKey(Language)
    lang_type = models.CharField(
        _('language type'), max_length=1, choices=LANGUAGE_TYPES, blank=True
    )
    identifier = models.CharField(
        _('identifier'), max_length=6, primary_key=True
    )

    class Meta:
        verbose_name = _('country & language')
        verbose_name_plural = _('countries & languages')
        ordering = ['country']

    def __unicode__(self):
        try:
            return " - ".join(
                (
                    force_unicode(self.country),
                    force_unicode(self.language),
                )
            )
        except:
            return "(broken; id=%s)" % self.identifier


class Area(models.Model):
    """Top-level area division in the country, such as
state, district, province, island, region, etc.

In some countries is necessary for the mail address.
In others it is omitted, and in others it is either optional,
or needed in some cases but omitted in others.
    """
    country = models.ForeignKey(Country)
    name_id = models.CharField(
        _('name identifier'), max_length=6, primary_key=True
    )
    name = models.CharField(_('area name'), max_length=50)
    alt_name = models.CharField(
        _('area alternate name'), max_length=50, blank=True
    )
    abbrev = models.CharField(
        _('postal abbreviation'), max_length=3, blank=True
    )
    reg_area = models.CharField(
        _('regional administrative area'),
        max_length=1,
        choices=AREA,
        blank=True
    )

    class Meta:
        verbose_name = _('area')
        verbose_name_plural = _('areas')
        ordering = ['country']
        unique_together = (('country', 'name'), )

    def __unicode__(self):
        if self.abbrev:
            return "%s (%s)" % (self.abbrev, self.name)
        else:
            return self.name


class TimeZone(models.Model):
    """The time zones for each country or territory.
    """
    country = models.ForeignKey(Country)
    zone = models.CharField(_('time zone'), max_length=32, unique=True)

    class Meta:
        verbose_name = _('time zone')
        verbose_name_plural = _('time zones')
        ordering = ['zone']

    def __unicode__(self):
        return self.zone


class Phone(models.Model):
    """Information related to phones as country code, lengths, and prefixes.
    """
    country = models.ForeignKey(Country)
    code = models.PositiveSmallIntegerField(
        _('country code'), null=True, blank=True
    )
    ln_area = models.CharField(
        _('length of area code'), max_length=10, blank=True
    )
    ln_sn = models.CharField(
        _('length of subscriber number (SN)'), max_length=8, blank=True
    )
    ln_area_sn = models.CharField(
        _('length of area code and SN'), max_length=8, blank=True
    )
    nat_prefix = models.CharField(
        _('national prefix'), max_length=2, blank=True
    )
    int_prefix = models.CharField(
        _('international prefix'), max_length=4, blank=True
    )

    class Meta:
        verbose_name = _('phone')
        verbose_name_plural = _('phones')
        ordering = ['country']

    def __unicode__(self):
        return u"%s %s" % (self.country, self.code)

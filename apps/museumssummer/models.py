# -*- coding: UTF-8 -*-
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from base_libs.models.models import UrlMixin
from base_libs.models.models import CreationModificationDateMixin
from base_libs.models.models import OpeningHoursMixin
from base_libs.models.models import SlugMixin
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualTextField

from filebrowser.fields import FileBrowseField

COUNTRY_CHOICES = (
    ('de', _("Germany")),
    ('-', "Other"),
)

STATUS_CHOICES = (
    ('draft', _("Draft")),
    ('published', _("Published")),
    ('not_listed', _("Not Listed")),
    ('import', _("Imported")),
    ('trashed', _("Trashed")),
)


class Location(CreationModificationDateMixin, SlugMixin(), UrlMixin):
    title = MultilingualCharField(_("Name"), max_length=255)
    subtitle = MultilingualCharField(_("Subtitle"), max_length=255, blank=True)
    description = MultilingualTextField(_("Description"), blank=True)

    cover_image = FileBrowseField(
        _('Image'), max_length=255, directory="museumssommer/",
        extensions=['.jpg', '.jpeg', '.gif', '.png'], blank=True,
    )

    street_address = models.CharField(_("Street address"), max_length=255)
    street_address2 = models.CharField(_("Street address (second line)"), max_length=255, blank=True)
    postal_code = models.CharField(_("Postal code"), max_length=255)
    city = models.CharField(_("City"), default="Berlin", max_length=255)
    country = models.CharField(_("Country"), choices=COUNTRY_CHOICES, default='de', max_length=255)
    latitude = models.FloatField(_("Latitude"), help_text=_(
        "Latitude (Lat.) is the angle between any point and the equator (north pole is at 90; south pole is at -90)."),
                                 blank=True, null=True)
    longitude = models.FloatField(_("Longitude"), help_text=_(
        "Longitude (Long.) is the angle east or west of an arbitrary point on Earth from Greenwich (UK), which is the international zero-longitude point (longitude=0 degrees). The anti-meridian of Greenwich is both 180 (direction to east) and -180 (direction to west)."),
                                  blank=True, null=True)

    link_url = MultilingualCharField(_("Link URL"), max_length=255, blank=True, help_text=_("e.g.: /de/museen/akademie-der-kunste-pariser-platz/"))

    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, blank=True, default="draft")

    row_level_permissions = True

    def __unicode__(self):
        return self.title

    def is_location(self):
        return True

    class Meta:
        ordering = ['title']
        verbose_name = _("Museum Summer Location")
        verbose_name_plural = _("Museum Summer Locations")

    def get_url_path(self):
        try:
            path = reverse("location_detail", kwargs={'slug': self.slug})
        except:
            # the apphook is not attached yet
            return ""
        else:
            return path

    def get_address(self):
        return ", ".join(
            [
                getattr(self, fn)
                for fn in ["street_address", "street_address2", "postal_code", "city"]
                if getattr(self, fn)
            ]
        )

    get_address.short_description = _("Address")

    def get_opening_hours(self):
        WEEKDAYS = (
            ("mon", _("Monday")),
            ("tue", _("Tuesday")),
            ("wed", _("Wednesday")),
            ("thu", _("Thursday")),
            ("fri", _("Friday")),
            ("sat", _("Saturday")),
            ("sun", _("Sunday")),
        )
        times = []
        for key, val in WEEKDAYS:
            times.append({
                "weekday": val,
                "open": getattr(self, "%s_open" % key),
                "break_close": getattr(self, "%s_break_close" % key),
                "break_open": getattr(self, "%s_break_open" % key),
                "close": getattr(self, "%s_close" % key),
                "times": "-".join((
                    str(getattr(self, "%s_open" % key)),
                    str(getattr(self, "%s_break_close" % key)),
                    str(getattr(self, "%s_break_open" % key)),
                    str(getattr(self, "%s_close" % key))
                )),
            })
        return times

    def get_current_season(self):
        today = datetime.today().date()
        current_seasons = self.season_set.filter(
            start__lte=today,
            end__gte=today,
        )
        if current_seasons:
            return current_seasons[0]
        return None


class Season(OpeningHoursMixin):
    museum = models.ForeignKey(Location)
    title = MultilingualCharField(_('Season title'), max_length=255)
    start = models.DateField(_("Start"))
    end = models.DateField(_("End"))
    last_entry = MultilingualCharField(_("Last entry"), max_length=255, blank=True)

    def __unicode__(self):
        if self.start and self.end:
            return u"%s - %s" % (self.start.strftime('%Y-%m-%d'), self.end.strftime('%Y-%m-%d'))
        return u""

    class Meta:
        ordering = ('start',)
        verbose_name = _("Season")
        verbose_name_plural = _("Seasons")

    def get_opening_hours(self):
        WEEKDAYS = (
            ("mon", _("Monday")),
            ("tue", _("Tuesday")),
            ("wed", _("Wednesday")),
            ("thu", _("Thursday")),
            ("fri", _("Friday")),
            ("sat", _("Saturday")),
            ("sun", _("Sunday")),
        )
        times = []
        for key, val in WEEKDAYS:
            times.append({
                "weekday": val,
                "open": getattr(self, "%s_open" % key),
                "break_close": getattr(self, "%s_break_close" % key),
                "break_open": getattr(self, "%s_break_open" % key),
                "close": getattr(self, "%s_close" % key),
                "times": "-".join((
                    str(getattr(self, "%s_open" % key)),
                    str(getattr(self, "%s_break_close" % key)),
                    str(getattr(self, "%s_break_open" % key)),
                    str(getattr(self, "%s_close" % key))
                )),
            })
        return times

    def is_current(self):
        today = datetime.today().date()
        return self.start <= today <= self.end

    def is_open(self, selected_date):
        WEEKDAYS = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")
        if getattr(self, "%s_open" % WEEKDAYS[selected_date.weekday()]):
            return True
        return False

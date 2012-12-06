# -*- coding: utf-8 -*-

from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel
from mptt.managers import TreeManager
from mptt.fields import TreeForeignKey, TreeManyToManyField

from tagging.fields import TagField
from tagging.models import Tag
from tagging_autocomplete.models import TagAutocompleteField

from base_libs.models.models import OpeningHoursMixin
from base_libs.models.models import SlugMixin
from base_libs.models.models import CreationModificationMixin
from base_libs.models.models import CreationModificationDateMixin
from base_libs.models.models import UrlMixin
from base_libs.models.models import SlugMixin
from base_libs.models.fields import URLField
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualTextField

from jetson.apps.i18n.models import Language
from jetson.apps.utils.models import MONTH_CHOICES
from filebrowser.fields import FileBrowseField

from museumsportal.apps.museums.models import Museum
from museumsportal.apps.exhibitions.models import Exhibition

STATUS_CHOICES = (
    ('draft', _("Draft")),
    ('published', _("Published")),
    ('not_listed', _("Not Listed")),
    ('import', _("Imported")),
    ('expired', _("Expired")),
    )

COUNTRY_CHOICES = (
    ('de', _("Germany")),
    ('-', "Other"),
    )

YEAR_CHOICES = [(i,i) for i in range(1997, datetime.now().year+10)]

DAY_CHOICES = [(i,i) for i in range(1, 32)]

HOUR_CHOICES = [(i,i) for i in range(0, 24)]

MINUTE_CHOICES = [(i,"%02d" % i) for i in range(0, 60)]

class WorkshopCategory(MPTTModel, SlugMixin()):
    parent = TreeForeignKey(
       'self',
       #related_name="%(class)s_children",
       related_name="child_set",
       blank=True,
       null=True,
    )
    title = MultilingualCharField(_('title'), max_length=255)
    
    objects = TreeManager()
    
    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")
        ordering = ["tree_id", "lft"]
        
    class MPTTMeta:
        order_insertion_by = ['sort_order']
        
    def __unicode__(self):
        return self.title

    def get_title(self, prefix="", postfix=""):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            WorkshopCategory.objects.insert_node(self, self.parent)
        super(WorkshopCategory, self).save(*args, **kwargs)

class AgeGroup(CreationModificationDateMixin, SlugMixin()):
    title = MultilingualCharField(_('Title'), max_length=200)
    sort_order = models.IntegerField(_("Sort Order"), default=0)
    
    def __unicode__(self):
        return self.title
        
    class Meta:
        ordering = ['sort_order']
        verbose_name = _("Age group")
        verbose_name_plural = _("Age groups")


class Workshop(CreationModificationMixin, UrlMixin, SlugMixin()):
    title = MultilingualCharField(_("Title"), max_length=255)
    subtitle = MultilingualCharField(_("Subtitle"), max_length=255)
    description = MultilingualTextField(_("Description"), blank=True)
    image = FileBrowseField(_('Image'), max_length=200, directory="workshops/", extensions=['.jpg', '.jpeg', '.gif','.png','.tif','.tiff'], blank=True)
    
    workshop_date = models.DateField(_("Workshop date"), null=True, blank=True)
    start = models.TimeField(_("Start time"), null=True, blank=True)
    end = models.TimeField(_("End time"), null=True, blank=True)

    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, blank=True, default="draft")

    categories = TreeManyToManyField(WorkshopCategory, verbose_name=_("Categories"))
    tags = TagAutocompleteField(verbose_name=_("tags"))
    languages = models.ManyToManyField(Language, verbose_name=_("Languages"), blank=True, limit_choices_to={'display': True})
    other_languages = models.CharField(_("Other languages"), max_length=255, blank=True)
    age_groups = models.ManyToManyField(AgeGroup, verbose_name=_("Age groups"), blank=True)
    
    museum = models.ForeignKey(Museum, verbose_name=_("Museum"), blank=True, null=True)
    location_name = models.CharField(_("Location name"), max_length=255, blank=True)
    street_address = models.CharField(_("Street address"), max_length=255, blank=True)
    street_address2 = models.CharField(_("Street address (second line)"), max_length=255, blank=True)
    postal_code = models.CharField(_("Postal code"), max_length=255, blank=True)
    district = models.CharField(_("District"), max_length=255, blank=True)
    city =  models.CharField(_("City"), default="Berlin", max_length=255, blank=True)
    country = models.CharField(_("Country"), choices=COUNTRY_CHOICES, default='de', max_length=255, blank=True)    
    latitude = models.FloatField(_("Latitude"), help_text=_("Latitude (Lat.) is the angle between any point and the equator (north pole is at 90; south pole is at -90)."), blank=True, null=True)
    longitude = models.FloatField(_("Longitude"), help_text=_("Longitude (Long.) is the angle east or west of an arbitrary point on Earth from Greenwich (UK), which is the international zero-longitude point (longitude=0 degrees). The anti-meridian of Greenwich is both 180 (direction to east) and -180 (direction to west)."), blank=True, null=True)
    exhibition = models.ForeignKey(Exhibition, verbose_name=_("Related exhibition"), blank=True, null=True)

    meeting_place = MultilingualCharField(_("Meeting place"), max_length=255, blank=True)
    admission_price = models.DecimalField(_(u"Admission price (€)"), max_digits=5, decimal_places=2, blank=True, null=True)
    admission_price_info = MultilingualTextField(_("Admission price info"), blank=True)
    reduced_price = models.DecimalField(_(u"Reduced admission price (€)"), max_digits=5, decimal_places=2, blank=True, null=True)
    booking_info = MultilingualTextField(_("Booking info"), blank=True)

    class Meta:
        verbose_name = _("workshop")
        verbose_name_plural = _("workshops")
        ordering = ['title', 'creation_date']
        
    def __unicode__(self):
        return self.title


class WorkshopTime(models.Model):

    workshop = models.ForeignKey(Workshop, verbose_name=_("Workshop"))
    
    start_yyyy = models.IntegerField(_("Start Year"), choices=YEAR_CHOICES, default=datetime.now().year)
    start_mm = models.SmallIntegerField(_("Start Month"), blank=True, null=True, choices=MONTH_CHOICES)
    start_dd = models.SmallIntegerField(_("Start Day"), blank=True, null=True, choices=DAY_CHOICES)
    start_hh = models.SmallIntegerField(_("Start Hour"), blank=True, null=True, choices=HOUR_CHOICES)
    start_ii = models.SmallIntegerField(_("Start Minute"), blank=True, null=True, choices=MINUTE_CHOICES)
    start = models.DateTimeField(_("Start"), editable=False)
    
    end_yyyy = models.IntegerField(_("End Year"), choices=YEAR_CHOICES, blank=True, null=True,)
    end_mm = models.SmallIntegerField(_("End Month"), blank=True, null=True, choices=MONTH_CHOICES)
    end_dd = models.SmallIntegerField(_("End Day"), blank=True, null=True, choices=DAY_CHOICES)
    end_hh = models.SmallIntegerField(_("End Hour"), blank=True, null=True, choices=HOUR_CHOICES)
    end_ii = models.SmallIntegerField(_("End Minute"), blank=True, null=True, choices=MINUTE_CHOICES)
    end = models.DateTimeField(_("End"), editable=False)
    
    is_all_day = models.BooleanField(_("All Day Workshop"), default=False)

    class Meta:
        verbose_name = _("workshop time")
        verbose_name_plural = _("workshop times")
        ordering = ('start', )
        
    def __unicode__(self):
        return "%s - %s" % (
            self.start.strftime("%Y-%m-%d %H:%M"),
            self.end.strftime("%Y-%m-%d %H:%M"),
            )
        
    def save(self, *args, **kwargs):
        self.start = datetime(
            int(self.start_yyyy),
            int(self.start_mm or 1),
            int(self.start_dd or 1),
            int(self.start_hh or 0),
            int(self.start_ii or 0),
            )
        
        end_hh = self.end_hh
        if end_hh in ("", None):
            end_hh = (self.start_hh, 23)[self.start_hh in ("", None)]
            
        end_ii = self.end_ii
        if end_ii in ("", None):
            end_ii = (self.start_ii, 59)[self.start_ii in ("", None)]
        
        self.end = datetime(
            int(self.end_yyyy or self.start_yyyy),
            int(self.end_mm or self.start_mm or 12),
            int(self.end_dd or self.start_dd or calendar.monthrange(
                int(self.end_yyyy or self.start_yyyy),
                int(self.end_mm or self.start_mm or 12),
                )[1]),
            int(end_hh),
            int(end_ii),
            )
        
        super(WorkshopTime, self).save(*args, **kwargs)
        # update the workshop
        self.workshop.save()
    save.alters_data = True

    def will_happen(self, timestamp=datetime.now):
        if callable(timestamp):
            timestamp = timestamp()
        return timestamp < self.start
        
    def is_happening(self, timestamp=datetime.now):
        if callable(timestamp):
            timestamp = timestamp()
        return self.start <= timestamp <= self.end
        
    def has_happened(self, timestamp=datetime.now):
        if callable(timestamp):
            timestamp = timestamp()
        return self.end < timestamp
        
    def is_end_date_defined(self):
        return self.end_yyyy or self.end_mm or self.end_dd
        
    def has_start_time(self):
        return self.start_hh != None
    
    def has_end_time(self):
        return self.end_hh != None
        
    def get_secure_id(self):
        return int(self.pk) + SECURITY_SUMMAND
        


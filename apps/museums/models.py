# -*- coding: UTF-8 -*-
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from base_libs.models.models import UrlMixin
from base_libs.models.models import CreationModificationDateMixin
from base_libs.models.models import OpeningHoursMixin
from base_libs.models.models import SlugMixin
from base_libs.models.fields import URLField
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualTextField
from base_libs.models.fields import ExtendedTextField
from base_libs.middleware import get_current_language

from filebrowser.fields import FileBrowseField

from tagging.fields import TagField
from tagging.models import Tag
from tagging_autocomplete.models import TagAutocompleteField

from mptt.models import MPTTModel
from mptt.managers import TreeManager
from mptt.fields import TreeForeignKey, TreeManyToManyField

from jetson.apps.utils.models import MONTH_CHOICES

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^tagging_autocomplete\.models\.TagAutocompleteField"])

COUNTRY_CHOICES = (
    ('de', _("Germany")),
    ('-', "Other"),
    )

STATUS_CHOICES = (
    ('draft', _("Draft")),
    ('published', _("Published")),
    ('not_listed', _("Not Listed")),
    ('import', _("Imported")),
    ) 

YEAR_CHOICES = [(i,i) for i in range(1997, datetime.now().year+10)]

DAY_CHOICES = [(i,i) for i in range(1, 32)]

class MuseumCategory(MPTTModel, CreationModificationDateMixin, SlugMixin()):
    parent = TreeForeignKey('self', blank=True, null=True)
    title = MultilingualCharField(_('Title'), max_length=200)
    
    objects = TreeManager()
    
    def __unicode__(self):
        return self.title
        
    class Meta:
        ordering = ["tree_id", "lft"]
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
    
class MuseumService(CreationModificationDateMixin, SlugMixin()):
    title = MultilingualCharField(_('Title'), max_length=200)
    sort_order = models.IntegerField(_("Sort Order"), default=0)
    
    def __unicode__(self):
        return self.title
        
    class Meta:
        ordering = ['sort_order']
        verbose_name = _("Service")
        verbose_name_plural = _("Services")
    

class Museum(CreationModificationDateMixin, SlugMixin(), UrlMixin):
    title = MultilingualCharField(_("Title"), max_length=255)
    subtitle = MultilingualCharField(_("Subtitle"), max_length=255, blank=True)
    teaser = MultilingualTextField(_("Teaser"), blank=True)
    description = MultilingualTextField(_("Description"), blank=True)
    press_text = MultilingualTextField(_("Press text"), blank=True)

    image = FileBrowseField(_('Image'), max_length=255, directory="museums/", extensions=['.jpg', '.jpeg', '.gif','.png','.tif','.tiff'], blank=True)
    image_caption = MultilingualTextField(_("Image Caption"), max_length=255, blank=True)

    categories = TreeManyToManyField(MuseumCategory, verbose_name=_("Categories"),)
    services = models.ManyToManyField(MuseumService, verbose_name=_("Services"), blank=True)
    tags = TagAutocompleteField(verbose_name=_("tags"))

    street_address = models.CharField(_("Street address"), max_length=255)
    street_address2 = models.CharField(_("Street address (second line)"), max_length=255, blank=True)
    postal_code = models.CharField(_("Postal code"), max_length=255)
    district = models.CharField(_("District"), max_length=255, blank=True)
    city =  models.CharField(_("City"), default="Berlin", max_length=255)
    country = models.CharField(_("Country"), choices=COUNTRY_CHOICES, default='de', max_length=255)    
    latitude = models.FloatField(_("Latitude"), help_text=_("Latitude (Lat.) is the angle between any point and the equator (north pole is at 90; south pole is at -90)."), blank=True, null=True)
    longitude = models.FloatField(_("Longitude"), help_text=_("Longitude (Long.) is the angle east or west of an arbitrary point on Earth from Greenwich (UK), which is the international zero-longitude point (longitude=0 degrees). The anti-meridian of Greenwich is both 180 (direction to east) and -180 (direction to west)."), blank=True, null=True)

    phone = models.CharField(_("Phone"), help_text="Ortsvorwahl-Telefonnummer", max_length=255, blank=True)
    fax = models.CharField(_("Fax"), help_text="Ortsvorwahl-Telefonnummer", max_length=255, blank=True)
    email = models.EmailField(_("Email"), max_length=255, blank=True)
    website = URLField("Website", blank=True)
    group_bookings_phone = models.CharField(_("Phone for group bookings"), help_text="Ortsvorwahl-Telefonnummer", max_length=255, blank=True)
    service_phone = models.CharField(_("Service/visitors phone"), help_text="Ortsvorwahl-Telefonnummer", max_length=255, blank=True)
    twitter = models.CharField(_("Twitter"), max_length=255, blank=True)
    facebook = URLField(_("Facebook"), max_length=255, blank=True)
    
    open_on_mondays = models.BooleanField(_("Open on Mondays"))
    
    # prices
    free_entrance = models.BooleanField(_("Free entrance"))
    admission_price = models.DecimalField(_(u"Admission price (€)"), max_digits=5, decimal_places=2, blank=True, null=True)
    admission_price_info = MultilingualTextField(_("Admission price info"), blank=True)
    reduced_price = models.DecimalField(_(u"Reduced admission price (€)"), max_digits=5, decimal_places=2, blank=True, null=True)
    reduced_price_info = MultilingualTextField(_("Reduced admission price info"), blank=True)
    arrangements_for_children = MultilingualTextField(_("Admission arrangements for children and youth"), blank=True)
    free_entrance_for = MultilingualTextField(_("Free entrance for"), blank=True)
    family_ticket = MultilingualTextField(_("Family ticket"), blank=True)
    group_ticket = MultilingualTextField(_("Group ticket"), blank=True)
    free_entrance_times = MultilingualTextField(_("Free entrance times"), blank=True)
    yearly_ticket = MultilingualTextField(_("Yearly ticket"), blank=True)
    other_tickets = MultilingualTextField(_("Other tickets"), blank=True)
    member_of_museumspass = models.BooleanField(_("Member of Museumspass Berlin"))

    # accessibility
    accessibility = MultilingualTextField(_("Accessibility"), blank=True)

    mediation_offer = MultilingualTextField(_("Mediation offer"), blank=True)
    
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, blank=True, default="draft")
    
    def __unicode__(self):
        return self.title
        
    class Meta:
        ordering = ['title']
        verbose_name = _("Museum")
        verbose_name_plural = _("Museums")
        
    def get_url_path(self):
        try:
            path = reverse("%s:museum_detail" % get_current_language(), kwargs={'slug': self.slug})
        except:
            # the apphook is not attached yet
            return ""
        else:
            return path
    
    def get_published_exhibitions(self):
        return self.exhibition_set.filter(status="published").order_by("-start")
        
    def get_museums_with_the_same_categories(self):
        categories = list(self.categories.all().values_list("pk", flat=True))
        museums = Museum.objects.filter(
            categories__in=categories,
            status="published",
            ).exclude(pk=self.pk).distinct()
        return museums
        
    def get_tags(self):
        return Tag.objects.get_for_object(self)
        
class Season(OpeningHoursMixin):
    museum = models.ForeignKey(Museum)
    start = models.DateField(_("Start"))
    end = models.DateField(_("End"))
    mon_last_entry = models.TimeField(_("Last entry on Monday"), blank=True, null=True)
    tue_last_entry = models.TimeField(_("Last entry on Tuesday"), blank=True, null=True)
    wed_last_entry = models.TimeField(_("Last entry on Wednesday"), blank=True, null=True)
    thu_last_entry = models.TimeField(_("Last entry on Thursday"), blank=True, null=True)
    fri_last_entry = models.TimeField(_("Last entry on Friday"), blank=True, null=True)
    sat_last_entry = models.TimeField(_("Last entry on Saturday"), blank=True, null=True)
    sun_last_entry = models.TimeField(_("Last entry on Sunday"), blank=True, null=True)
    
    def __unicode__(self):
        if self.start and self.end:
            return u"%s - %s" % (self.start.strftime('%Y-%m-%d'), self.end.strftime('%Y-%m-%d'))
        return u""
        
    class Meta:
        ordering = ('start',)
        verbose_name = _("Season")
        verbose_name_plural = _("Seasons")
        
class SpecialOpeningTime(models.Model):
    museum = models.ForeignKey(Museum)
    yyyy = models.PositiveIntegerField(_("Year"), blank=True, null=True, choices=YEAR_CHOICES, help_text=_("Leave this field empty, if the occasion happens every year at the same time."))
    mm = models.PositiveIntegerField(_("Month"), choices=MONTH_CHOICES)
    dd = models.PositiveIntegerField(_("Day"), choices=DAY_CHOICES)

    day_label = MultilingualCharField(_('Day label'), max_length=255, blank=True, help_text=_("e.g. Christmas, Easter, etc."))

    is_closed = models.BooleanField(_("Closed?"))
    is_regular = models.BooleanField(_("Regular opening times?"))
    
    opening = models.TimeField(_('Opens'), blank=True, null=True)
    break_close = models.TimeField(_('Break Starts'), blank=True, null=True)
    break_open = models.TimeField(_('Break Ends'), blank=True, null=True)
    closing = models.TimeField(_('Closes'), blank=True, null=True)
    
    def __unicode__(self):
        if self.yyyy:
            return u"%s-%s-%s %s" % (self.yyyy, self.mm, self.dd, self.day_label)
        return u"%s-%s %s" % (self.mm, self.dd, self.day_label)
    
    class Meta:
        ordering = ("yyyy", "mm", "dd")
        verbose_name = _("Special opening time")
        verbose_name_plural = _("Special opening times")

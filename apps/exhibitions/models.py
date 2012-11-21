# -*- coding: UTF-8 -*-

from datetime import datetime, date, timedelta

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from base_libs.models.models import UrlMixin
from base_libs.models.models import CreationModificationDateMixin
from base_libs.models import SlugMixin

from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualTextField
from base_libs.models.fields import ExtendedTextField # for south
from base_libs.models.fields import URLField
from base_libs.middleware import get_current_language

from filebrowser.fields import FileBrowseField

from cms.models import CMSPlugin

from tagging.fields import TagField
from tagging.models import Tag
from tagging_autocomplete.models import TagAutocompleteField

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
    ('expired', _("Expired")),
    ('import', _("Imported")),
    ) 

class ExhibitionCategory(CreationModificationDateMixin, SlugMixin()):
    title = MultilingualCharField(_('Title'), max_length=200)
    sort_order = models.IntegerField(_("Sort Order"), default=0)
    
    def __unicode__(self):
        return self.title
        
    class Meta:
        ordering = ['sort_order']
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

class ExhibitionManager(models.Manager):
    def newly_opened(self):
        lang_code = get_current_language()
        return self.filter(newly_opened=True, status="published").order_by("-featured", "-start", "title_%s" % lang_code)
        
    def featured(self):
        return self.filter(featured=True, status="published")
        
    def closing_soon(self):
        lang_code = get_current_language()
        return self.filter(closing_soon=True, status="published").order_by("-featured", "end", "title_%s" % lang_code)
    
    def past(self, timestamp=date.today):
        """ Past events """
        if callable(timestamp):
            timestamp = timestamp()
        return self.filter(
            end__lt=timestamp,
            ).distinct()
            
    def update_expired(self):
        queryset = self.past().exclude(
            status="expired",
            )
        for obj in queryset:
            obj.status = "expired"
            obj.save()

class Exhibition(CreationModificationDateMixin, SlugMixin(), UrlMixin):
    museum = models.ForeignKey("museums.Museum", verbose_name=_("Museum"), blank=True, null=True)
    
    title = MultilingualCharField(_("Title"), max_length=255)
    subtitle = MultilingualCharField(_("Subtitle"), max_length=255, blank=True)
    teaser = MultilingualTextField(_("Teaser"), blank=True)
    description = MultilingualTextField(_("Description"), blank=True)
    press_text = MultilingualTextField(_("Press text"), blank=True)
    website = MultilingualCharField(_("Website"), max_length=255, blank=True)

    start = models.DateField(_("Start"))
    end = models.DateField(_("End"))

    image = FileBrowseField(_('Image'), max_length=255, directory="exhibitions/", extensions=['.jpg', '.jpeg', '.gif','.png','.tif','.tiff'], blank=True)
    image_caption = MultilingualTextField(_("Image Caption"), max_length=255, blank=True)

    location_name = models.CharField(_("Location name"), max_length=255, blank=True)
    street_address = models.CharField(_("Street address"), max_length=255, blank=True)
    street_address2 = models.CharField(_("Street address (second line)"), max_length=255, blank=True)
    postal_code = models.CharField(_("Postal code"), max_length=255, blank=True)
    district = models.CharField(_("District"), max_length=255, blank=True)
    city =  models.CharField(_("City"), default="Berlin", max_length=255, blank=True)
    country = models.CharField(_("Country"), choices=COUNTRY_CHOICES, default='de', max_length=255, blank=True)    
    latitude = models.FloatField(_("Latitude"), help_text=_("Latitude (Lat.) is the angle between any point and the equator (north pole is at 90; south pole is at -90)."), blank=True, null=True)
    longitude = models.FloatField(_("Longitude"), help_text=_("Longitude (Long.) is the angle east or west of an arbitrary point on Earth from Greenwich (UK), which is the international zero-longitude point (longitude=0 degrees). The anti-meridian of Greenwich is both 180 (direction to east) and -180 (direction to west)."), blank=True, null=True)

    newly_opened = models.BooleanField(_("Newly opened"))
    featured = models.BooleanField(_("Featured"))
    closing_soon = models.BooleanField(_("Closing soon"))
    
    # prices
    museum_prices = models.BooleanField(_("See prices from museum"))
    free_entrance = models.BooleanField(_("Free entrance for this exhibition"))
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
    
    # organizer
    organizing_museum = models.ForeignKey("museums.Museum", verbose_name=_("Organizing museum"), blank=True, null=True, related_name="organized_exhibitions")
    organizer_title = models.CharField(_("Other Organizer"), max_length=255, blank=True)
    organizer_url_link = URLField(_("Organizer URL"), blank=True)
    
    categories = models.ManyToManyField(ExhibitionCategory, verbose_name=_("Categories"), blank=True)
    tags = TagAutocompleteField(verbose_name=_("tags"))
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, blank=True, default="draft")
    
    objects = ExhibitionManager()
    
    def __unicode__(self):
        return self.title
        
    class Meta:
        ordering = ['title']
        verbose_name = _("Exhibition")
        verbose_name_plural = _("Exhibitions")

    def get_url_path(self):
        try:
            path = reverse("%s:exhibition_detail" % get_current_language(), kwargs={'slug': self.slug})
        except:
            # the apphook is not attached yet
            return ""
        else:
            return path

    def is_newly_open(self):
        today = date.today()
        two_weeks = timedelta(days=14)
        return today - two_weeks < self.start < today
        
    def is_closing_soon(self):
        today = date.today()
        two_weeks = timedelta(days=14)
        return today < self.end < today + two_weeks
        
    def get_tags(self):
        return Tag.objects.get_for_object(self)
        
class NewlyOpenedExhibition(CMSPlugin):
    exhibition = models.ForeignKey(Exhibition, limit_choices_to={'newly_opened': True})
    
    def __unicode__(self):
        return self.exhibition.title
        
    class Meta:
        ordering = ['exhibition__title']
        verbose_name = _("Newly opened exhibition")
        verbose_name_plural = _("Newly opened exhibitions")


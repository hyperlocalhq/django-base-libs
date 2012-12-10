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
    
class AccessibilityOption(CreationModificationDateMixin, SlugMixin()):
    title = MultilingualCharField(_('Title'), max_length=200)
    image = FileBrowseField(_('Image'), max_length=255, directory="museums/", extensions=['.jpg', '.jpeg', '.gif','.png','.tif','.tiff'], blank=True)
    sort_order = models.IntegerField(_("Sort Order"), default=0)
    
    def __unicode__(self):
        return self.title
        
    class Meta:
        ordering = ['sort_order']
        verbose_name = _("Accessibility option")
        verbose_name_plural = _("Accessibility options")

    '''
    Signet "Berlin barrierefrei"
    gute Ausstattung bei Sehbebehinderung
    bedingt geeignete Ausstattung bei Sehbehinderung
    gute Ausstattung für blinde Menschen
    bedingt geeignete Ausstattung für blinde Menschen
    gute Ausstattung für gehörlose Menschen
    bedingt geeignete Ausstattung für gehörlose Menschen
    gute Ausstattung für hörgeschädigte Menschen
    bedingt geeignete Ausstattung für hörgeschädigte Menschen
    gute Ausstattung für Menschen mit einer Lernbehinderung
    bedingt geeignete Ausstattung für Menschen mit einer Lernbehinderung
    gute rollstuhlgerechte Zugänglichkeit
    rollstuhlgeeignete Zugänglichkeit
    bedingt rollstuhlgeeignete Zugänglichkeit
    gutes rollstuhlgerechtes WC
    rollstuhlgeeignetes WC
    bedingt rollstuhlgeeignetes WC
    guter rollstuhlgerechter Aufzug
    rollstuhlgeeigneter Aufzug
    Aufzug bedingt rollstuhlgeeignet
    Parkmöglichkeit
    Parkplatz für Menschen mit Behinderung
    gutes rollstuhlgerechtes Zimmer in Beherbergungsstätte
    rollstuhlgeeignetes Zimmer in Beherbergungsstätte
    bedingt rollstuhlgeeignetes Zimmer in Beherbergungstätte
    gute rollstuhlgerechte Nasszelle (Bad, Dusche)
    rollstuhlgeeignete Nasszelle (Bad, Dusche)
    Nasszelle bedingt rollstuhlgeeignet (Bad, Dusche)
    gut rollstuhlgerechtes Schwimmbad
    Schwimmbad rollstuhlgeeignet
    Schwimmbad bedingt rollstuhlgeeignet
    Sportstätte / Umkleidebereich gut rollstuhlgerecht
    Sportstätte / Umkleidebereich rollstuhlgeeignet
    Sportstätten / Umkleidebereich bedingt rollstuhlgeeignet
    gute rollstuhlgerechte Küche
    Küche rollstuhlgeeignet
    Küche bedingt rollstuhlgeeignet
    '''


class Museum(CreationModificationDateMixin, SlugMixin(), UrlMixin):
    title = MultilingualCharField(_("Name"), max_length=255)
    subtitle = MultilingualCharField(_("Subtitle"), max_length=255, blank=True)
    teaser = MultilingualTextField(_("Teaser"), blank=True)
    description = MultilingualTextField(_("Description"), blank=True)
    press_text = MultilingualTextField(_("Press text"), blank=True)

    image = FileBrowseField(_('Image'), max_length=255, directory="museums/", extensions=['.jpg', '.jpeg', '.gif','.png','.tif','.tiff'], blank=True)
    image_caption = MultilingualTextField(_("Image Caption"), max_length=255, blank=True)

    categories = TreeManyToManyField(MuseumCategory, verbose_name=_("Categories"),)
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

    contact_name = models.CharField(_("Contact person"), max_length=255, blank=True)
    contact_phone_country = models.CharField(_("Country Code"), max_length=4, blank=True, default="49")
    contact_phone_area = models.CharField(_("Area Code"), max_length=6, blank=True)
    contact_phone_number = models.CharField(_("Subscriber Number and Extension"), max_length=25, blank=True)
    contact_email = models.EmailField(_("Email"), max_length=255, blank=True)

    post_street_address = models.CharField(_("Street address"), max_length=255, blank=True)
    post_street_address2 = models.CharField(_("Street address (second line)"), max_length=255, blank=True)
    post_postal_code = models.CharField(_("Postal code"), max_length=255, blank=True)
    post_city =  models.CharField(_("City"), default="Berlin", max_length=255, blank=True)
    post_country = models.CharField(_("Country"), choices=COUNTRY_CHOICES, default='de', max_length=255, blank=True)    

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
    accessibility_options = models.ManyToManyField(AccessibilityOption, verbose_name=_("Accessibility options"), blank=True)
    
    service_shop = models.BooleanField(_("Shop"), blank=True)
    service_shop_info = MultilingualTextField(_("Shop info"), blank=True)
    service_books = models.BooleanField(_("Bookstore"), blank=True)
    service_books_info = MultilingualTextField(_("Books info"), blank=True)
    service_restaurant = models.BooleanField(_("Restaurant"), blank=True)
    service_restaurant_info = MultilingualTextField(_("Restaurant info"), blank=True)
    service_cafe = models.BooleanField(_("Cafe"), blank=True)
    service_cafe_info = MultilingualTextField(_("Cafe info"), blank=True)
    service_library = models.BooleanField(_("Library"), blank=True)
    service_library_info = MultilingualTextField(_("Library info"), blank=True)
    service_archive = models.BooleanField(_("Archive"), blank=True)
    service_archive_info = MultilingualTextField(_("Archive info"), blank=True)
    service_studio = models.BooleanField(_("Studio"), blank=True)
    service_studio_info = MultilingualTextField(_("Studio info"), blank=True)
    service_online = models.BooleanField(_("Online offers"), blank=True)
    service_online_info = MultilingualTextField(_("Online offers info"), blank=True)
    service_diaper_changing_table = models.BooleanField(_("Diaper changing table"))
    service_birthdays = models.BooleanField(_("Children birthdays"), blank=True)
    service_birthdays_info = MultilingualTextField(_("Children birthdays info"), blank=True)
    service_rent = models.BooleanField(_("Rent"), blank=True)
    service_rent_info = MultilingualTextField(_("Rent info"), blank=True)
    service_other = models.BooleanField(_("Other services"), blank=True)
    service_other_info = MultilingualTextField(_("Other services info"), blank=True)
    
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
    last_entry = MultilingualCharField(_("Last entry"), max_length=255, blank=True)
    
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
    
    exceptions = MultilingualTextField(_('Exceptions for working hours'), blank=True)

    def __unicode__(self):
        if self.yyyy:
            return u"%s-%s-%s %s" % (self.yyyy, self.mm, self.dd, self.day_label)
        return u"%s-%s %s" % (self.mm, self.dd, self.day_label)
    
    class Meta:
        ordering = ("yyyy", "mm", "dd")
        verbose_name = _("Special opening time")
        verbose_name_plural = _("Special opening times")

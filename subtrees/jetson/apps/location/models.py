# -*- coding: UTF-8 -*-
from django.db.models.loading import load_app
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from django.utils.encoding import force_unicode
from django.conf import settings

from mptt.models import MPTTModel
from mptt.managers import TreeManager
from mptt.fields import TreeForeignKey, TreeManyToManyField

from base_libs.models.models import SlugMixin
from base_libs.models.fields import MultilingualCharField

verbose_name = _("Location")

def _is_numeric(obj):
    success = False
    try:
        float(obj)
        success = True
    except:
        pass
    return success

class CountryChoices(object):
    def __iter__(self):
        from jetson.apps.i18n.models import Country
        choices = [(item.iso2_code, item.name) for item in Country.objects.filter(display=True)]
        return iter(choices)

class AddressManager(models.Manager):
    def cleanup(self):
        ### TODO: find more generic way to remove unassigned Address objects
        IndividualContact = models.get_model("people", "IndividualContact")
        InstitutionalContact = models.get_model("institutions", "InstitutionalContact")
        Event = models.get_model("events", "Event")
        for el in self.get_queryset():
            if el.address_events.count() + el.individual_address.count() + el.institutional_address.count() == 0:
                el.delete()
        for el in InstitutionalContact.objects.all():
            if el.postal_address:
                self.set_for(
                    el,
                    "postal_address",
                    **el.postal_address.get_dict()
                    )
        
        for el in IndividualContact.objects.all():
            if el.postal_address:
                self.set_for(
                    el,
                    "postal_address",
                    **el.postal_address.get_dict()
                    )
        
        for el in Event.objects.all():
            if el.postal_address:
                self.set_for(
                    el,
                    "postal_address",
                    **el.postal_address.get_dict()
                    )
    def set_for(self, address_owner, address_field,
        country="", state="", city="", street_address="", street_address2="",
        street_address3="", postal_code="", district="", neighborhood="",
        latitude="", longitude="", altitude=""):
        """
        Example:
            
            Address.objects.set_for(
                event, "postal_address"
                country="DE",
                city="Berlin",
                latitude="52.524048",
                longitude="13.402728",
                )
        """
        from jetson.apps.i18n.models import Country
        old_address=getattr(address_owner, address_field, None)
        delete_the_old = False
        # if old address exists
        if old_address:
            relation_count = (
                old_address.address_events.count()
                + old_address.individual_address.count()
                + old_address.institutional_address.count()
                )
            #... and it is assigned only to 1 object
            if relation_count < 2:
                # it will have to get removed
                delete_the_old = True
        # check the existance of the new address
        geo_filter = {
            'geoposition__latitude': latitude or None,
            'geoposition__longitude': longitude or None,
            'geoposition__altitude': altitude or None,
            }
            
        if country and not isinstance(country, Country):
            country = Country.objects.get(pk=country)
            
        as_necessary = self.filter(
            country=country,
            state=state,
            city=city,
            street_address=street_address,
            street_address2=street_address2,
            street_address3=street_address3,
            postal_code=postal_code,
            locality__district=district,
            locality__neighborhood=neighborhood,
            **geo_filter
            )
        new_address = None
        # if there is one in the DB, use it
        if as_necessary.count() == 1:
            new_address = as_necessary.get()
            if new_address == old_address:
                delete_the_old = False
        # if there are more
        elif as_necessary.count() > 1:
            # ...reassign the objects and remove duplicates
            for el in as_necessary:
                if not new_address:
                    # the 1st one will be the original
                    new_address = el
                else:
                    # the others will be duplicates
                    for rel in el.address_events.all():
                        rel.postal_address = new_address
                        super(type(rel), rel).save()
                    for rel in el.individual_address.all():
                        rel.postal_address = new_address
                        super(type(rel), rel).save()
                    for rel in el.institutional_address.all():
                        rel.postal_address = new_address
                        super(type(rel), rel).save()
                    # ..and it will get removed
                    el.delete()
            if new_address == old_address:
                delete_the_old = False
        # else create one
        else:
            new_address = self.create(
                country=country,
                state=state,
                city=city,
                street_address=street_address,
                street_address2=street_address2,
                street_address3=street_address3,
                postal_code=postal_code,
                )
            new_address.locality_set.create(
                district=district,
                neighborhood=neighborhood,
                )
            new_address.geoposition_set.create(
                latitude=(not _is_numeric(latitude) and [None] or [float(latitude)])[0],
                longitude=(not _is_numeric(longitude) and [None] or [float(longitude)])[0],
                altitude=(not _is_numeric(altitude) and [None] or [int(altitude)])[0],
                )
        # set it to the object and save the object
        setattr(address_owner, address_field, new_address)
        # save it without triggering any signals
        address_owner.save_base(raw=True)
        # delete the old address when necessary
        if delete_the_old:
            old_address.delete()
    
class Address(models.Model):
    #country = models.CharField(_("Country"), max_length=255, default="DE", choices=CountryChoices())
    country = models.ForeignKey("i18n.Country", verbose_name=_("Country"), default="DE", null=True, blank=True)
    state = models.CharField(_("State"), max_length=255, blank=True)
    city = models.CharField(_("City"), max_length=255, blank=True)
    street_address = models.CharField(_("Street Address"), max_length=255, blank=True)
    street_address2 = models.CharField(_("Additional Address"), max_length=255, blank=True)
    street_address3 = models.CharField(_("Additional Address"), max_length=255, blank=True)
    postal_code = models.CharField(_("Postal/ZIP Code"), max_length=10, blank=True)

    objects = AddressManager()

    class Meta:
        verbose_name = _("address")
        verbose_name_plural = _("addresses")
        
    def __unicode__(self):
        return u", ".join([force_unicode(item) for item in (self.street_address, self.street_address2, self.city, self.country) if item]).strip()
    
    def get_dict(self):
        locality = self.get_locality()
        geoposition = self.get_geoposition()
        result = {
            'country': self.country,
            'state': self.state,
            'city': self.city,
            'street_address': self.street_address,
            'street_address2': self.street_address2,
            'street_address3': self.street_address3,
            'postal_code': self.postal_code,
            'district': locality.district,
            'neighborhood': locality.neighborhood,
            'latitude': geoposition.get_latitude(),
            'longitude': geoposition.get_longitude(),
            'altitude': geoposition.get_altitude(),
            }
        return result
    def get_locality(self):
        try:
            return self.locality_set.get()
        except:
            return Locality()

    def get_geoposition(self):
        try:
            return self.geoposition_set.get()
        except:
            return Geoposition()


class Locality(models.Model):
    address = models.ForeignKey(Address)
    district = models.CharField(_("District"), max_length=255, blank=True)
    neighborhood = models.CharField(_("Neighborhood"), max_length=255, blank=True)
    class Meta:
        verbose_name = _("locality")
        verbose_name_plural = _("localities")
    def __unicode__(self):
        return self.neighborhood


class Geoposition(models.Model):
    address = models.ForeignKey(Address)
    latitude = models.FloatField(_("Latitude"), help_text=_("Latitude (Lat.) is the angle between any point and the equator (north pole is at 90; south pole is at -90)."), blank=True, null=True)
    longitude = models.FloatField(_("Longitude"), help_text=_("Longitude (Long.) is the angle east or west of an arbitrary point on Earth from Greenwich (UK), which is the international zero-longitude point (longitude=0 degrees). The anti-meridian of Greenwich is both 180 (direction to east) and -180 (direction to west)."), blank=True, null=True)
    altitude = models.IntegerField(_("Altitude"), help_text=_("The elevation above the sea level measured in meters"), blank=True, null=True)
    class Meta:
        verbose_name = _("geoposition")
        verbose_name_plural = _("geopositions")
    def __unicode__(self):
        return "Lat. %s, Long. %s" % (
            self.get_latitude() or ugettext("N/A"),
            self.get_longitude() or ugettext("N/A"),
        )
    def get_latitude(self):
        result = ""
        try:
            result = "%.6f" % float(self.latitude)
        except TypeError:
            pass
        return result
        
    def get_longitude(self):
        result = ""
        try:
            result = "%.6f" % float(self.longitude)
        except TypeError:
            pass
        return result
        
    def get_altitude(self):
        result = ""
        try:
            result = "%d" % int(self.longitude)
        except TypeError:
            pass
        return result
            
            
class LocalityType(MPTTModel, SlugMixin()):
    parent = TreeForeignKey(
       'self',
       related_name="child_set",
       blank=True,
       null=True,
    )
    title = MultilingualCharField(_('title'), max_length=255)

    objects = TreeManager()

    class Meta:
        verbose_name = _("locality type")
        verbose_name_plural = _("locality types")
        ordering = ["tree_id", "lft"]

    def __unicode__(self):
        return self.title

# -*- coding: UTF-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.urlresolvers import reverse

from base_libs.models.models import UrlMixin
from base_libs.models.models import SlugMixin
from base_libs.models.models import CreationModificationMixin
from base_libs.models.models import CreationModificationDateMixin
from base_libs.models.models import OpeningHoursMixin
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualTextField
from base_libs.models.fields import URLField
from base_libs.models.fields import ExtendedTextField # needed for south to work
from base_libs.models.fields import PositionField
from base_libs.utils.misc import get_translation

from filebrowser.fields import FileBrowseField

from mptt.models import MPTTModel
from mptt.managers import TreeManager
from mptt.fields import TreeForeignKey, TreeManyToManyField

STATUS_CHOICES = (
    ('draft', _("Draft")),
    ('published', _("Published")),
    ('not_listed', _("Not Listed")),
    ('import', _("Imported")),
    ('trashed', _("Trashed")),
)

COPYRIGHT_RESTRICTION_CHOICES = (
    ('general_use', _("Released for general use")),
    ('protected', _("Released for this and own site only"))
)


TOKENIZATION_SUMMAND = 56436  # used to hide the ids of media files


class District(CreationModificationDateMixin, SlugMixin()):
    title = MultilingualCharField(_('Title'), max_length=200)
    sort_order = models.IntegerField(_("Sort Order"), default=0)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['sort_order']
        verbose_name = _("District")
        verbose_name_plural = _("Districts")


class Service(CreationModificationDateMixin, SlugMixin()):
    title = MultilingualCharField(_('Title'), max_length=200)
    image = FileBrowseField(_('Image'), max_length=255, directory="services/", extensions=['.jpg', '.jpeg', '.gif', '.png'], blank=True)
    sort_order = models.IntegerField(_("Sort Order"), default=0)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['sort_order']
        verbose_name = _("Service")
        verbose_name_plural = _("Services")


class AccessibilityOption(CreationModificationDateMixin, SlugMixin()):
    title = MultilingualCharField(_('Title'), max_length=200)
    image = FileBrowseField(_('Image'), max_length=255, directory="accessibility/", extensions=['.jpg', '.jpeg', '.gif', '.png'], blank=True)
    sort_order = models.IntegerField(_("Sort Order"), default=0)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['sort_order']
        verbose_name = _("Accessibility option")
        verbose_name_plural = _("Accessibility options")


class LocationCategory(MPTTModel, CreationModificationDateMixin, SlugMixin()):
    parent = TreeForeignKey('self', blank=True, null=True, related_name="children")
    title = MultilingualCharField(_('Title'), max_length=200)

    objects = TreeManager()

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["tree_id", "lft"]
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def save(self, *args, **kwargs):
        if not self.pk:
            LocationCategory.objects.insert_node(self, self.parent)
        super(LocationCategory, self).save(*args, **kwargs)


class LocationManager(models.Manager):
    def accessible_to(self, user):
        from jetson.apps.permissions.models import PerObjectGroup
        if user.has_perm("locations.change_location"):
            return self.get_query_set().exclude(status="trashed")
        ids = PerObjectGroup.objects.filter(
            content_type__app_label="locations",
            content_type__model="location",
            sysname__startswith="owners",
            users=user,
        ).values_list("object_id", flat=True)
        return self.get_query_set().filter(pk__in=ids).exclude(status="trashed")

    def owned_by(self, user):
        from jetson.apps.permissions.models import PerObjectGroup
        ids = PerObjectGroup.objects.filter(
            content_type__app_label="locations",
            content_type__model="location",
            sysname__startswith="owners",
            users=user,
        ).values_list("object_id", flat=True)
        return self.get_query_set().filter(pk__in=ids).exclude(status="trashed")

    def for_newsletter(self):
        return self.filter(
            status="published",
            newsletter=True
        )

class Location(CreationModificationMixin, UrlMixin, SlugMixin(), OpeningHoursMixin):
    title = MultilingualCharField(_("Title"), max_length=255)
    subtitle = MultilingualCharField(_("Subtitle"), max_length=255, blank=True)
    description = MultilingualTextField(_("Description"), blank=True)
    logo = FileBrowseField(_('Logo'), max_length=255, directory="locations/", extensions=['.jpg', '.jpeg', '.gif', '.png'], blank=True)
    teaser = MultilingualTextField(_("Teaser"), blank=True)
    categories = TreeManyToManyField(LocationCategory, verbose_name=_("Categories"), blank=True)

    street_address = models.CharField(_("Street address"), max_length=255)
    street_address2 = models.CharField(_("Street address (second line)"), max_length=255, blank=True)
    postal_code = models.CharField(_("Postal code"), max_length=255)
    city = models.CharField(_("City"), default="Berlin", max_length=255)
    latitude = models.FloatField(_("Latitude"), help_text=_("Latitude (Lat.) is the angle between any point and the equator (north pole is at 90; south pole is at -90)."), blank=True, null=True)
    longitude = models.FloatField(_("Longitude"), help_text=_("Longitude (Long.) is the angle east or west of an arbitrary point on Earth from Greenwich (UK), which is the international zero-longitude point (longitude=0 degrees). The anti-meridian of Greenwich is both 180 (direction to east) and -180 (direction to west)."), blank=True, null=True)

    phone_country = models.CharField(_("Country Code"), max_length=4, blank=True, default="49")
    phone_area = models.CharField(_("Area Code"), max_length=6, blank=True)
    phone_number = models.CharField(_("Subscriber Number and Extension"), max_length=25, blank=True)
    fax_country = models.CharField(_("Country Code"), max_length=4, blank=True, default="49")
    fax_area = models.CharField(_("Area Code"), max_length=6, blank=True)
    fax_number = models.CharField(_("Subscriber Number and Extension"), max_length=25, blank=True)
    email = models.EmailField(_("Email"), max_length=255, blank=True)
    website = URLField("Website", blank=True)

    tickets_street_address = models.CharField(_("Street address"), max_length=255, blank=True)
    tickets_street_address2 = models.CharField(_("Street address (second line)"), max_length=255, blank=True)
    tickets_postal_code = models.CharField(_("Postal code"), max_length=255, blank=True)
    tickets_city = models.CharField(_("City"), default="Berlin", max_length=255, blank=True)
    tickets_email = models.EmailField(_("Tickets Email"), max_length=255, blank=True)
    tickets_website = URLField("Tickets Website", blank=True)

    tickets_phone_country = models.CharField(_("Country Code"), max_length=4, blank=True, default="49")
    tickets_phone_area = models.CharField(_("Area Code"), max_length=6, blank=True)
    tickets_phone_number = models.CharField(_("Subscriber Number and Extension"), max_length=25, blank=True)
    tickets_fax_country = models.CharField(_("Country Code"), max_length=4, blank=True, default="49")
    tickets_fax_area = models.CharField(_("Area Code"), max_length=6, blank=True)
    tickets_fax_number = models.CharField(_("Subscriber Number and Extension"), max_length=25, blank=True)

    tickets_calling_prices = MultilingualTextField(_("Phone calling prices"), blank=True)
    tickets_additional_info = MultilingualTextField(_("Additional information"), blank=True)

    press_contact_name = models.CharField(_("Press contact name"), max_length=255, blank=True)
    press_phone_country = models.CharField(_("Country Code"), max_length=4, blank=True, default="49")
    press_phone_area = models.CharField(_("Area Code"), max_length=6, blank=True)
    press_phone_number = models.CharField(_("Subscriber Number and Extension"), max_length=25, blank=True)
    press_fax_country = models.CharField(_("Country Code"), max_length=4, blank=True, default="49")
    press_fax_area = models.CharField(_("Area Code"), max_length=6, blank=True)
    press_fax_number = models.CharField(_("Subscriber Number and Extension"), max_length=25, blank=True)
    press_email = models.EmailField(_("Press Email"), max_length=255, blank=True)
    press_website = URLField("Press Website", blank=True)

    districts = models.ManyToManyField(District, verbose_name=_("District"), blank=True)
    services = models.ManyToManyField(Service, verbose_name=_("Service"), blank=True)
    accessibility_options = models.ManyToManyField(AccessibilityOption, verbose_name=_("Accessibility options"), blank=True)

    newsletter = models.BooleanField(_("Show in newsletter"))
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, blank=True, default="draft")

    objects = LocationManager()

    row_level_permissions = True

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = _("Theater")
        verbose_name_plural = _("Theaters")

    def get_url_path(self):
        try:
            path = reverse("location_detail", kwargs={'slug': self.slug})
        except:
            # the apphook is not attached yet
            return ""
        else:
            return path

    def set_owner(self, user):
        ContentType = models.get_model("contenttypes", "ContentType")
        PerObjectGroup = models.get_model("permissions", "PerObjectGroup")
        RowLevelPermission = models.get_model("permissions", "RowLevelPermission")
        try:
            role = PerObjectGroup.objects.get(
                sysname__startswith="owners",
                object_id=self.pk,
                content_type=ContentType.objects.get_for_model(Location),
            )
        except:
            role = PerObjectGroup(
                sysname="owners",
            )
            for lang_code, lang_name in settings.LANGUAGES:
                setattr(role, "title_%s" % lang_code, get_translation("Owners", language=lang_code))
            role.content_object = self
            role.save()

            RowLevelPermission.objects.create_default_row_permissions(
                model_instance=self,
                owner=role,
            )

        if not role.users.filter(pk=user.pk).count():
            role.users.add(user)
    set_owner.alters_data = True

    def remove_owner(self, user):
        ContentType = models.get_model("contenttypes", "ContentType")
        PerObjectGroup = models.get_model("permissions", "PerObjectGroup")
        try:
            role = PerObjectGroup.objects.get(
                sysname__startswith="owners",
                object_id=self.pk,
                content_type=ContentType.objects.get_for_model(Location),
                )
        except:
            return
        role.users.remove(user)
        if not role.users.count():
            role.delete()
    remove_owner.alters_data = True

    def get_owners(self):
        ContentType = models.get_model("contenttypes", "ContentType")
        PerObjectGroup = models.get_model("permissions", "PerObjectGroup")
        try:
            role = PerObjectGroup.objects.get(
                sysname__startswith="owners",
                object_id=self.pk,
                content_type=ContentType.objects.get_for_model(Location),
            )
        except:
            return []
        return role.users.all()

    def get_social_media(self):
        return self.socialmediachannel_set.all()

    def _get_first_image(self):
        if not hasattr(self, '_first_image_cache'):
            self._first_image_cache = None
            qs = self.image_set.all()
            if qs.count():
                self._first_image_cache = qs[0]
        return self._first_image_cache
    first_image = property(_get_first_image)

    def is_editable(self, user=None):
        from django.contrib.auth.models import AnonymousUser
        from base_libs.middleware.threadlocals import get_current_user
        if not hasattr(self, "_is_editable_cache"):
            user = get_current_user(user) or AnonymousUser()
            self._is_editable_cache = user.has_perm("locations.change_location", self)
        return self._is_editable_cache

    def is_deletable(self, user=None):
        from django.contrib.auth.models import AnonymousUser
        from base_libs.middleware.threadlocals import get_current_user
        if not hasattr(self, "_is_deletable_cache"):
            user = get_current_user(user) or AnonymousUser()
            self._is_deletable_cache = user.has_perm("locations.delete_location", self)
        return self._is_deletable_cache

    def get_previous_item(self):
        try:
            return Location.objects.filter(
                ~models.Q(pk=self.pk),
                title__lt=self.title,
                status="published",
            ).order_by("-title")[0]
        except:
            return None

    def get_next_item(self):
        try:
            return Location.objects.filter(
                ~models.Q(pk=self.pk),
                title__gt=self.title,
                status="published",
            ).order_by("title")[0]
        except:
            return None


class Stage(CreationModificationMixin, SlugMixin()):
    location = models.ForeignKey(Location, verbose_name=_("Location"))
    title = MultilingualCharField(_("Title"), max_length=255)
    description = MultilingualTextField(_("Description"), blank=True)

    street_address = models.CharField(_("Street address"), max_length=255, blank=True)
    street_address2 = models.CharField(_("Street address (second line)"), max_length=255, blank=True)
    postal_code = models.CharField(_("Postal code"), max_length=255, blank=True)
    city = models.CharField(_("City"), default="Berlin", max_length=255, blank=True)
    latitude = models.FloatField(_("Latitude"), help_text=_("Latitude (Lat.) is the angle between any point and the equator (north pole is at 90; south pole is at -90)."), blank=True, null=True)
    longitude = models.FloatField(_("Longitude"), help_text=_("Longitude (Long.) is the angle east or west of an arbitrary point on Earth from Greenwich (UK), which is the international zero-longitude point (longitude=0 degrees). The anti-meridian of Greenwich is both 180 (direction to east) and -180 (direction to west)."), blank=True, null=True)
    district = models.ForeignKey(District, verbose_name=_("District"), blank=True, null=True)

    sort_order = models.IntegerField(_("Sort Order"), default=0)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['sort_order', 'title']
        verbose_name = _("Stage")
        verbose_name_plural = _("Stages")


class Image(CreationModificationDateMixin):
    location = models.ForeignKey(Location, verbose_name=_("Location"))
    path = FileBrowseField(_('File path'), max_length=255, directory="locations/", extensions=['.jpg', '.jpeg', '.gif', '.png'], help_text=_("A path to a locally stored image."))
    copyright_restrictions = models.CharField(_('Copyright restrictions'), max_length=20, blank=True, choices=COPYRIGHT_RESTRICTION_CHOICES)
    sort_order = PositionField(_("Sort order"), collection="location")

    class Meta:
        ordering = ["sort_order", "creation_date"]
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def __unicode__(self):
        if self.path:
            return self.path.path
        return "Missing file (id=%s)" % self.pk

    def get_token(self):
        if self.pk:
            return int(self.pk) + TOKENIZATION_SUMMAND
        else:
            return None

    @staticmethod
    def token_to_pk(token):
        return int(token) - TOKENIZATION_SUMMAND


class SocialMediaChannel(models.Model):
    location = models.ForeignKey(Location)
    channel_type = models.CharField(_("Social media type"), max_length=255, help_text=_("e.g. twitter, facebook, etc."))
    url = URLField(_("URL"), max_length=255)

    class Meta:
        ordering = ['channel_type']
        verbose_name = _("Social media channel")
        verbose_name_plural = _("Social media channels")

    def __unicode__(self):
        return self.channel_type
        
    def get_class(self):
        social = self.channel_type.lower()
        if social == "google+":
            return u"googleplus"
        return social


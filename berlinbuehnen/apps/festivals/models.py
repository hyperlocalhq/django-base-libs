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
from base_libs.models.fields import URLField
from base_libs.models.fields import MultilingualTextField
from base_libs.models.fields import PositionField
from base_libs.utils.misc import get_translation
from base_libs.utils.misc import get_unique_value
from base_libs.utils.betterslugify import better_slugify

from filebrowser.fields import FileBrowseField

STATUS_CHOICES = (
    ('draft', _("Draft")),
    ('published', _("Published")),
    ('not_listed', _("Not Listed")),
    ('import', _("Imported")),
    ('expired', _("Expired")),
    ('trashed', _("Trashed")),
)

COPYRIGHT_RESTRICTION_CHOICES = (
    ('general_use', _("Released for general use")),
    ('protected', _("Released for this and own site only"))
)

TOKENIZATION_SUMMAND = 56436  # used to hide the ids of media files


class FestivalManager(models.Manager):
    def accessible_to(self, user):
        from berlinbuehnen.apps.locations.models import Location
        if user.has_perm("festivals.change_production"):
            return self.get_queryset().exclude(status="trashed")

        owned_locations = Location.objects.owned_by(user=user)
        return self.get_queryset().filter(
            organizers__in=owned_locations,
        ).exclude(status="trashed").distinct()

    def owned_by(self, user):
        from jetson.apps.permissions.models import PerObjectGroup
        if user.has_perm("festivals.change_festival"):
            return self.get_queryset().exclude(status="trashed")
        ids = map(int, PerObjectGroup.objects.filter(
            content_type__app_label="festivals",
            content_type__model="festival",
            sysname__startswith="owners",
            users=user,
        ).values_list("object_id", flat=True))
        return self.get_queryset().filter(pk__in=ids).exclude(status="trashed")

    def for_newsletter(self):
        return self.filter(
            status="published",
            newsletter=True
        ).order_by('start')


class Festival(CreationModificationMixin, UrlMixin, SlugMixin(), OpeningHoursMixin):
    title = MultilingualCharField(_("Title"), max_length=255)
    subtitle = MultilingualCharField(_("Subtitle"), max_length=255, blank=True)
    description = MultilingualTextField(_("Description"), blank=True)
    logo = FileBrowseField(_('Logo'), max_length=255, directory="festivals/", extensions=['.jpg', '.jpeg', '.gif', '.png'], blank=True)

    street_address = models.CharField(_("Street address"), max_length=255, blank=True)
    street_address2 = models.CharField(_("Street address (second line)"), max_length=255, blank=True)
    postal_code = models.CharField(_("Postal code"), max_length=255, blank=True)
    city = models.CharField(_("City"), default="Berlin", max_length=255, blank=True)
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

    press_contact_name = models.CharField(_("Press contact name"), max_length=255, blank=True)
    press_phone_country = models.CharField(_("Country Code"), max_length=4, blank=True, default="49")
    press_phone_area = models.CharField(_("Area Code"), max_length=6, blank=True)
    press_phone_number = models.CharField(_("Subscriber Number and Extension"), max_length=25, blank=True)
    press_mobile_country = models.CharField(_("Country Code"), max_length=4, blank=True, default="49")
    press_mobile_area = models.CharField(_("Area Code"), max_length=6, blank=True)
    press_mobile_number = models.CharField(_("Subscriber Number and Extension"), max_length=25, blank=True)
    press_fax_country = models.CharField(_("Country Code"), max_length=4, blank=True, default="49")
    press_fax_area = models.CharField(_("Area Code"), max_length=6, blank=True)
    press_fax_number = models.CharField(_("Subscriber Number and Extension"), max_length=25, blank=True)
    press_email = models.EmailField(_("Press Email"), max_length=255, blank=True)
    press_website = URLField("Press Website", blank=True)

    start = models.DateField(_("Start date"))
    end = models.DateField(_("End date"))

    organizers = models.ManyToManyField("locations.Location", verbose_name=_("Organizers"), blank=True)

    newsletter = models.BooleanField(_("Show in newsletter"), default=False)
    featured = models.BooleanField(_("Featured in overview"), default=False)
    slideshow = models.BooleanField(_("Show in slideshow"), default=False)
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, blank=True, default="draft")

    objects = FestivalManager()

    row_level_permissions = True

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = _("Festival")
        verbose_name_plural = _("Festivals")

    def get_url_path(self):
        try:
            path = reverse("festival_detail", kwargs={'slug': self.slug})
        except:
            # the apphook is not attached yet
            return ""
        else:
            return path

    def get_social_media(self):
        return self.socialmediachannel_set.all()

    def get_pdfs(self):
        return self.festivalpdf_set.all()

    def set_owner(self, user):
        ContentType = models.get_model("contenttypes", "ContentType")
        PerObjectGroup = models.get_model("permissions", "PerObjectGroup")
        RowLevelPermission = models.get_model("permissions", "RowLevelPermission")
        try:
            role = PerObjectGroup.objects.get(
                sysname__startswith="owners",
                object_id=self.pk,
                content_type=ContentType.objects.get_for_model(Festival),
            )
        except PerObjectGroup.DoesNotExist:
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
                content_type=ContentType.objects.get_for_model(Festival),
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
                content_type=ContentType.objects.get_for_model(Festival),
            )
        except:
            return []
        return role.users.all()

    def _get_first_image(self):
        if not hasattr(self, '_first_image_cache'):
            self._first_image_cache = None
            qs = self.image_set.all()
            if qs.count():
                self._first_image_cache = qs[0]
        return self._first_image_cache
    first_image = property(_get_first_image)

    def duplicate(self, new_values=None):
        import os
        from distutils.dir_util import copy_tree
        from filebrowser.models import FileDescription
        if not new_values:
            new_values = {}

        # copy the model
        source_festival = self
        target_festival = Festival.objects.get(pk=self.pk)
        target_festival.pk = None

        for key, value in new_values.items():
            setattr(target_festival, key, value)

        target_festival.slug = get_unique_value(Festival, better_slugify(target_festival.title_de))
        target_festival.creation_date = None
        target_festival.modified_date = None
        target_festival.status = "draft"

        source_media_dir = "festivals/%s" % source_festival.slug
        target_media_dir = "festivals/%s" % target_festival.slug

        if source_festival.logo:
            target_festival.logo = source_festival.logo.path.replace(source_media_dir, target_media_dir)
        target_festival.save()
        # add m2m relationships
        target_festival.organizers = source_festival.organizers.all()
        # copy media directory
        abs_source_media_path = os.path.join(settings.MEDIA_ROOT, source_media_dir)
        abs_target_media_path = os.path.join(settings.MEDIA_ROOT, target_media_dir)
        if os.path.exists(abs_source_media_path):
            copy_tree(abs_source_media_path, abs_target_media_path)
        for file_desc in FileDescription.objects.filter(file_path__startswith=source_media_dir):
            file_desc.pk = None
            file_desc.file_path = file_desc.file_path.path.replace(source_media_dir, target_media_dir)
            file_desc.save()
        # add m2o relationships
        for image in source_festival.image_set.all():
            image.pk = None
            image.path = image.path.path.replace(source_media_dir, target_media_dir)
            image.festival = target_festival
            image.save()
        for social_media in source_festival.socialmediachannel_set.all():
            social_media.pk = None
            social_media.festival = target_festival
            social_media.save()
        for pdf in source_festival.festivalpdf_set.all():
            pdf.pk = None
            pdf.path = pdf.path.path.replace(source_media_dir, target_media_dir)
            pdf.production = target_festival
            pdf.save()
        # set ownership
        for owner in source_festival.get_owners():
            target_festival.set_owner(owner)
        return target_festival
    duplicate.alters_data = True

    def is_editable(self, user=None):
        from django.contrib.auth.models import AnonymousUser
        from base_libs.middleware.threadlocals import get_current_user
        if not hasattr(self, "_is_editable_cache"):
            user = get_current_user(user) or AnonymousUser()
            if user.has_perm("festivals.change_festival", self):
                return True
            # return True when the first editable location is found
            self._is_editable_cache = any((
                location.is_editable()
                for location in self.organizers.all()
            ))
        return self._is_editable_cache

    def is_deletable(self, user=None):
        return self.is_editable(user=user)

    def get_previous_item(self):
        try:
            return Festival.objects.filter(
                ~models.Q(pk=self.pk),
                start__lt=self.start,
                status="published",
                ).order_by("-start")[0]
        except:
            return None

    def get_next_item(self):
        try:
            return Festival.objects.filter(
                ~models.Q(pk=self.pk),
                start__gt=self.start,
                status="published",
                ).order_by("start")[0]
        except:
            return None


class Image(CreationModificationDateMixin):
    festival = models.ForeignKey(Festival, verbose_name=_("Festival"))
    path = FileBrowseField(_('File path'), max_length=255, directory="festivals/", extensions=['.jpg', '.jpeg', '.gif', '.png'], help_text=_("A path to a locally stored image."))
    copyright_restrictions = models.CharField(_('Copyright restrictions'), max_length=20, blank=True, choices=COPYRIGHT_RESTRICTION_CHOICES)
    sort_order = PositionField(_("Sort order"), collection="festival")

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
    festival = models.ForeignKey(Festival)
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

class FestivalPDF(CreationModificationDateMixin):
    festival = models.ForeignKey(Festival, verbose_name=_("Festival"))
    path = FileBrowseField(_('File path'), max_length=255, directory="festivals/", extensions=['.pdf'], help_text=_("A path to a locally stored PDF file."))
    sort_order = PositionField(_("Sort order"), collection="festival")

    class Meta:
        ordering = ["sort_order", "creation_date"]
        verbose_name = _("PDF")
        verbose_name_plural = _("PDFs")

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
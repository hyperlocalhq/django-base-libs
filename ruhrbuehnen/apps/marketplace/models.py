# -*- coding: UTF-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.conf import settings

from base_libs.models.models import CreationModificationDateMixin
from base_libs.models.models import CreationModificationMixin
from base_libs.models.models import PublishingMixin
from base_libs.models.models import UrlMixin
from base_libs.models.models import SlugMixin
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualTextField
from base_libs.models.fields import URLField
from base_libs.utils.misc import get_translation

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

SECURITY_SUMMAND = getattr(settings, "MARKETPLACE_SECURITY_SUMMAND", 7654102)


class JobType(CreationModificationDateMixin, SlugMixin()):
    title = MultilingualCharField(_('Title'), max_length=200)
    sort_order = models.IntegerField(_("Sort Order"), default=0)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['sort_order']
        verbose_name = _("Job type")
        verbose_name_plural = _("Job types")


class JobCategory(MPTTModel, CreationModificationDateMixin, SlugMixin()):
    parent = TreeForeignKey(
        'self', blank=True, null=True, related_name="children"
    )
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
            JobCategory.objects.insert_node(self, self.parent)
        super(JobCategory, self).save(*args, **kwargs)


class JobOfferManager(models.Manager):
    def accessible_to(self, user):
        from jetson.apps.permissions.models import PerObjectGroup
        if user.has_perm("marketplace.change_joboffer"):
            return self.get_queryset().exclude(status="trashed")
        ids = map(
            int,
            PerObjectGroup.objects.filter(
                content_type__app_label="marketplace",
                content_type__model="joboffer",
                sysname__startswith="owners",
                users=user,
            ).values_list("object_id", flat=True)
        )
        return self.get_queryset().filter(pk__in=ids).exclude(status="trashed")

    def owned_by(self, user):
        from jetson.apps.permissions.models import PerObjectGroup
        ids = map(
            int,
            PerObjectGroup.objects.filter(
                content_type__app_label="marketplace",
                content_type__model="joboffer",
                sysname__startswith="owners",
                users=user,
            ).values_list("object_id", flat=True)
        )
        return self.get_queryset().filter(pk__in=ids).exclude(status="trashed")


class JobOffer(CreationModificationMixin, UrlMixin):
    #title = MultilingualCharField(_("Title"), max_length=255)
    #subtitle = MultilingualCharField(_("Subtitle"), max_length=255, blank=True)
    description = MultilingualTextField(_("Description"), blank=True)
    remarks = MultilingualTextField(_("Remarks"), blank=True)
    position = MultilingualCharField(_('Position'), max_length=200)
    job_type = models.ForeignKey(
        JobType, verbose_name=_("Job type"), blank=True, null=True
    )
    deadline = models.DateField(_("Deadline"), blank=True, null=True)
    start_contract_on = models.DateField(
        _("Start contract on"), blank=True, null=True
    )
    categories = models.ManyToManyField(
        JobCategory, verbose_name=_("Categories"), blank=True
    )

    name = models.CharField(_("Name"), max_length=255, blank=True)
    company = models.CharField(_("Company"), max_length=255)
    street_address = models.CharField(_("Street address"), max_length=255)
    street_address2 = models.CharField(
        _("Street address (second line)"), max_length=255, blank=True
    )
    postal_code = models.CharField(_("Postal code"), max_length=255)
    city = models.CharField(_("City"), default="Berlin", max_length=255)
    latitude = models.FloatField(
        _("Latitude"),
        help_text=_(
            "Latitude (Lat.) is the angle between any point and the equator (north pole is at 90; south pole is at -90)."
        ),
        blank=True,
        null=True
    )
    longitude = models.FloatField(
        _("Longitude"),
        help_text=_(
            "Longitude (Long.) is the angle east or west of an arbitrary point on Earth from Greenwich (UK), which is the international zero-longitude point (longitude=0 degrees). The anti-meridian of Greenwich is both 180 (direction to east) and -180 (direction to west)."
        ),
        blank=True,
        null=True
    )

    phone_country = models.CharField(
        _("Country Code"), max_length=4, blank=True, default="49"
    )
    phone_area = models.CharField(_("Area Code"), max_length=6, blank=True)
    phone_number = models.CharField(
        _("Subscriber Number and Extension"), max_length=25, blank=True
    )
    fax_country = models.CharField(
        _("Country Code"), max_length=4, blank=True, default="49"
    )
    fax_area = models.CharField(_("Area Code"), max_length=6, blank=True)
    fax_number = models.CharField(
        _("Subscriber Number and Extension"), max_length=25, blank=True
    )
    email = models.EmailField(_("Email"), max_length=255, blank=True)
    website = URLField("Website", blank=True)

    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=STATUS_CHOICES,
        blank=True,
        default="draft"
    )

    objects = JobOfferManager()

    row_level_permissions = True

    def __unicode__(self):
        return self.position

    class Meta:
        ordering = ['position']
        verbose_name = _("Job Offer")
        verbose_name_plural = _("Job Offers")

    def get_url_path(self):
        try:
            path = reverse(
                "job_offer_detail", kwargs={'secure_id': self.get_secure_id()}
            )
        except:
            # the apphook is not attached yet
            return ""
        else:
            return path

    def set_owner(self, user):
        ContentType = models.get_model("contenttypes", "ContentType")
        PerObjectGroup = models.get_model("permissions", "PerObjectGroup")
        RowLevelPermission = models.get_model(
            "permissions", "RowLevelPermission"
        )
        try:
            role = PerObjectGroup.objects.get(
                sysname__startswith="owners",
                object_id=self.pk,
                content_type=ContentType.objects.get_for_model(JobOffer),
            )
        except PerObjectGroup.DoesNotExist:
            role = PerObjectGroup(sysname="owners", )
            for lang_code, lang_name in settings.LANGUAGES:
                setattr(
                    role, "position_%s" % lang_code,
                    get_translation("Owners", language=lang_code)
                )
            role.content_object = self
            role.save()

            RowLevelPermission.objects.create_default_row_permissions(
                model_instance=self,
                owner=role,
            )

        if not role.users.filter(pk=user.pk).count():
            role.users.add(user)

    def remove_owner(self, user):
        ContentType = models.get_model("contenttypes", "ContentType")
        PerObjectGroup = models.get_model("permissions", "PerObjectGroup")
        try:
            role = PerObjectGroup.objects.get(
                sysname__startswith="owners",
                object_id=self.pk,
                content_type=ContentType.objects.get_for_model(JobOffer),
            )
        except:
            return
        role.users.remove(user)
        if not role.users.count():
            role.delete()

    def get_owners(self):
        ContentType = models.get_model("contenttypes", "ContentType")
        PerObjectGroup = models.get_model("permissions", "PerObjectGroup")
        try:
            role = PerObjectGroup.objects.get(
                sysname__startswith="owners",
                object_id=self.pk,
                content_type=ContentType.objects.get_for_model(JobOffer),
            )
        except:
            return []
        return role.users.all()

    def get_secure_id(self):
        return int(self.pk) + SECURITY_SUMMAND

    def is_editable(self, user=None):
        from django.contrib.auth.models import AnonymousUser
        from base_libs.middleware.threadlocals import get_current_user
        if not hasattr(self, "_is_editable_cache"):
            user = get_current_user(user) or AnonymousUser()
            self._is_editable_cache = user.has_perm(
                "marketplace.change_joboffer", self
            )
        return self._is_editable_cache

    def is_deletable(self, user=None):
        from django.contrib.auth.models import AnonymousUser
        from base_libs.middleware.threadlocals import get_current_user
        if not hasattr(self, "_is_deletable_cache"):
            user = get_current_user(user) or AnonymousUser()
            self._is_deletable_cache = user.has_perm(
                "marketplace.delete_joboffer", self
            )
        return self._is_deletable_cache

    def get_previous_item(self):
        try:
            return JobOffer.objects.filter(
                ~models.Q(pk=self.pk),
                creation_date__lt=self.creation_date,
                status="published",
            ).order_by("-creation_date")[0]
        except:
            return None

    def get_next_item(self):
        try:
            return JobOffer.objects.filter(
                ~models.Q(pk=self.pk),
                creation_date__gt=self.creation_date,
                status="published",
            ).order_by("creation_date")[0]
        except:
            return None

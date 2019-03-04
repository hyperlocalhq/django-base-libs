# -*- coding: UTF-8 -*-
import os
import re
import calendar
import sys
from datetime import datetime
from urlparse import urlparse

from django.db import models
from django.db.models.base import ModelBase
from django.db.models.fields import FieldDoesNotExist
from django.conf import settings
from django.utils import dateformat

if "makemigrations" in sys.argv:
    from django.utils.translation import ugettext_noop as _
else:
    from django.utils.translation import ugettext_lazy as _

from django.utils.translation import ugettext
from django.utils.safestring import mark_safe
from django.utils.functional import lazy
from django.utils.encoding import force_unicode
from django.utils.text import capfirst
from django.utils.timezone import now as tz_now
from django.apps import apps

from base_libs.models.models import UrlMixin
from base_libs.models.models import SlugMixin
from base_libs.models.models import CreationModificationMixin
from base_libs.models.models import PublishingMixin
from base_libs.utils.misc import get_unique_value
from base_libs.utils.misc import get_website_url
from base_libs.utils.misc import is_installed
from base_libs.middleware import get_current_language, get_current_user
from base_libs.models.query import ExtendedQuerySet
from base_libs.models.fields import URLField
from base_libs.models.fields import MultilingualCharField
from base_libs.models.base_libs_settings import STATUS_CODE_PUBLISHED

from tagging.models import Tag
from tagging_autocomplete.models import TagAutocompleteField

from jetson.apps.location.models import Address
from jetson.apps.optionset.models import PhoneType, EmailType, URLType, IMType
from jetson.apps.optionset.models import get_default_phonetype_for_phone
from jetson.apps.optionset.models import get_default_phonetype_for_fax
from jetson.apps.optionset.models import get_default_phonetype_for_mobile

verbose_name = _("Marketplace")

YEAR_CHOICES = [(i, i) for i in range(1997, tz_now().year + 10)]

DAY_CHOICES = [(i, i) for i in range(1, 32)]

HOUR_CHOICES = [(i, i) for i in range(0, 24)]

MINUTE_CHOICES = [(i, "%02d" % i) for i in range(0, 60)]

URL_ID_JOB_OFFER = getattr(settings, "URL_ID_JOB_OFFER", "job")
URL_ID_JOB_OFFERS = getattr(settings, "URL_ID_JOB_OFFERS", "jobs")

SECURITY_SUMMAND = getattr(settings, "MARKETPLACE_SECURITY_SUMMAND", 7654102)


def get_default_url_type():
    try:
        return URLType.objects.get(slug="homepage").pk
    except:
        return None


class JobType(SlugMixin()):
    title = MultilingualCharField(_("title"), max_length=255)
    sort_order = models.IntegerField(_("Sort order"), default=0)
    is_internship = models.BooleanField(_("Internship?"), default=False)

    class Meta:
        verbose_name = _("job type")
        verbose_name_plural = _("job types")
        ordering = ['sort_order', 'title']

    def __unicode__(self):
        return self.title


class JobQualification(SlugMixin()):
    title = MultilingualCharField(_("title"), max_length=255)
    sort_order = models.IntegerField(_("Sort order"), default=0)

    class Meta:
        verbose_name = _("qualification")
        verbose_name_plural = _("qualifications")
        ordering = ['sort_order', 'title']

    def __unicode__(self):
        return self.title


class JobSector(SlugMixin()):
    title = MultilingualCharField(_("title"), max_length=255)
    sort_order = models.IntegerField(_("Sort order"), default=0)

    class Meta:
        verbose_name = _("job sector")
        verbose_name_plural = _("job sectors")
        ordering = ['sort_order', 'title']

    def __unicode__(self):
        return self.title


class JobOfferManager(models.Manager):
    """
    for comments, see institutions.InstitutionManager
    """

    def get_queryset(self):
        return ExtendedQuerySet(self.model)

    def get_sort_order_mapper(self):
        sort_order_mapper = {
            'creation_date_desc': (
                1,
                _('Creation date'),
                ['-creation_date'],
            ),
            'published_from_desc':
                (
                    2,
                    _('Publishing date'),
                    ['-published_from'],
                ),
            'alphabetical_asc': (
                3,
                _('Alphabetical'),
                ['position'],
            ),
        }
        return sort_order_mapper

    def latest_published(self):
        return self.filter(
            status=STATUS_CODE_PUBLISHED,
        ).order_by("-published_from")


class JobOfferBase(CreationModificationMixin, PublishingMixin, UrlMixin):
    """
    The base class for the job offer.
    """

    position = models.CharField(_("Position"), max_length=255)
    description = models.TextField(_("Description"), blank=True)

    job_type = models.ForeignKey(
        JobType,
        verbose_name=_("Job type"),
    )

    qualifications = models.ManyToManyField(
        JobQualification,
        verbose_name=_("Qualifications"),
        related_name="joboffers",
        blank=True,
    )

    job_sectors = models.ManyToManyField(
        JobSector,
        verbose_name=_("Job sectors"),
        related_name="job_sector_joboffers",
        blank=True,
    )

    if is_installed("institutions.models"):
        offering_institution = models.ForeignKey(
            "institutions.Institution",
            verbose_name=_("Organizing institution"),
            blank=True,
            null=True,
        )

    offering_institution_title = models.CharField(
        _("Organizer"), blank=True, max_length=255
    )

    if is_installed("people.models"):
        contact_person = models.ForeignKey(
            "people.Person",
            verbose_name=_("Organizing person"),
            blank=True,
            null=True,
            related_name="jobs_posted",
        )

    contact_person_name = models.CharField(
        _("Organizer"), blank=True, max_length=255
    )

    postal_address = models.ForeignKey(
        Address,
        verbose_name=_("Postal Address"),
        related_name="address_job_offers",
        null=True,
        blank=True
    )

    additional_info = models.TextField(_("Additional Info"), blank=True)

    # PHONES

    phone0_type = models.ForeignKey(
        PhoneType,
        verbose_name=_("Phone Type"),
        blank=True,
        null=True,
        related_name='job_offers0',
        default=get_default_phonetype_for_phone
    )
    phone0_country = models.CharField(
        _("Country Code"), max_length=4, blank=True, default="49"
    )
    phone0_area = models.CharField(
        _("Area Code"), max_length=6, blank=True, default="30"
    )
    phone0_number = models.CharField(
        _("Subscriber Number and Extension"), max_length=25, blank=True
    )
    is_phone0_default = models.BooleanField(_("Default?"), default=True)
    is_phone0_on_hold = models.BooleanField(_("On Hold?"), default=False)

    phone1_type = models.ForeignKey(
        PhoneType,
        verbose_name=_("Phone Type"),
        blank=True,
        null=True,
        related_name='job_offers1',
        default=get_default_phonetype_for_fax
    )
    phone1_country = models.CharField(
        _("Country Code"), max_length=4, blank=True, default="49"
    )
    phone1_area = models.CharField(
        _("Area Code"), max_length=6, blank=True, default="30"
    )
    phone1_number = models.CharField(
        _("Subscriber Number and Extension"), max_length=25, blank=True
    )
    is_phone1_default = models.BooleanField(_("Default?"), default=False)
    is_phone1_on_hold = models.BooleanField(_("On Hold?"), default=False)

    phone2_type = models.ForeignKey(
        PhoneType,
        verbose_name=_("Phone Type"),
        blank=True,
        null=True,
        related_name='job_offers2',
        default=get_default_phonetype_for_mobile
    )
    phone2_country = models.CharField(
        _("Country Code"), max_length=4, blank=True, default="49"
    )
    phone2_area = models.CharField(_("Area Code"), max_length=6, blank=True)
    phone2_number = models.CharField(
        _("Subscriber Number and Extension"), max_length=25, blank=True
    )
    is_phone2_default = models.BooleanField(_("Default?"), default=False)
    is_phone2_on_hold = models.BooleanField(_("On Hold?"), default=False)

    # WEBSITES

    url0_type = models.ForeignKey(
        URLType,
        verbose_name=_("URL Type"),
        blank=True,
        null=True,
        related_name='job_offers0',
        on_delete=models.SET_NULL
    )
    url0_link = URLField(_("URL"), max_length=500, blank=True)
    is_url0_default = models.BooleanField(_("Default?"), default=True)
    is_url0_on_hold = models.BooleanField(_("On Hold?"), default=False)

    url1_type = models.ForeignKey(
        URLType,
        verbose_name=_("URL Type"),
        blank=True,
        null=True,
        related_name='job_offers1',
        on_delete=models.SET_NULL
    )
    url1_link = URLField(_("URL"), max_length=500, blank=True)
    is_url1_default = models.BooleanField(_("Default?"), default=False)
    is_url1_on_hold = models.BooleanField(_("On Hold?"), default=False)

    url2_type = models.ForeignKey(
        URLType,
        verbose_name=_("URL Type"),
        blank=True,
        null=True,
        related_name='job_offers2',
        on_delete=models.SET_NULL
    )
    url2_link = URLField(_("URL"), max_length=500, blank=True)
    is_url2_default = models.BooleanField(_("Default?"), default=False)
    is_url2_on_hold = models.BooleanField(_("On Hold?"), default=False)

    # INSTANT MESSENGERS

    im0_type = models.ForeignKey(
        IMType,
        verbose_name=_("IM Type"),
        blank=True,
        null=True,
        related_name='job_offers0',
        on_delete=models.SET_NULL
    )
    im0_address = models.CharField(
        _("Instant Messenger"), blank=True, max_length=255
    )
    is_im0_default = models.BooleanField(_("Default?"), default=True)
    is_im0_on_hold = models.BooleanField(_("On Hold?"), default=False)

    im1_type = models.ForeignKey(
        IMType,
        verbose_name=_("IM Type"),
        blank=True,
        null=True,
        related_name='job_offers1',
        on_delete=models.SET_NULL
    )
    im1_address = models.CharField(
        _("Instant Messenger"), blank=True, max_length=255
    )
    is_im1_default = models.BooleanField(_("Default?"), default=False)
    is_im1_on_hold = models.BooleanField(_("On Hold?"), default=False)

    im2_type = models.ForeignKey(
        IMType,
        verbose_name=_("IM Type"),
        blank=True,
        null=True,
        related_name='job_offers2',
        on_delete=models.SET_NULL
    )
    im2_address = models.CharField(
        _("Instant Messenger"), blank=True, max_length=255
    )
    is_im2_default = models.BooleanField(_("Default?"), default=False)
    is_im2_on_hold = models.BooleanField(_("On Hold?"), default=False)

    # EMAILS

    email0_type = models.ForeignKey(
        EmailType,
        verbose_name=_("Email Type"),
        blank=True,
        null=True,
        related_name='job_offers0',
        on_delete=models.SET_NULL
    )
    email0_address = models.CharField(
        _("Email Address"), blank=True, max_length=255
    )
    is_email0_default = models.BooleanField(_("Default?"), default=True)
    is_email0_on_hold = models.BooleanField(_("On Hold?"), default=False)

    email1_type = models.ForeignKey(
        EmailType,
        verbose_name=_("Email Type"),
        blank=True,
        null=True,
        related_name='job_offers1',
        on_delete=models.SET_NULL
    )
    email1_address = models.CharField(
        _("Email Address"), blank=True, max_length=255
    )
    is_email1_default = models.BooleanField(_("Default?"), default=False)
    is_email1_on_hold = models.BooleanField(_("On Hold?"), default=False)

    email2_type = models.ForeignKey(
        EmailType,
        verbose_name=_("Email Type"),
        blank=True,
        null=True,
        related_name='job_offers2',
        on_delete=models.SET_NULL
    )
    email2_address = models.CharField(
        _("Email Address"), blank=True, max_length=255
    )
    is_email2_default = models.BooleanField(_("Default?"), default=False)
    is_email2_on_hold = models.BooleanField(_("On Hold?"), default=False)

    tags = TagAutocompleteField(verbose_name=_("tags"))

    publish_emails = models.BooleanField(
        _("Show email addresses to unregistered visitors?"), default=False
    )
    is_commercial = models.BooleanField(
        _("One has to pay to get information about the job"), default=False
    )

    row_level_permissions = True

    objects = JobOfferManager()

    class Meta:
        abstract = True
        verbose_name = _("job offer")
        verbose_name_plural = _("job offers")
        ordering = ['position', 'creation_date']

    def __unicode__(self):
        return self.position

    def is_job_offer(self):
        return True

    def get_url_path(self):
        from django.conf import settings
        return "/%s/%s/" % (URL_ID_JOB_OFFER, self.get_secure_id())

    def get_description(self, language=None):
        language = language or get_current_language()
        return mark_safe(
            getattr(self, "description_%s" % language, "") or self.description
        )

    def get_tags(self):
        return Tag.objects.get_for_object(self)

    def get_object_types(self):
        return self.job_type and [self.job_type] or []

    def get_contacts(self):
        if self.get_postal_address() or self.get_phones() or self.get_urls(
        ) or self.get_ims() or self.get_emails():
            l = [self]
            return l
        return None

    def get_postal_address(self):
        return self.postal_address

    def get_phones(self):
        if not hasattr(self, '_phones_cache'):
            self._phones_cache = [
                {
                    "type": getattr(self, "phone%d_type" % pos),
                    "country": getattr(self, "phone%d_country" % pos),
                    "area": getattr(self, "phone%d_area" % pos),
                    "number": getattr(self, "phone%d_number" % pos),
                    "is_default": getattr(self, "is_phone%d_default" % pos),
                    "is_on_hold": getattr(self, "is_phone%d_on_hold" % pos),
                }
                for pos in range(3) if getattr(self, "phone%d_number" % pos) and
                not getattr(self, "is_phone%d_on_hold" % pos)
            ]
            self._phones_cache.sort(
                lambda p1, p2: cmp(p2['is_default'], p1['is_default'])
            )
        return self._phones_cache

    def get_urls(self):
        if not hasattr(self, '_urls_cache'):
            self._urls_cache = [
                {
                    "type":
                        getattr(self, "url%d_type" % pos),
                    "link":
                        getattr(self, "url%d_link" % pos),
                    "domain":
                        urlparse(getattr(self, "url%d_link" % pos)).netloc,
                    "is_default":
                        getattr(self, "is_url%d_default" % pos),
                    "is_on_hold":
                        getattr(self, "is_url%d_on_hold" % pos),
                } for pos in range(3) if getattr(self, "url%d_link" % pos) and
                not getattr(self, "is_url%d_on_hold" % pos)
            ]
            self._urls_cache.sort(
                lambda p1, p2: cmp(p2['is_default'], p1['is_default'])
            )

        return self._urls_cache

    def get_ims(self):
        if not hasattr(self, '_ims_cache'):
            self._ims_cache = [
                {
                    "type": getattr(self, "im%d_type" % pos),
                    "address": getattr(self, "im%d_address" % pos),
                    "is_default": getattr(self, "is_im%d_default" % pos),
                    "is_on_hold": getattr(self, "is_im%d_on_hold" % pos),
                } for pos in range(3) if getattr(self, "im%d_address" % pos) and
                not getattr(self, "is_im%d_on_hold" % pos)
            ]
            self._ims_cache.sort(
                lambda p1, p2: cmp(p2['is_default'], p1['is_default'])
            )

        return self._ims_cache

    def get_emails(self):
        if not hasattr(self, '_emails_cache'):
            self._emails_cache = [
                {
                    "type":
                        getattr(self, "email%d_type" % pos),
                    "address":
                        getattr(self, "email%d_address" % pos),
                    "address_protected":
                        getattr(self, "email%d_address" % pos).replace(
                            "@", ugettext(" (at) ")
                        ).replace(".", ugettext(" (dot) ")),
                    "is_default":
                        getattr(self, "is_email%d_default" % pos),
                    "is_on_hold":
                        getattr(self, "is_email%d_on_hold" % pos),
                } for pos in range(3)
                if getattr(self, "email%d_address" % pos) and
                not getattr(self, "is_email%d_on_hold" % pos)
            ]
            self._emails_cache.sort(
                lambda p1, p2: cmp(p2['is_default'], p1['is_default'])
            )

        return self._emails_cache

    def are_contacts_displayed(self, user=None):
        if not hasattr(self, "_are_contacts_displayed_cache"):
            user = get_current_user(user)
            self._are_contacts_displayed_cache = bool(
                self.postal_address or
                (user and user.has_perm("marketplace.change_job_offer", self))
            )
        return self._are_contacts_displayed_cache

    def get_additional_search_data(self):
        """ used by ContextItemManager """
        search_data = []
        # add urls
        for url in self.get_urls():
            search_data.append(url["link"])
        search_data.append(self.tags)
        return search_data

    def get_secure_id(self):
        return int(self.pk) + SECURITY_SUMMAND

    def save(self, *args, **kwargs):
        from jetson.apps.permissions.models import RowLevelPermission
        is_new = not self.id

        super(JobOfferBase, self).save(*args, **kwargs)

        if is_new:
            if self.creator:
                RowLevelPermission.objects.create_default_row_permissions(
                    model_instance=self,
                    owner=self.creator,
                )
            if getattr(self, "contact_person", None):
                if self.creator != self.contact_person.user:
                    RowLevelPermission.objects.create_default_row_permissions(
                        model_instance=self,
                        owner=self.contact_person.user,
                    )
            if getattr(self, "offering_institution", None):
                for role in self.offering_institution.get_object_permission_roles(
                ):
                    RowLevelPermission.objects.create_default_row_permissions(
                        model_instance=self,
                        owner=role,
                    )

    save.alters_data = True

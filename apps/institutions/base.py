# -*- coding: UTF-8 -*-
import os
import re
import StringIO
import codecs
import vobject
from datetime import datetime, date

from django.db import models
from django.db.models.base import ModelBase
from django.db.models.fields import FieldDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.utils.functional import lazy
from django.utils.encoding import force_unicode
from django.conf import settings
from django.utils.timezone import now as tz_now
from django.apps import apps

from base_libs.models.models import UrlMixin
from base_libs.models.models import CreationModificationDateMixin
from base_libs.models.models import OpeningHoursMixin
from base_libs.models import SlugMixin
from base_libs.utils.misc import get_unique_value
from base_libs.utils.misc import get_website_url
from base_libs.utils.betterslugify import better_slugify
from base_libs.middleware import get_current_language
from base_libs.middleware import get_current_user
from base_libs.models.query import ExtendedQuerySet
from base_libs.models.fields import URLField
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualTextField
from base_libs.models.fields import ExtendedTextField  # for south

from filebrowser.fields import FileBrowseField

from jetson.apps.structure.models import Term
from jetson.apps.structure.models import ContextCategory
from jetson.apps.structure.models import Category
from jetson.apps.location.models import Address
from jetson.apps.optionset.models import InstitutionalLocationType
from jetson.apps.optionset.models import PhoneType
from jetson.apps.optionset.models import EmailType
from jetson.apps.optionset.models import URLType
from jetson.apps.optionset.models import IMType
from jetson.apps.optionset.models import get_default_phonetype_for_phone
from jetson.apps.optionset.models import get_default_phonetype_for_fax
from jetson.apps.optionset.models import get_default_phonetype_for_mobile

from jetson.apps.utils.models import MONTH_CHOICES
from jetson.apps.image_mods.models import FileManager

from mptt.models import MPTTModel
from mptt.managers import TreeManager
from mptt.fields import TreeForeignKey, TreeManyToManyField

verbose_name = _("Institutions")

### Institution class ###


def get_default_url_type():
    try:
        return URLType.objects.get(slug="homepage").id
    except:
        return None


STATUS_CHOICES = (
    ('draft', _("Draft")),
    ('published', _("Published")),
    ('published_commercial', _("Published-Commercial")),
    ('not_listed', _("Not Listed")),
    ('import', _("Imported")),
    ('event_location', _("Event Location")),
)

YEAR_OF_ESTABLISHMENT_CHOICES = [
    (i, i) for i in range(tz_now().year,
                          tz_now().year - 200, -1)
]

YEAR_OF_VALIDITY_CHOICES = [
    (i, i) for i in range(tz_now().year - 10,
                          tz_now().year + 10)
]

DAY_CHOICES = [(i, i) for i in range(1, 32)]

URL_ID_INSTITUTION = getattr(settings, "URL_ID_INSTITUTION", "institution")
URL_ID_INSTITUTIONS = getattr(settings, "URL_ID_INSTITUTIONS", "institutions")

DEFAULT_LOGO_4_INSTITUTION = getattr(
    settings,
    "DEFAULT_LOGO_4_INSTITUTION",
    "%ssite/img/website/placeholder/institution.png" % settings.STATIC_URL,
)
DEFAULT_FORM_LOGO_4_INSTITUTION = getattr(
    settings,
    "DEFAULT_FORM_LOGO_4_INSTITUTION",
    "%ssite/img/website/placeholder/institution_f.png" % settings.STATIC_URL,
)
DEFAULT_SMALL_LOGO_4_INSTITUTION = getattr(
    settings,
    "DEFAULT_SMALL_LOGO_4_INSTITUTION",
    "%ssite/img/website/placeholder/institution_s.png" % settings.STATIC_URL,
)


def get_default_ins_loc_type():
    try:
        return InstitutionalLocationType.objects.get(slug="main").id
    except:
        return None


def get_utf8buffer():
    f = StringIO.StringIO()
    enc, dec, reader, writer = codecs.lookup("utf-8")
    srw = codecs.StreamReaderWriter(f, reader, writer, errors="strict")
    srw.encoding = "utf-8"
    return srw


class LegalForm(CreationModificationDateMixin, SlugMixin()):
    title = MultilingualCharField(_('title'), max_length=200)
    sort_order = models.IntegerField(_("Sort Order"), default=0)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['sort_order']
        verbose_name = _("Legal Form")
        verbose_name_plural = _("Legal Forms")


class InstitutionType(MPTTModel, SlugMixin()):
    sort_order = models.IntegerField(
        _("sort order"),
        blank=True,
        editable=False,
        default=0,
    )
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
        verbose_name = _("institution type")
        verbose_name_plural = _("institution types")
        ordering = ["tree_id", "lft"]

    class MPTTMeta:
        order_insertion_by = ['sort_order']

    def __unicode__(self):
        return self.title

    def get_title(self, prefix="", postfix=""):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            InstitutionType.objects.insert_node(self, self.parent)
        super(InstitutionType, self).save(*args, **kwargs)


class InstitutionManager(models.Manager):
    def get_queryset(self):
        return ExtendedQuerySet(self.model)

    """
    sort_order mapper is a dictionary containing information for list sort_order:
    the key is a string (whatever you want)
    the value tuple contains three values:
        1. A display value
        2. The sort_order field of the model (optionally with preceeding "-"
        3. An sort_order indicator for the selectboxes. The one with the lowest index is the default sort_order.
    """

    def get_sort_order_mapper(self):
        sort_order_mapper = {
            'creation_date_desc': (
                1,
                _('Creation date'),
                ['-creation_date'],
            ),
            'alphabetical_asc': (
                2,
                _('Alphabetical'),
                ['title'],
            ),
        }
        return sort_order_mapper

    def latest_published(self):
        return self.filter(
            status__in=("published", "published_commercial"),
        ).order_by("-creation_date")


class InstitutionBase(
    CreationModificationDateMixin, UrlMixin, OpeningHoursMixin
):
    """
    The base class for the institution. Wherever institution is located - jetson or site-specific project - it should be in an app called "institutions" and it should be called "Institution"
    """

    title = models.CharField(_("Title"), max_length=255)
    title2 = models.CharField(
        _("Title (second line)"), max_length=255, blank=True
    )
    slug = models.CharField(_("Slug"), max_length=255)
    parent = models.ForeignKey(
        "self", verbose_name=_("Member of"), blank=True, null=True
    )
    description = MultilingualTextField(_("Description"), blank=True)

    image = FileBrowseField(
        _('Image'),
        max_length=255,
        directory="%s/" % URL_ID_INSTITUTIONS,
        extensions=['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff'],
        blank=True
    )

    institution_types = TreeManyToManyField(
        InstitutionType,
        verbose_name=_("Types"),
    )
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=STATUS_CHOICES,
        blank=True,
        default="draft"
    )
    legal_form = models.ForeignKey(
        LegalForm,
        verbose_name=_("Legal form"),
        blank=True,
        null=True,
        related_name="legal_form_institution"
    )

    context_categories = TreeManyToManyField(
        ContextCategory,
        verbose_name=_("Context categories"),
        limit_choices_to={'is_applied4institution': True},
        blank=True
    )

    # D E T A I L S

    access = models.CharField(_("Access"), max_length=255, blank=True)
    is_parking_avail = models.BooleanField(
        _("Is parking available?"), default=False
    )
    is_wlan_avail = models.BooleanField(
        _("Is WLAN Internet available?"), default=False
    )

    # TYPE

    is_non_profit = models.BooleanField(
        _("Non profit (business elsewhere)?"), default=False
    )
    tax_id_number = models.CharField(_("Tax ID"), max_length=100, blank=True)
    vat_id_number = models.CharField(_("VAT ID"), max_length=100, blank=True)

    # CARDS ACCEPTED

    is_card_visa_ok = models.BooleanField(_("Visa"), default=False)
    is_card_mastercard_ok = models.BooleanField(_("MasterCard"), default=False)
    is_card_americanexpress_ok = models.BooleanField(
        _("American Express"), default=False
    )
    is_paypal_ok = models.BooleanField(_("PayPal"), default=False)
    is_cash_ok = models.BooleanField(_("Cash"), default=False)
    is_transaction_ok = models.BooleanField(_("Bank transfer"), default=False)
    is_prepayment_ok = models.BooleanField(_("Prepayment"), default=False)
    is_on_delivery_ok = models.BooleanField(
        _("Payment on delivery"), default=False
    )
    is_invoice_ok = models.BooleanField(_("Invoice"), default=False)
    is_ec_maestro_ok = models.BooleanField(_("EC Maestro"), default=False)
    is_giropay_ok = models.BooleanField(_("Giropay"), default=False)

    establishment_yyyy = models.IntegerField(
        _("Year of Establishment"),
        blank=True,
        null=True,
        choices=YEAR_OF_ESTABLISHMENT_CHOICES
    )
    establishment_mm = models.SmallIntegerField(
        _("Month of Establishment"),
        blank=True,
        null=True,
        choices=MONTH_CHOICES
    )
    nof_employees = models.IntegerField(
        _("Number of Employees"), blank=True, null=True
    )

    row_level_permissions = True

    objects = InstitutionManager()

    class Meta:
        ordering = ('title', 'title2')
        verbose_name = _("institution (place)")
        verbose_name_plural = _("institutions (places)")
        #db_table = "accounts_institution"
        abstract = True

    def is_institution(self):
        return True

    def has_maps(self):
        return bool(self.get_primary_contact())

    def has_photos(self):
        return False

    def has_videos(self):
        return False

    def get_absolute_url(self):
        from django.conf import settings
        return "%snetwork/member/%s/" % (get_website_url(), self.slug)

    def get_url_path(self):
        from django.conf import settings
        return "/network/member/%s/" % (self.slug, )

    def get_title(self):
        return u", ".join(
            [force_unicode(item) for item in (self.title, self.title2) if item]
        ).strip()
        #return ("%s %s" % (
        #    force_unicode(self.title),
        #    force_unicode(self.title2),
        #    )).strip()

    def get_slug(self):
        return self.slug

    def __unicode__(self):
        return force_unicode(self.title)

    def get_supported_payments(self):
        all_payments = [
            "is_card_visa_ok", "is_card_mastercard_ok",
            "is_card_americanexpress_ok", "is_paypal_ok", "is_cash_ok",
            "is_transaction_ok", "is_prepayment_ok", "is_on_delivery_ok",
            "is_invoice_ok", "is_ec_maestro_ok", "is_giropay_ok"
        ]
        supported_payments = [
            force_unicode(type(self)._meta.get_field(field_name).verbose_name)
            for field_name in all_payments if getattr(self, field_name, False)
        ]
        return supported_payments

    title_en = property(get_title)
    title_de = property(get_title)

    def get_address_string(self):
        contact = self.get_primary_contact()
        if not contact:
            return ""
        address_components = []
        if contact.get("street_address", ""):
            address_components.append(contact["street_address"])
        combo = []
        if contact.get("postal_code", ""):
            combo.append(contact["postal_code"])
        if contact.get("city", ""):
            combo.append(contact["city"])
        if combo:
            address_components.append(" ".join(combo))
        if contact.get("country_name", ""):
            address_components.append(contact["country_name"])
        return ", ".join(address_components)

    def get_description(self, language=None):
        language = language or get_current_language()
        return mark_safe(
            getattr(self, "description_%s" % language, "") or self.description
        )

    def get_institution_types(self):
        return self.institution_types.all()

    def get_locality_type(self):
        from jetson.apps.location.models import LocalityType
        contacts = self.get_contacts(cache=False)
        if contacts and contacts[0].postal_address:
            postal_address = contacts[0].postal_address
            if postal_address.country_id != "DE":
                international, _created = LocalityType.objects.get_or_create(
                    slug="international",
                    defaults=dict(
                        title_de="International",
                        title_en="International",
                    )
                )
                return international
            elif postal_address.city.lower() != "berlin":
                national, _created = LocalityType.objects.get_or_create(
                    slug="national",
                    defaults=dict(
                        title_de="National",
                        title_en="National",
                    )
                )
                return national
            else:
                import re
                from jetson.apps.location.data import POSTAL_CODE_2_DISTRICT
                locality = postal_address.get_locality()
                regional, _created = LocalityType.objects.get_or_create(
                    slug="regional",
                    defaults=dict(
                        title_de="Regional",
                        title_en="Regional",
                    )
                )
                p = re.compile('[^\d]*')  # remove non numbers
                postal_code = p.sub("", postal_address.postal_code)

                district = ""
                if locality and locality.district:
                    district = locality.district
                elif postal_code in POSTAL_CODE_2_DISTRICT:
                    district = POSTAL_CODE_2_DISTRICT[postal_code]
                if district:
                    try:
                        return LocalityType.objects.get(
                            slug=better_slugify(district),
                            parent=regional,
                        )
                    except LocalityType.DoesNotExist:
                        pass
                return regional
        else:
            return None

    def get_object_types(self):
        return self.get_institution_types()

    def get_context_categories(self):
        return self.context_categories.all()

    def get_primary_contact(self):
        """returns a dictionary containing primary contact information"""
        contact_dict = {}
        primary_contact = self.institutionalcontact_set.filter(is_primary=True)
        if primary_contact:
            primary_contact = primary_contact[0]
            contact_dict = primary_contact.__dict__
            address = primary_contact.postal_address
            for phone in primary_contact.get_phones():
                if phone['type']:
                    if phone[
                        'type'
                    ].slug == "phone" and "phone_number" not in contact_dict:
                        contact_dict['phone_country'] = phone['country']
                        contact_dict['phone_area'] = phone['area']
                        contact_dict['phone_number'] = phone['number']
                    elif phone[
                        'type'
                    ].slug == "fax" and "fax_number" not in contact_dict:
                        contact_dict['fax_country'] = phone['country']
                        contact_dict['fax_area'] = phone['area']
                        contact_dict['fax_number'] = phone['number']
                    elif phone[
                        'type'
                    ].slug == "mobile" and "mobile_number" not in contact_dict:
                        contact_dict['mobile_country'] = phone['country']
                        contact_dict['mobile_area'] = phone['area']
                        contact_dict['mobile_number'] = phone['number']
            if address:
                contact_dict.update(address.get_dict())
                if address.country:
                    contact_dict['country_name'] = address.country.get_name()
                contact_dict.pop('_postal_address_cache', '')
                contact_dict.pop('_phones_cache', '')
        return contact_dict

    def get_contacts(self, cache=True):
        if not hasattr(self, "_contacts_cache") or not cache:
            self._contacts_cache = self.institutionalcontact_set.order_by(
                '-is_primary', 'id'
            )
        return self._contacts_cache

    def get_neighborhoods(self):
        if not hasattr(self, '_neighborhoods_cache'):
            neighborhoods = []
            contact_queryset = self.institutionalcontact_set.all()
            for contact in contact_queryset:
                try:
                    neighborhood = contact.postal_address.get_locality(
                    ).neighborhood
                except:
                    pass
                else:
                    if neighborhood:
                        neighborhoods.append(neighborhood)
            self._neighborhoods_cache = neighborhoods
        return self._neighborhoods_cache

    def get_contact_persons(self):
        if not hasattr(self, "_contact_persons_cache"):
            self._contact_persons_cache = [
                contact.person for contact in self.individualcontact_set.all()
            ]
        return self._contact_persons_cache

    def save(self, *args, **kwargs):
        title = self.get_title()
        if not self.slug:
            self.slug = title
        self.slug = get_unique_value(
            self.__class__,
            better_slugify(self.slug),
            separator="_",
            instance_pk=self.id,
        )
        super(InstitutionBase, self).save(*args, **kwargs)

    save.alters_data = True

    def delete(self, *args, **kwargs):
        FileManager.delete_file(self.get_filebrowser_dir())
        super(InstitutionBase, self).delete(*args, **kwargs)

    delete.alters_data = True

    # information visibility

    def are_opening_hours_displayed(self, user=None):
        if not hasattr(self, "_are_opening_hours_displayed_cache"):
            user = get_current_user(user)
            self._are_opening_hours_displayed_cache = (
                self.has_opening_hours() or (
                    user and
                    user.has_perm("institutions.change_institution", self)
                )
            )
        return self._are_opening_hours_displayed_cache

    def are_payments_displayed(self, user=None):
        if not hasattr(self, "_are_payments_displayed_cache"):
            user = get_current_user(user)
            self._are_payments_displayed_cache = (
                self.get_supported_payments() or (
                    user and
                    user.has_perm("institutions.change_institution", self)
                )
            )
        return self._are_payments_displayed_cache

    def get_filebrowser_dir(self):
        return "%s/%s/" % (
            URL_ID_INSTITUTIONS,
            self.slug,
        )

    def get_additional_search_data(self):
        """ used by ContextItemManager """
        search_data = []
        # add urls
        contacts = self.get_contacts(cache=False)
        if contacts:
            for contact in contacts:
                for url in contact.get_urls():
                    search_data.append(url['link'])
        return search_data

    @staticmethod
    def autocomplete_search_fields():
        return (
            "id__iexact",
            "title__icontains",
            "title2__icontains",
        )


### InstitutionalContact


class InstitutionalContactBase(models.Model):
    """
    The base class for the institutional contact. Wherever it is located - jetson or site-specific project - it should be in an app called "institutions" and it should be called "InstitutionalContact"
    """

    # a foreign key to Institution will be added when Institution is created
    institution = models.ForeignKey(
        "institutions.Institution",
        verbose_name=_("Institution"),
    )

    location_type = models.ForeignKey(
        InstitutionalLocationType,
        verbose_name=_("Location type"),
        default=get_default_ins_loc_type
    )
    location_title = models.CharField(
        _("Location title"), max_length=255, blank=True
    )
    is_primary = models.BooleanField(_("Primary contact"), default=True)

    is_temporary = models.BooleanField(_("Temporary"), default=False)
    validity_start_yyyy = models.IntegerField(
        _("From Year"), blank=True, null=True, choices=YEAR_OF_VALIDITY_CHOICES
    )
    validity_start_mm = models.SmallIntegerField(
        _("From Month"), blank=True, null=True, choices=MONTH_CHOICES
    )
    validity_start_dd = models.SmallIntegerField(
        _("From Day"), blank=True, null=True, choices=DAY_CHOICES
    )
    validity_end_yyyy = models.IntegerField(
        _("Till Year"), blank=True, null=True, choices=YEAR_OF_VALIDITY_CHOICES
    )
    validity_end_mm = models.SmallIntegerField(
        _("Till Month"), blank=True, null=True, choices=MONTH_CHOICES
    )
    validity_end_dd = models.SmallIntegerField(
        _("Till Day"), blank=True, null=True, choices=DAY_CHOICES
    )

    postal_address = models.ForeignKey(
        Address,
        verbose_name=_("Postal Address"),
        related_name="institutional_address",
        null=True,
        blank=True
    )
    is_billing_address = models.BooleanField(
        _("Use this address for billing"), default=True
    )
    is_shipping_address = models.BooleanField(
        _("Use this address for shipping"), default=True
    )

    # PHONES

    phone0_type = models.ForeignKey(
        PhoneType,
        verbose_name=_("Phone Type"),
        blank=True,
        null=True,
        related_name='institutional_contacts0',
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
        related_name='institutional_contacts1',
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
        related_name='institutional_contacts2',
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
        related_name='institutional_contacts0',
        on_delete=models.SET_NULL
    )
    url0_link = URLField(_("URL"), blank=True)
    is_url0_default = models.BooleanField(_("Default?"), default=True)
    is_url0_on_hold = models.BooleanField(_("On Hold?"), default=False)

    url1_type = models.ForeignKey(
        URLType,
        verbose_name=_("URL Type"),
        blank=True,
        null=True,
        related_name='institutional_contacts1',
        on_delete=models.SET_NULL
    )
    url1_link = URLField(_("URL"), blank=True)
    is_url1_default = models.BooleanField(_("Default?"), default=False)
    is_url1_on_hold = models.BooleanField(_("On Hold?"), default=False)

    url2_type = models.ForeignKey(
        URLType,
        verbose_name=_("URL Type"),
        blank=True,
        null=True,
        related_name='institutional_contacts2',
        on_delete=models.SET_NULL
    )
    url2_link = URLField(_("URL"), blank=True)
    is_url2_default = models.BooleanField(_("Default?"), default=False)
    is_url2_on_hold = models.BooleanField(_("On Hold?"), default=False)

    # INSTANT MESSENGERS

    im0_type = models.ForeignKey(
        IMType,
        verbose_name=_("IM Type"),
        blank=True,
        null=True,
        related_name='institutional_contacts0',
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
        related_name='institutional_contacts1',
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
        related_name='institutional_contacts2',
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
        related_name='institutional_contacts0',
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
        related_name='institutional_contacts1',
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
        related_name='institutional_contacts2',
        on_delete=models.SET_NULL
    )
    email2_address = models.CharField(
        _("Email Address"), blank=True, max_length=255
    )
    is_email2_default = models.BooleanField(_("Default?"), default=False)
    is_email2_on_hold = models.BooleanField(_("On Hold?"), default=False)

    class Meta:
        verbose_name = _("institutional contact")
        verbose_name_plural = _("institutional contacts")
        ordering = ["-is_primary"]
        #db_table = "accounts_institutionalcontact"
        abstract = True

    def __unicode__(self):
        return unicode(self.institution)

    def get_phones(self):
        if not hasattr(self, '_phones_cache'):
            self._phones_cache = []
            for pos in range(3):
                phone_type = getattr(self, "phone%d_type" % pos)
                phone_country = getattr(self, "phone%d_country" % pos)
                phone_area = getattr(self, "phone%d_area" % pos)
                phone_number = getattr(self, "phone%d_number" % pos)
                is_default = getattr(self, "is_phone%d_default" % pos)
                is_on_hold = getattr(self, "is_phone%d_on_hold" % pos)
                if phone_number and not is_on_hold:
                    if (
                        not phone_type or getattr(
                            self.institution,
                            "is_%s_displayed" % phone_type.slug, lambda: True
                        )()
                    ):
                        self._phones_cache.append(
                            {
                                "type": phone_type,
                                "country": phone_country,
                                "area": phone_area,
                                "number": phone_number,
                                "is_default": is_default,
                                "is_on_hold": is_on_hold,
                            }
                        )
            self._phones_cache.sort(
                lambda p1, p2: cmp(p2['is_default'], p1['is_default'])
            )
        return self._phones_cache

    def get_urls(self):
        if not hasattr(self, '_urls_cache'):
            self._urls_cache = [
                {
                    "type": getattr(self, "url%d_type" % pos),
                    "link": getattr(self, "url%d_link" % pos),
                    "is_default": getattr(self, "is_url%d_default" % pos),
                    "is_on_hold": getattr(self, "is_url%d_on_hold" % pos),
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
                            "@", " %s " % _("(at)")
                        ).replace(".", " %s " % _("(dot)")),
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

    def get_vcard(self):
        PHONE_TYPE_PHONE = PhoneType.objects.get(slug="phone").id
        PHONE_TYPE_FAX = PhoneType.objects.get(slug="fax").id
        PHONE_TYPE_MOBILE = PhoneType.objects.get(slug="mobile").id

        v = vobject.vCard()
        v.add('n')
        v.n.charset_param = 'utf-8'
        v.n.value = vobject.vcard.Name(family=self.institution.title, given="")
        v.add('fn')
        v.fn.value = "%s" % self.institution.title
        v.add('email')
        v.email.value = self.email0_address

        v.add('adr')
        v.adr.charset_param = 'utf-8'
        v.adr.value = vobject.vcard.Address(
            street=self.postal_address.street_address,
            city=self.postal_address.city,
            country=self.postal_address.country_id,
            code=self.postal_address.postal_code,
        )

        for pos in range(3):
            country = getattr(self, "phone%d_country" % pos)
            area = getattr(self, "phone%d_area" % pos)
            number = getattr(self, "phone%d_number" % pos)
            phone_string = ""
            if number:
                if country:
                    phone_string = phone_string + "+" + country + " "
                if area:
                    phone_string = phone_string + "(0)" + area + " "
                phone_string = phone_string + number

                phone_type = getattr(self, "phone%d_type" % pos)

                if phone_type:
                    if phone_type.id == PHONE_TYPE_PHONE:
                        t = v.add('tel')
                        t.type_param = 'WORK'
                        t.value = phone_string

                    elif phone_type.id == PHONE_TYPE_MOBILE:
                        t = v.add('tel')
                        t.type_param = 'CELL'
                        t.value = phone_string

                    elif phone_type.id == PHONE_TYPE_FAX:
                        t = v.add('tel')
                        t.type_param = 'FAX'
                        t.value = phone_string

        # for simplicity, we just take the first found url-link
        for pos in range(3):
            url = getattr(self, "url%d_link" % pos)
            if url:
                u = v.add('url')
                u.type_param = 'HOME'
                u.value = url
                break
        output = v.serialize(get_utf8buffer())
        return output

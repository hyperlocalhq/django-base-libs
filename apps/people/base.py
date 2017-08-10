# -*- coding: UTF-8 -*-
import StringIO
import codecs
import vobject
from datetime import datetime, date

from django.db import models
from django.db.models.base import ModelBase
from django.db.models.fields import FieldDoesNotExist
from django.template import Context, Template
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy as _, ugettext
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, AnonymousUser
from django.conf import settings
from django.utils.timezone import now as tz_now

from base_libs.models.models import SlugMixin
from base_libs.models.models import UrlMixin
from base_libs.models import CreationModificationDateMixin
from base_libs.middleware import get_current_language
from base_libs.middleware import get_current_user
from base_libs.models.query import ExtendedQuerySet
from base_libs.utils.misc import get_website_url
from base_libs.utils.betterslugify import better_slugify
from base_libs.models.fields import URLField
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualTextField
from base_libs.models.fields import ExtendedTextField # for south

from filebrowser.fields import FileBrowseField

from jetson.apps.structure.models import Term
from jetson.apps.structure.models import ContextCategory
from jetson.apps.structure.models import Category
from jetson.apps.location.models import Address
from jetson.apps.optionset.models import Prefix
from jetson.apps.optionset.models import Salutation
from jetson.apps.optionset.models import IndividualLocationType
from jetson.apps.optionset.models import PhoneType
from jetson.apps.optionset.models import EmailType
from jetson.apps.optionset.models import URLType
from jetson.apps.optionset.models import IMType
from jetson.apps.optionset.models import get_default_phonetype_for_phone
from jetson.apps.optionset.models import get_default_phonetype_for_fax
from jetson.apps.optionset.models import get_default_phonetype_for_mobile
#from jetson.apps.i18n.models import Nationality
#from jetson.apps.i18n.models import Language
#from jetson.apps.i18n.models import TimeZone
from jetson.apps.utils.models import MONTH_CHOICES
from jetson.apps.image_mods.models import FileManager

from mptt.models import MPTTModel
from mptt.managers import TreeManager
from mptt.fields import TreeForeignKey, TreeManyToManyField

verbose_name = _("People")

### User-to-person synchronisation

def create_person(sender, instance, created, *args, **kwargs):
    """
    Create a person if a User is created
    """
    Person = models.get_model("people", "Person")
    if created and Person:
        p, p_created = Person.objects.get_or_create(user=instance)

def delete_user(sender, instance, *args, **kwargs):
    """
    Delete a User if a Person is deleted
    """
    User.objects.filter(pk=instance.user_id).delete()

models.signals.post_save.connect(create_person, sender=User)

### PersonCreator class ###

class PersonCreator(ModelBase):
    """
    A model extending from PersonalContactBase will get a foreign key to the model extending from PersonBase
    """
    PersonModel = None
    def __new__(cls, name, bases, attrs):
        model = super(PersonCreator, cls).__new__(cls, name, bases, attrs)
        for b in bases:
            if b.__name__ == "PersonBase":
                cls.PersonModel = model
        if cls.PersonModel:
            models.signals.post_delete.connect(
                delete_user,
                sender=cls.PersonModel,
                )
        return model

### Person class ###

def get_default_url_type():
    try:
        return URLType.objects.get(slug="homepage").id
    except:
        return None
    
GENDER_CHOICES = (
    ('M',_('Male')),
    ('F',_('Female'))
)

STATUS_CHOICES = getattr(settings, "PERSON_STATUS_CHOICES", (
    ('unconfirmed', _("Unconfirmed")),
    ('published', _("Published")),
    ('not_listed', _("Not Listed")),
    ('import', _("Imported")),
    ))

PERSON2PERSON_PERMISSIONS = (
    ('can_see_birthday', 'Can see birthday'),
    ('can_see_addresses', 'Can see addresses'),
    ('can_see_phones', 'Can see phone numbers'),
    ('can_see_faxes', 'Can see fax numbers'),
    ('can_see_mobiles', 'Can see mobile phone numbers'),
    ('can_see_ims', 'Can see instant messengers'),
)

YEAR_OF_BIRTH_CHOICES = [
    (i,i)
    for i in range(
        tz_now().year-16,
        tz_now().year-100,
        -1
        )
    ]

YEAR_OF_VALIDITY_CHOICES = [
    (i,i)
    for i in range(
        tz_now().year-10,
        tz_now().year+10
        )
    ]

DAY_CHOICES = [(i,i) for i in range(1, 32)]

URL_ID_PERSON = getattr(settings, "URL_ID_PERSON", "person")
URL_ID_PEOPLE = getattr(settings, "URL_ID_PEOPLE", "people")

DEFAULT_LOGO_4_PERSON = getattr(
    settings,
    "DEFAULT_LOGO_4_PERSON",
    "%ssite/img/website/placeholder/person.png" % settings.STATIC_URL,
    )
DEFAULT_FORM_LOGO_4_PERSON = getattr(
    settings,
    "DEFAULT_FORM_LOGO_4_PERSON",
    "%ssite/img/website/placeholder/person_f.png" % settings.STATIC_URL,
    )
DEFAULT_SMALL_LOGO_4_PERSON = getattr(
    settings,
    "DEFAULT_SMALL_LOGO_4_PERSON",
    "%ssite/img/website/placeholder/person_s.png" % settings.STATIC_URL,
    )

def get_default_ind_loc_type():
    try:
        return IndividualLocationType.objects.get(slug="main").id
    except:
        return None

def get_utf8buffer():
    f = StringIO.StringIO()
    enc, dec, reader, writer = codecs.lookup("utf-8")
    srw = codecs.StreamReaderWriter(f, reader, writer, errors="strict")
    srw.encoding = "utf-8"
    return srw

class IndividualType(MPTTModel, SlugMixin()):
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
        verbose_name = _("individual type")
        verbose_name_plural = _("individual types")
        ordering = ["tree_id", "lft"]
        
    class MPTTMeta:
        order_insertion_by = ['sort_order']
        
    def __unicode__(self):
        return self.title

    def get_title(self, prefix="", postfix=""):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            IndividualType.objects.insert_node(self, self.parent)
        super(IndividualType, self).save(*args, **kwargs)


class PersonManager(models.Manager):
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
    
    """
    There seems to be a bug in applying the order_by clause to a queryset. 
    According to 
        http://groups.google.com/group/django-users/browse_thread/thread/90552bc06a8a2939
    there is a workaround ...
    """
    def get_sort_order_mapper(self):
        sort_order_mapper = {
            'alphabetical_asc': (
                1,
                _('Alphabetical'),
                ['user__last_name'],
                ),
            'creation_date_desc': (
                2,
                _('Sign-up date'),
                ['-user__date_joined'],
                ),
            }
        return sort_order_mapper
    def latest_published(self):
        return self.filter(
            status="published",
            ).order_by("-user__date_joined")
    
    def update_creation_date(self):
        """
        this method is used for recreating the correct 
        creation_date from the user model.
        """
        for p in self.all():
            p.creation_date =  p.user.date_joined
            p.save()


class PersonBase(CreationModificationDateMixin, UrlMixin):
    """
    The base class for the person. Wherever person is located - jetson or site-specific project - it should be in an app called "people" and it should be called "Person"
    """    
    __metaclass__ = PersonCreator
    
    user = models.OneToOneField(User, verbose_name=_("User"), unique=True, related_name="profile")
    user.primary_key = False
    
    
    # P E R S O N A L   I N F O R M A T I O N
    
    individual_type = TreeForeignKey(IndividualType, verbose_name=_("Type"), blank=True, null=True)
    prefix = models.ForeignKey(Prefix, verbose_name=_("Prefix"), null=True, blank=True)
    salutation = models.ForeignKey(Salutation, verbose_name=_("Salutation"), null=True, blank=True)
    person_repr = models.CharField(_("Person Representation"), max_length=200, blank=True, editable=False)
    nickname = models.CharField(_("Nickname"), max_length=200, blank=True)
    birthname = models.CharField(_("Birth / Maiden name"), max_length=200, blank=True)
    gender = models.CharField(_("Gender"), max_length=1, choices=GENDER_CHOICES, blank=True)
    birthday_yyyy = models.IntegerField(_("Year of Birth"), blank=True, null=True, choices=YEAR_OF_BIRTH_CHOICES)
    birthday_mm = models.SmallIntegerField(_("Month of Birth"), blank=True, null=True, choices=MONTH_CHOICES)
    birthday_dd = models.SmallIntegerField(_("Day of Birth"), blank=True, null=True, choices=DAY_CHOICES)
    # can have choices
    nationality = models.ForeignKey("i18n.Nationality", verbose_name=_("Nationality"), max_length=200, blank=True, null=True, limit_choices_to={'display': True})
    # can have choices
    spoken_languages = models.ManyToManyField("i18n.Language", verbose_name=_("Languages spoken"), blank=True, related_name="speaking_people")
    # http://en.wikipedia.org/wiki/Academic_degree#Types_of_academic_degree
    degree = models.CharField(_("Academic Degree"), max_length=200, blank=True)
    occupation = models.CharField(_("Current Occupation"), max_length=200, blank=True)
    # should be checkboxes/selection list -- many to many relationship
    interests = models.CharField(_("Interests"), max_length=200, blank=True)
    description = MultilingualTextField(_("Description"), blank=True)
    image = FileBrowseField(_('Image'), max_length=255, directory="%s/" % URL_ID_PEOPLE, extensions=['.jpg', '.jpeg', '.gif','.png','.tif','.tiff'], blank=True)
    
    context_categories = TreeManyToManyField(ContextCategory, verbose_name=_("Context categories"), limit_choices_to={'is_applied4person': True}, blank=True)
    
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, blank=True, default="unconfirmed")
    
    # PREFERENCES
    
    preferred_language = models.ForeignKey("i18n.Language", verbose_name=_("Preferred Language"), blank=True, null=True, limit_choices_to={'display': True})
    timezone = models.ForeignKey("i18n.TimeZone", verbose_name=_("Current Timezone"), max_length=200, blank=True, null=True)
    # current location
    # privacy settings
    
    display_birthday = models.BooleanField(_("Display birthday to public"), default=True)
    display_email = models.BooleanField(_("Display email address to public"), default=False)
    display_address = models.BooleanField(_("Display address data to public"), default=True)
    display_phone = models.BooleanField(_("Display phone numbers to public"), default=True)
    display_fax = models.BooleanField(_("Display fax numbers to public"), default=True)
    display_mobile = models.BooleanField(_("Display mobile phones to public"), default=True)
    display_im = models.BooleanField(_("Display instant messengers to public"), default=True)
    
    display_username = models.BooleanField(_("Display user name instead of full name"), default=False)
    allow_search_engine_indexing = models.BooleanField(_("Allow indexing by search engines"), default=True)
    
    row_level_permissions = True
    
    objects = PersonManager()
    
    class Meta:
        abstract = True
        verbose_name = _("individual (person)")
        verbose_name_plural = _("individuals (people)")
        #row_level_permissions = True
        permissions = PERSON2PERSON_PERMISSIONS
    
    def __unicode__(self):
        return self.person_repr
        #return self.get_title()
    
    def get_description(self, language=None):
        language = language or get_current_language()
        return mark_safe(getattr(self, "description_%s" % language, "") or self.description)
        
    def is_person(self):
        return True
        
    def has_maps(self):
        return bool(self.get_primary_contact())
        
    def has_photos(self):
        return False
        
    def has_videos(self):
        return False
    
    def get_absolute_url(self):
        return "%snetwork/member/%s/" % (get_website_url(), self.user.username)

    def get_url_path(self):
        return "/network/member/%s/" % (self.user.username, )
    
    def get_context_categories(self):
        return self.context_categories.all()
        
    def get_spoken_languages(self):
        from jetson.apps.i18n.models import Language
        sl_db_table = self._meta.get_field(
            "spoken_languages",
            )._get_m2m_db_table(self._meta)
        l_db_table = Language._meta.db_table
        return Language.objects.distinct().extra(
            tables=[sl_db_table],
            where=[
               '%s.id=%s.language_id' % (l_db_table, sl_db_table), 
               '%s.person_id=%d' % (sl_db_table, self.id or 0)
            ],
        )
        
    def get_locality_type(self):
        from jetson.apps.location.models import LocalityType
        contacts = self.get_contacts(cache=False)
        if contacts and contacts[0].postal_address:
            postal_address = contacts[0].postal_address
            if postal_address.country_id != "DE":
                return LocalityType.objects.get(
                    slug="international",
                )
            elif postal_address.city.lower() != "berlin":
                return LocalityType.objects.get(
                    slug="national",
                )
            else:
                import re
                from jetson.apps.location.data import POSTAL_CODE_2_DISTRICT
                locality = postal_address.get_locality()
                regional = LocalityType.objects.get(
                    slug="regional",
                )
                p = re.compile('[^\d]*') # remove non numbers
                postal_code = p.sub("", postal_address.postal_code)
                
                district = ""
                if locality and locality.district:
                    district = locality.district
                elif postal_code in POSTAL_CODE_2_DISTRICT:
                    district = POSTAL_CODE_2_DISTRICT[postal_code]
                if district:
                    d = {}
                    for lang_code, lang_verbose in settings.LANGUAGES:
                        d["title_%s" % lang_code] = district
                    term, created = LocalityType.objects.get_or_create(
                        slug=better_slugify(district),
                        parent=regional,
                        defaults=d,
                    )
                    return term
                else:
                    return regional
        else:
            return None
        
    def get_object_types(self):
        return self.individual_type and [self.individual_type] or []
        
    def get_username(self):
        return self.user.username
        
    def get_name_and_email(self):
        name = ("%s %s" % (self.user.first_name, self.user.last_name)).strip()
        email = self.user.email
        if email:
            email = " (%s)" % email
        return "".join([name, email])
        
    def get_title(self):
        """ returns the username or 'first_name last_name' of 
        the person depending on the display_username flag"""
        if self.display_username:
            return self.nickname.strip() or self.user.username.strip()
        else:
            return ("%s %s" % (self.user.first_name, self.user.last_name)).strip()

    def get_title_for_sorting(self):
        """ returns the username or 'last_name first_name' of 
        the person depending on the display_username flag"""
        if self.display_username:
            return self.nickname.strip() or self.user.username.strip()
        else:
            return "%s %s".strip() % (self.user.last_name, self.user.first_name)
            
    def get_slug(self):
        return self.user.username
    
    def get_preferred_language_iso2_code(self):
        language = self.preferred_language
        if language:
            return language.iso2_code
        return 'de'
    
    def get_salutation(self, language=""):
        language = language or get_current_language()
        if self.salutation:
            t = Template(getattr(self.salutation, "template_%s" % language, ""))
            c = Context({"person": self})
            return t.render(c)
        else:
            return None     
    
    def get_birthday(self):
        if not hasattr(self, "_birthday_cache"):
            try:
                self._birthday_cache = date(
                    self.birthday_yyyy,
                    self.birthday_mm,
                    self.birthday_dd,
                    )
            except:
                self._birthday_cache = None
        return self._birthday_cache
        
    title = property(get_title_for_sorting)
    title_en = property(get_title_for_sorting)
    title_de = property(get_title_for_sorting)
    slug = property(get_slug)
            
    def get_first_name(self):
        return self.user.first_name
    get_first_name.short_description = _('First name')
    
    def get_last_name(self):
        return self.user.last_name
    get_last_name.short_description = _('Last name')

    def get_email(self):
        return self.user.email
    get_email.short_description = _('E-mail address')
    
    def get_contacts(self, cache=True):
        if not hasattr(self, "_contacts_cache") or not cache:
            self._contacts_cache = self.individualcontact_set.order_by('-is_primary', 'id')
        return self._contacts_cache
    
    def get_primary_contact(self):
        """returns a dictionary containing primary contact information"""
        contact_dict = {}
        primary_contact = self.individualcontact_set.filter(is_primary=True)
        if primary_contact:
            primary_contact = primary_contact[0]
            contact_dict = primary_contact.__dict__
            address = primary_contact.postal_address
            for phone in primary_contact.get_phones():
                if phone['type']:
                    if phone['type'].slug == "phone" and "phone_number" not in contact_dict:
                        contact_dict['phone_country'] = phone['country']
                        contact_dict['phone_area'] = phone['area']
                        contact_dict['phone_number'] = phone['number']
                    elif phone['type'].slug == "fax" and "fax_number" not in contact_dict:
                        contact_dict['fax_country'] = phone['country']
                        contact_dict['fax_area'] = phone['area']
                        contact_dict['fax_number'] = phone['number']
                    elif phone['type'].slug == "mobile" and "mobile_number" not in contact_dict:
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
        
    def has_multiple_contacts(self):
        return self.get_contacts(cache=False).count() > 1
        
    def get_neighborhoods(self):
        if not hasattr(self, '_neighborhoods_cache'):
            neighborhoods = []
            contact_queryset = self.individualcontact_set.all()
            for contact in contact_queryset:
                try:
                    neighborhood = contact.postal_address.get_locality().neighborhood
                except:
                    pass
                else:
                    if neighborhood:
                        neighborhoods.append(neighborhood)
            self._neighborhoods_cache = neighborhoods
        return self._neighborhoods_cache
        
    def get_previous_login(self):
        from jetson.apps.utils.models import ExtendedLogEntry
        u = self.user
        ct = ContentType.objects.get_for_model(u) 
        previous_login = ExtendedLogEntry.objects.filter(
            user=u,
            object_id=u.id,
            content_type=ct,
            change_message="Changed last login.",
            action_flag=settings.A_CHANGE,
            scope=settings.AS_SYSTEM,
            )[1:2]
        if previous_login:
            return previous_login[0].action_time
        else:
            return None
            
    def get_representatives(self):
        """
        Returns the default owners of this object for permission manipulation
        """
        return [self.user]
        
    def save(self, *args, **kwargs):
        from jetson.apps.permissions.models import RowLevelPermission
        is_new = not self.id
        if not self.person_repr:
            self.person_repr = ("%s %s (%s)" % (
                self.user.first_name,
                self.user.last_name,
                self.user.username,
                ))[:200]
                
        super(PersonBase, self).save(*args, **kwargs)
        if is_new and not self.user.is_superuser:
            RowLevelPermission.objects.create_default_row_permissions(
                self,
                self.user,
                delete=False,
                )
    save.alters_data = True

    def delete(self, *args, **kwargs):
        FileManager.delete_file(self.get_filebrowser_dir())
        super(PersonBase, self).delete(*args, **kwargs)
    delete.alters_data = True
    
    # information visibility
    
    def is_birthday_displayed(self, user=None):
        if not hasattr(self, "_is_birthday_displayed_cache"):
            user = get_current_user(user) or AnonymousUser()
            self._is_birthday_displayed_cache = bool(
                self.display_birthday
                or user.has_perm("people.can_see_birthday", self)
                )
        return self._is_birthday_displayed_cache
        
    def is_email_displayed(self, user=None):
        if not hasattr(self, "_is_email_displayed_cache"):
            user = get_current_user(user) or AnonymousUser()
            self._is_email_displayed_cache = bool(
                self.display_email
                or user.has_perm("people.can_see_email", self)
                )
        return self._is_email_displayed_cache
        
    def is_address_displayed(self, user=None):
        if not hasattr(self, "_is_address_displayed_cache"):
            user = get_current_user(user) or AnonymousUser()
            self._is_address_displayed_cache = bool(
                self.display_address
                or user.has_perm("people.can_see_addresses", self)
                )
        return self._is_address_displayed_cache
        
    def is_phone_displayed(self, user=None):
        if not hasattr(self, "_is_phone_displayed_cache"):
            user = get_current_user(user) or AnonymousUser()
            self._is_phone_displayed_cache = bool(
                self.display_phone
                or user.has_perm("people.can_see_phones", self)
                )
        return self._is_phone_displayed_cache
        
    def is_fax_displayed(self, user=None):
        if not hasattr(self, "_is_fax_displayed_cache"):
            user = get_current_user(user) or AnonymousUser()
            self._is_fax_displayed_cache = bool(
                self.display_fax
                or user.has_perm("people.can_see_faxes", self)
                )
        return self._is_fax_displayed_cache
        
    def is_mobile_displayed(self, user=None):
        if not hasattr(self, "_is_mobile_displayed_cache"):
            user = get_current_user(user) or AnonymousUser()
            self._is_mobile_displayed_cache = bool(
                self.display_mobile
                or user.has_perm("people.can_see_mobiles", self)
                )
        return self._is_mobile_displayed_cache
        
    def is_im_displayed(self, user=None):
        if not hasattr(self, "_is_im_displayed_cache"):
            user = get_current_user(user) or AnonymousUser()
            self._is_im_displayed_cache = bool(
                self.display_im
                or user.has_perm("people.can_see_ims", self)
                )
        return self._is_im_displayed_cache
    def get_filebrowser_dir(self):
        return "%s/%s/" % (
            URL_ID_PEOPLE,
            self.user.username,
            )
    def get_additional_search_data(self):
        """ used by ContextItemManager """
        search_data = []
        contacts = self.get_contacts(cache=False)
        if contacts:
            for contact in contacts:
                # add urls
                for url in contact.get_urls():
                    search_data.append(url['link'])
        # add occupation
        search_data.append(self.occupation)
        return search_data


### IndividualContact class ###

class IndividualContactBase(models.Model):
    """
    The base class for the individual contact. Wherever it is located - jetson or site-specific project - it should be in an app called "people" and it should be called "IndividualContact"
    """
    
    # a foreign key to Person will be added when people.Person is created
    person = models.ForeignKey("people.Person", verbose_name=_("Person"))

    location_type = models.ForeignKey(IndividualLocationType, verbose_name=_("Location type"), default=get_default_ind_loc_type)
    location_title = models.CharField(_("Location title"), max_length=255, blank=True)
    is_primary = models.BooleanField(_("Primary contact"), default=True)
    is_seasonal = models.BooleanField(_("Seasonal"), default=False)
    validity_start_yyyy = models.IntegerField(_("From Year"), blank=True, null=True, choices=YEAR_OF_VALIDITY_CHOICES)
    validity_start_mm = models.SmallIntegerField(_("From Month"), blank=True, null=True, choices=MONTH_CHOICES)
    validity_start_dd = models.SmallIntegerField(_("From Day"), blank=True, null=True, choices=DAY_CHOICES)
    validity_end_yyyy = models.IntegerField(_("Till Year"), blank=True, null=True, choices=YEAR_OF_VALIDITY_CHOICES)
    validity_end_mm = models.SmallIntegerField(_("Till Month"), blank=True, null=True, choices=MONTH_CHOICES)
    validity_end_dd = models.SmallIntegerField(_("Till Day"), blank=True, null=True, choices=DAY_CHOICES)

    institutional_title = models.CharField(_("Title in the institution"), max_length=255, blank=True, help_text=_('i.e. "director", "manager", "student", "doctor", etc.'))
    
    # C O N T A C T

    postal_address = models.ForeignKey(Address, verbose_name=_("Postal Address"), related_name="individual_address", null=True, blank=True)
    is_billing_address = models.BooleanField(_("Use this address for billing"), default=True)    
    is_shipping_address = models.BooleanField(_("Use this address for shipping"), default=True)    
    
    # PHONES

    phone0_type = models.ForeignKey(PhoneType, verbose_name=_("Phone Type"), blank=True, null=True,
                                    related_name='individual_contacts0',
                                    default=get_default_phonetype_for_phone)
    phone0_country = models.CharField(_("Country Code"), max_length=4, blank=True, default="49")
    phone0_area = models.CharField(_("Area Code"), max_length=6, blank=True, default="30")
    phone0_number = models.CharField(_("Subscriber Number and Extension"), max_length=25, blank=True)
    is_phone0_default = models.BooleanField(_("Default?"), default=True)
    is_phone0_on_hold = models.BooleanField(_("Default?"), default=False)

    phone1_type = models.ForeignKey(PhoneType, verbose_name=_("Phone Type"), blank=True, null=True,
                                    related_name='individual_contacts1',
                                    default=get_default_phonetype_for_fax)
    phone1_country = models.CharField(_("Country Code"), max_length=4, blank=True, default="49")
    phone1_area = models.CharField(_("Area Code"), max_length=6, blank=True, default="30")
    phone1_number = models.CharField(_("Subscriber Number and Extension"), max_length=25, blank=True)
    is_phone1_default = models.BooleanField(_("Default?"), default=False)
    is_phone1_on_hold = models.BooleanField(_("Default?"), default=False)

    phone2_type = models.ForeignKey(PhoneType, verbose_name=_("Phone Type"), blank=True, null=True,
                                    related_name='individual_contacts2',
                                    default=get_default_phonetype_for_mobile)
    phone2_country = models.CharField(_("Country Code"), max_length=4, blank=True, default="49")
    phone2_area = models.CharField(_("Area Code"), max_length=6, blank=True)
    phone2_number = models.CharField(_("Subscriber Number and Extension"), max_length=25, blank=True)
    is_phone2_default = models.BooleanField(_("Default?"), default=False)
    is_phone2_on_hold = models.BooleanField(_("On Hold?"), default=False)


    # WEBSITES
    
    url0_type = models.ForeignKey(URLType, verbose_name=_("URL Type"), blank=True, null=True, related_name='individual_contacts0', on_delete=models.SET_NULL)
    url0_link = URLField(_("URL"), blank=True)
    is_url0_default = models.BooleanField(_("Default?"), default=True)
    is_url0_on_hold = models.BooleanField(_("On Hold?"), default=False)
    
    url1_type = models.ForeignKey(URLType, verbose_name=_("URL Type"), blank=True, null=True, related_name='individual_contacts1', on_delete=models.SET_NULL)
    url1_link = URLField(_("URL"), blank=True)
    is_url1_default = models.BooleanField(_("Default?"), default=False)
    is_url1_on_hold = models.BooleanField(_("On Hold?"), default=False)
    
    url2_type = models.ForeignKey(URLType, verbose_name=_("URL Type"), blank=True, null=True, related_name='individual_contacts2', on_delete=models.SET_NULL)
    url2_link = URLField(_("URL"), blank=True)
    is_url2_default = models.BooleanField(_("Default?"), default=False)
    is_url2_on_hold = models.BooleanField(_("On Hold?"), default=False)
    

    # INSTANT MESSENGERS
    
    im0_type = models.ForeignKey(IMType, verbose_name=_("IM Type"), blank=True, null=True, related_name='individual_contacts0', on_delete=models.SET_NULL)
    im0_address = models.CharField(_("Instant Messenger"), blank=True, max_length=255)
    is_im0_default = models.BooleanField(_("Default?"), default=True)
    is_im0_on_hold = models.BooleanField(_("On Hold?"), default=False)

    im1_type = models.ForeignKey(IMType, verbose_name=_("IM Type"), blank=True, null=True, related_name='individual_contacts1', on_delete=models.SET_NULL)
    im1_address = models.CharField(_("Instant Messenger"), blank=True, max_length=255)
    is_im1_default = models.BooleanField(_("Default?"), default=False)
    is_im1_on_hold = models.BooleanField(_("On Hold?"), default=False)

    im2_type = models.ForeignKey(IMType, verbose_name=_("IM Type"), blank=True, null=True, related_name='individual_contacts2', on_delete=models.SET_NULL)
    im2_address = models.CharField(_("Instant Messenger"), blank=True, max_length=255)
    is_im2_default = models.BooleanField(_("Default?"), default=False)
    is_im2_on_hold = models.BooleanField(_("On Hold?"), default=False)


    # EMAILS
    
    email0_type = models.ForeignKey(EmailType, verbose_name=_("Email Type"), blank=True, null=True, related_name='individual_contacts0', on_delete=models.SET_NULL)
    email0_address = models.CharField(_("Email Address"), blank=True, max_length=255)
    is_email0_default = models.BooleanField(_("Default?"), default=True)
    is_email0_on_hold = models.BooleanField(_("On Hold?"), default=False)

    email1_type = models.ForeignKey(EmailType, verbose_name=_("Email Type"), blank=True, null=True, related_name='individual_contacts1', on_delete=models.SET_NULL)
    email1_address = models.CharField(_("Email Address"), blank=True, max_length=255)
    is_email1_default = models.BooleanField(_("Default?"), default=False)
    is_email1_on_hold = models.BooleanField(_("On Hold?"), default=False)

    email2_type = models.ForeignKey(EmailType, verbose_name=_("Email Type"), blank=True, null=True, related_name='individual_contacts2', on_delete=models.SET_NULL)
    email2_address = models.CharField(_("Email Address"), blank=True, max_length=255)
    is_email2_default = models.BooleanField(_("Default?"), default=False)
    is_email2_on_hold = models.BooleanField(_("On Hold?"), default=False)
    
    class Meta:
        abstract = True
        verbose_name = _("individual contact")
        verbose_name_plural = _("individual contacts")
        ordering = ["-is_primary"]
        
    def __unicode__(self):
        return u" @ ".join((
            force_unicode(self.person),
            force_unicode(self.location_type),
            ))
    
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
                        not phone_type or
                        getattr(
                            self.person,
                            "is_%s_displayed" % phone_type.slug,
                            lambda: True
                            )()
                        ):
                        self._phones_cache.append({
                            "type": phone_type,
                            "country": phone_country,
                            "area": phone_area,
                            "number": phone_number,
                            "is_default": is_default,
                            "is_on_hold": is_on_hold,
                            }) 
            self._phones_cache.sort(
                lambda p1, p2: cmp(p2['is_default'], p1['is_default'])
                )
        return self._phones_cache
        
    def get_urls(self):
        if not hasattr(self, '_urls_cache'):
            self._urls_cache = [{
                "type": getattr(self, "url%d_type" % pos),
                "link": getattr(self, "url%d_link" % pos),
                "is_default": getattr(self, "is_url%d_default" % pos),
                "is_on_hold": getattr(self, "is_url%d_on_hold" % pos),
            } for pos in range(3)
            if getattr(self, "url%d_link" % pos) and not getattr(self, "is_url%d_on_hold" % pos)
            ]
            self._urls_cache.sort(
                lambda p1, p2: cmp(p2['is_default'], p1['is_default'])
                )
        return self._urls_cache
        
    def get_ims(self):
        if not hasattr(self, '_ims_cache'):
            if self.person.is_im_displayed():
                self._ims_cache = [{
                    "type": getattr(self, "im%d_type" % pos),
                    "address": getattr(self, "im%d_address" % pos),
                    "is_default": getattr(self, "is_im%d_default" % pos),
                    "is_on_hold": getattr(self, "is_im%d_on_hold" % pos),
                } for pos in range(3)
                if getattr(self, "im%d_address" % pos) and not getattr(self, "is_im%d_on_hold" % pos)
                ]
                self._ims_cache.sort(
                    lambda p1, p2: cmp(p2['is_default'], p1['is_default'])
                    )
            else:
                self._ims_cache = []
        return self._ims_cache

    def get_emails(self):
        if not hasattr(self, '_emails_cache'):
            if self.person.is_email_displayed():
                self._emails_cache = [{
                    "type": getattr(self, "email%d_type" % pos),
                    "address": getattr(self, "email%d_address" % pos),
                    "address_protected": getattr(self, "email%d_address" % pos).replace("@", " %s " % ugettext("(at)")).replace(".", " %s " % ugettext("(dot)")),
                    "is_default": getattr(self, "is_email%d_default" % pos),
                    "is_on_hold": getattr(self, "is_email%d_on_hold" % pos),
                } for pos in range(3)
                if getattr(self, "email%d_address" % pos) and not getattr(self, "is_email%d_on_hold" % pos)
                ]
                self._emails_cache.sort(
                    lambda p1, p2: cmp(p2['is_default'], p1['is_default'])
                    )
            else:
                self._emails_cache = []
        return self._emails_cache
    
    def get_vcard(self):
        PHONE_TYPE_PHONE = PhoneType.objects.get(slug="phone").id
        PHONE_TYPE_FAX = PhoneType.objects.get(slug="fax").id
        PHONE_TYPE_MOBILE = PhoneType.objects.get(slug="mobile").id
        
        v = vobject.vCard()
        v.add('n')
        v.n.charset_param = 'utf-8'
        v.n.value = vobject.vcard.Name(family=self.person.get_last_name(), given=self.person.get_first_name())
        v.add('fn')
        v.fn.value = "%s %s" % (self.person.get_first_name(), self.person.get_last_name())
        v.add('email')
        v.email.value = self.person.get_email()
        
        if self.postal_address:
            v.add('adr')
            v.adr.charset_param = 'utf-8'
            v.adr.value = vobject.vcard.Address(
                street = unicode(self.postal_address.street_address),
                city = self.postal_address.city,
                code = self.postal_address.postal_code,
                country = self.postal_address.country_id,
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


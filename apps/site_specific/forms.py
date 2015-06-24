# -*- coding: UTF-8 -*-
import datetime
from itertools import chain

from django.db import models
from django.db.models.loading import load_app
from django import forms
from django.forms.formsets import formset_factory, BaseFormSet
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils.encoding import force_unicode
from django.utils.dates import MONTHS
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from base_libs.forms import dynamicforms
from base_libs.forms.fields import ImageField
from base_libs.forms.fields import SecurityField
from base_libs.utils.misc import get_related_queryset, XChoiceList
from base_libs.forms.fields import AutocompleteField
from base_libs.middleware import get_current_user
from base_libs.forms.fields import SecurityField, SingleEmailTextField

image_mods = models.get_app("image_mods")

from tagging.forms import TagField
from tagging_autocomplete.widgets import TagAutocomplete

from jetson.apps.location.models import Address
from jetson.apps.utils.images import validate_image, parse_dimensions
from jetson.apps.optionset.models import IndividualLocationType
from jetson.apps.optionset.models import InstitutionalLocationType
from jetson.apps.optionset.models import PhoneType

from ccb.apps.people.models import Person, IndividualContact
from ccb.apps.institutions.models import Institution, InstitutionalContact
from ccb.apps.events.models import Event, EventTime
from ccb.apps.resources.models import Document
from ccb.apps.marketplace.models import JobOffer
from ccb.apps.groups_networks.models import PersonGroup
from ccb.apps.site_specific.models import ContextItem, ClaimRequest

NULL_PREFIX_CHOICES = XChoiceList(get_related_queryset(Person, 'prefix'))

LEGAL_FORM_CHOICES = XChoiceList(get_related_queryset(Institution, 'legal_form'))

WEEK_DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

YEARS_CHOICES = [("", _("Year"))] + [(i, i) for i in range(2008, 2040)]
MONTHS_CHOICES = [("", _("Month"))] + MONTHS.items()
DAYS_CHOICES = [("", _("Day"))] + [(i, i) for i in range(1, 32)]
HOURS_CHOICES = [("", _("HH"))] + [(i, "%02d" % i) for i in range(0, 24)]
MINUTES_CHOICES = [("", _("MM"))] + [(i, "%02d" % i) for i in range(0, 60, 5)]

# prexixes of fields to guarantee uniqueness
PREFIX_CI = 'CI_' # Creative Sector aka Creative Industry
PREFIX_BC = 'BC_' # Context Category aka Business Category
PREFIX_OT = 'OT_' # Object Type
PREFIX_LT = 'LT_' # Location Type
PREFIX_JS = 'JS_' # Job Sector

BIRTHDAY_DD_CHOICES = Person._meta.get_field('birthday_dd').get_choices()
BIRTHDAY_DD_CHOICES[0] = ("", "----")
BIRTHDAY_MM_CHOICES = Person._meta.get_field('birthday_mm').get_choices()
BIRTHDAY_MM_CHOICES[0] = ("", "----")
BIRTHDAY_YYYY_CHOICES = Person._meta.get_field('birthday_yyyy').get_choices()
BIRTHDAY_YYYY_CHOICES[0] = ("", "----")

NATIONALITY_CHOICES = XChoiceList(get_related_queryset(Person, 'nationality'))
SALUTATION_CHOICES = XChoiceList(get_related_queryset(Person, 'salutation'))

contact_meta = IndividualContact._meta
URL_TYPE_CHOICES = XChoiceList(get_related_queryset(IndividualContact, 'url0_type'))
IM_TYPE_CHOICES = XChoiceList(get_related_queryset(IndividualContact, 'im0_type'))

ORGANIZER_CHOICES = [
    (0, _("selected venue is organizer")),
    (1, _("organized by other institution")),
    (2, _("organized by myself")),
]

CONTACT_PERSON_CHOICES = [
    (0, _("I am the contact person")),
    (1, _("I am not the contact person")),
]

LOCATION_TYPE_CHOICES = XChoiceList(get_related_queryset(IndividualContact, "location_type"))
INSTITUTION_LOCATION_TYPE_CHOICES = XChoiceList(get_related_queryset(InstitutionalContact, "location_type"))
INDIVIDUAL_TYPE_CHOICES = XChoiceList(get_related_queryset(Person, "individual_type"))
EVENT_TYPE_CHOICES = XChoiceList(get_related_queryset(Event, "event_type"))
ORGANIZING_INSTITUTION_CHOICES = XChoiceList(get_related_queryset(Event, "organizing_institution"))

ACCESS_TYPE_CHOICES = (
    ("", _("- Please select -")),
    ("public", _("Public")),
    ("private", _("Private")),
    ("secret", _("Secret")),
    )

GROUP_TYPE_CHOICES = [
    ('', _("- Please select -"))
    ] + [
        (str(el.id), el.get_title())
        for el in get_related_queryset(PersonGroup, 'group_type')
        ]

MEMBERSHIP_OPTION_CHOICES = (
    ('', _("- Please select -")),
    ("invite", _("By invitation only")),
    ("invite_or_confirm", _("By approved request or by invitation")),
    ("anyone", _("Anyone can join")),
)
PREFERRED_LANGUAGE_CHOICES = XChoiceList(
    get_related_queryset(PersonGroup, 'preferred_language'),
    null_choice_text=_("- Please select -"),
    )

ESTABLISHMENT_YYYY_CHOICES = Institution._meta.get_field('establishment_yyyy').get_choices()
ESTABLISHMENT_YYYY_CHOICES[0] = ("", _("Year"))
ESTABLISHMENT_MM_CHOICES = Institution._meta.get_field('establishment_mm').get_choices()
ESTABLISHMENT_MM_CHOICES[0] = ("", _("Month"))


LOGO_SIZE = getattr(settings, "LOGO_SIZE", (100,100))
MIN_LOGO_SIZE = getattr(settings, "MIN_LOGO_SIZE", (100,100))
STR_LOGO_SIZE = "%sx%s" % LOGO_SIZE
STR_MIN_LOGO_SIZE = "%sx%s" % MIN_LOGO_SIZE

class ProfileFormSet(BaseFormSet):
    def __init__(self, parent_instance, index, get_instances, *args, **kwargs):
        self.parent_instance = parent_instance
        self.index = index
        qs = get_instances(parent_instance)
        kwargs.setdefault('initial', [])
        for instance in qs:
            kwargs['initial'].append(instance.__dict__)
        super(ProfileFormSet, self).__init__(*args, **kwargs)
        
    def _construct_form(self, i, **kwargs):
        """
        Instantiates and returns the i-th form instance in a formset.
        """
        defaults = {'auto_id': self.auto_id, 'prefix': self.add_prefix(i)}
        if self.data or self.files:
            defaults['data'] = self.data
            defaults['files'] = self.files
        if self.initial:
            try:
                defaults['initial'] = self.initial[i]
            except IndexError:
                pass
        # Allow extra forms to be empty.
        if i >= self.initial_form_count():
            defaults['empty_permitted'] = True
        defaults.update(kwargs)
        form = self.form(self.parent_instance, self.index, **defaults)
        self.add_fields(form, i)
        return form


# TODO: each form could be ModelForm. Each formset could be ModelFormSet.
class PersonProfile: # namespace
    class IdentityForm(dynamicforms.Form):
        first_name = forms.CharField(
            required=True,
            label=_("First Name"),
            )
        last_name = forms.CharField(
            required=True,
            label=_("Last Name"),
            )

        def __init__(self, person, index, *args, **kwargs):
            super(IdentityForm, self).__init__()
            self.person = person
            self.index = index
            super(type(self), self).__init__(*args, **kwargs)
            if not args and not kwargs:  # if nothing is posted
                self.fields['first_name'].initial = person.user.first_name
                self.fields['last_name'].initial = person.user.last_name
        def save(self):
            person = self.person
            user = person.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.save()
            person.save()
            return person
            
        def get_extra_context(self):
            return {}
            
    class DescriptionForm(dynamicforms.Form):
        description_en = forms.CharField(
            label=_("Description (English)"),
            required=False,
            widget=forms.Textarea(),
            )
        description_de = forms.CharField(
            label=_("Description (German)"),
            required=False,
            widget=forms.Textarea(),
            )

        def __init__(self, person, index, *args, **kwargs):
            super(DescriptionForm, self).__init__()
            self.person = person
            self.index = index
            super(type(self), self).__init__(*args, **kwargs)
            if not args and not kwargs:  # if nothing is posted
                self.fields['description_en'].initial = person.description_en
                self.fields['description_de'].initial = person.description_de
        def save(self):
            person = self.person
            person.description_en = self.cleaned_data['description_en']
            person.description_de = self.cleaned_data['description_de']
            person.save()
            return person
            
        def get_extra_context(self):
            return {}
    
    class AvatarForm(dynamicforms.Form):
        media_file = ImageField(
            label= _("Photo"),
            help_text= _("You can upload GIF, JPG, PNG, TIFF, and BMP images. The minimal dimensions are %s px.") % STR_MIN_LOGO_SIZE,
            required=False,
            min_dimensions=MIN_LOGO_SIZE,
            )

        def __init__(self, person, index, *args, **kwargs):
            super(AvatarForm, self).__init__()
            self.person = person
            self.index = index
            super(type(self), self).__init__(*args, **kwargs)
        def save(self):
            person = self.person
            if "media_file" in self.files:
                media_file = self.files['media_file']
                image_mods.FileManager.save_file_for_object(
                    person,
                    media_file.name,
                    media_file,
                    subpath = "avatar/"
                    )
            return person
        def get_extra_context(self):
            return {}
    
    class ContactForm(dynamicforms.Form):
        location_type = forms.ChoiceField(
            required=True,
            label=_("Location type"),
            choices=LOCATION_TYPE_CHOICES,
            )
        """
        institution:
        
        The parameters below are as follows:
        app:              the "app"
        qs_function:      the function to get the queryset, 
                          must be placed in ajax.py under <app> 
                          folder
        display_atrr:     a model field or function to get the 
                          required display title for the autocomplete
                          field
        add_display_atrr: a model field or function to get the 
                          required display descriptione for the 
                          autocomplete field
        """
        institution = AutocompleteField(
            required=False,
            label=_("Institution"),
            help_text=_("Please enter a letter to display a list of available institutions"),
            app="institutions", 
            qs_function="get_all_institutions",   
            display_attr="title", 
            add_display_attr="get_address_string",
            options={
                "minChars": 1,
                "max": 20,
                "mustMatch": 1,
                "highlight" : False,
                },
            )
        institution_title = forms.CharField(
            required=False,
            label=_("Institution Title"),
        )
        
        institution_website = forms.URLField(
            required=False,
            label=_("Institution Website"),
        )
        
        location_title = forms.CharField(
            required=False,
            label=_("Location title"),
            max_length=255,
            )
        street_address = forms.CharField(
            required=False,
            label=_("Street Address"),
            )
        street_address2 = forms.CharField(
            required=False,
            label=_("Street Address (2nd line)"),
            )
        city = forms.CharField(
            required=False,
            label=_("City"),
            )
        postal_code = forms.CharField(
            required=False,
            label=_("Postal Code"),
            )
        country = forms.ChoiceField(
            required=False,
            choices=Address._meta.get_field("country").get_choices(),
            label=_("Country"),
            )
        district = forms.CharField(
            required=False,
            widget = forms.HiddenInput(
                attrs={
                    "class": "form_hidden",
                    }
                ),
            )
        longitude = forms.CharField(
            required=False,
            widget = forms.HiddenInput(
                attrs={
                    "class": "form_hidden",
                    }
                ),
            )
        latitude = forms.CharField(
            required=False,
            widget = forms.HiddenInput(
                attrs={
                    "class": "form_hidden",
                    }
                ),
            )
        phone_country = forms.CharField(
            required=False,
            max_length=4,
            initial="49",
            )
        phone_area = forms.CharField(
            required=False,
            max_length=5,
            )
        phone_number = forms.CharField(
            required=False,
            max_length=15,
            label=_("Phone"),
            )
        fax_country = forms.CharField(
            required=False,
            max_length=4,
            initial="49",
            )
        fax_area = forms.CharField(
            required=False,
            max_length=5,
            )
        fax_number = forms.CharField(
            required=False,
            max_length=15,
            label=_("Fax"),
            )
        mobile_country = forms.CharField(
            required=False,
            max_length=4,
            initial="49",
            )
        mobile_area = forms.CharField(
            required=False,
            max_length=5,
            )
        mobile_number = forms.CharField(
            required=False,
            max_length=15,
            label=_("Mobile"),
            )
        email0 = forms.EmailField(
            required=False,
            label=_("E-mail"),
            )
        email1 = forms.EmailField(
            required=False,
            label=_("E-mail"),
            )
        email2 = forms.EmailField(
            required=False,
            label=_("E-mail"),
            )
        url0_type = forms.ChoiceField(
            required=False,
            choices=URL_TYPE_CHOICES,
            label=_("Type"),
            )
        url0_link = forms.URLField(
            required=False,
            label=_("URL"),
            )
        url1_type = forms.ChoiceField(
            required=False,
            choices=URL_TYPE_CHOICES,
            label=_("Type"),
            )
        url1_link = forms.URLField(
            required=False,
            label=_("URL"),
            )
        url2_type = forms.ChoiceField(
            required=False,
            choices=URL_TYPE_CHOICES,
            label=_("Type"),
            )
        url2_link = forms.URLField(
            required=False,
            label=_("URL"),
            )
        im0_type = forms.ChoiceField(
            required=False,
            choices=IM_TYPE_CHOICES,
            label=_("Type"),
            )
        im0_address = forms.CharField(
            required=False,
            max_length=255,
            label=_("Address"),
            )
        im1_type = forms.ChoiceField(
            required=False,
            choices=IM_TYPE_CHOICES,
            label=_("Type"),
            )
        im1_address = forms.CharField(
            required=False,
            max_length=255,
            label=_("Address"),
            )
        im2_type = forms.ChoiceField(
            required=False,
            choices=IM_TYPE_CHOICES,
            label=_("Type"),
            )
        im2_address = forms.CharField(
            required=False,
            max_length=255,
            label=_("Address"),
            )
        save_as_primary = forms.CharField(
            required=False,
            widget = forms.HiddenInput(
                attrs={
                    "class": "form_hidden",
                    }
                ),
            )

        def __init__(self, person, index, *args, **kwargs):
            super(ContactForm, self).__init__()
            self.person = person
            self.index = index
            super(type(self), self).__init__(*args, **kwargs)
            if not args and not kwargs:  # if nothing is posted
                if index is not None and index.isdigit():
                    index = int(index)
                    contact = person.get_contacts()[index]
                    postal_address = contact.postal_address
                    if postal_address:
                        geopos = postal_address.get_geoposition()
                        locality = postal_address.get_locality()
                        self.fields['street_address'].initial = postal_address.street_address
                        self.fields['street_address2'].initial = postal_address.street_address2
                        self.fields['city'].initial = postal_address.city
                        self.fields['postal_code'].initial = postal_address.postal_code
                        self.fields['country'].initial = postal_address.country_id
                        self.fields['district'].initial = getattr(locality, "district", "")
                        self.fields['longitude'].initial = getattr(geopos, "longitude", "")
                        self.fields['latitude'].initial = getattr(geopos, "latitude", "")
                    self.fields['location_type'].initial = contact.location_type_id
                    self.fields['location_title'].initial = contact.location_title
                    self.fields['institution'].initial = contact.institution_id
                    self.fields['phone_country'].initial = contact.phone0_country
                    self.fields['phone_area'].initial = contact.phone0_area
                    self.fields['phone_number'].initial = contact.phone0_number
                    self.fields['fax_country'].initial = contact.phone1_country
                    self.fields['fax_area'].initial = contact.phone1_area
                    self.fields['fax_number'].initial = contact.phone1_number
                    self.fields['mobile_country'].initial = contact.phone2_country
                    self.fields['mobile_area'].initial = contact.phone2_area
                    self.fields['mobile_number'].initial = contact.phone2_number
                    self.fields['url0_type'].initial = contact.url0_type_id
                    self.fields['url0_link'].initial = contact.url0_link
                    self.fields['url1_type'].initial = contact.url1_type_id
                    self.fields['url1_link'].initial = contact.url1_link
                    self.fields['url2_type'].initial = contact.url2_type_id
                    self.fields['url2_link'].initial = contact.url2_link
                    self.fields['im0_type'].initial = contact.im0_type_id
                    self.fields['im0_address'].initial = contact.im0_address
                    self.fields['im1_type'].initial = contact.im1_type_id
                    self.fields['im1_address'].initial = contact.im1_address
                    self.fields['im2_type'].initial = contact.im2_type_id
                    self.fields['im2_address'].initial = contact.im2_address
                    self.fields['email0'].initial = contact.email0_address
                    self.fields['email1'].initial = contact.email1_address
                    self.fields['email2'].initial = contact.email2_address
        def save(self):
            person = self.person
            index = self.index
            data = self.cleaned_data
            save_as_primary = bool(data.get("save_as_primary", False)) 
            if save_as_primary:
                for contact in person.get_contacts():
                    contact.is_primary = False
                    super(type(contact), contact).save()
            elif not person.get_contacts():
                save_as_primary = True
            institution_title = data.get('institution_title', '')
            institution = None
            institution_id = None
            if institution_title:
                institution = Institution.objects.create(
                    title = institution_title
                    )
                institution_id = institution.id
                if hasattr(institution, "create_default_group"):
                    person_group = institution.create_default_group()
                    person_group.content_object = institution
                    person_group.save()
                    membership = person_group.groupmembership_set.create(
                        user = person.user,
                        role = "owners",
                        inviter = person.user,
                        confirmer = person.user,
                        is_accepted = True,
                        )
            if index is not None and index.isdigit(): # change
                index = int(index)
                contact = person.get_contacts()[index]
                contact.location_type_id = data.get('location_type', '')
                contact.location_title = data.get('location_title', '')
                contact.institution_id = institution_id or data.get('institution', None)
                contact.phone0_type = PhoneType.objects.get(slug='phone')
                contact.phone0_country = data.get('phone_country', '')
                contact.phone0_area = data.get('phone_area', '')
                contact.phone0_number = data.get('phone_number', '')
                contact.phone1_type = PhoneType.objects.get(slug='fax')
                contact.phone1_country = data.get('fax_country', '')
                contact.phone1_area = data.get('fax_area', '')
                contact.phone1_number = data.get('fax_number', '')
                contact.phone2_type = PhoneType.objects.get(slug='mobile')
                contact.phone2_country = data.get('mobile_country', '')
                contact.phone2_area = data.get('mobile_area', '')
                contact.phone2_number = data.get('mobile_number', '')
                contact.url0_type_id = data['url0_type'] or None
                contact.url1_type_id = data['url1_type'] or None
                contact.url2_type_id = data['url2_type'] or None
                contact.url0_link = data.get('url0_link', '')
                contact.url1_link = data.get('url1_link', '')
                contact.url2_link = data.get('url2_link', '')
                contact.im0_type_id = data['im0_type'] or None
                contact.im1_type_id = data['im1_type'] or None
                contact.im2_type_id = data['im2_type'] or None
                contact.im0_address = data.get('im0_address', '')
                contact.im1_address = data.get('im1_address', '')
                contact.im2_address = data.get('im2_address', '')
                contact.email0_address = data.get('email0', '')
                contact.email1_address = data.get('email1', '')
                contact.email2_address = data.get('email2', '')
                contact.is_primary = save_as_primary
                contact.save()
            else: # create new
                contact = person.individualcontact_set.create(
                    location_type_id=data['location_type'] or None,
                    location_title=data.get('location_title', ''),
                    institution_id=institution_id or data.get('institution', None),
                    phone0_type=PhoneType.objects.get(slug='phone'),
                    phone0_country=data.get('phone_country', ''),
                    phone0_area=data.get('phone_area', ''),
                    phone0_number=data.get('phone_number', ''),
                    phone1_type=PhoneType.objects.get(slug='fax'),
                    phone1_country=data.get('fax_country', ''),
                    phone1_area=data.get('fax_area', ''),
                    phone1_number=data.get('fax_number', ''),
                    phone2_type=PhoneType.objects.get(slug='mobile'),
                    phone2_country=data.get('mobile_country', ''),
                    phone2_area=data.get('mobile_area', ''),
                    phone2_number=data.get('mobile_number', ''),
                    url0_type_id=data['url0_type'] or None,
                    url1_type_id=data['url1_type'] or None,
                    url2_type_id=data['url2_type'] or None,
                    url0_link=data.get('url0_link', ''),
                    url1_link=data.get('url1_link', ''),
                    url2_link=data.get('url2_link', ''),
                    im0_type_id=data['im0_type'] or None,
                    im1_type_id=data['im1_type'] or None,
                    im2_type_id=data['im2_type'] or None,
                    im0_address=data.get('im0_address', ''),
                    im1_address=data.get('im1_address', ''),
                    im2_address=data.get('im2_address', ''),
                    email0_address=data.get('email0', ''),
                    email1_address=data.get('email1', ''),
                    email2_address=data.get('email2', ''),
                    is_primary=save_as_primary,
                    )
            if data['country']:
                Address.objects.set_for(
                    contact,
                    "postal_address",
                    country=data['country'],
                    district=data['district'],
                    city=data['city'],
                    street_address=data['street_address'],
                    street_address2=data['street_address2'],
                    postal_code=data['postal_code'],
                    latitude=data['latitude'],
                    longitude=data['longitude'],
                    )
            else:
                contact.postal_address = None
            if institution and person in institution.get_owners():
                contact = institution.institutionalcontact_set.create(
                    url0_link = data['institution_website'],
                    is_primary = True,
                    )
                if data['country']:
                    Address.objects.set_for(
                        contact,
                        "postal_address",
                        country=data['country'],
                        district=data['district'],
                        city=data['city'],
                        street_address=data['street_address'],
                        street_address2=data['street_address2'],
                        postal_code=data['postal_code'],
                        latitude=data['latitude'],
                        longitude=data['longitude'],
                        )
            return person
        def get_extra_context(self):
            person = self.person
            index = self.index
            contact = getattr(self, "contact", None)
            if index is not None and index.isdigit():
                index = int(index)
                contact = person.get_contacts()[index]
            return {'contact': contact}
        
    class DetailsForm(dynamicforms.Form):
        individual_type = forms.ChoiceField(
            required=False,
            choices=INDIVIDUAL_TYPE_CHOICES,
            label=_("Status"),
            )
        salutation = forms.ChoiceField(
            required=False,
            choices=SALUTATION_CHOICES,
            label=_("Salutation"),
            )
        birthday_dd = forms.ChoiceField(
            required=False,
            choices=BIRTHDAY_DD_CHOICES,
            label=_("Birthday"),
            )
        birthday_mm = forms.ChoiceField(
            required=False,
            choices=BIRTHDAY_MM_CHOICES,
            label=_("Birthday"),
            )
        birthday_yyyy = forms.ChoiceField(
            required=False,
            choices=BIRTHDAY_YYYY_CHOICES,
            label=_("Birthday"),
            )
        occupation = forms.CharField(
            required=False,
            label=_("Position in the company"),
            )
        nationality = forms.ChoiceField(
            required=False,
            label=_("Nationality"),
            choices=NATIONALITY_CHOICES,
            )
        preferred_language = forms.ChoiceField(
            required=False,
            label=_("Preferred Language"),
            choices=PREFERRED_LANGUAGE_CHOICES,
            )

        def __init__(self, person, index, *args, **kwargs):
            super(DetailsForm, self).__init__()
            self.person = person
            self.index = index
            super(type(self), self).__init__(*args, **kwargs)
            if not args and not kwargs:  # if nothing is posted
                self.fields['individual_type'].initial = person.individual_type_id
                self.fields['salutation'].initial = person.salutation_id
                self.fields['birthday_dd'].initial = person.birthday_dd
                self.fields['birthday_mm'].initial = person.birthday_mm
                self.fields['birthday_yyyy'].initial = person.birthday_yyyy
                self.fields['occupation'].initial = person.occupation
                self.fields['nationality'].initial = person.nationality_id
                self.fields['preferred_language'].initial = person.preferred_language_id
        def save(self):
            person = self.person
            person.individual_type_id = self.cleaned_data['individual_type'] or None
            person.salutation_id = self.cleaned_data['salutation'] or None
            person.birthday_dd = self.cleaned_data['birthday_dd'] or None
            person.birthday_mm = self.cleaned_data['birthday_mm'] or None
            person.birthday_yyyy = self.cleaned_data['birthday_yyyy'] or None
            person.occupation = self.cleaned_data['occupation']
            person.nationality_id = self.cleaned_data['nationality'] or None
            person.preferred_language_id = self.cleaned_data['preferred_language'] or None
            person.save()
            return person
        def get_extra_context(self):
            return {}
    
    class CategoriesForm(dynamicforms.Form):
        choose_creative_sectors = forms.BooleanField(
            initial=True,
            widget=forms.HiddenInput(
                attrs={
                    "class": "form_hidden",
                    }
                ),
            required=False,
            )
        def clean_choose_creative_sectors(self):
            data = self.data
            el_count = 0
            for el in self.creative_sectors.values():
                if el['field_name'] in data:
                    el_count += 1
            if not el_count:
                raise forms.ValidationError(_("Please choose at least one creative sector."))
            return True
            
        choose_context_categories = forms.BooleanField(
            initial=True,
            widget=forms.HiddenInput(
                attrs={
                    "class": "form_hidden",
                    }
                ),
            required=False,
            )
        def clean_choose_context_categories(self):
            data = self.data
            el_count = 0
            for el in self.context_categories.values():
                if el['field_name'] in data:
                    el_count += 1
            if not el_count:
                raise forms.ValidationError(_("Please choose at least one context category."))
            return True

        def __init__(self, person, index, *args, **kwargs):
            super(CategoriesForm, self).__init__()
            self.person = person
            super(type(self), self).__init__(*args, **kwargs)
            self.creative_sectors = {}
            for item in get_related_queryset(Person, "creative_sectors"):
                self.creative_sectors[item.sysname] = {
                    'id': item.id,
                    'field_name': PREFIX_CI + str(item.id),
                }
            self.context_categories = {}
            for item in get_related_queryset(Person, "context_categories"):
                self.context_categories[item.sysname] = {
                    'id': item.id,
                    'field_name': PREFIX_BC + str(item.id),
                }
            for s in self.creative_sectors.values():
                self.fields[s['field_name']] = forms.BooleanField(
                    required=False
                )
            for el in person.get_creative_sectors():
                for ancestor in el.get_ancestors(include_self=True):
                    self.fields[PREFIX_CI + str(ancestor.id)].initial = True
            for c in self.context_categories.values():
                self.fields[c['field_name']] = forms.BooleanField(
                    required=False
                )
            for el in person.get_context_categories():
                for ancestor in el.get_ancestors(include_self=True):
                    self.fields[PREFIX_BC + str(ancestor.id)].initial = True
            
        def save(self, *args, **kwargs):
            person = self.person
            cleaned = self.cleaned_data
            selected_cs = {}
            for item in get_related_queryset(Person, "creative_sectors"):
                if cleaned.get(PREFIX_CI + str(item.id), False):
                    # remove all the parents
                    for ancestor in item.get_ancestors():
                        if ancestor.id in selected_cs:
                            del(selected_cs[ancestor.id])
                    # add current
                    selected_cs[item.id] = item
            person.creative_sectors.clear()
            person.creative_sectors.add(*selected_cs.values())
            
            selected_cc = {}
            for item in get_related_queryset(Person, "context_categories"):
                if cleaned.get(PREFIX_BC + str(item.id), False):
                    # remove all the parents
                    for ancestor in item.get_ancestors():
                        if ancestor.id in selected_cc:
                            del(selected_cc[ancestor.id])
                    # add current
                    selected_cc[item.id] = item
            person.context_categories.clear()
            person.context_categories.add(*selected_cc.values())
            ContextItem.objects.update_for(person)
            return person
            
        def get_extra_context(self):
            return {}
    
    forms = {
        'identity': IdentityForm,
        'description': DescriptionForm,
        'avatar': AvatarForm,
        'contact': ContactForm,
        'details': DetailsForm,
        'categories': CategoriesForm,
        }

class InstitutionProfile: # namespace
    class IdentityForm(dynamicforms.Form):
        title = forms.CharField(
            required=True,
            label=_("Institution Name"),
            )
        title2 = forms.CharField(
            required=False,
            label=_("Institution Name 2nd line"),
            )

        def __init__(self, institution, index, *args, **kwargs):
            super(IdentityForm, self).__init__()
            self.institution = institution
            self.index = index
            super(type(self), self).__init__(*args, **kwargs)
            if not args and not kwargs:  # if nothing is posted
                self.fields['title'].initial = institution.title
                self.fields['title2'].initial = institution.title2
        def save(self):
            institution = self.institution
            institution.title = self.cleaned_data['title']
            institution.title2 = self.cleaned_data['title2']
            institution.save()
            return institution
        def get_extra_context(self):
            return {}
            
    class DescriptionForm(dynamicforms.Form):
        description_en = forms.CharField(
            label=_("Description (English)"),
            required=False,
            widget=forms.Textarea(),
            )
        description_de = forms.CharField(
            label=_("Description (German)"),
            required=False,
            widget=forms.Textarea(),
            )

        def __init__(self, institution, index, *args, **kwargs):
            super(DescriptionForm, self).__init__()
            self.institution = institution
            self.index = index
            super(type(self), self).__init__(*args, **kwargs)
            if not args and not kwargs:  # if nothing is posted
                self.fields['description_en'].initial = institution.description_en
                self.fields['description_de'].initial = institution.description_de
        def save(self):
            institution = self.institution
            institution.description_en = self.cleaned_data['description_en']
            institution.description_de = self.cleaned_data['description_de']
            institution.save()
            return institution
        def get_extra_context(self):
            return {}
    
    class AvatarForm(dynamicforms.Form):
        media_file = ImageField(
            label= _("Photo"),
            help_text= _("You can upload GIF, JPG, PNG, TIFF, and BMP images. The minimal dimensions are %s px.") % STR_MIN_LOGO_SIZE,
            required=False,
            min_dimensions=MIN_LOGO_SIZE,
            )

        def __init__(self, institution, index, *args, **kwargs):
            super(AvatarForm, self).__init__()
            self.institution = institution
            self.index = index
            super(type(self), self).__init__(*args, **kwargs)
        def save(self):
            institution = self.institution
            if "media_file" in self.files:
                media_file = self.files['media_file']
                image_mods.FileManager.save_file_for_object(
                    institution,
                    media_file.name,
                    media_file,
                    subpath = "avatar/"
                    )
            return institution
            
        def get_extra_context(self):
            return {}
    
    class ContactForm(dynamicforms.Form):
        location_type = forms.ChoiceField(
            required=True,
            label=_("Location type"),
            choices=INSTITUTION_LOCATION_TYPE_CHOICES,
            )
        location_title = forms.CharField(
            required=False,
            label=_("Location title"),
            max_length=255,
            )
        street_address = forms.CharField(
            required=True,
            label=_("Street Address"),
            )
        street_address2 = forms.CharField(
            required=False,
            label=_("Street Address (2nd line)"),
            )
        city = forms.CharField(
            required=True,
            label=_("City"),
            )
        postal_code = forms.CharField(
            required=True,
            label=_("Postal Code"),
            )
        country = forms.ChoiceField(
            required=True,
            choices=Address._meta.get_field("country").get_choices(),
            label=_("Country"),
            )
        district = forms.CharField(
            required=False,
            widget = forms.HiddenInput(
                attrs={
                    "class": "form_hidden",
                    }
                ),
            )
        longitude = forms.CharField(
            required=False,
            widget = forms.HiddenInput(
                attrs={
                    "class": "form_hidden",
                    }
                ),
            )
        latitude = forms.CharField(
            required=False,
            widget = forms.HiddenInput(
                attrs={
                    "class": "form_hidden",
                    }
                ),
            )
        phone_country = forms.CharField(
            required=False,
            max_length=4,
            initial="49",
            )
        phone_area = forms.CharField(
            required=False,
            max_length=5,
            )
        phone_number = forms.CharField(
            required=False,
            max_length=15,
            label=_("Phone"),
            )
        fax_country = forms.CharField(
            required=False,
            max_length=4,
            initial="49",
            )
        fax_area = forms.CharField(
            required=False,
            max_length=5,
            )
        fax_number = forms.CharField(
            required=False,
            max_length=15,
            label=_("Fax"),
            )
        mobile_country = forms.CharField(
            required=False,
            max_length=4,
            initial="49",
            )
        mobile_area = forms.CharField(
            required=False,
            max_length=5,
            )
        mobile_number = forms.CharField(
            required=False,
            max_length=15,
            label=_("Mobile"),
            )
        email0 = forms.EmailField(
            required=False,
            label=_("E-mail"),
            )
        email1 = forms.EmailField(
            required=False,
            label=_("E-mail"),
            )
        email2 = forms.EmailField(
            required=False,
            label=_("E-mail"),
            )
        url0_type = forms.ChoiceField(
            required=False,
            choices=URL_TYPE_CHOICES,
            label=_("Type"),
            )
        url0_link = forms.URLField(
            required=False,
            label=_("URL"),
            )
        url1_type = forms.ChoiceField(
            required=False,
            choices=URL_TYPE_CHOICES,
            label=_("Type"),
            )
        url1_link = forms.URLField(
            required=False,
            label=_("URL"),
            )
        url2_type = forms.ChoiceField(
            required=False,
            choices=URL_TYPE_CHOICES,
            label=_("Type"),
            )
        url2_link = forms.URLField(
            required=False,
            label=_("URL"),
            )
        im0_type = forms.ChoiceField(
            required=False,
            choices=IM_TYPE_CHOICES,
            label=_("Type"),
            )
        im0_address = forms.CharField(
            required=False,
            max_length=255,
            label=_("Address"),
            )
        im1_type = forms.ChoiceField(
            required=False,
            choices=IM_TYPE_CHOICES,
            label=_("Type"),
            )
        im1_address = forms.CharField(
            required=False,
            max_length=255,
            label=_("Address"),
            )
        im2_type = forms.ChoiceField(
            required=False,
            choices=IM_TYPE_CHOICES,
            label=_("Type"),
            )
        im2_address = forms.CharField(
            required=False,
            max_length=255,
            label=_("Address"),
            )
        save_as_primary = forms.CharField(
            required=False,
            widget = forms.HiddenInput(
                attrs={
                    "class": "form_hidden",
                    }
                ),
            )

        def __init__(self, institution, index, *args, **kwargs):
            super(ContactForm, self).__init__()
            self.institution = institution
            self.index = index
            super(type(self), self).__init__(*args, **kwargs)
            if not args and not kwargs:  # if nothing is posted
                if index is not None and index.isdigit():
                    index = int(index)
                    contact = institution.get_contacts()[index]
                    postal_address = contact.postal_address
                    geopos = None
                    self.fields['location_type'].initial = contact.location_type_id
                    self.fields['location_title'].initial = contact.location_title
                    if postal_address:
                        geopos = postal_address.get_geoposition()
                        locality = postal_address.get_locality()
                        self.fields['street_address'].initial = postal_address.street_address
                        self.fields['street_address2'].initial = postal_address.street_address2
                        self.fields['city'].initial = postal_address.city
                        self.fields['postal_code'].initial = postal_address.postal_code
                        self.fields['country'].initial = postal_address.country_id
                        self.fields['district'].initial = getattr(locality, "district", "")
                        self.fields['longitude'].initial = getattr(geopos, "longitude", "")
                        self.fields['latitude'].initial = getattr(geopos, "latitude", "")
                    self.fields['phone_country'].initial = contact.phone0_country
                    self.fields['phone_area'].initial = contact.phone0_area
                    self.fields['phone_number'].initial = contact.phone0_number
                    self.fields['fax_country'].initial = contact.phone1_country
                    self.fields['fax_area'].initial = contact.phone1_area
                    self.fields['fax_number'].initial = contact.phone1_number
                    self.fields['mobile_country'].initial = contact.phone2_country
                    self.fields['mobile_area'].initial = contact.phone2_area
                    self.fields['mobile_number'].initial = contact.phone2_number
                    self.fields['url0_type'].initial = contact.url0_type_id
                    self.fields['url0_link'].initial = contact.url0_link
                    self.fields['url1_type'].initial = contact.url1_type_id
                    self.fields['url1_link'].initial = contact.url1_link
                    self.fields['url2_type'].initial = contact.url2_type_id
                    self.fields['url2_link'].initial = contact.url2_link
                    self.fields['im0_type'].initial = contact.im0_type_id
                    self.fields['im0_address'].initial = contact.im0_address
                    self.fields['im1_type'].initial = contact.im1_type_id
                    self.fields['im1_address'].initial = contact.im1_address
                    self.fields['im2_type'].initial = contact.im2_type_id
                    self.fields['im2_address'].initial = contact.im2_address
                    self.fields['email0'].initial = contact.email0_address
                    self.fields['email1'].initial = contact.email1_address
                    self.fields['email2'].initial = contact.email2_address
        def save(self):
            institution = self.institution
            index = self.index
            data = self.cleaned_data
            save_as_primary = bool(data.get("save_as_primary", False)) 
            if save_as_primary:
                for contact in institution.get_contacts():
                    contact.is_primary = False
                    super(type(contact), contact).save()
            elif not institution.get_contacts():
                save_as_primary = True
            if index is not None and index.isdigit(): # change
                index = int(index)
                contact = institution.get_contacts()[index]
                contact.location_type_id = data.get('location_type', '')
                contact.location_title = data.get('location_title', '')
                contact.phone0_type = PhoneType.objects.get(slug='phone')
                contact.phone0_country = data.get('phone_country', '')
                contact.phone0_area = data.get('phone_area', '')
                contact.phone0_number = data.get('phone_number', '')
                contact.phone1_type = PhoneType.objects.get(slug='fax')
                contact.phone1_country = data.get('fax_country', '')
                contact.phone1_area = data.get('fax_area', '')
                contact.phone1_number = data.get('fax_number', '')
                contact.phone2_type = PhoneType.objects.get(slug='mobile')
                contact.phone2_country = data.get('mobile_country', '')
                contact.phone2_area = data.get('mobile_area', '')
                contact.phone2_number = data.get('mobile_number', '')
                contact.url0_type_id = data['url0_type'] or None
                contact.url1_type_id = data['url1_type'] or None
                contact.url2_type_id = data['url2_type'] or None
                contact.url0_link = data.get('url0_link', '')
                contact.url1_link = data.get('url1_link', '')
                contact.url2_link = data.get('url2_link', '')
                contact.im0_type_id = data['im0_type'] or None
                contact.im1_type_id = data['im1_type'] or None
                contact.im2_type_id = data['im2_type'] or None
                contact.im0_address = data.get('im0_address', '')
                contact.im1_address = data.get('im1_address', '')
                contact.im2_address = data.get('im2_address', '')
                contact.email0_address = data.get('email0', '')
                contact.email1_address = data.get('email1', '')
                contact.email2_address = data.get('email2', '')
                contact.is_primary = save_as_primary
                contact.save()
            else: # create new
                contact = institution.institutionalcontact_set.create(
                    location_type_id=data['location_type'] or None,
                    location_title=data.get('location_title', ''),
                    phone0_type=PhoneType.objects.get(slug='phone'),
                    phone0_country=data.get('phone_country', ''),
                    phone0_area=data.get('phone_area', ''),
                    phone0_number=data.get('phone_number', ''),
                    phone1_type=PhoneType.objects.get(slug='fax'),
                    phone1_country=data.get('fax_country', ''),
                    phone1_area=data.get('fax_area', ''),
                    phone1_number=data.get('fax_number', ''),
                    phone2_type=PhoneType.objects.get(slug='mobile'),
                    phone2_country=data.get('mobile_country', ''),
                    phone2_area=data.get('mobile_area', ''),
                    phone2_number=data.get('mobile_number', ''),
                    url0_type_id=data['url0_type'] or None,
                    url1_type_id=data['url1_type'] or None,
                    url2_type_id=data['url2_type'] or None,
                    url0_link=data.get('url0_link', ''),
                    url1_link=data.get('url1_link', ''),
                    url2_link=data.get('url2_link', ''),
                    im0_type_id=data['im0_type'] or None,
                    im1_type_id=data['im1_type'] or None,
                    im2_type_id=data['im2_type'] or None,
                    im0_address=data.get('im0_address', ''),
                    im1_address=data.get('im1_address', ''),
                    im2_address=data.get('im2_address', ''),
                    email0_address=data.get('email0', ''),
                    email1_address=data.get('email1', ''),
                    email2_address=data.get('email2', ''),
                    is_primary=save_as_primary,
                    )
            Address.objects.set_for(
                contact,
                "postal_address",
                country=data['country'],
                district=data['district'],
                city=data['city'],
                street_address=data['street_address'],
                street_address2=data['street_address2'],
                postal_code=data['postal_code'],
                latitude=data['latitude'],
                longitude=data['longitude'],
                )
            return institution
            
        def get_extra_context(self):
            institution = self.institution
            index = self.index
            contact = getattr(self, "contact", None)
            if index is not None and index.isdigit():
                index = int(index)
                contact = institution.get_contacts()[index]
            return {'contact': contact}
        
    class DetailsForm(dynamicforms.Form):
        legal_form = forms.ChoiceField(
            required=True,
            choices=LEGAL_FORM_CHOICES,
            label=_("Legal Form"),
            )
        
        establishment_yyyy = forms.ChoiceField(
            required=False, #should be required=True ???
            choices=ESTABLISHMENT_YYYY_CHOICES,
            label=_("Establishment"),
            error_messages={
                'required': _("Year of establishment is required"),
                },
            )
        establishment_mm = forms.ChoiceField(
            required=False, #should be required=True ???
            choices=ESTABLISHMENT_MM_CHOICES,
            label=_("Establishment"),
            error_messages={
                'required': _("Month of establishment is required"),
                },
            )
        nof_employees = forms.IntegerField(
            required=False,
            label=_("Number of Employees")
            )

        def __init__(self, institution, index, *args, **kwargs):
            super(DetailsForm, self).__init__()
            self.institution = institution
            self.index = index
            super(type(self), self).__init__(*args, **kwargs)
            if not args and not kwargs:  # if nothing is posted
                self.fields['legal_form'].initial = institution.legal_form_id
                self.fields['establishment_yyyy'].initial = institution.establishment_yyyy
                self.fields['establishment_mm'].initial = institution.establishment_mm
                self.fields['nof_employees'].initial = institution.nof_employees
        def save(self):
            institution = self.institution
            institution.legal_form_id = self.cleaned_data.get('legal_form', None)
            institution.establishment_yyyy = self.cleaned_data.get('establishment_yyyy') or None
            institution.establishment_mm = self.cleaned_data.get('establishment_mm') or None
            institution.nof_employees = self.cleaned_data['nof_employees']
            institution.save()
            return institution
            
        def get_extra_context(self):
            return {}
        
    class PaymentForm(dynamicforms.Form):
        is_card_visa_ok = forms.BooleanField(
            label=_("Visa"),
            required=False,
            initial=False,
        )
        
        is_card_mastercard_ok = forms.BooleanField(
            label=_("MasterCard"),
            required=False,
            initial=False,
        )

        is_card_americanexpress_ok = forms.BooleanField(
            label=_("American Express"),
            required=False,
            initial=False,
        )        

        is_paypal_ok = forms.BooleanField(
            label=_("PayPal"),
            required=False,
            initial=False,
        )  
        
        is_cash_ok = forms.BooleanField(
            label=_("Cash"),
            required=False,
            initial=False,
        )  

        is_transaction_ok = forms.BooleanField(
            label=_("Bank transfer"),
            required=False,
            initial=False,
        )
        
        is_prepayment_ok = forms.BooleanField(
            label=_("Prepayment"),
            required=False,
            initial=False,
        )
        
        is_on_delivery_ok = forms.BooleanField(
            label=_("Payment on delivery"),
            required=False,
            initial=False,
        )  
        
        is_invoice_ok = forms.BooleanField(
            label=_("Invoice"),
            required=False,
            initial=False,
        )  

        is_ec_maestro_ok = forms.BooleanField(
            label=_("EC Maestro"),
            required=False,
            initial=False,
        )  
        
        is_giropay_ok = forms.BooleanField(
            label=_("Giropay"),
            required=False,
            initial=False,
        )

        def __init__(self, institution, index, *args, **kwargs):
            super(PaymentForm, self).__init__()
            self.institution = institution
            self.index = index
            super(type(self), self).__init__(*args, **kwargs)
            if not args and not kwargs:  # if nothing is posted
                self.fields['is_card_visa_ok'].initial = institution.is_card_visa_ok
                self.fields['is_card_mastercard_ok'].initial = institution.is_card_mastercard_ok
                self.fields['is_card_americanexpress_ok'].initial = institution.is_card_americanexpress_ok
                self.fields['is_paypal_ok'].initial = institution.is_paypal_ok
                self.fields['is_cash_ok'].initial = institution.is_cash_ok
                self.fields['is_transaction_ok'].initial = institution.is_transaction_ok
                self.fields['is_prepayment_ok'].initial = institution.is_prepayment_ok
                self.fields['is_on_delivery_ok'].initial = institution.is_on_delivery_ok
                self.fields['is_invoice_ok'].initial = institution.is_invoice_ok
                self.fields['is_ec_maestro_ok'].initial = institution.is_ec_maestro_ok
                self.fields['is_giropay_ok'].initial = institution.is_giropay_ok
        def save(self):
            institution = self.institution
            institution.is_card_visa_ok = self.cleaned_data['is_card_visa_ok']
            institution.is_card_mastercard_ok = self.cleaned_data['is_card_mastercard_ok']
            institution.is_card_americanexpress_ok = self.cleaned_data['is_card_americanexpress_ok']
            institution.is_paypal_ok = self.cleaned_data['is_paypal_ok']
            institution.is_cash_ok = self.cleaned_data['is_cash_ok']
            institution.is_transaction_ok = self.cleaned_data['is_transaction_ok']
            institution.is_prepayment_ok = self.cleaned_data['is_prepayment_ok']
            institution.is_on_delivery_ok = self.cleaned_data['is_on_delivery_ok']
            institution.is_invoice_ok = self.cleaned_data['is_invoice_ok']
            institution.is_ec_maestro_ok = self.cleaned_data['is_ec_maestro_ok']
            institution.is_giropay_ok = self.cleaned_data['is_giropay_ok']
            institution.save()
            return institution
            
        def get_extra_context(self):
            return {}
    
    class OpeningHoursForm(dynamicforms.Form):
        show_breaks = forms.BooleanField(
            required=False,                                 
            label=_("Morning/Afternoon"),
            initial=False,
            )
        
        is_appointment_based = forms.BooleanField(
            label=_("Visiting by appointment"),
            required=False,
            initial=False,
            )
        
        mon_open0 = forms.TimeField(required=False)
        mon_close0 = forms.TimeField(required=False)
        mon_open1 = forms.TimeField(required=False)
        mon_close1 = forms.TimeField(required=False)
        mon_is_closed = forms.BooleanField(
            label=_("Closed"),
            required=False,
            initial=False,
            )
    
        tue_open0 = forms.TimeField(required=False)
        tue_close0 = forms.TimeField(required=False)
        tue_open1 = forms.TimeField(required=False)
        tue_close1 = forms.TimeField(required=False)
        tue_is_closed = forms.BooleanField(
            label=_("Closed"),
            required=False,
            initial=False,
            )
    
        wed_open0 = forms.TimeField(required=False)
        wed_close0 = forms.TimeField(required=False)
        wed_open1 = forms.TimeField(required=False)
        wed_close1 = forms.TimeField(required=False)
        wed_is_closed = forms.BooleanField(
            label=_("Closed"),
            required=False,
            initial=False,
            )
        
        thu_open0 = forms.TimeField(required=False)
        thu_close0 = forms.TimeField(required=False)
        thu_open1 = forms.TimeField(required=False)
        thu_close1 = forms.TimeField(required=False)
        thu_is_closed = forms.BooleanField(
            label=_("Closed"),
            required=False,
            initial=False,
            )
        
        fri_open0 = forms.TimeField(required=False)
        fri_close0 = forms.TimeField(required=False)
        fri_open1 = forms.TimeField(required=False)
        fri_close1 = forms.TimeField(required=False)
        fri_is_closed = forms.BooleanField(
            label=_("Closed"),
            required=False,
            initial=False,
            )
        
        sat_open0 = forms.TimeField(required=False)
        sat_close0 = forms.TimeField(required=False)
        sat_open1 = forms.TimeField(required=False)
        sat_close1 = forms.TimeField(required=False)
        sat_is_closed = forms.BooleanField(
            label=_("Closed"),
            required=False,
            initial=False,
            )
        
        sun_open0 = forms.TimeField(required=False)
        sun_close0 = forms.TimeField(required=False)
        sun_open1 = forms.TimeField(required=False)
        sun_close1 = forms.TimeField(required=False)
        sun_is_closed = forms.BooleanField(
            label=_("Closed"),
            required=False,
            initial=False,
            )
        
        exceptions_en = forms.CharField(
            label=_('Exceptions for working hours (English)'),
            required=False,
            widget=forms.Textarea,
            )
        exceptions_de = forms.CharField(
            label=_('Exceptions for working hours (German)'),
            required=False,
            widget=forms.Textarea,
            )

        def __init__(self, institution, index, *args, **kwargs):
            super(OpeningHoursForm, self).__init__()
            self.institution = institution
            self.index = index
            super(type(self), self).__init__(*args, **kwargs)
            if not args and not kwargs:  # if nothing is posted
                self.fields['is_appointment_based'].initial = institution.is_appointment_based
                show_breaks = False
                for d in WEEK_DAYS:
                    time_open = getattr(
                        institution,
                        '%s_open' % d,
                        None,
                    )
                    time_break_close = getattr(
                        institution,
                        '%s_break_close' % d,
                        None,
                    )
                    time_break_open = getattr(
                        institution,
                        '%s_break_open' % d,
                        None,
                    )
                    time_close = getattr(
                        institution,
                        '%s_close' % d,
                        None,
                    )

                    self.fields['%s_open0' % d].initial = time_open
                    if not time_break_close:
                        self.fields['%s_close0' % d].initial = time_close
                    else:
                        self.fields['%s_close0' % d].initial = time_break_close
                        self.fields['%s_open1' % d].initial = time_break_open
                        self.fields['%s_close1' % d].initial = time_close
                        show_breaks = True
                    self.fields['%s_is_closed' % d].initial = not time_open
                self.fields['exceptions_en'].initial = institution.exceptions_en
                self.fields['exceptions_de'].initial = institution.exceptions_de
                self.fields['show_breaks'].initial = show_breaks
                
        def clean(self):
            
            show_breaks = self.cleaned_data.get('show_breaks', False)
            for week_day in WEEK_DAYS:

                is_closed = self.cleaned_data.get(week_day + '_is_closed', False)
                open0 = self.cleaned_data.get(week_day + '_open0', None)
                close0 = self.cleaned_data.get(week_day + '_close0', None)
                open1 = self.cleaned_data.get(week_day + '_open1', None)
                close1 = self.cleaned_data.get(week_day + '_close1', None)
                    
                # here, we apply opening hours and do some checks
                if not is_closed:
                    if open0:
                        if not close0:
                            self._errors[week_day + '_open0'] = [_("Please enter a closing time.")]
                        elif close0 < open0:
                            self._errors[week_day + '_open0'] = [_("A closing time must not be before an opening time.")]
                    if close0:
                        if not open0:
                            self._errors[week_day + '_open0'] = [_("Please enter an opening time.")]
                    
                    if show_breaks:
                        if open1:
                            if not close1:
                                self._errors[week_day + '_open1'] = [_("Please enter a closing time.")]
                            elif close1 < open1:
                                self._errors[week_day + '_open1'] = [_("A closing time must not be before an opening time.")]
                        if close1:
                            if not open1:
                                self._errors[week_day + '_open1'] = [_("Please enter an opening time.")]
                        
                        if open1 or close1:
                            if not open0 or not close0:
                                self._errors[week_day + '_open1']  = [_("When specifying breaks, you must enter all data.")]
                            else:
                                if open1 < close0:
                                    self._errors[week_day + '_open1']  = [_("An opening time after break must not be before the closing time to break.")]
                        
                        if open0 and open1 and close0 and close1:
                           self.cleaned_data[week_day + '_open'] = open0
                           self.cleaned_data[week_day + '_break_close'] = close0
                           self.cleaned_data[week_day + '_break_open'] = open1
                           self.cleaned_data[week_day + '_close'] = close1
                        elif open0 and close0:
                           self.cleaned_data[week_day + '_open'] = open0
                           self.cleaned_data[week_day + '_close'] = close0
                    else:
                        if open0 and close0:
                           self.cleaned_data[week_day + '_open'] = open0
                           self.cleaned_data[week_day + '_close'] = close0
                           
            return self.cleaned_data
            
        def save(self):
            institution = self.institution
            for d in WEEK_DAYS:
                time_open0 = self.cleaned_data['%s_open0' % d]
                time_close0 = self.cleaned_data['%s_close0' % d]
                time_open1 = self.cleaned_data['%s_open1' % d]
                time_close1 = self.cleaned_data['%s_close1' % d]
                setattr(institution, '%s_open' % d, time_open0)
                if time_open1:
                    setattr(institution, '%s_break_close' % d, time_close0)
                    setattr(institution, '%s_break_open' % d, time_open1)
                    setattr(institution, '%s_close' % d, time_close1)
                else:
                    setattr(institution, '%s_break_close' % d, None)
                    setattr(institution, '%s_break_open' % d, None)
                    setattr(institution, '%s_close' % d, time_close0)
            
            institution.exceptions_en = self.cleaned_data.get('exceptions_en', '')
            institution.exceptions_de = self.cleaned_data.get('exceptions_de', '')
            institution.is_appointment_based = self.cleaned_data.get('is_appointment_based', False)
            
            institution.save()
            return institution
            
        def get_extra_context(self):
            return {}
    
    class CategoriesForm(dynamicforms.Form):
        choose_creative_sectors = forms.BooleanField(
            initial=True,
            widget=forms.HiddenInput(
                attrs={
                    "class": "form_hidden",
                    }
                ),
            required=False,
            )
        def clean_choose_creative_sectors(self):
            data = self.data
            el_count = 0
            for el in self.creative_sectors.values():
                if el['field_name'] in data:
                    el_count += 1
            if not el_count:
                raise forms.ValidationError(_("Please choose at least one creative sector."))
            return True
            
        choose_context_categories = forms.BooleanField(
            initial=True,
            widget=forms.HiddenInput(
                attrs={
                    "class": "form_hidden",
                    }
                ),
            required=False,
            )
        def clean_choose_context_categories(self):
            data = self.data
            el_count = 0
            for el in self.context_categories.values():
                if el['field_name'] in data:
                    el_count += 1
            if not el_count:
                raise forms.ValidationError(_("Please choose at least one context category."))
            return True
            
        choose_object_types = forms.BooleanField(
            initial=True,
            widget=forms.HiddenInput(
                attrs={
                    "class": "form_hidden",
                    }
                ),
            required=False,
            )
        def clean_choose_object_types(self):
            data = self.data
            el_count = 0
            for el in self.object_types.values():
                if el['field_name'] in data:
                    el_count += 1
            if not el_count:
                raise forms.ValidationError(_("Please choose at least one object type."))
            return True

        def __init__(self, institution, index, *args, **kwargs):
            super(CategoriesForm, self).__init__()
            self.institution = institution
            super(type(self), self).__init__(*args, **kwargs)
            self.creative_sectors = {}
            for item in get_related_queryset(Institution, "creative_sectors"):
                self.creative_sectors[item.sysname] = {
                    'id': item.id,
                    'field_name': PREFIX_CI + str(item.id),
                }
            self.context_categories = {}
            for item in get_related_queryset(Institution, "context_categories"):
                self.context_categories[item.sysname] = {
                    'id': item.id,
                    'field_name': PREFIX_BC + str(item.id),
                }
            self.object_types = {}
            for item in get_related_queryset(Institution, "institution_types"):
                self.object_types[item.slug] = {
                    'id': item.id,
                    'field_name': PREFIX_OT + str(item.id),
                }
            for s in self.creative_sectors.values():
                self.fields[s['field_name']] = forms.BooleanField(
                    required=False
                )
            for el in institution.get_creative_sectors():
                for ancestor in el.get_ancestors(include_self=True):
                    self.fields[PREFIX_CI + str(ancestor.id)].initial = True
            for c in self.context_categories.values():
                self.fields[c['field_name']] = forms.BooleanField(
                    required=False
                )
            for el in institution.get_context_categories():
                for ancestor in el.get_ancestors(include_self=True):
                    self.fields[PREFIX_BC + str(ancestor.id)].initial = True
            for t in self.object_types.values():
                self.fields[t['field_name']] = forms.BooleanField(
                    required=False
                )
            for el in institution.get_object_types():
                for ancestor in el.get_ancestors(include_self=True):
                    self.fields[PREFIX_OT + str(ancestor.id)].initial = True
            
        def save(self, *args, **kwargs):
            institution = self.institution
            cleaned = self.cleaned_data
            selected_cs = {}
            for item in get_related_queryset(Institution, "creative_sectors"):
                if cleaned.get(PREFIX_CI + str(item.id), False):
                    # remove all the parents
                    for ancestor in item.get_ancestors():
                        if ancestor.id in selected_cs:
                            del(selected_cs[ancestor.id])
                    # add current
                    selected_cs[item.id] = item
            institution.creative_sectors.clear()
            institution.creative_sectors.add(*selected_cs.values())
            
            selected_cc = {}
            for item in get_related_queryset(Institution, "context_categories"):
                if cleaned.get(PREFIX_BC + str(item.id), False):
                    # remove all the parents
                    for ancestor in item.get_ancestors():
                        if ancestor.id in selected_cc:
                            del(selected_cc[ancestor.id])
                    # add current
                    selected_cc[item.id] = item
            institution.context_categories.clear()
            institution.context_categories.add(*selected_cc.values())
            
            selected_ot = {}
            for item in get_related_queryset(Institution, "institution_types"):
                if cleaned.get(PREFIX_OT + str(item.id), False):
                    # remove all the parents
                    for ancestor in item.get_ancestors():
                        if ancestor.id in selected_ot:
                            del(selected_ot[ancestor.id])
                    # add current
                    selected_ot[item.id] = item
            institution.institution_types.clear()
            institution.institution_types.add(*selected_ot.values())
            ContextItem.objects.update_for(institution)
            return institution

        def get_extra_context(self):
            return {}
    
    forms = {
        'identity': IdentityForm,
        'description': DescriptionForm,
        'avatar': AvatarForm,
        'contact': ContactForm,
        'details': DetailsForm,
        'payment': PaymentForm,
        'opening_hours': OpeningHoursForm,
        'categories': CategoriesForm,
        }

class EventProfile: # namespace
    class IdentityForm(dynamicforms.Form):
        title_en = forms.CharField(
            required=True,
            label=_("Title (English)"),
            )
        title_de = forms.CharField(
            required=True,
            label=_("Title (German)"),
            )
        event_type = forms.ChoiceField(
            required=True,
            choices=EVENT_TYPE_CHOICES,
            label=_("Event Type"),
            )

        def __init__(self, event, index, *args, **kwargs):
            super(IdentityForm, self).__init__()
            self.event = event
            self.index = index
            super(type(self), self).__init__(*args, **kwargs)
            if not args and not kwargs:  # if nothing is posted
                self.fields['title_de'].initial = event.title_de
                self.fields['title_en'].initial = event.title_en
                self.fields['event_type'].initial = event.event_type_id
        def save(self):
            event = self.event
            event.title_de = self.cleaned_data['title_de']
            event.title_en = self.cleaned_data['title_en']
            event.event_type_id = self.cleaned_data['event_type']
            event.save()
            return event
            
        def get_extra_context(self):
            return {}
            
    class DescriptionForm(dynamicforms.Form):
        description_en = forms.CharField(
            label=_("Description (English)"),
            required=False,
            widget=forms.Textarea(),
            )
        description_de = forms.CharField(
            label=_("Description (German)"),
            required=False,
            widget=forms.Textarea(),
            )

        def __init__(self, event, index, *args, **kwargs):
            super(DescriptionForm, self).__init__()
            self.event = event
            self.index = index
            super(type(self), self).__init__(*args, **kwargs)
            if not args and not kwargs:  # if nothing is posted
                self.fields['description_en'].initial = event.description_en
                self.fields['description_de'].initial = event.description_de
        def save(self):
            event = self.event
            event.description_en = self.cleaned_data['description_en']
            event.description_de = self.cleaned_data['description_de']
            event.save()
            return event
        def get_extra_context(self):
            return {}
    
    class AvatarForm(dynamicforms.Form):
        media_file = ImageField(
            label= _("Photo"),
            help_text= _("You can upload GIF, JPG, PNG, TIFF, and BMP images. The minimal dimensions are %s px.") % STR_MIN_LOGO_SIZE,
            required=False,
            min_dimensions=MIN_LOGO_SIZE,
            )

        def __init__(self, event, index, *args, **kwargs):
            super(AvatarForm, self).__init__()
            self.event = event
            self.index = index
            super(type(self), self).__init__(*args, **kwargs)
        def save(self):
            event = self.event
            if "media_file" in self.files:
                media_file = self.files['media_file']
                image_mods.FileManager.save_file_for_object(
                    event,
                    media_file.name,
                    media_file,
                    subpath = "avatar/"
                    )
            return event
        def get_extra_context(self):
            return {}
    
    class ContactForm(dynamicforms.Form):
        venue = AutocompleteField(
            label=_("Venue/Institution"),
            required=False,
            help_text=_("Please enter a letter to display a list of available venues"),
            app="events", 
            qs_function="get_venues",   
            display_attr="title", 
            add_display_attr="get_address_string",
            options={
                "minChars": 1,
                "max": 20,
                "mustMatch": 1,
                "highlight" : False,
            }
        )
        
        venue_title = forms.CharField(
            required=False,
            label=_("Venue/Institution Title"),
        )
        
        street_address = forms.CharField(
            required=False,
            label=_("Street Address"),
            )
        street_address2 = forms.CharField(
            required=False,
            label=_("Street Address (2nd line)"),
            )
        city = forms.CharField(
            required=True,
            label=_("City"),
            )
        postal_code = forms.CharField(
            required=False,
            label=_("Postal Code"),
            )
        country = forms.ChoiceField(
            required=True,
            choices=Address._meta.get_field("country").get_choices(),
            label=_("Country"),
            )
        district = forms.CharField(
            required=False,
            widget = forms.HiddenInput(
                attrs={
                    "class": "form_hidden",
                    }
                ),
            )
        longitude = forms.CharField(
            required=False,
            widget = forms.HiddenInput(
                attrs={
                    "class": "form_hidden",
                    }
                ),
            )
        latitude = forms.CharField(
            required=False,
            widget = forms.HiddenInput(
                attrs={
                    "class": "form_hidden",
                    }
                ),
            )
        phone_country = forms.CharField(
            required=False,
            max_length=4,
            initial="49",
            )
        phone_area = forms.CharField(
            required=False,
            max_length=5,
            )
        phone_number = forms.CharField(
            required=False,
            max_length=15,
            label=_("Phone"),
            )
        fax_country = forms.CharField(
            required=False,
            max_length=4,
            initial="49",
            )
        fax_area = forms.CharField(
            required=False,
            max_length=5,
            )
        fax_number = forms.CharField(
            required=False,
            max_length=15,
            label=_("Fax"),
            )
        mobile_country = forms.CharField(
            required=False,
            max_length=4,
            initial="49",
            )
        mobile_area = forms.CharField(
            required=False,
            max_length=5,
            )
        mobile_number = forms.CharField(
            required=False,
            max_length=15,
            label=_("Mobile"),
            )
        email0 = forms.EmailField(
            required=False,
            label=_("E-mail"),
            )
        email1 = forms.EmailField(
            required=False,
            label=_("E-mail"),
            )
        email2 = forms.EmailField(
            required=False,
            label=_("E-mail"),
            )
        url0_type = forms.ChoiceField(
            required=False,
            choices=URL_TYPE_CHOICES,
            label=_("Type"),
            )
        url0_link = forms.URLField(
            required=False,
            label=_("URL"),
            )
        url1_type = forms.ChoiceField(
            required=False,
            choices=URL_TYPE_CHOICES,
            label=_("Type"),
            )
        url1_link = forms.URLField(
            required=False,
            label=_("URL"),
            )
        url2_type = forms.ChoiceField(
            required=False,
            choices=URL_TYPE_CHOICES,
            label=_("Type"),
            )
        url2_link = forms.URLField(
            required=False,
            label=_("URL"),
            )
        im0_type = forms.ChoiceField(
            required=False,
            choices=IM_TYPE_CHOICES,
            label=_("Type"),
            )
        im0_address = forms.CharField(
            required=False,
            max_length=255,
            label=_("Address"),
            )
        im1_type = forms.ChoiceField(
            required=False,
            choices=IM_TYPE_CHOICES,
            label=_("Type"),
            )
        im1_address = forms.CharField(
            required=False,
            max_length=255,
            label=_("Address"),
            )
        im2_type = forms.ChoiceField(
            required=False,
            choices=IM_TYPE_CHOICES,
            label=_("Type"),
            )
        im2_address = forms.CharField(
            required=False,
            max_length=255,
            label=_("Address"),
            )

        def __init__(self, event, index, *args, **kwargs):
            super(ContactForm, self).__init__()
            self.event = event
            self.index = index
            super(type(self), self).__init__(*args, **kwargs)
            if not args and not kwargs:  # if nothing is posted
                contact = event.get_contacts()[0]
                postal_address = contact.postal_address
                geopos = postal_address.get_geoposition()
                locality = postal_address.get_locality()
                self.fields['venue'].initial = event.venue_id
                self.fields['venue_title'].initial = event.venue_title
                self.fields['street_address'].initial = postal_address.street_address
                self.fields['street_address2'].initial = postal_address.street_address2
                self.fields['city'].initial = postal_address.city
                self.fields['postal_code'].initial = postal_address.postal_code
                self.fields['country'].initial = postal_address.country_id
                self.fields['district'].initial = getattr(locality, "district", "")
                self.fields['longitude'].initial = getattr(geopos, "longitude", "")
                self.fields['latitude'].initial = getattr(geopos, "latitude", "")
                self.fields['phone_country'].initial = contact.phone0_country
                self.fields['phone_area'].initial = contact.phone0_area
                self.fields['phone_number'].initial = contact.phone0_number
                self.fields['fax_country'].initial = contact.phone1_country
                self.fields['fax_area'].initial = contact.phone1_area
                self.fields['fax_number'].initial = contact.phone1_number
                self.fields['mobile_country'].initial = contact.phone2_country
                self.fields['mobile_area'].initial = contact.phone2_area
                self.fields['mobile_number'].initial = contact.phone2_number
                self.fields['url0_type'].initial = contact.url0_type_id
                self.fields['url0_link'].initial = contact.url0_link
                self.fields['url1_type'].initial = contact.url1_type_id
                self.fields['url1_link'].initial = contact.url1_link
                self.fields['url2_type'].initial = contact.url2_type_id
                self.fields['url2_link'].initial = contact.url2_link
                self.fields['im0_type'].initial = contact.im0_type_id
                self.fields['im0_address'].initial = contact.im0_address
                self.fields['im1_type'].initial = contact.im1_type_id
                self.fields['im1_address'].initial = contact.im1_address
                self.fields['im2_type'].initial = contact.im2_type_id
                self.fields['im2_address'].initial = contact.im2_address
                self.fields['email0'].initial = contact.email0_address
                self.fields['email1'].initial = contact.email1_address
                self.fields['email2'].initial = contact.email2_address
                
        def clean(self):
            # if venue is selected, the venue_title etc need not to be filled in and vice versa!
            data = super(type(self), self).clean()
            if data.get('venue_title', None):
                if 'venue' in self._errors:
                    del self._errors['venue']
            else:
                if data.get('venue', None):
                    for field_name in [
                        'venue_title',
                        'street_address',
                        'postal_code',
                        'city',
                        'country'
                        ]:
                        if field_name in self._errors:
                            del self._errors[field_name]
            return data
            
        def save(self):
            event = self.event
            index = self.index
            data = self.cleaned_data
            
            # venue data
            venue = None
            if data.get('venue', None):
                try:
                    venue = Institution.objects.get(id=data['venue'])
                except:
                    return
                #venue_title = venue.get_title()
            #else:
            venue_title = data.get('venue_title', None)
            
            event.venue = venue
            event.venue_title = venue_title
            event.phone0_type = PhoneType.objects.get(slug='phone')
            event.phone0_country = data.get('phone_country', '')
            event.phone0_area = data.get('phone_area', '')
            event.phone0_number = data.get('phone_number', '')
            event.phone1_type = PhoneType.objects.get(slug='fax')
            event.phone1_country = data.get('fax_country', '')
            event.phone1_area = data.get('fax_area', '')
            event.phone1_number = data.get('fax_number', '')
            event.phone2_type = PhoneType.objects.get(slug='mobile')
            event.phone2_country = data.get('mobile_country', '')
            event.phone2_area = data.get('mobile_area', '')
            event.phone2_number = data.get('mobile_number', '')
            event.url0_type_id = data['url0_type'] or None
            event.url1_type_id = data['url1_type'] or None
            event.url2_type_id = data['url2_type'] or None
            event.url0_link = data.get('url0_link', '')
            event.url1_link = data.get('url1_link', '')
            event.url2_link = data.get('url2_link', '')
            event.im0_type_id = data['im0_type'] or None
            event.im1_type_id = data['im1_type'] or None
            event.im2_type_id = data['im2_type'] or None
            event.im0_address = data.get('im0_address', '')
            event.im1_address = data.get('im1_address', '')
            event.im2_address = data.get('im2_address', '')
            event.email0_address = data.get('email0', '')
            event.email1_address = data.get('email1', '')
            event.email2_address = data.get('email2', '')
            event.save()
            Address.objects.set_for(
                event,
                "postal_address",
                country=data.get("country", ""),
                district=data.get("district", ""),
                city=data.get("city", ""),
                street_address=data.get("street_address", ""),
                street_address2=data.get("street_address2", ""),
                postal_code=data.get("postal_code", ""),
                latitude=data.get("latitude", ""),
                longitude=data.get("longitude", ""),
                )
            return event
        def get_extra_context(self):
            return {}

    class OrganizerForm(dynamicforms.Form):
        """
        A form for the informaton who or what institution organizes the event
        """
        organizing_institution = AutocompleteField(
            required=False,
            label=_("Organizing institution"),
            help_text=_("Please enter a letter to display a list of available institutions"),
            app="events", 
            qs_function="get_organizing_institutions",   
            display_attr="title", 
            add_display_attr="get_address_string",
            options={
                "minChars": 1,
                "max": 20,
                "mustMatch": 1,
                "highlight" : False,
                }
            )
        
        organizer_title = forms.CharField(
            required=False,
            label=_("Name of Institution"),
            )
        
        organizer_url_link = forms.URLField(
            required=False,
            label=_("Website"),
            )

        is_organized_by_myself = forms.BooleanField(
            required=False,
            label=_("Organized by myself")
            )

        def __init__(self, event, index, *args, **kwargs):
            super(OrganizerForm, self).__init__()
            self.event = event
            self.index = index
            super(type(self), self).__init__(*args, **kwargs)
            self.fields['organizing_institution'].initial = event.organizing_institution_id
            self.fields['organizer_title'].initial = event.organizer_title
            self.fields['organizer_url_link'].initial = event.organizer_url_link
            current_user = get_current_user()
            self.fields['is_organized_by_myself'].initial = bool(event.organizing_person)
            if event.creator and current_user != event.creator:
                self.fields['is_organized_by_myself'].label = _(
                    "Organized by %s") % event.creator.profile.get_title()
                
        def save(self):
            event = self.event
            data = self.cleaned_data

            event.organizing_person = (
                None,
                not event.creator and get_current_user().profile or event.creator.profile,
                )[data.get("is_organized_by_myself", False)]
            event.organizing_institution_id=data['organizing_institution'] or None
            event.organizer_title = data.get('organizer_title', None)
            event.organizer_url_link = data.get('organizer_url_link', None)
            event.save()
            return event
            
        def get_extra_context(self):
            return {}

    class AdditionalInfoForm(dynamicforms.Form):
        
        additional_info_en = forms.CharField(
            label= _("Additional Info English (Max 500 Characters)"),
            required=False,
            widget=forms.Textarea(),
            max_length=500,
            )
        additional_info_de = forms.CharField(
            label= _("Additional Info German (Max 500 Characters)"),
            required=False,
            widget=forms.Textarea(),
            max_length=500,
            )
        
        related_events = forms.ModelMultipleChoiceField(
            label=_("Related Events"),
            queryset=get_related_queryset(Event, "related_events").all(),
            required=False,
        )

        def __init__(self, event, index, *args, **kwargs):
            super(AdditionalInfoForm, self).__init__()
            self.event = event
            self.index = index
            super(type(self), self).__init__(*args, **kwargs)
            self.fields['related_events'].initial = event.related_events.values_list("pk", flat=True)
            self.fields['additional_info_en'].initial = event.additional_info_en
            self.fields['additional_info_de'].initial = event.additional_info_de
                
        def save(self):
            event = self.event
            data = self.cleaned_data

            event.additional_info_en = data['additional_info_en']
            event.additional_info_de = data['additional_info_de']
            event.save()
            event.related_events.clear()
            for ev in data['related_events']:
                event.related_events.add(ev)
            return event
            
        def get_extra_context(self):
            return {}
    
    class EventTimesForm(dynamicforms.Form):
        """
        Dummy form for using together with a formset of EventTimeForm
        """

        def __init__(self, event, index, *args, **kwargs):
            super(EventTimesForm, self).__init__()
            self.event = event
            self.index = index
            super(type(self), self).__init__(*args, **kwargs)
        def save(self):
            return self.event
        def get_extra_context(self):
            return {}
            
    class EventTimeForm(dynamicforms.Form):
        """
        Form for event "main data"
        """
        
        id = forms.IntegerField(
            required=False,
            widget=forms.HiddenInput,
            )
        
        label = forms.ModelChoiceField(
            required=False,
            queryset=get_related_queryset(EventTime, "label"),
            )
        
        start_yyyy = forms.ChoiceField(
            required=True,
            choices=YEARS_CHOICES,
            label=_("Start Year"),
            )
    
        start_mm = forms.ChoiceField(
            required=False,
            choices=MONTHS_CHOICES,
            label=_("Start Month"),
            )
        
        start_dd = forms.ChoiceField(
            required=False,
            choices=DAYS_CHOICES,
            label=_("Start Day"),
            )
        
        start_hh = forms.ChoiceField(
            required=False,
            choices=HOURS_CHOICES,
            label=_("Start Hours"),
            )
        
        start_ii = forms.ChoiceField(
            required=False,
            choices=MINUTES_CHOICES,
            label=_("Start Minutes"),
            )
        
        end_yyyy = forms.ChoiceField(
            required=False,
            choices=YEARS_CHOICES,
            label=_("End Year"),
            )
        
        end_mm = forms.ChoiceField(
            required=False,
            choices=MONTHS_CHOICES,
            label=_("End Month"),
            )
        
        end_dd = forms.ChoiceField(
            required=False,
            choices=DAYS_CHOICES,
            label=_("End Day"),
            )
        
        end_hh = forms.ChoiceField(
            required=False,
            choices=HOURS_CHOICES,
            label=_("End Hours"),
            )
        
        end_ii = forms.ChoiceField(
            required=False,
            choices=MINUTES_CHOICES,
            label=_("End Minutes"),
            )
        
        is_all_day = forms.BooleanField(
            required=False,
            label=_("All Day")
            )

        def __init__(self, event, index, *args, **kwargs):
            super(EventTimeForm, self).__init__()
            self.event = event
            self.index = index
            kwargs.setdefault('initial', {})
            kwargs['initial']['label'] = kwargs['initial'].get("label_id", None)
            super(type(self), self).__init__(*args, **kwargs)
            
        def clean(self):
            """"
            Below, there is some (simple and complex) validation logic:
            for example, some fields are not required, if a venue is seleceted.
            the "_errors" stuff there is a bit of a hack, but there seems 
            to be no other possibility to simulate the "required" attribute after
            field validation, because the fields clean method is called
            before and there is some "field required error" raised, which
            we have to eliminate manually. We set all the fields "required", even
            if you can enter alternatiave data. (You have this nice "*" attached
            to the label of the field indicating that you must fill in!
            (TODO Aidas, maybe you know something better!)
            """ 

            # start date must be valid!
            start_date = None
            end_date = None
            start_yyyy = self.cleaned_data.get('start_yyyy', None)
            start_mm = self.cleaned_data.get('start_mm', None)
            start_dd = self.cleaned_data.get('start_dd', None)
 
            # any error handling is overwritten!
            if self._errors.get('start_yyyy', False):
                del self._errors['start_yyyy']
            if self._errors.get('start_mm', False):
                del self._errors['start_mm']
            if self._errors.get('start_dd', False):
                del self._errors['start_dd']

            if start_dd:
                if not start_mm:
                    self._errors['start_dd'] = [_("Please enter a valid month.")]
            try:
                start_date = datetime.date(int(start_yyyy), int(start_mm or 1), int(start_dd or 1))
            except:
                self._errors['start_dd'] = [_("Please enter a valid date.")]
        
            # start time or "all day must be entered"
            if 'start_hh' in self._errors or 'start_ii' in self._errors:
                self._errors['start_dd'] = [_("Please enter a valid time using format 'HH:MM' or choose 'All Day'")]
                if self.cleaned_data.get('is_all_day', False):
                    del self._errors['start_hh']
                    del self._errors['start_ii']
            
            if self.cleaned_data.get('start_hh', None) and not self.cleaned_data.get('start_ii', None):
                self.cleaned_data['start_ii'] = '0'
            
            if self.cleaned_data.get('end_hh', None) and not self.cleaned_data.get('end_ii', None):
                self.cleaned_data['end_ii'] = '0'

            
            
            # if start time is specified, day, month and year must be specified
            if self.cleaned_data.get('start_hh', None):
                if not (start_yyyy and start_mm and start_dd):
                    self._errors['start_hh'] = [_("If you choose a time, please enter a valid day, month and year.")]

            # if end date is specified, all fields must be specified!
            end_yyyy = self.cleaned_data.get('end_yyyy', None)
            end_mm = self.cleaned_data.get('end_mm', None)
            end_dd = self.cleaned_data.get('end_dd', None)
            
            if self._errors.get('end_yyyy', False):
                del self._errors['end_yyyy'] 
            if self._errors.get('end_mm', False):                    
                del self._errors['end_mm']
            if self._errors.get('end_dd', False):                    
                del self._errors['end_dd']     
            
            if end_yyyy or end_mm or end_dd:
                if end_dd:
                    if not end_mm:
                        self._errors['end_dd'] = [_("Please enter a valid month.")]
                try:
                    end_date = datetime.date(int(end_yyyy), int(end_mm or 1), int(end_dd or 1))
                except:
                    self._errors['end_dd'] = [_("If you want to specify an end date, please enter a valid one.")]

            if end_date and start_date:
                if start_date > end_date:
                    self._errors['end_dd'] = [_("End date must be after start date.")]
                    
            # if end time is specified, day, month and year must be specified
            if self.cleaned_data.get('end_hh', None):
                if not (end_yyyy and end_mm and end_dd):
                    self._errors['end_hh'] = [_("If you choose a time, please enter a valid day, month and year.")]
                    
            return self.cleaned_data
        
        def is_valid(self):
            is_valid = super(EventForm.EventTimeForm, self).is_valid()
            errors = self._errors
            return is_valid
            
        def save(self):
            cleaned = self.cleaned_data
            if cleaned['id']:
                time = self.event.eventtime_set.get(pk=cleaned["id"])
            else:
                time = EventTime(event=self.event)
                
            time.label = cleaned['label'] or None
            
            time.start_yyyy = cleaned['start_yyyy'] or None 
            time.start_mm = cleaned['start_mm'] or None 
            time.start_dd = cleaned['start_dd'] or None
            time.start_hh = cleaned['start_hh'] or None
            time.start_ii = cleaned['start_ii'] or None
            
            time.end_yyyy = cleaned['end_yyyy'] or None 
            time.end_mm = cleaned['end_mm'] or None 
            time.end_dd = cleaned['end_dd'] or None
            time.end_hh = cleaned['end_hh'] or None
            time.end_ii = cleaned['end_ii'] or None
            time.is_all_day = cleaned.get('is_all_day', False)
            
            time.save()
            
            event = time.event
            event.status = "published"
            event.save()
            
            return time
            
    class FeesOpeningHoursForm(dynamicforms.Form):
        """
        Form for fees and opening hours
        """
        fees_en = forms.CharField(
            label=_("Fees (English)"),
            required=False,
            widget=forms.Textarea(),
            )
        fees_de = forms.CharField(
            label=_("Fees (German)"),
            required=False,
            widget=forms.Textarea(),
            )
        
        show_breaks = forms.BooleanField(
            required=False,                                 
            label=_("Morning/Afternoon"),
            initial=False,
            )
        
        mon_open0 = forms.TimeField(required=False)
        mon_close0 = forms.TimeField(required=False)
        mon_open1 = forms.TimeField(required=False)
        mon_close1 = forms.TimeField(required=False)
        mon_is_closed = forms.BooleanField(
            label=_("Closed"),
            required=False,
            initial=False,
            )
    
        tue_open0 = forms.TimeField(required=False)
        tue_close0 = forms.TimeField(required=False)
        tue_open1 = forms.TimeField(required=False)
        tue_close1 = forms.TimeField(required=False)
        tue_is_closed = forms.BooleanField(
            label=_("Closed"),
            required=False,
            initial=False,
            )
    
        wed_open0 = forms.TimeField(required=False)
        wed_close0 = forms.TimeField(required=False)
        wed_open1 = forms.TimeField(required=False)
        wed_close1 = forms.TimeField(required=False)
        wed_is_closed = forms.BooleanField(
            label=_("Closed"),
            required=False,
            initial=False,
            )
        
        thu_open0 = forms.TimeField(required=False)
        thu_close0 = forms.TimeField(required=False)
        thu_open1 = forms.TimeField(required=False)
        thu_close1 = forms.TimeField(required=False)
        thu_is_closed = forms.BooleanField(
            label=_("Closed"),
            required=False,
            initial=False,
            )
        
        fri_open0 = forms.TimeField(required=False)
        fri_close0 = forms.TimeField(required=False)
        fri_open1 = forms.TimeField(required=False)
        fri_close1 = forms.TimeField(required=False)
        fri_is_closed = forms.BooleanField(
            label=_("Closed"),
            required=False,
            initial=False,
            )
        
        sat_open0 = forms.TimeField(required=False)
        sat_close0 = forms.TimeField(required=False)
        sat_open1 = forms.TimeField(required=False)
        sat_close1 = forms.TimeField(required=False)
        sat_is_closed = forms.BooleanField(
            label=_("Closed"),
            required=False,
            initial=False,
            )
        
        sun_open0 = forms.TimeField(required=False)
        sun_close0 = forms.TimeField(required=False)
        sun_open1 = forms.TimeField(required=False)
        sun_close1 = forms.TimeField(required=False)
        sun_is_closed = forms.BooleanField(
            label=_("Closed"),
            required=False,
            initial=False,
            )
        
        exceptions_en = forms.CharField(
            label=_('Exceptions for working hours (English)'),
            required=False,
            widget=forms.Textarea,
            )
        exceptions_de = forms.CharField(
            label=_('Exceptions for working hours (German)'),
            required=False,
            widget=forms.Textarea,
            )

        def __init__(self, event, index, *args, **kwargs):
            super(FeesOpeningHoursForm, self).__init__()
            self.event = event
            self.index = index
            kwargs['initial'] = {
                'fees_en': event.fees_en,
                'fees_de': event.fees_de,
            }
            super(type(self), self).__init__(*args, **kwargs)
            show_breaks = False
            for d in WEEK_DAYS:
                time_open = getattr(
                    event,
                    '%s_open' % d,
                    None,
                )
                time_break_close = getattr(
                    event,
                    '%s_break_close' % d,
                    None,
                )
                time_break_open = getattr(
                    event,
                    '%s_break_open' % d,
                    None,
                )
                time_close = getattr(
                    event,
                    '%s_close' % d,
                    None,
                )

                self.fields['%s_open0' % d].initial = time_open
                if not time_break_close:
                    self.fields['%s_close0' % d].initial = time_close
                else:
                    self.fields['%s_close0' % d].initial = time_break_close
                    self.fields['%s_open1' % d].initial = time_break_open
                    self.fields['%s_close1' % d].initial = time_close
                    show_breaks = True
                self.fields['%s_is_closed' % d].initial = not time_open
            self.fields['exceptions_en'].initial = event.exceptions_en
            self.fields['exceptions_de'].initial = event.exceptions_de
            self.fields['show_breaks'].initial = show_breaks
                
        def clean(self):
            
            for week_day in WEEK_DAYS:
                # here, we apply opening hours and do some checks
                if self.cleaned_data.get(week_day + '_open0', None) and \
                   self.cleaned_data.get(week_day + '_open1', None) and  \
                   self.cleaned_data.get(week_day + '_close0', None) and  \
                   self.cleaned_data.get(week_day + '_close1', None):
                    
                   if self.cleaned_data[week_day + '_open1'] < self.cleaned_data[week_day + '_close0']:
                       self._errors[week_day + '_open1']  = [_("An opening time after break must not be before the closing time to break.")]
                       
                   # map to custom forms fields
                   if not self.cleaned_data.get(week_day + '_is_closed', False):
                       self.cleaned_data[week_day + '_open'] = self.cleaned_data[week_day + '_open0']
                       self.cleaned_data[week_day + '_break_close'] = self.cleaned_data[week_day + '_close0']
                       self.cleaned_data[week_day + '_break_open'] = self.cleaned_data[week_day + '_open1']
                       self.cleaned_data[week_day + '_close'] = self.cleaned_data[week_day + '_close1']
                   
                elif self.cleaned_data.get(week_day + '_open0', None) and \
                     self.cleaned_data.get(week_day + '_close0', None):
                   self.cleaned_data[week_day + '_open'] = self.cleaned_data[week_day + '_open0']
                   self.cleaned_data[week_day + '_close'] = self.cleaned_data[week_day + '_close0']
                
                if self.cleaned_data.get(week_day + '_open0', None):
                    if not self.cleaned_data.get(week_day + '_close0', None):
                        self._errors[week_day + '_open0'] = [_("Please enter a closing time.")]
                    elif self.cleaned_data[week_day + '_close0'] < self.cleaned_data[week_day + '_open0']:
                        self._errors[week_day + '_open0'] = [_("A closing time must not be before an opening time.")]
                        
                if self.cleaned_data.get(week_day + '_close0', None):
                    if not self.cleaned_data.get(week_day + '_open0', None):
                        self._errors[week_day + '_open0'] = [_("Please enter an opening time.")]
    
                if self.cleaned_data.get(week_day + '_open1', None):
                    if not self.cleaned_data.get(week_day + '_close1', None):
                        self._errors[week_day + '_open1'] = [_("Please enter a closing time.")]
                    elif self.cleaned_data[week_day + '_close1'] < self.cleaned_data[week_day + '_open1']:
                        self._errors[week_day + '_open1'] = [_("A closing time must not be before an opening time.")]
    
                if self.cleaned_data.get(week_day + '_close1', None):
                    if not self.cleaned_data.get(week_day + '_open1', None):
                        self._errors[week_day + '_open1'] = [_("Please enter an opening time.")]
                    
            return self.cleaned_data
            
        def save(self):
            event = self.event
            event.fees_en = self.cleaned_data.get("fees_en", "")
            event.fees_de = self.cleaned_data.get("fees_de", "")
            for d in WEEK_DAYS:
                time_open0 = self.cleaned_data['%s_open0' % d]
                time_close0 = self.cleaned_data['%s_close0' % d]
                time_open1 = self.cleaned_data['%s_open1' % d]
                time_close1 = self.cleaned_data['%s_close1' % d]
                setattr(event, '%s_open' % d, time_open0)
                if time_open1:
                    setattr(event, '%s_break_close' % d, time_close0)
                    setattr(event, '%s_break_open' % d, time_open1)
                    setattr(event, '%s_close' % d, time_close1)
                else:
                    setattr(event, '%s_break_close' % d, None)
                    setattr(event, '%s_break_open' % d, None)
                    setattr(event, '%s_close' % d, time_close0)
            event.exceptions_en = self.cleaned_data['exceptions_en']
            event.exceptions_de = self.cleaned_data['exceptions_de']
            event.save()
            
            return event
            
        def get_extra_context(self):
            return {}
            
    class CategoriesForm(dynamicforms.Form):
        choose_creative_sectors = forms.BooleanField(
            initial=True,
            widget=forms.HiddenInput(
                attrs={
                    "class": "form_hidden",
                    }
                ),
            required=False,
            )
        
        tags = TagField(
            label= _("Tags"),
            help_text=_("Separate tags with commas"),
            max_length=200,
            required=False,
            widget=TagAutocomplete,
            )

        def clean_choose_creative_sectors(self):
            data = self.data
            el_count = 0
            for el in self.creative_sectors.values():
                if el['field_name'] in data:
                    el_count += 1
            if not el_count:
                raise forms.ValidationError(_("Please choose at least one creative sector."))
            return True

        def __init__(self, event, index, *args, **kwargs):
            super(CategoriesForm, self).__init__()
            self.event = event
            super(type(self), self).__init__(*args, **kwargs)
            self.creative_sectors = {}
            for item in get_related_queryset(Event, "creative_sectors"):
                self.creative_sectors[item.sysname] = {
                    'id': item.id,
                    'field_name': PREFIX_CI + str(item.id),
                }
            for s in self.creative_sectors.values():
                self.fields[s['field_name']] = forms.BooleanField(
                    required=False
                )
            for el in event.get_creative_sectors():
                for ancestor in el.get_ancestors(include_self=True):
                    self.fields[PREFIX_CI + str(ancestor.id)].initial = True
            self.fields['tags'].initial = event.tags
            
        def save(self, *args, **kwargs):
            event = self.event
            cleaned = self.cleaned_data
            event.tags = cleaned['tags']
            event.save()
            
            selected_cs = {}
            for item in get_related_queryset(Event, "creative_sectors"):
                if cleaned.get(PREFIX_CI + str(item.id), False):
                    # remove all the parents
                    for ancestor in item.get_ancestors():
                        if ancestor.id in selected_cs:
                            del(selected_cs[ancestor.id])
                    # add current
                    selected_cs[item.id] = item
            event.creative_sectors.clear()
            event.creative_sectors.add(*selected_cs.values())
            
            ContextItem.objects.update_for(event)
            
            return event

        def get_extra_context(self):
            return {}
    
    forms = {
        'identity': IdentityForm,
        'description': DescriptionForm,
        'avatar': AvatarForm,
        'event_times': EventTimesForm,
        'contact': ContactForm,
        'fees_opening_hours': FeesOpeningHoursForm,
        'organizer': OrganizerForm,
        'additional_info': AdditionalInfoForm,
        'categories': CategoriesForm,
        }
    formsets = {
        'event_times': {
            'event_times': {
                'formset': formset_factory(
                    EventTimeForm,
                    formset=ProfileFormSet,
                    can_delete=True,
                    ),
                'get_instances': lambda event: event.eventtime_set.all(),
                }
            },
        }

class DocumentProfile: # namespace
    class DescriptionForm(dynamicforms.Form):
        description_en = forms.CharField(
            label=_("Description (English)"),
            required=False,
            widget=forms.Textarea(),
            )
        description_de = forms.CharField(
            label=_("Description (German)"),
            required=False,
            widget=forms.Textarea(),
            )

        def __init__(self, document, index, *args, **kwargs):
            super(DescriptionForm, self).__init__()
            self.document = document
            self.index = index
            super(type(self), self).__init__(*args, **kwargs)
            if not args and not kwargs:  # if nothing is posted
                self.fields['description_en'].initial = document.description_en
                self.fields['description_de'].initial = document.description_de
        def save(self):
            document = self.document
            document.description_en = self.cleaned_data['description_en']
            document.description_de = self.cleaned_data['description_de']
            document.save()
            return document
            
        def get_extra_context(self):
            return {}
    
    class AvatarForm(dynamicforms.Form):
        media_file = ImageField(
            label= _("Photo"),
            help_text= _("You can upload GIF, JPG, PNG, TIFF, and BMP images. The minimal dimensions are %s px.") % STR_MIN_LOGO_SIZE,
            required=False,
            min_dimensions=MIN_LOGO_SIZE,
            )

        def __init__(self, document, index, *args, **kwargs):
            super(AvatarForm, self).__init__()
            self.document = document
            self.index = index
            super(type(self), self).__init__(*args, **kwargs)
            
        def save(self):
            document = self.document
            if "media_file" in self.files:
                media_file = self.files['media_file']
                image_mods.FileManager.save_file_for_object(
                    document,
                    media_file.name,
                    media_file,
                    subpath = "avatar/"
                    )
            return document
        def get_extra_context(self):
            return {}
    
    class DetailsForm(dynamicforms.Form):
        document_type = forms.ModelChoiceField(
            label=_("Document Type"),
            queryset=get_related_queryset(Document, "document_type"),
            required=False,
            )
        url_link = forms.URLField(
            label=_("URL"),
            required=False,
            )
        medium = forms.ModelChoiceField(
            label=_("Medium"),
            queryset=get_related_queryset(Document, "medium"),
            required=False,
            )

        def __init__(self, document, index, *args, **kwargs):
            super(DetailsForm, self).__init__()
            self.document = document
            self.index = index
            super(type(self), self).__init__(*args, **kwargs)
            if not args and not kwargs:  # if nothing is posted
                self.fields['document_type'].initial = self.document.document_type
                self.fields['medium'].initial = self.document.medium
                self.fields['url_link'].initial = self.document.url_link
        def save(self):
            document = self.document
            document.url_link = self.cleaned_data['url_link']
            document.document_type = self.cleaned_data['document_type']
            document.medium = self.cleaned_data['medium']
            document.save()
            return document
            
        def get_extra_context(self):
            return {}
   
    class CategoriesForm(dynamicforms.Form):
        choose_creative_sectors = forms.BooleanField(
            initial=True,
            widget=forms.HiddenInput(
                attrs={
                    "class": "form_hidden",
                    }
                ),
            required=False,
            )
        def clean_choose_creative_sectors(self):
            data = self.data
            el_count = 0
            for el in self.creative_sectors.values():
                if el['field_name'] in data:
                    el_count += 1
            if not el_count:
                raise forms.ValidationError(_("Please choose at least one creative sector."))
            return True
            
        choose_context_categories = forms.BooleanField(
            initial=True,
            widget=forms.HiddenInput(
                attrs={
                    "class": "form_hidden",
                    }
                ),
            required=False,
            )
        def clean_choose_context_categories(self):
            data = self.data
            el_count = 0
            for el in self.context_categories.values():
                if el['field_name'] in data:
                    el_count += 1
            if not el_count:
                raise forms.ValidationError(_("Please choose at least one context category."))
            return True

        def __init__(self, document, index, *args, **kwargs):
            super(CategoriesForm, self).__init__()
            self.document = document
            super(type(self), self).__init__(*args, **kwargs)
            self.creative_sectors = {}
            for item in get_related_queryset(Document, "creative_sectors"):
                self.creative_sectors[item.sysname] = {
                    'id': item.id,
                    'field_name': PREFIX_CI + str(item.id),
                }
            self.context_categories = {}
            for item in get_related_queryset(Document, "context_categories"):
                self.context_categories[item.sysname] = {
                    'id': item.id,
                    'field_name': PREFIX_BC + str(item.id),
                }
            for s in self.creative_sectors.values():
                self.fields[s['field_name']] = forms.BooleanField(
                    required=False
                )
            for el in document.get_creative_sectors():
                for ancestor in el.get_ancestors(include_self=True):
                    self.fields[PREFIX_CI + str(ancestor.id)].initial = True
            for c in self.context_categories.values():
                self.fields[c['field_name']] = forms.BooleanField(
                    required=False
                )
            for el in document.get_context_categories():
                for ancestor in el.get_ancestors(include_self=True):
                    self.fields[PREFIX_BC + str(ancestor.id)].initial = True
            
        def save(self, *args, **kwargs):
            document = self.document
            cleaned = self.cleaned_data
            selected_cs = {}
            for item in get_related_queryset(Document, "creative_sectors"):
                if cleaned.get(PREFIX_CI + str(item.id), False):
                    # remove all the parents
                    for ancestor in item.get_ancestors():
                        if ancestor.id in selected_cs:
                            del(selected_cs[ancestor.id])
                    # add current
                    selected_cs[item.id] = item
            document.creative_sectors.clear()
            document.creative_sectors.add(*selected_cs.values())
            
            selected_cc = {}
            for item in get_related_queryset(Document, "context_categories"):
                if cleaned.get(PREFIX_BC + str(item.id), False):
                    # remove all the parents
                    for ancestor in item.get_ancestors():
                        if ancestor.id in selected_cc:
                            del(selected_cc[ancestor.id])
                    # add current
                    selected_cc[item.id] = item
            document.context_categories.clear()
            document.context_categories.add(*selected_cc.values())
            ContextItem.objects.update_for(document)
            
            return document
            
        def get_extra_context(self):
            return {}
    
    forms = {
        'description': DescriptionForm,
        'avatar': AvatarForm,
        'details': DetailsForm,
        'categories': CategoriesForm,
        }

class GroupProfile: # namespace
    class DescriptionForm(dynamicforms.Form):
        description_en = forms.CharField(
            label=_("Description (English)"),
            required=False,
            widget=forms.Textarea(),
            )
        description_de = forms.CharField(
            label=_("Description (German)"),
            required=False,
            widget=forms.Textarea(),
            )

        def __init__(self, group, index, *args, **kwargs):
            super(DescriptionForm, self).__init__()
            self.group = group
            self.index = index
            super(type(self), self).__init__(*args, **kwargs)
            if not args and not kwargs:  # if nothing is posted
                self.fields['description_en'].initial = group.description_en
                self.fields['description_de'].initial = group.description_de
        def save(self):
            group = self.group
            group.description_en = self.cleaned_data['description_en']
            group.description_de = self.cleaned_data['description_de']
            group.save()
            return group
            
        def get_extra_context(self):
            return {}
    
    class AvatarForm(dynamicforms.Form):
        media_file = ImageField(
            label= _("Photo"),
            help_text= _("You can upload GIF, JPG, PNG, TIFF, and BMP images. The minimal dimensions are %s px.") % STR_MIN_LOGO_SIZE,
            required=False,
            min_dimensions=MIN_LOGO_SIZE,
            )

        def __init__(self, group, index, *args, **kwargs):
            super(AvatarForm, self).__init__()
            self.group = group
            self.index = index
            super(type(self), self).__init__(*args, **kwargs)
        def save(self):
            group = self.group
            if "media_file" in self.files:
                media_file = self.files['media_file']
                image_mods.FileManager.save_file_for_object(
                    group,
                    media_file.name,
                    media_file,
                    subpath = "avatar/"
                    )
            return group
            
        def get_extra_context(self):
            return {}
    
    class DetailsForm(dynamicforms.Form):
        group_type = forms.ChoiceField(
            required=True,
            choices=GROUP_TYPE_CHOICES,
            label=_("Group type"),
            )
        
        access_type = forms.ChoiceField(
            required=True,
            choices=ACCESS_TYPE_CHOICES,
            label=_("Security"),
            )
        
        institution = forms.ChoiceField(
            required=False,
            choices=[],
            label=_("Attach to profile"),
            )
        
        membership_options = forms.ChoiceField(
            required=True,
            choices=MEMBERSHIP_OPTION_CHOICES,
            label=_("Membership"),
            )
        
        main_language = forms.ChoiceField(
            required=True,
            choices=PREFERRED_LANGUAGE_CHOICES,
            label=_("Main language"),
            )

        def __init__(self, group, index, *args, **kwargs):
            super(DetailsForm, self).__init__()
            self.group = group
            self.index = index
            super(type(self), self).__init__(*args, **kwargs)
            user = get_current_user()
            person = user.profile
            INSTITUTION_CHOICES = [("", "---------")]
            INSTITUTION_CHOICES.extend([(str(el.id), force_unicode(el))
                                        for el in person.get_institutions()
                                        ])
            self.fields['institution'].choices = self.fields['institution'].widget.choices = INSTITUTION_CHOICES
            if not args and not kwargs:  # if nothing is posted
                self.fields['group_type'].initial = group.group_type_id
                self.fields['access_type'].initial = group.access_type_id
                self.fields['institution'].initial = group.organizing_institution_id
                self.fields['main_language'].initial = group.preferred_language_id
                if group.is_by_invitation and group.is_by_confirmation:
                    self.fields['membership_options'].initial = "invite_or_confirm"
                elif group.is_by_invitation:
                    self.fields['membership_options'].initial = "invite"
                else:
                    self.fields['membership_options'].initial = "anyone"
        def save(self):
            group = self.group
            cleaned = self.cleaned_data
            group.group_type_id = cleaned['group_type']
            group.access_type_id = cleaned['access_type']
            group.organizing_institution_id = cleaned.get('institution', None)
            group.preferred_language = get_related_queryset(
                PersonGroup,
                "preferred_language"
                ).get(
                    pk=cleaned.get('main_language', ""),
                    )
            membership_options = cleaned.get('membership_options', 'anyone')
            group.is_by_invitation = membership_options in ("invite", "invite_or_confirm")
            group.is_by_confirmation = membership_options == "invite_or_confirm"
            group.save()
            return group
            
        def get_extra_context(self):
            return {}
    
    class CategoriesForm(dynamicforms.Form):
        choose_creative_sectors = forms.BooleanField(
            initial=True,
            widget=forms.HiddenInput(
                attrs={
                    "class": "form_hidden",
                    }
                ),
            required=False,
            )
        def clean_choose_creative_sectors(self):
            data = self.data
            el_count = 0
            for el in self.creative_sectors.values():
                if el['field_name'] in data:
                    el_count += 1
            if not el_count:
                raise forms.ValidationError(_("Please choose at least one creative sector."))
            return True
            
        choose_context_categories = forms.BooleanField(
            initial=True,
            widget=forms.HiddenInput(
                attrs={
                    "class": "form_hidden",
                    }
                ),
            required=False,
            )
        def clean_choose_context_categories(self):
            data = self.data
            el_count = 0
            for el in self.context_categories.values():
                if el['field_name'] in data:
                    el_count += 1
            if not el_count:
                raise forms.ValidationError(_("Please choose at least one context category."))
            return True
            
        choose_object_types = forms.BooleanField(
            initial=True,
            widget=forms.HiddenInput(
                attrs={
                    "class": "form_hidden",
                    }
                ),
            required=False,
            )
        def clean_choose_object_types(self):
            data = self.data
            el_count = 0
            for el in self.object_types.values():
                if el['field_name'] in data:
                    el_count += 1
            if not el_count:
                raise forms.ValidationError(_("Please choose at least one object type."))
            return True

        def __init__(self, group, index, *args, **kwargs):
            super(CategoriesForm, self).__init__()
            self.group = group
            super(type(self), self).__init__(*args, **kwargs)
            self.creative_sectors = {}
            for item in get_related_queryset(PersonGroup, "creative_sectors"):
                self.creative_sectors[item.sysname] = {
                    'id': item.id,
                    'field_name': PREFIX_CI + str(item.id),
                }
            self.context_categories = {}
            for item in get_related_queryset(PersonGroup, "context_categories"):
                self.context_categories[item.sysname] = {
                    'id': item.id,
                    'field_name': PREFIX_BC + str(item.id),
                }
            for s in self.creative_sectors.values():
                self.fields[s['field_name']] = forms.BooleanField(
                    required=False
                )
            for el in group.get_creative_sectors():
                for ancestor in el.get_ancestors(include_self=True):
                    self.fields[PREFIX_CI + str(ancestor.id)].initial = True
            for c in self.context_categories.values():
                self.fields[c['field_name']] = forms.BooleanField(
                    required=False
                )
            for el in group.get_context_categories():
                for ancestor in el.get_ancestors(include_self=True):
                    self.fields[PREFIX_BC + str(ancestor.id)].initial = True
            
        def save(self, *args, **kwargs):
            group = self.group
            cleaned = self.cleaned_data
            selected_cs = {}
            for item in get_related_queryset(PersonGroup, "creative_sectors"):
                if cleaned.get(PREFIX_CI + str(item.id), False):
                    # remove all the parents
                    for ancestor in item.get_ancestors():
                        if ancestor.id in selected_cs:
                            del(selected_cs[ancestor.id])
                    # add current
                    selected_cs[item.id] = item
            group.creative_sectors.clear()
            group.creative_sectors.add(*selected_cs.values())
            
            selected_cc = {}
            for item in get_related_queryset(PersonGroup, "context_categories"):
                if cleaned.get(PREFIX_BC + str(item.id), False):
                    # remove all the parents
                    for ancestor in item.get_ancestors():
                        if ancestor.id in selected_cc:
                            del(selected_cc[ancestor.id])
                    # add current
                    selected_cc[item.id] = item
            group.context_categories.clear()
            group.context_categories.add(*selected_cc.values())
            ContextItem.objects.update_for(group)
            return group
            
        def get_extra_context(self):
            return {}
    
    forms = {
        'description': DescriptionForm,
        'avatar': AvatarForm,
        'details': DetailsForm,
        'categories': CategoriesForm,
        }

class JobOfferProfile: # namespace
    class DetailsForm(dynamicforms.Form):
        position = forms.CharField(
            required=True,
            label=_("Position"),
            )
        job_type = forms.ModelChoiceField(
            required=True,
            queryset=get_related_queryset(JobOffer, "job_type"),
            label=_("Job Type"),
            )
        qualifications = forms.ModelMultipleChoiceField(
            required=False,
            widget=forms.CheckboxSelectMultiple,
            queryset=get_related_queryset(JobOffer, "qualifications"),
            label=_("Qualification"),
            )
        description = forms.CharField(
            label=_("Description"),
            required=True,
            widget=forms.Textarea(attrs={'class':'vSystemTextField'}),
            )
        end_yyyy = forms.ChoiceField(
            required=False,
            choices=YEARS_CHOICES,
            label=_("End Year"),
        )
        
        end_mm = forms.ChoiceField(
            required=False,
            choices=MONTHS_CHOICES,
            label=_("End Month"),
        )
        
        end_dd = forms.ChoiceField(
            required=False,
            choices=DAYS_CHOICES,
            label=_("End Day"),
        )

        def __init__(self, job_offer, index, *args, **kwargs):
            super(DetailsForm, self).__init__()
            self.job_offer = job_offer
            self.index = index
            super(type(self), self).__init__(*args, **kwargs)
            if not args and not kwargs:  # if nothing is posted
                self.fields['position'].initial = job_offer.position
                self.fields['job_type'].initial = job_offer.job_type_id
                self.fields['qualifications'].initial = [q.pk for q in job_offer.qualifications.all()]
                self.fields['description'].initial = job_offer.description
                if job_offer.published_till:
                    self.fields['end_yyyy'].initial = job_offer.published_till.year
                    self.fields['end_mm'].initial = job_offer.published_till.month
                    self.fields['end_dd'].initial = job_offer.published_till.day

        def save(self):
            job_offer = self.job_offer
            data = self.cleaned_data
            job_offer.position = data['position']
            job_offer.job_type = data['job_type']
            job_offer.description = data['description']
            
            end_date = None
            end_yyyy = data.get('end_yyyy', None)
            end_mm = data.get('end_mm', None)
            end_dd = data.get('end_dd', None)
    
            if end_yyyy or end_mm or end_dd:
                try:
                    end_date = datetime.date(int(end_yyyy), int(end_mm or 1), int(end_dd or 1))
                except:
                    pass
                
            job_offer.published_till = end_date
            
            job_offer.save()
            
            job_offer.qualifications.clear()
            for q in data['qualifications']:
                job_offer.qualifications.add(q)
                
            return job_offer
            
        def get_extra_context(self):
            return {}
            
            
    class ContactForm(dynamicforms.Form):
        offering_institution = AutocompleteField(
            required=False,
            label=_("Offering institution"),
            help_text=_("Please enter a letter to display a list of available institutions"),
            app="marketplace", 
            qs_function="get_institutions",   
            display_attr="title",
            add_display_attr="get_address_string",
            options={
                "minChars": 1,
                "max": 20,
                "mustMatch": 1,
                "highlight" : False,
                },
            )
        offering_institution_title = forms.CharField(
            required=False,
            label=_("Institution/Company Title"),
        )
        
        contact_person_ind = forms.ChoiceField(
            initial=0,
            choices=CONTACT_PERSON_CHOICES,
            widget=forms.RadioSelect()
        )
        
        contact_person_name = forms.CharField(
            required=False,
            label=_("Contact Person Name"),
        )
        
        street_address = forms.CharField(
            required=False,
            label=_("Street Address"),
            )
        street_address2 = forms.CharField(
            required=False,
            label=_("Street Address (2nd line)"),
            )
        city = forms.CharField(
            required=True,
            label=_("City"),
            )
        postal_code = forms.CharField(
            required=False,
            label=_("Postal Code"),
            )
        country = forms.ChoiceField(
            required=True,
            choices=Address._meta.get_field("country").get_choices(),
            label=_("Country"),
            )
        district = forms.CharField(
            required=False,
            widget = forms.HiddenInput(
                attrs={
                    "class": "form_hidden",
                    }
                ),
            )
        longitude = forms.CharField(
            required=False,
            widget = forms.HiddenInput(
                attrs={
                    "class": "form_hidden",
                    }
                ),
            )
        latitude = forms.CharField(
            required=False,
            widget = forms.HiddenInput(
                attrs={
                    "class": "form_hidden",
                    }
                ),
            )
        phone_country = forms.CharField(
            required=False,
            max_length=4,
            initial="49",
            )
        phone_area = forms.CharField(
            required=False,
            max_length=5,
            )
        phone_number = forms.CharField(
            required=False,
            max_length=15,
            label=_("Phone"),
            )
        fax_country = forms.CharField(
            required=False,
            max_length=4,
            initial="49",
            )
        fax_area = forms.CharField(
            required=False,
            max_length=5,
            )
        fax_number = forms.CharField(
            required=False,
            max_length=15,
            label=_("Fax"),
            )
        mobile_country = forms.CharField(
            required=False,
            max_length=4,
            initial="49",
            )
        mobile_area = forms.CharField(
            required=False,
            max_length=5,
            )
        mobile_number = forms.CharField(
            required=False,
            max_length=15,
            label=_("Mobile"),
            )
        email0 = forms.EmailField(
            required=False,
            label=_("E-mail"),
            )
        email1 = forms.EmailField(
            required=False,
            label=_("E-mail"),
            )
        email2 = forms.EmailField(
            required=False,
            label=_("E-mail"),
            )
        publish_emails = forms.BooleanField(
            label=_("Publish emails to unregistered visitors"),
            initial=True,
            required=False,
            )
        
        url0_type = forms.ChoiceField(
            required=False,
            choices=URL_TYPE_CHOICES,
            label=_("Type"),
            )
        url0_link = forms.URLField(
            required=False,
            label=_("URL"),
            )
        url1_type = forms.ChoiceField(
            required=False,
            choices=URL_TYPE_CHOICES,
            label=_("Type"),
            )
        url1_link = forms.URLField(
            required=False,
            label=_("URL"),
            )
        url2_type = forms.ChoiceField(
            required=False,
            choices=URL_TYPE_CHOICES,
            label=_("Type"),
            )
        url2_link = forms.URLField(
            required=False,
            label=_("URL"),
            )
        im0_type = forms.ChoiceField(
            required=False,
            choices=IM_TYPE_CHOICES,
            label=_("Type"),
            )
        im0_address = forms.CharField(
            required=False,
            max_length=255,
            label=_("Address"),
            )
        im1_type = forms.ChoiceField(
            required=False,
            choices=IM_TYPE_CHOICES,
            label=_("Type"),
            )
        im1_address = forms.CharField(
            required=False,
            max_length=255,
            label=_("Address"),
            )
        im2_type = forms.ChoiceField(
            required=False,
            choices=IM_TYPE_CHOICES,
            label=_("Type"),
            )
        im2_address = forms.CharField(
            required=False,
            max_length=255,
            label=_("Address"),
            )

        def __init__(self, job_offer, index, *args, **kwargs):
            super(ContactForm, self).__init__()
            self.job_offer = job_offer
            self.index = index
            super(type(self), self).__init__(*args, **kwargs)
            if not args and not kwargs:  # if nothing is posted
                self.fields['contact_person_name'].initial = job_offer.contact_person_name

                if job_offer.creator and job_offer.creator != get_current_user():
                    self.fields['contact_person_ind'].choices = (
                        (0, _("%s is the contact person") % job_offer.creator.profile.get_title()),
                        (1, _("%s is not the contact person") % job_offer.creator.profile.get_title()),
                    )
                if job_offer.contact_person:
                    self.fields['contact_person_ind'].initial = 0
                else:
                    self.fields['contact_person_ind'].initial = 1

                contact = job_offer.get_contacts()[0]
                postal_address = contact.postal_address
                geopos = postal_address.get_geoposition()
                locality = postal_address.get_locality()
                self.fields['offering_institution'].initial = job_offer.offering_institution_id
                self.fields['offering_institution_title'].initial = job_offer.offering_institution_title
                self.fields['street_address'].initial = postal_address.street_address
                self.fields['street_address2'].initial = postal_address.street_address2
                self.fields['city'].initial = postal_address.city
                self.fields['postal_code'].initial = postal_address.postal_code
                self.fields['country'].initial = postal_address.country_id
                self.fields['district'].initial = getattr(locality, "district", "")
                self.fields['longitude'].initial = getattr(geopos, "longitude", "")
                self.fields['latitude'].initial = getattr(geopos, "latitude", "")
                self.fields['phone_country'].initial = contact.phone0_country
                self.fields['phone_area'].initial = contact.phone0_area
                self.fields['phone_number'].initial = contact.phone0_number
                self.fields['fax_country'].initial = contact.phone1_country
                self.fields['fax_area'].initial = contact.phone1_area
                self.fields['fax_number'].initial = contact.phone1_number
                self.fields['mobile_country'].initial = contact.phone2_country
                self.fields['mobile_area'].initial = contact.phone2_area
                self.fields['mobile_number'].initial = contact.phone2_number
                self.fields['url0_type'].initial = contact.url0_type_id
                self.fields['url0_link'].initial = contact.url0_link
                self.fields['url1_type'].initial = contact.url1_type_id
                self.fields['url1_link'].initial = contact.url1_link
                self.fields['url2_type'].initial = contact.url2_type_id
                self.fields['url2_link'].initial = contact.url2_link
                self.fields['im0_type'].initial = contact.im0_type_id
                self.fields['im0_address'].initial = contact.im0_address
                self.fields['im1_type'].initial = contact.im1_type_id
                self.fields['im1_address'].initial = contact.im1_address
                self.fields['im2_type'].initial = contact.im2_type_id
                self.fields['im2_address'].initial = contact.im2_address
                self.fields['email0'].initial = contact.email0_address
                self.fields['email1'].initial = contact.email1_address
                self.fields['email2'].initial = contact.email2_address
                self.fields['publish_emails'].initial = contact.publish_emails
            
        def save(self):
            job_offer = self.job_offer
            index = self.index
            data = self.cleaned_data
            
            contact_person_ind = int(data.get("contact_person_ind", 0))
            # the creator is contact person
            contact_person = None
            contact_person_name = data.get('contact_person_name', "")
            if contact_person_ind == 0:
                if job_offer.creator and job_offer.creator != get_current_user():
                    contact_person = job_offer.creator.profile
                else:
                    contact_person = get_current_user().profile
                contact_person_name = ""
                
            job_offer.offering_institution_id = data['offering_institution'] or None
            job_offer.offering_institution_title = data['offering_institution_title']

            job_offer.contact_person = contact_person
            job_offer.contact_person_name = contact_person_name

            job_offer.phone0_type = PhoneType.objects.get(slug='phone')
            job_offer.phone0_country = data.get('phone_country', '')
            job_offer.phone0_area = data.get('phone_area', '')
            job_offer.phone0_number = data.get('phone_number', '')
            job_offer.phone1_type = PhoneType.objects.get(slug='fax')
            job_offer.phone1_country = data.get('fax_country', '')
            job_offer.phone1_area = data.get('fax_area', '')
            job_offer.phone1_number = data.get('fax_number', '')
            job_offer.phone2_type = PhoneType.objects.get(slug='mobile')
            job_offer.phone2_country = data.get('mobile_country', '')
            job_offer.phone2_area = data.get('mobile_area', '')
            job_offer.phone2_number = data.get('mobile_number', '')
            job_offer.url0_type_id = data['url0_type'] or None
            job_offer.url1_type_id = data['url1_type'] or None
            job_offer.url2_type_id = data['url2_type'] or None
            job_offer.url0_link = data.get('url0_link', '')
            job_offer.url1_link = data.get('url1_link', '')
            job_offer.url2_link = data.get('url2_link', '')
            job_offer.im0_type_id = data['im0_type'] or None
            job_offer.im1_type_id = data['im1_type'] or None
            job_offer.im2_type_id = data['im2_type'] or None
            job_offer.im0_address = data.get('im0_address', '')
            job_offer.im1_address = data.get('im1_address', '')
            job_offer.im2_address = data.get('im2_address', '')
            job_offer.email0_address = data.get('email0', '')
            job_offer.email1_address = data.get('email1', '')
            job_offer.email2_address = data.get('email2', '')
            job_offer.publish_emails = data.get('publish_emails', False)
            job_offer.save()
            Address.objects.set_for(
                job_offer,
                "postal_address",
                country=data.get("country", ""),
                district=data.get("district", ""),
                city=data.get("city", ""),
                street_address=data.get("street_address", ""),
                street_address2=data.get("street_address2", ""),
                postal_code=data.get("postal_code", ""),
                latitude=data.get("latitude", ""),
                longitude=data.get("longitude", ""),
                )
            return job_offer
        def get_extra_context(self):
            return {}

    class CategoriesForm(dynamicforms.Form):
        choose_job_sectors = forms.BooleanField(
            initial=True,
            widget=forms.HiddenInput(
                attrs={
                    "class": "form_hidden",
                    }
                ),
            required=False,
            )
        
        tags = TagField(
            label= _("Tags"),
            help_text=_("Separate tags with commas"),
            max_length=200,
            required=False,
            widget=TagAutocomplete,
            )

        def clean_choose_job_sectors(self):
            data = self.data
            el_count = 0
            for el in self.job_sectors.values():
                if el['field_name'] in data:
                    el_count += 1
            if not el_count:
                raise forms.ValidationError(_("Please choose at least one job sector."))
            return True

        def __init__(self, job_offer, index, *args, **kwargs):
            super(CategoriesForm, self).__init__()
            self.job_offer = job_offer
            super(type(self), self).__init__(*args, **kwargs)
            self.job_sectors = {}
            for item in get_related_queryset(JobOffer, "job_sectors"):
                self.job_sectors[item.slug] = {
                    'id': item.id,
                    'field_name': PREFIX_JS + str(item.id),
                    'title': item.title,
                }
            js_ids = [el.id for el in job_offer.job_sectors.all()]
            for s in self.job_sectors.values():
                self.fields[s['field_name']] = forms.BooleanField(
                    required=False
                )
            for s in self.job_sectors.values():
                if s['id'] in js_ids:
                    self.fields[PREFIX_JS + str(s['id'])].initial = True
            self.fields['tags'].initial = job_offer.tags
            
        def save(self, *args, **kwargs):
            job_offer = self.job_offer
            cleaned = self.cleaned_data
            job_offer.tags = cleaned['tags']
            job_offer.save()
            
            selected_js = {}
            for item in get_related_queryset(JobOffer, "job_sectors"):
                if cleaned.get(PREFIX_JS + str(item.id), False):
                    selected_js[item.id] = item
            job_offer.job_sectors.clear()
            job_offer.job_sectors.add(*selected_js.values())
            
            return job_offer

        def get_extra_context(self):
            return {}
    
    forms = {
        'details': DetailsForm,
        'contact': ContactForm,
        'categories': CategoriesForm,
        }

class ClaimForm(dynamicforms.Form):
    """
    Form for claiming institutions, events, documents
    """
    
    name = forms.CharField(
        label=_("Name"),
        required=True,
        max_length=80,
        )
    
    email = forms.EmailField(
        label=_("Email"),
        required=True,
        max_length=80,
        )
    
    best_time_to_call = forms.ChoiceField(
        required=False,
        choices=ClaimRequest._meta.get_field("best_time_to_call").get_choices(),
        label=_("Best Time to Call"),
        )
    
    phone_country = forms.CharField(
        required=False,
        max_length=4,
        )
    phone_area = forms.CharField(
        required=False,
        max_length=5,
        )
    phone_number = forms.CharField(
        required=False,
        max_length=15,
        label=_("Phone"),
        )
    
    role = forms.CharField(
        label=_("Role"),
        required=False,
        max_length=80,
        )

    comments = forms.CharField(
        label= _("Comments"),
        required=False,
        widget=forms.Textarea(attrs={'class':'vSystemTextField'}),
        )
    
    def __init__(self, content_type, object_id, *args, **kwargs):
        super(ClaimForm, self).__init__(*args, **kwargs)
        
        self.content_type = content_type
        self.object_id = object_id
        self.user = get_current_user()
        self.fields["name"].initial = "%s %s" % (self.user.first_name, self.user.last_name)
        self.fields["email"].initial = self.user.email
        
        person = self.user.profile
        contacts = person.get_contacts()
        if contacts:
            for phone in contacts[0].get_phones():
                if phone["type"] == get_related_queryset(type(contacts[0]), "phone0_type").get(slug="phone"):
                    self.fields["phone_country"].initial = phone["country"]
                    self.fields["phone_area"].initial = phone["area"]
                    self.fields["phone_number"].initial = phone["number"]
                    break    

    def save(self):
        # do character encoding
        cleaned = self.cleaned_data
        #for key, value in cleaned.items():
        #    if type(value).__name__ == "unicode":
        #        cleaned[key] = value.encode(settings.DEFAULT_CHARSET)
        
        claim_request, created = ClaimRequest.objects.get_or_create(
            user=self.user,
            name=cleaned.get('name', None),
            email=cleaned.get('email', None),
            best_time_to_call=cleaned.get('best_time_to_call', None),
            phone_country=cleaned.get('phone_country', None),
            phone_area=cleaned.get('phone_area', None),
            phone_number=cleaned.get('phone_number', None),
            role=cleaned.get('role', None),
            comments=cleaned.get('comments', None),
            content_type=self.content_type,
            object_id=self.object_id,
            status=0,
            )

class InvitationForm(dynamicforms.Form):
    
    body = forms.CharField(
        label= _("Message"),
        required=True,
        widget=forms.Textarea(attrs={'class':'vSystemTextField'}),
        )
    
    recipient_email = forms.EmailField(
        label=_("Recipient email"),
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs={'class':'vTextField'}),
        help_text=_("Enter an email of a person you want to invite to this website."),
        )   
    
    # prevent spam
    prevent_spam = SecurityField()
    
    def __init__(self, sender, *args, **kwargs):
        super(InvitationForm, self).__init__(*args, **kwargs)
        self.sender = sender
    
    def send(self):
        from jetson.apps.mailing.views import send_email_using_template
        from jetson.apps.mailing.recipient import Recipient
        
        sender = self.sender
        cleaned = self.cleaned_data
        
        body = cleaned["body"]
        recipient_email = cleaned["recipient_email"]
        

        send_email_using_template(
            recipients_list = [Recipient(
                email=recipient_email,
                )],
            email_template_slug = "invitation",
            obj_placeholders = {
                'object_creator_title': self.sender.profile.get_title(),
                'object_creator_url': self.sender.profile.get_url(),
                'object_description': body,
                },
            sender_name = settings.ADMINS[0][0],
            sender_email = settings.ADMINS[0][1],
            send_immediately = True,
            )

class CCBCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<ul>']
        # Normalize to strings
        str_values = set([force_unicode(v) for v in value])
        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = u' for="%s"' % final_attrs['id']
            else:
                label_for = ''

            cb = forms.CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            option_value = force_unicode(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = conditional_escape(force_unicode(option_label))
            output.append(u'<li class="line_checkbox">%s <label%s>%s</label></li>' % (rendered_cb, label_for, option_label))
        output.append(u'</ul>')
        return mark_safe(u'\n'.join(output))


class ProfileDeletionForm(dynamicforms.Form):
    delete_events = forms.BooleanField(
        required=False,
        label=_("Delete related events")
        )
    delete_job_offers = forms.BooleanField(
        required=False,
        label=_("Delete related job offers")
        )
    
    user_deleted = False
    deleted_institutions = []
    
    def __init__(self, user, *args, **kwargs):
        self.user_deleted = False
        self.deleted_institutions = []

        super(ProfileDeletionForm, self).__init__(*args, **kwargs)
        self.user = user
        profile_choices = [
            ('auth.user', user.profile.get_title()),
            ]
        for inst in user.profile.get_institutions(clear_cache=True):
            profile_choices.append((inst.slug, inst.get_title()))
        
        self.fields['profiles'] = forms.MultipleChoiceField(
            required=False,
            label=_("Profiles to delete"),
            choices=profile_choices,
            widget=CCBCheckboxSelectMultiple,
            )
    def clean_profiles(self):
        value = self.cleaned_data.get('profiles', [])
        if not value:
            raise forms.ValidationError(_("You haven't selected anything to delete."))
        if 'auth.user' in value and self.user.is_superuser:
            raise forms.ValidationError(_("Superuser's profile cannot be deleted."))
        return value

    def delete(self):
        for p in self.cleaned_data['profiles']:
            if p == "auth.user":
                self.user_deleted = True
            else:
                self.deleted_institutions.append(
                    Institution.objects.get(slug=p)
                    )
                
        User = models.get_model("auth", "User")
        Blog = models.get_model("blog", "Blog")
        MediaGallery = models.get_model("media_gallery", "MediaGallery")
        Bookmark = models.get_model("bookmarks", "Bookmark")
        Memo = models.get_model("memos", "Memo")
        Favorite = models.get_model("favorites", "Favorite")
        Comment = models.get_model("comments", "Comment")
        Ticket = models.get_model("tracker", "Ticket")
        ContentType = models.get_model("contenttypes", "ContentType")

        delete_events = self.cleaned_data['delete_events']
        delete_job_offers = self.cleaned_data['delete_job_offers']
        
        inst_content_type = ContentType.objects.get_for_model(Institution)
        event_content_type = ContentType.objects.get_for_model(Event)
        job_offer_content_type = ContentType.objects.get_for_model(JobOffer)
        # DELETE INSTITUTIONS
        for inst in self.deleted_institutions:
            # delete person group
            PersonGroup.objects.filter(
                content_type=inst_content_type,
                object_id=inst.pk,
                ).delete()
            # delete blog
            Blog.objects.filter(
                content_type=inst_content_type,
                object_id=inst.pk,
                ).delete()
            # delete media gallery
            MediaGallery.objects.filter(
                content_type=inst_content_type,
                object_id=inst.pk,
                ).delete()
            # delete bookmarks
            Bookmark.objects.filter(
                url_path=inst.get_url_path(),
                ).delete()
            # delete memos
            Memo.objects.filter(
                content_type=inst_content_type,
                object_id=inst.pk,
                ).delete()
            # delete favorites
            Favorite.objects.filter(
                content_type=inst_content_type,
                object_id=inst.pk,
                ).delete()
            # optionally keep events
            if not delete_events:
                for ev in Event.objects.filter(
                    models.Q(organizing_institution=inst) |
                    models.Q(venue=inst)
                    ):
                    if ev.organizing_institution == inst:
                        if not ev.organizer_title:
                            ev.organizer_title = ev.organizing_institution.get_title()
                        ev.organizing_institution = None
                    if ev.venue == inst:
                        if not ev.venue_title:
                            ev.venue_title = ev.venue.get_title()
                        ev.venue = None
                    ev.save()
            else:
                for ev in Event.objects.filter(
                    models.Q(organizing_institution=inst) |
                    models.Q(venue=inst)
                    ):
                    # delete media galleries
                    MediaGallery.objects.filter(
                        content_type=event_content_type,
                        object_id=ev.pk,
                        ).delete()
                    # delete bookmarks
                    Bookmark.objects.filter(
                        url_path=ev.get_url_path(),
                        ).delete()
                    # delete memos
                    Memo.objects.filter(
                        content_type=event_content_type,
                        object_id=ev.pk,
                        ).delete()
                    # delete favorites
                    Favorite.objects.filter(
                        content_type=event_content_type,
                        object_id=ev.pk,
                        ).delete()
                    # delete event
                    ev.delete()
            # optionally keep job offers
            if not delete_job_offers:
                for job in JobOffer.objects.filter(
                    offering_institution=inst,
                    ):
                    if not job.offering_institution_title:
                        job.offering_institution_title = job.offering_institution.get_title()
                    job.offering_institution=None
                    job.save()
            else:
                for job in JobOffer.objects.filter(
                    offering_institution=inst,
                    ):
                    # delete bookmarks
                    Bookmark.objects.filter(
                        url_path=job.get_url_path(),
                        ).delete()
                    # delete memos
                    Memo.objects.filter(
                        content_type=job_offer_content_type,
                        object_id=job.pk,
                        ).delete()
                    # delete favorites
                    Favorite.objects.filter(
                        content_type=job_offer_content_type,
                        object_id=job.pk,
                        ).delete()
                    # delete job offer
                    job.delete()
            # delete institution
            inst.delete()
        # DELETE USER
        person = self.user.profile
        person_content_type = ContentType.objects.get_for_model(person)
        superuser = User.objects.filter(is_superuser=True)[0]
        if self.user_deleted:
            # delete blog
            Blog.objects.filter(
                content_type=person_content_type,
                object_id=person.pk,
                ).delete()
            # delete media gallery
            MediaGallery.objects.filter(
                content_type=person_content_type,
                object_id=person.pk,
                ).delete()
            # keep comments
            for comment in Comment.objects.filter(
                user=self.user,
                ):
                comment.name = person.get_title()
                comment.email = self.user.email
                comment.user = None
                comment.save()
            # keep tickets
            Ticket.objects.filter(
                submitter=self.user
                ).update(
                    submitter_name=person.get_title(),
                    submitter_email=self.user.email,
                    submitter=None,
                    )
            Ticket.objects.filter(
                modifier=self.user,
                ).update(
                    modifier=None
                    )
            # delete bookmarks
            Bookmark.objects.filter(
                url_path=person.get_url_path(),
                ).delete()
            # delete memos
            Memo.objects.filter(
                content_type=person_content_type,
                object_id=person.pk,
                ).delete()
            # delete favorites
            Favorite.objects.filter(
                content_type=person_content_type,
                object_id=person.pk,
                ).delete()
            # optionally keep events
            if not delete_events:
                for ev in Event.objects.filter(
                    models.Q(organizing_person=person) |
                    models.Q(creator=self.user) |
                    models.Q(modifier=self.user)
                    ):
                    if ev.organizing_person == person:
                        ev.organizing_person=None
                    if ev.creator == self.user:
                        ev.creator = superuser
                    if ev.modifier == self.user:
                        ev.modifier = None
                    ev.save_base()
            else:
                for ev in Event.objects.filter(
                    models.Q(organizing_person=person) |
                    models.Q(creator=self.user) |
                    models.Q(modifier=self.user)
                    ):
                    # delete media galleries
                    MediaGallery.objects.filter(
                        content_type=event_content_type,
                        object_id=ev.pk,
                        ).delete()
                    # delete bookmarks
                    Bookmark.objects.filter(
                        url_path=ev.get_url_path(),
                        ).delete()
                    # delete memos
                    Memo.objects.filter(
                        content_type=event_content_type,
                        object_id=ev.pk,
                        ).delete()
                    # delete favorites
                    Favorite.objects.filter(
                        content_type=event_content_type,
                        object_id=ev.pk,
                        ).delete()
                    # delete event
                    ev.delete()
            # optionally keep job offers
            if not delete_job_offers:
                JobOffer.objects.filter(
                    contact_person=person,
                    ).update(
                        contact_person_name=person.get_title(),
                        contact_person = None,
                        )
                JobOffer.objects.filter(
                    creator=self.user
                    ).update(
                        creator=superuser,
                        )
                JobOffer.objects.filter(
                    author=self.user
                    ).update(
                        author=superuser,
                        )
                JobOffer.objects.filter(
                    modifier=self.user
                    ).update(
                        modifier=None,
                        )
            else:
                for job in JobOffer.objects.filter(
                    models.Q(contact_person=person) |
                    models.Q(creator=self.user) |
                    models.Q(modifier=self.user)
                    ):
                    # delete bookmarks
                    Bookmark.objects.filter(
                        url_path=job.get_url_path(),
                        ).delete()
                    # delete memos
                    Memo.objects.filter(
                        content_type=job_offer_content_type,
                        object_id=job.pk,
                        ).delete()
                    # delete favorites
                    Favorite.objects.filter(
                        content_type=job_offer_content_type,
                        object_id=job.pk,
                        ).delete()
                    # delete job offer
                    job.delete()
            # delete user
            self.user.delete()
            
class ObjectDeletionForm(dynamicforms.Form):
    def __init__(self, obj, *args, **kwargs):
        super(ObjectDeletionForm, self).__init__(*args, **kwargs)
        self.obj = obj
        
    def delete(self):
        self.obj.delete()
        
class KreativArbeitenContactForm(dynamicforms.Form):
    
    subject = forms.CharField(
        label=_("Subject"),
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs={'class':'vTextField'}),
        )
    
    body = forms.CharField(
        label= _("Message"),
        required=True,
        widget=forms.Textarea(attrs={'class':'vSystemTextField'}),
        )
    
    sender_name = forms.CharField(
        label=_("Your name"),
        required=True, 
        max_length=255,
        widget=forms.TextInput(attrs={'class':'vTextField'}),
        )
    sender_email = SingleEmailTextField(
        label=_("Your e-mail address"),
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs={'class':'vTextField'}),
        )   
    
    # prevent spam
    prevent_spam = SecurityField()
    
    def save(self, sender=None):
        
        # do character encoding
        cleaned = self.cleaned_data
        #for key, value in cleaned.items():
        #    if type(value).__name__ == "unicode":
        #        cleaned[key] = value.encode(settings.DEFAULT_CHARSET)
        
        if not sender.is_authenticated():
            sender=None
        
        subject = cleaned["subject"]
        body = cleaned["body"]
        sender_name = cleaned["sender_name"]
        sender_email = cleaned["sender_email"]
        
        recipient_emails = []
        recipient_emails.append("%s <%s>" % (
            "Dirk Kiefer",
            "kiefer@rkw.de",
            ))
        message = EmailMessage.objects.create(
            sender=sender,
            sender_name=sender_name,
            sender_email=sender_email,
            recipient_emails=",".join(recipient_emails),
            subject=subject,
            body_html=body,
        )
        message.send()


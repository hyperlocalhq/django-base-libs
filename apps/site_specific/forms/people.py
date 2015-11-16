# -*- coding: UTF-8 -*-
from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from base_libs.forms import dynamicforms
from base_libs.forms.fields import ImageField
from base_libs.utils.misc import get_related_queryset, XChoiceList
from base_libs.forms.fields import AutocompleteField

from jetson.apps.location.models import Address
from jetson.apps.optionset.models import PhoneType

from ccb.apps.people.models import Person, IndividualContact
from ccb.apps.institutions.models import Institution
from ccb.apps.site_specific.models import ContextItem
from ccb.apps.people.models import URL_ID_PERSON

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

image_mods = models.get_app("image_mods")

# prexixes of fields to guarantee uniqueness
PREFIX_CI = 'CI_'  # Creative Sector aka Creative Industry
PREFIX_BC = 'BC_'  # Context Category aka Business Category
PREFIX_OT = 'OT_'  # Object Type
PREFIX_LT = 'LT_'  # Location Type
PREFIX_JS = 'JS_'  # Job Sector

BIRTHDAY_DD_CHOICES = Person._meta.get_field('birthday_dd').get_choices()
BIRTHDAY_DD_CHOICES[0] = ("", "----")
BIRTHDAY_MM_CHOICES = Person._meta.get_field('birthday_mm').get_choices()
BIRTHDAY_MM_CHOICES[0] = ("", "----")
BIRTHDAY_YYYY_CHOICES = Person._meta.get_field('birthday_yyyy').get_choices()
BIRTHDAY_YYYY_CHOICES[0] = ("", "----")

NATIONALITY_CHOICES = XChoiceList(get_related_queryset(Person, 'nationality'))
SALUTATION_CHOICES = XChoiceList(get_related_queryset(Person, 'salutation'))

URL_TYPE_CHOICES = XChoiceList(get_related_queryset(IndividualContact, 'url0_type'))
IM_TYPE_CHOICES = XChoiceList(get_related_queryset(IndividualContact, 'im0_type'))

LOCATION_TYPE_CHOICES = XChoiceList(get_related_queryset(IndividualContact, "location_type"))
INDIVIDUAL_TYPE_CHOICES = XChoiceList(get_related_queryset(Person, "individual_type"))


PREFERRED_LANGUAGE_CHOICES = XChoiceList(
    get_related_queryset(Person, 'preferred_language'),
    null_choice_text=_("- Please select -"),
)

LOGO_SIZE = getattr(settings, "LOGO_SIZE", (100, 100))
MIN_LOGO_SIZE = getattr(settings, "MIN_LOGO_SIZE", (100, 100))
STR_LOGO_SIZE = "%sx%s" % LOGO_SIZE
STR_MIN_LOGO_SIZE = "%sx%s" % MIN_LOGO_SIZE

# Collect translatable strings
_("Not listed? Enter manually")
_("Back to selection")
_('Is some category missing? You can <a href="/ticket/new-category/" target="_blank">suggest it here</a>.')


# TODO: each form could be ModelForm. Each formset could be ModelFormSet.
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
        super(IdentityForm, self).__init__(*args, **kwargs)
        self.person = person
        self.index = index
        if not args and not kwargs:  # if nothing is posted
            self.fields['first_name'].initial = person.user.first_name
            self.fields['last_name'].initial = person.user.last_name

        self.helper = FormHelper()
        self.helper.form_action = "/helper/edit-%(URL_ID_PERSON)s-profile/%(username)s/identity/" % {
            'URL_ID_PERSON': URL_ID_PERSON,
            'username': self.person.user.username,
        }
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'target': "hidden_iframe",
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Identity"),
                "first_name",
                "last_name",
            ),
            bootstrap.FormActions(
                layout.Button('cancel', _('Cancel')),
                layout.Submit('submit', _('Save')),
            )
        )

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
        super(DescriptionForm, self).__init__(*args, **kwargs)
        self.person = person
        self.index = index
        if not args and not kwargs:  # if nothing is posted
            self.fields['description_en'].initial = person.description_en
            self.fields['description_de'].initial = person.description_de

        self.helper = FormHelper()
        self.helper.form_action = "/helper/edit-%(URL_ID_PERSON)s-profile/%(username)s/description/" % {
            'URL_ID_PERSON': URL_ID_PERSON,
            'username': self.person.user.username,
        }
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'target': "hidden_iframe",
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Description"),
                "description_en",
                "description_de",
            ),
            bootstrap.FormActions(
                layout.Button('cancel', _('Cancel')),
                layout.Submit('submit', _('Save')),
            )
        )

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
        label=_("Photo"),
        help_text=_(
            "You can upload GIF, JPG, PNG, TIFF, and BMP images. The minimal dimensions are %s px.") % STR_MIN_LOGO_SIZE,
        required=False,
        min_dimensions=MIN_LOGO_SIZE,
    )

    def __init__(self, person, index, *args, **kwargs):
        super(AvatarForm, self).__init__(*args, **kwargs)
        self.person = person
        self.index = index

        self.helper = FormHelper()
        self.helper.form_action = "/helper/edit-%(URL_ID_PERSON)s-profile/%(username)s/avatar/" % {
            'URL_ID_PERSON': URL_ID_PERSON,
            'username': self.person.user.username,
        }
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'target': "hidden_iframe",
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Avatar"),
                layout.HTML("""{% load image_modifications %}
                    {% if object.image %}
                        <img src="{{ UPLOADS_URL }}{{ object.image|modified_path:"ap" }}" alt="{{ object.get_title|escape }}"/>
                    {% else %}
                        <img src="{{ DEFAULT_FORM_LOGO_4_PERSON }}" alt="{{ object.get_title|escape }}"/>
                    {% endif %}
                """),
                "media_file",
            ),
            bootstrap.FormActions(
                layout.Button('cancel', _('Cancel')),
                layout.Submit('submit', _('Save')),
            )
        )

    def save(self):
        person = self.person
        if "media_file" in self.files:
            media_file = self.files['media_file']
            image_mods.FileManager.save_file_for_object(
                person,
                media_file.name,
                media_file,
                subpath="avatar/"
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
            "highlight": False,
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
        widget=forms.HiddenInput(
            attrs={
                "class": "form_hidden",
            }
        ),
    )
    longitude = forms.CharField(
        required=False,
        widget=forms.HiddenInput(
            attrs={
                "class": "form_hidden",
            }
        ),
    )
    latitude = forms.CharField(
        required=False,
        widget=forms.HiddenInput(
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
        widget=forms.HiddenInput(
            attrs={
                "class": "form_hidden",
            }
        ),
    )

    def __init__(self, person, index, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.person = person
        self.index = index
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

        self.helper = FormHelper()
        self.helper.form_action = "/helper/edit-%(URL_ID_PERSON)s-profile/%(username)s/contact/%(index)s/" % {
            'URL_ID_PERSON': URL_ID_PERSON,
            'username': self.person.user.username,
            'index': self.index,
        }
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'target': "hidden_iframe",
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Location"),
                "location_type",
                "location_title",
            ),
            layout.Fieldset(
                _("Institution"),
                "institution",
                layout.HTML("""{% load i18n %}
                    <button id="id_institution_enter" class="btn btn-link">{% trans "Not listed? Enter manually" %}</button>
                """),
                css_id="fieldset_institution_select",
            ),
            layout.Fieldset(
                _("Institution"),
                "institution_title",
                "institution_website",
                layout.HTML("""{% load i18n %}
                    <button id="id_institution_select" class="btn btn-link">{% trans "Back to selection" %}</button>
                """),
                css_id="fieldset_institution_enter",
                css_class="hidden",
            ),
            layout.Fieldset(
                _("Address"),
                "latitude",  # hidden field
                "longitude",  # hidden field
                "district",  # hidden field
                "street_address",
                "street_address2",
                layout.Row(
                    layout.Div(
                        "postal_code",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                    layout.Div(
                        "city",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                ),
                "country",
                layout.HTML("""{% include "bootstrap3/custom_widgets/editable_map.html" %}"""),
                css_id="fieldset_institution_select",
            ),
            layout.Fieldset(
                _("Phones"),
                layout.Row(
                    layout.Div(
                        layout.HTML(_("Phone")),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "phone_country",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "phone_area",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "phone_number",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        layout.HTML(_("Fax")),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "fax_country",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "fax_area",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "fax_number",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        layout.HTML(_("Mobile")),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "mobile_country",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "mobile_area",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "mobile_number",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
            ),
            layout.Fieldset(
                _("Emails"),
                "email0",
                "email1",
                "email2",
            ),
            layout.Fieldset(
                _("Websites"),
                layout.Row(
                    layout.Div(
                        "url0_type",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                    layout.Div(
                        "url0_link",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        "url1_type",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                    layout.Div(
                        "url1_link",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        "url2_type",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                    layout.Div(
                        "url2_link",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                ),
            ),
            layout.Fieldset(
                _("Instant Messengers"),
                layout.Row(
                    layout.Div(
                        "im0_type",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                    layout.Div(
                        "im0_address",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        "im1_type",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                    layout.Div(
                        "im1_address",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        "im2_type",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                    layout.Div(
                        "im2_address",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                ),
            ),
            bootstrap.FormActions(
                layout.Button('cancel', _('Cancel')),
                layout.Submit('save_as_primary', _('Save as Primary')),
                layout.Submit('submit', _('Save')),
            )
        )

    def save(self):
        person = self.person
        index = self.index
        data = self.cleaned_data
        save_as_primary = bool(data.get("save_as_primary", False))
        if save_as_primary:
            IndividualContact.objects.filter(person=person).update(is_primary=False)
        elif not person.get_contacts():
            save_as_primary = True
        institution_title = data.get('institution_title', '')
        institution = None
        institution_id = None
        if institution_title:
            institution = Institution.objects.create(
                title=institution_title
            )
            institution_id = institution.id
            if hasattr(institution, "create_default_group"):
                person_group = institution.create_default_group()
                person_group.content_object = institution
                person_group.save()
                membership = person_group.groupmembership_set.create(
                    user=person.user,
                    role="owners",
                    inviter=person.user,
                    confirmer=person.user,
                    is_accepted=True,
                )
        if index is not None and index.isdigit():  # change
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
        else:  # create new
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
                url0_link=data['institution_website'],
                is_primary=True,
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
        super(DetailsForm, self).__init__(*args, **kwargs)
        self.person = person
        self.index = index
        if not args and not kwargs:  # if nothing is posted
            self.fields['individual_type'].initial = person.individual_type_id
            self.fields['salutation'].initial = person.salutation_id
            self.fields['birthday_dd'].initial = person.birthday_dd
            self.fields['birthday_mm'].initial = person.birthday_mm
            self.fields['birthday_yyyy'].initial = person.birthday_yyyy
            self.fields['occupation'].initial = person.occupation
            self.fields['nationality'].initial = person.nationality_id
            self.fields['preferred_language'].initial = person.preferred_language_id

        self.helper = FormHelper()
        self.helper.form_action = "/helper/edit-%(URL_ID_PERSON)s-profile/%(username)s/details/" % {
            'URL_ID_PERSON': URL_ID_PERSON,
            'username': self.person.user.username,
        }
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'target': "hidden_iframe",
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Details"),
                "individual_type",
                "occupation",
                "salutation",
                "nationality",
                "preferred_language",
            ),
            layout.Fieldset(
                _("Birthday"),
                layout.Row(
                    layout.Div(
                        "birthday_dd",
                        css_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                    ),
                    layout.Div(
                        "birthday_mm",
                        css_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                    ),
                    layout.Div(
                        "birthday_yyyy",
                        css_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                    ),
                ),
            ),
            bootstrap.FormActions(
                layout.Button('cancel', _('Cancel')),
                layout.Submit('submit', _('Save')),
            )
        )

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
    # TODO: rework categories to use CheckboxSelectMultiple widget when it is clear what categorizations to use at all
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
        super(CategoriesForm, self).__init__(*args, **kwargs)
        self.person = person
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

        self.helper = FormHelper()
        self.helper.form_action = "/helper/edit-%(URL_ID_PERSON)s-profile/%(username)s/categories/" % {
            'URL_ID_PERSON': URL_ID_PERSON,
            'username': self.person.user.username,
        }
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'target': "hidden_iframe",
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Categories"),
                "choose_creative_sectors",
                "choose_context_categories",
                layout.HTML("""{% load i18n %}
                    <p class="disclaimer">{% blocktrans %}Is some category missing? You can <a href="/ticket/new-category/" target="_blank">suggest it here</a>.{% endblocktrans %}</p>
                """),
            ),
            bootstrap.FormActions(
                layout.Button('cancel', _('Cancel')),
                layout.Submit('submit', _('Save')),
            )
        )

    def save(self, *args, **kwargs):
        person = self.person
        cleaned = self.cleaned_data
        selected_cs = {}
        for item in get_related_queryset(Person, "creative_sectors"):
            if cleaned.get(PREFIX_CI + str(item.id), False):
                # remove all the parents
                for ancestor in item.get_ancestors():
                    if ancestor.id in selected_cs:
                        del (selected_cs[ancestor.id])
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
                        del (selected_cc[ancestor.id])
                # add current
                selected_cc[item.id] = item
        person.context_categories.clear()
        person.context_categories.add(*selected_cc.values())
        ContextItem.objects.update_for(person)
        return person

    def get_extra_context(self):
        return {}

profile_forms = {
    'identity': IdentityForm,
    'description': DescriptionForm,
    'avatar': AvatarForm,
    'contact': ContactForm,
    'details': DetailsForm,
    'categories': CategoriesForm,
}

# -*- coding: UTF-8 -*-
from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat
from django.conf import settings

from base_libs.forms import dynamicforms
from base_libs.forms.fields import ImageField
from base_libs.utils.misc import get_related_queryset, XChoiceList

image_mods = models.get_app("image_mods")

from jetson.apps.location.models import Address
from jetson.apps.optionset.models import PhoneType

from ccb.apps.institutions.models import Institution, InstitutionalContact
from ccb.apps.site_specific.models import ContextItem

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

LEGAL_FORM_CHOICES = XChoiceList(get_related_queryset(Institution, 'legal_form'))

WEEK_DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

# prexixes of fields to guarantee uniqueness
PREFIX_CI = 'CI_'  # Creative Sector aka Creative Industry
PREFIX_BC = 'BC_'  # Context Category aka Business Category
PREFIX_OT = 'OT_'  # Object Type
PREFIX_LT = 'LT_'  # Location Type
PREFIX_JS = 'JS_'  # Job Sector

URL_TYPE_CHOICES = XChoiceList(get_related_queryset(InstitutionalContact, 'url0_type'))
IM_TYPE_CHOICES = XChoiceList(get_related_queryset(InstitutionalContact, 'im0_type'))

INSTITUTION_LOCATION_TYPE_CHOICES = XChoiceList(get_related_queryset(InstitutionalContact, "location_type"))

ESTABLISHMENT_YYYY_CHOICES = Institution._meta.get_field('establishment_yyyy').get_choices()
ESTABLISHMENT_YYYY_CHOICES[0] = ("", _("Year"))
ESTABLISHMENT_MM_CHOICES = Institution._meta.get_field('establishment_mm').get_choices()
ESTABLISHMENT_MM_CHOICES[0] = ("", _("Month"))

LOGO_SIZE = getattr(settings, "LOGO_SIZE", (100, 100))
MIN_LOGO_SIZE = getattr(settings, "MIN_LOGO_SIZE", (100, 100))
STR_LOGO_SIZE = "%sx%s" % LOGO_SIZE
STR_MIN_LOGO_SIZE = "%sx%s" % MIN_LOGO_SIZE

from ccb.apps.institutions.models import URL_ID_INSTITUTION

# Collect translatable strings
_("")


# TODO: each form could be ModelForm. Each formset could be ModelFormSet.
# noinspection PyClassHasNoInit
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
        super(IdentityForm, self).__init__(*args, **kwargs)
        self.institution = institution
        self.index = index
        if not args and not kwargs:  # if nothing is posted
            self.fields['title'].initial = institution.title
            self.fields['title2'].initial = institution.title2

        self.helper = FormHelper()
        self.helper.form_action = "/helper/edit-%(URL_ID_INSTITUTION)s-profile/%(slug)s/identity/" % {
            'URL_ID_INSTITUTION': URL_ID_INSTITUTION,
            'slug': self.institution.slug,
        }
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'target': "hidden_iframe",
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Name"),
                "title",
                "title2",
            ),
            bootstrap.FormActions(
                layout.Button('cancel', _('Cancel')),
                layout.Submit('submit', _('Save')),
            )
        )

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
        super(DescriptionForm, self).__init__(*args, **kwargs)
        self.institution = institution
        self.index = index
        if not args and not kwargs:  # if nothing is posted
            self.fields['description_en'].initial = institution.description_en
            self.fields['description_de'].initial = institution.description_de

        self.helper = FormHelper()
        self.helper.form_action = "/helper/edit-%(URL_ID_INSTITUTION)s-profile/%(slug)s/description/" % {
            'URL_ID_INSTITUTION': URL_ID_INSTITUTION,
            'slug': self.institution.slug,
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
        institution = self.institution
        institution.description_en = self.cleaned_data['description_en']
        institution.description_de = self.cleaned_data['description_de']
        institution.save()
        return institution

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

    def __init__(self, institution, index, *args, **kwargs):
        super(AvatarForm, self).__init__(*args, **kwargs)
        self.institution = institution
        self.index = index

        self.helper = FormHelper()
        self.helper.form_action = "/helper/edit-%(URL_ID_INSTITUTION)s-profile/%(slug)s/avatar/" % {
            'URL_ID_INSTITUTION': URL_ID_INSTITUTION,
            'slug': self.institution.slug,
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
                        <img src="{{ DEFAULT_FORM_LOGO_4_INSTITUTION }}" alt="{{ object.get_title|escape }}"/>
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
        institution = self.institution
        if "media_file" in self.files:
            media_file = self.files['media_file']
            image_mods.FileManager.save_file_for_object(
                institution,
                media_file.name,
                media_file,
                subpath="avatar/"
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

    def __init__(self, institution, index, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.institution = institution
        self.index = index
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

        self.helper = FormHelper()
        self.helper.form_action = "/helper/edit-%(URL_ID_INSTITUTION)s-profile/%(slug)s/contact/%(index)s/" % {
            'URL_ID_INSTITUTION': URL_ID_INSTITUTION,
            'slug': self.institution.slug,
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
                layout.HTML("""{% load i18n %}
                    <div class="map_container">
                        <div class="map_canvas">
                            <!-- THE GMAPS WILL BE INSERTED HERE DYNAMICALLY -->
                        </div>
                        <div class="buttonHolder">
                            <button id="dyn_remove_geo" class="btn">{% filter upper %}{% trans "Remove from map" %}{% endfilter %}</button>
                        </div>
                    </div>
                """),
                css_id="fieldset_institution_select",
            ),
            layout.Fieldset(
                _("Phone"),
                layout.Row(
                    layout.Div(
                        "phone_country",
                        css_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                    ),
                    layout.Div(
                        "phone_area",
                        css_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                    ),
                    layout.Div(
                        "phone_number",
                        css_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                    ),
                ),
            ),
            layout.Fieldset(
                _("Fax"),
                layout.Row(
                    layout.Div(
                        "fax_country",
                        css_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                    ),
                    layout.Div(
                        "fax_area",
                        css_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                    ),
                    layout.Div(
                        "fax_number",
                        css_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                    ),
                ),
            ),
            layout.Fieldset(
                _("Mobile"),
                layout.Row(
                    layout.Div(
                        "mobile_country",
                        css_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                    ),
                    layout.Div(
                        "mobile_area",
                        css_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                    ),
                    layout.Div(
                        "mobile_number",
                        css_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
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
        institution = self.institution
        index = self.index
        data = self.cleaned_data
        save_as_primary = bool(data.get("save_as_primary", False))
        if save_as_primary:
            InstitutionalContact.objects.filter(institution=institution).update(is_primary=False)
        elif not institution.get_contacts():
            save_as_primary = True
        if index is not None and index.isdigit():  # change
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
        else:  # create new
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
        required=False,  # should be required=True ???
        choices=ESTABLISHMENT_YYYY_CHOICES,
        label=_("Establishment"),
        error_messages={
            'required': _("Year of establishment is required"),
        },
    )
    establishment_mm = forms.ChoiceField(
        required=False,  # should be required=True ???
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
        super(DetailsForm, self).__init__(*args, **kwargs)
        self.institution = institution
        self.index = index
        if not args and not kwargs:  # if nothing is posted
            self.fields['legal_form'].initial = institution.legal_form_id
            self.fields['establishment_yyyy'].initial = institution.establishment_yyyy
            self.fields['establishment_mm'].initial = institution.establishment_mm
            self.fields['nof_employees'].initial = institution.nof_employees

        self.helper = FormHelper()
        self.helper.form_action = "/helper/edit-%(URL_ID_INSTITUTION)s-profile/%(slug)s/details/" % {
            'URL_ID_INSTITUTION': URL_ID_INSTITUTION,
            'slug': self.institution.slug,
        }
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'target': "hidden_iframe",
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Details"),
                "legal_form",
                layout.Row(
                    layout.Div(
                        "establishment_mm",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                    layout.Div(
                        "establishment_yyyy",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                ),
                "nof_employees",
            ),
            bootstrap.FormActions(
                layout.Button('cancel', _('Cancel')),
                layout.Submit('submit', _('Save')),
            )
        )

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
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.institution = institution
        self.index = index
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

        self.helper = FormHelper()
        self.helper.form_action = "/helper/edit-%(URL_ID_INSTITUTION)s-profile/%(slug)s/payment/" % {
            'URL_ID_INSTITUTION': URL_ID_INSTITUTION,
            'slug': self.institution.slug,
        }
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'target': "hidden_iframe",
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Payment Options"),
                layout.Row(
                    layout.Div(
                        "is_cash_ok",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                    layout.Div(
                        "is_card_visa_ok",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        "is_invoice_ok",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                    layout.Div(
                        "is_card_mastercard_ok",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        "is_on_delivery_ok",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                    layout.Div(
                        "is_card_americanexpress_ok",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        "is_ec_maestro_ok",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                    layout.Div(
                        "is_giropay_ok",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        "is_prepayment_ok",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                    layout.Div(
                        "is_paypal_ok",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                ),
            ),
            bootstrap.FormActions(
                layout.Button('cancel', _('Cancel')),
                layout.Submit('submit', _('Save')),
            )
        )

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

    mon_open0 = forms.TimeField(
        label=_("opens"),
        required=False,
    )
    mon_close0 = forms.TimeField(
        label=_("closes"),
        required=False,
    )
    mon_open1 = forms.TimeField(
        label=_("opens again"),
        required=False,
    )
    mon_close1 = forms.TimeField(
        label=_("closes"),
        required=False,
    )
    mon_is_closed = forms.BooleanField(
        label=_("Closed"),
        required=False,
        initial=False,
    )

    tue_open0 = forms.TimeField(
        label=_("opens"),
        required=False,
    )
    tue_close0 = forms.TimeField(
        label=_("closes"),
        required=False,
    )
    tue_open1 = forms.TimeField(
        label=_("opens again"),
        required=False,
    )
    tue_close1 = forms.TimeField(
        label=_("closes"),
        required=False,
    )
    tue_is_closed = forms.BooleanField(
        label=_("Closed"),
        required=False,
        initial=False,
    )

    wed_open0 = forms.TimeField(
        label=_("opens"),
        required=False,
    )
    wed_close0 = forms.TimeField(
        label=_("closes"),
        required=False,
    )
    wed_open1 = forms.TimeField(
        label=_("opens again"),
        required=False,
    )
    wed_close1 = forms.TimeField(
        label=_("closes"),
        required=False,
    )
    wed_is_closed = forms.BooleanField(
        label=_("Closed"),
        required=False,
        initial=False,
    )

    thu_open0 = forms.TimeField(
        label=_("opens"),
        required=False,
    )
    thu_close0 = forms.TimeField(
        label=_("closes"),
        required=False,
    )
    thu_open1 = forms.TimeField(
        label=_("opens again"),
        required=False,
    )
    thu_close1 = forms.TimeField(
        label=_("closes"),
        required=False,
    )
    thu_is_closed = forms.BooleanField(
        label=_("Closed"),
        required=False,
        initial=False,
    )

    fri_open0 = forms.TimeField(
        label=_("opens"),
        required=False,
    )
    fri_close0 = forms.TimeField(
        label=_("closes"),
        required=False,
    )
    fri_open1 = forms.TimeField(
        label=_("opens again"),
        required=False,
    )
    fri_close1 = forms.TimeField(
        label=_("closes"),
        required=False,
    )
    fri_is_closed = forms.BooleanField(
        label=_("Closed"),
        required=False,
        initial=False,
    )

    sat_open0 = forms.TimeField(
        label=_("opens"),
        required=False,
    )
    sat_close0 = forms.TimeField(
        label=_("closes"),
        required=False,
    )
    sat_open1 = forms.TimeField(
        label=_("opens again"),
        required=False,
    )
    sat_close1 = forms.TimeField(
        label=_("closes"),
        required=False,
    )
    sat_is_closed = forms.BooleanField(
        label=_("Closed"),
        required=False,
        initial=False,
    )

    sun_open0 = forms.TimeField(
        label=_("opens"),
        required=False,
    )
    sun_close0 = forms.TimeField(
        label=_("closes"),
        required=False,
    )
    sun_open1 = forms.TimeField(
        label=_("opens again"),
        required=False,
    )
    sun_close1 = forms.TimeField(
        label=_("closes"),
        required=False,
    )
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
        super(OpeningHoursForm, self).__init__(*args, **kwargs)
        self.institution = institution
        self.index = index
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

        self.helper = FormHelper()
        self.helper.form_action = "/helper/edit-%(URL_ID_INSTITUTION)s-profile/%(slug)s/opening_hours/" % {
            'URL_ID_INSTITUTION': URL_ID_INSTITUTION,
            'slug': self.institution.slug,
        }
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'target': "hidden_iframe",
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                string_concat(_("Opening Time"), " - ",  _("Closing Time")),
                layout.Row(
                    layout.Div(
                        layout.HTML(_("Monday")),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "mon_open0",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "mon_close0",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "mon_is_closed",
                        "show_breaks",
                        layout.HTML("""{% load i18n %}
                            <p>
                                <a id="id_apply_all_days" href="#">{% trans "Apply to all days" %}</a>
                            </p>
                        """),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        layout.HTML("&nbsp;"),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "mon_open1",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "mon_close1",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        layout.HTML("&nbsp;"),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
                
                layout.Row(
                    layout.Div(
                        layout.HTML(_("Tuesday")),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "tue_open0",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "tue_close0",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "tue_is_closed",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        layout.HTML("&nbsp;"),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "tue_open1",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "tue_close1",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        layout.HTML("&nbsp;"),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
                
                layout.Row(
                    layout.Div(
                        layout.HTML(_("Wednesday")),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "wed_open0",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "wed_close0",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "wed_is_closed",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        layout.HTML("&nbsp;"),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "wed_open1",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "wed_close1",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        layout.HTML("&nbsp;"),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
                
                layout.Row(
                    layout.Div(
                        layout.HTML(_("Thursday")),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "thu_open0",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "thu_close0",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "thu_is_closed",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        layout.HTML("&nbsp;"),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "thu_open1",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "thu_close1",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        layout.HTML("&nbsp;"),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
                
                layout.Row(
                    layout.Div(
                        layout.HTML(_("Friday")),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "fri_open0",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "fri_close0",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "fri_is_closed",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        layout.HTML("&nbsp;"),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "fri_open1",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "fri_close1",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        layout.HTML("&nbsp;"),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
                
                layout.Row(
                    layout.Div(
                        layout.HTML(_("Saturday")),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "sat_open0",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "sat_close0",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "sat_is_closed",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        layout.HTML("&nbsp;"),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "sat_open1",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "sat_close1",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        layout.HTML("&nbsp;"),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
                
                layout.Row(
                    layout.Div(
                        layout.HTML(_("Sunday")),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "sun_open0",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "sun_close0",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "sun_is_closed",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        layout.HTML("&nbsp;"),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "sun_open1",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "sun_close1",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        layout.HTML("&nbsp;"),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
                
                "exceptions_de",
                "exceptions_en",
                "is_appointment_based",
            ),
            bootstrap.FormActions(
                layout.Button('cancel', _('Cancel')),
                layout.Submit('submit', _('Save')),
            )
        )

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
                        self._errors[week_day + '_open0'] = [
                            _("A closing time must not be before an opening time.")]
                if close0:
                    if not open0:
                        self._errors[week_day + '_open0'] = [_("Please enter an opening time.")]

                if show_breaks:
                    if open1:
                        if not close1:
                            self._errors[week_day + '_open1'] = [_("Please enter a closing time.")]
                        elif close1 < open1:
                            self._errors[week_day + '_open1'] = [
                                _("A closing time must not be before an opening time.")]
                    if close1:
                        if not open1:
                            self._errors[week_day + '_open1'] = [_("Please enter an opening time.")]

                    if open1 or close1:
                        if not open0 or not close0:
                            self._errors[week_day + '_open1'] = [
                                _("When specifying breaks, you must enter all data.")]
                        else:
                            if open1 < close0:
                                self._errors[week_day + '_open1'] = [
                                    _("An opening time after break must not be before the closing time to break.")]

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
        super(CategoriesForm, self).__init__(*args, **kwargs)
        self.institution = institution
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

        self.helper = FormHelper()
        self.helper.form_action = "/helper/edit-%(URL_ID_INSTITUTION)s-profile/%(slug)s/categories/" % {
            'URL_ID_INSTITUTION': URL_ID_INSTITUTION,
            'slug': self.institution.slug,
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
                "choose_object_types",
            ),
            bootstrap.FormActions(
                layout.Button('cancel', _('Cancel')),
                layout.Submit('submit', _('Save')),
            )
        )

    def save(self, *args, **kwargs):
        institution = self.institution
        cleaned = self.cleaned_data
        selected_cs = {}
        for item in get_related_queryset(Institution, "creative_sectors"):
            if cleaned.get(PREFIX_CI + str(item.id), False):
                # remove all the parents
                for ancestor in item.get_ancestors():
                    if ancestor.id in selected_cs:
                        del (selected_cs[ancestor.id])
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
                        del (selected_cc[ancestor.id])
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
                        del (selected_ot[ancestor.id])
                # add current
                selected_ot[item.id] = item
        institution.institution_types.clear()
        institution.institution_types.add(*selected_ot.values())
        ContextItem.objects.update_for(institution)
        return institution

    def get_extra_context(self):
        return {}


profile_forms = {
    'identity': IdentityForm,
    'description': DescriptionForm,
    'avatar': AvatarForm,
    'contact': ContactForm,
    'details': DetailsForm,
    'payment': PaymentForm,
    'opening_hours': OpeningHoursForm,
    'categories': CategoriesForm,
}

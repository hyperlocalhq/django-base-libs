# -*- coding: UTF-8 -*-
from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat
from django.conf import settings
from django.shortcuts import redirect

from base_libs.forms import dynamicforms
from base_libs.forms.fields import ImageField
from base_libs.utils.misc import get_related_queryset, XChoiceList

from jetson.apps.location.models import Address
from jetson.apps.optionset.models import PhoneType
from jetson.apps.utils.forms import ModelMultipleChoiceTreeField

from ccb.apps.institutions.models import Institution, InstitutionalContact
from ccb.apps.site_specific.models import ContextItem
from ccb.apps.institutions.models import URL_ID_INSTITUTION

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

image_mods = models.get_app("image_mods")

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
MIN_LOGO_SIZE = getattr(settings, "LOGO_SIZE", (100, 100))
STR_LOGO_SIZE = "%sx%s" % LOGO_SIZE
STR_MIN_LOGO_SIZE = "%sx%s" % MIN_LOGO_SIZE

# Collect translatable strings
_("Apply to all days")


# TODO: each form could be ModelForm. Each formset could be ModelFormSet.
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
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Identity"),
                "title",
                "title2",
                bootstrap.FormActions(
                    layout.Button('cancel', _('Cancel'), css_class="cancel"),
                    layout.Submit('submit', _('Save')),
                    css_class = "button-group form-buttons"
                ),
                
                css_class = "switch on"
            ),
        )

    def save(self):
        institution = self.institution
        institution.title = self.cleaned_data['title']
        institution.title2 = self.cleaned_data['title2']
        institution.calculate_completeness()
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
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Description"),
                "description_en",
                "description_de",
                bootstrap.FormActions(
                    layout.Button('cancel', _('Cancel'), css_class="cancel"),
                    layout.Submit('submit', _('Save')),
                    css_class = "button-group form-buttons"
                ),
                
                css_class = "switch on"
            ),
        )

    def save(self):
        institution = self.institution
        institution.description_en = self.cleaned_data['description_en']
        institution.description_de = self.cleaned_data['description_de']
        institution.calculate_completeness()
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
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Avatar"),
                layout.HTML("""{% load image_modifications %}
                    {% if object.image %}
                        <dt>""" + (_("Image") + "") + """</dt><dd><img src="{{ UPLOADS_URL }}{{ object.image|modified_path:"profile" }}" alt="{{ object.get_title|escape }}"/></dd>
                    {% else %}
                        <dt>""" + (_("Image") + "") + """</dt><dd><img src="{{ STATIC_URL }}site/img/placeholder/institution.png" alt="{{ object.get_title|escape }}"/></dd>
                    {% endif %}
                """),
                "media_file",
                bootstrap.FormActions(
                    layout.Button('cancel', _('Cancel'), css_class="cancel"),
                    layout.Submit('submit', _('Save')),
                    css_class="button-group form-buttons"
                ),
                css_class="switch on",
            ),
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
        institution.calculate_completeness()
        institution.save()
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
        label=_("Phone Country Code"),
        required=False,
        max_length=4,
        initial="49",
    )
    phone_area = forms.CharField(
        label=_("Phone Area Code"),
        required=False,
        max_length=5,
    )
    phone_number = forms.CharField(
        label=_("Phone Number"),
        required=False,
        max_length=15,
    )
    fax_country = forms.CharField(
        label=_("Fax Country Code"),
        required=False,
        max_length=4,
        initial="49",
    )
    fax_area = forms.CharField(
        label=_("Fax Area Code"),
        required=False,
        max_length=5,
    )
    fax_number = forms.CharField(
        label=_("Fax Number"),
        required=False,
        max_length=15,
    )
    mobile_country = forms.CharField(
        label=_("Mobile Country Code"),
        required=False,
        max_length=4,
        initial="49",
    )
    mobile_area = forms.CharField(
        label=_("Mobile Area Code"),
        required=False,
        max_length=5,
    )
    mobile_number = forms.CharField(
        label=_("Mobile Number"),
        required=False,
        max_length=15,
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
                contact = institution.get_contacts(cache=False)[index]
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
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _('Contact Data'),
                
                layout.HTML(string_concat('<dd class="no-label"><h3>', _("Address"), "-", _("Institution"), '</h3></dd>')),
                "location_type",
                "location_title",
                
                layout.HTML(string_concat('<dd class="no-label"><h3 class="section">', _("Address"), '</h3></dd>')),
                _("Address"),
                "latitude",  # hidden field
                "longitude",  # hidden field
                "district",  # hidden field
                "street_address",
                "street_address2",
                layout.MultiField(
                    string_concat(_('ZIP'), "*, ", _('City'), "*"),
                    layout.Field(
                        "postal_code",
                        wrapper_class = "col-xs-4 col-sm-5 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "city",
                        wrapper_class = "col-xs-8 col-sm-7 col-md-9 col-lg-9",
                        template = "ccb_form/multifield.html"
                    )
                ),
                "country",
                layout.HTML("""{% include "ccb_form/custom_widgets/editable_map.html" %}"""),
                
                layout.HTML(string_concat('<dd class="no-label"><h3 class="section">', _("Phones"), '</h3></dd>')),
                layout.MultiField(
                    _("Phone"),
                    layout.Field(
                        "phone_country",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "phone_area",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "phone_number",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template = "ccb_form/multifield.html"
                    ),
                    css_class = "show-labels"
                ),
                layout.MultiField(
                    _("Fax"),
                    layout.Field(
                        "fax_country",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "fax_area",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "fax_number",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template = "ccb_form/multifield.html"
                    ),
                    css_class = "show-labels"
                ),
                layout.MultiField(
                    _("Mobile"),
                    layout.Field(
                        "mobile_country",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "mobile_area",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "mobile_number",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template = "ccb_form/multifield.html"
                    ),
                    css_class = "show-labels"
                ),
                
                layout.HTML(string_concat('<dd class="no-label"><h3 class="section">', _("Emails"), '</h3></dd>')),
                "email0",
                "email1",
                "email2",
                
                layout.HTML(string_concat('<dd class="no-label"><h3 class="section">', _("Websites"), '</h3></dd>')),
                layout.MultiField(
                    string_concat(_('Type'), ", ", _('Url')),
                    layout.Field(
                        "url0_type",
                        wrapper_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "url0_link",
                        wrapper_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html"
                    ),
                ),
                layout.MultiField(
                    string_concat(_('Type'), ", ", _('Url')),
                    layout.Field(
                        "url1_type",
                        wrapper_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "url1_link",
                        wrapper_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html"
                    ),
                ),
                layout.MultiField(
                    string_concat(_('Type'), ", ", _('Url')),
                    layout.Field(
                        "url2_type",
                        wrapper_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "url2_link",
                        wrapper_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html"
                    ),
                ),
                
                layout.HTML(string_concat('<dd class="no-label"><h3 class="section">', _("Instant Messengers"), '</h3></dd>')),
                layout.MultiField(
                    string_concat(_('Type'), ", ", _('Address')),
                    layout.Field(
                        "im0_type",
                        wrapper_class="col-xs-6 col-sm-6 col-md-4 col-lg-4",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "im0_address",
                        wrapper_class="col-xs-6 col-sm-6 col-md-8 col-lg-8",
                        template = "ccb_form/multifield.html"
                    ),
                ),
                layout.MultiField(
                    string_concat(_('Type'), ", ", _('Address')),
                    layout.Field(
                        "im1_type",
                        wrapper_class="col-xs-6 col-sm-6 col-md-4 col-lg-4",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "im1_address",
                        wrapper_class="col-xs-6 col-sm-6 col-md-8 col-lg-8",
                        template = "ccb_form/multifield.html"
                    ),
                ),
                layout.MultiField(
                    string_concat(_('Type'), ", ", _('Address')),
                    layout.Field(
                        "im2_type",
                        wrapper_class="col-xs-6 col-sm-6 col-md-4 col-lg-4",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "im2_address",
                        wrapper_class="col-xs-6 col-sm-6 col-md-8 col-lg-8",
                        template = "ccb_form/multifield.html"
                    ),
                ),
                
                bootstrap.FormActions(
                    layout.Button('cancel', _('Cancel'), css_class = "cancel"),
                    layout.Submit('save_as_primary', _('Save as Primary')),
                    layout.Submit('submit', _('Save')),
                    css_class = "button-group form-buttons"
                ),
                
                css_class = "switch on"
            )
        )

    def save(self):
        institution = self.institution
        index = self.index
        data = self.cleaned_data
        save_as_primary = bool(data.get("save_as_primary", False))
        if index is not None and index.isdigit():  # change
            index = int(index)
            contact = institution.get_contacts(cache=False)[index]

            if save_as_primary:
                InstitutionalContact.objects.filter(institution=institution).update(is_primary=False)
            elif not institution.get_contacts(cache=False):
                save_as_primary = True

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
            contact.is_primary = contact.is_primary or save_as_primary
            contact.save()
        else:  # create new

            if save_as_primary:
                InstitutionalContact.objects.filter(institution=institution).update(is_primary=False)
            elif not institution.get_contacts(cache=False):
                save_as_primary = True

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
        institution.calculate_completeness()
        institution.save()
        return institution

    def get_extra_context(self):
        institution = self.institution
        index = self.index
        contact = getattr(self, "contact", None)
        if index is not None and index.isdigit():
            index = int(index)
            contact = institution.get_contacts(cache=False)[index]
        return {'contact': contact}

    def get_success_response(self):
        return redirect("show_profile_contacts", object_type='institution', slug=self.institution.slug)

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
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Details"),
                "legal_form",
                layout.MultiField(
                    _('Establishment'),
                    layout.Field(
                        "establishment_mm",
                        wrapper_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html",
                        placeholder=_("Month"),
                    ),
                    layout.Field(
                        "establishment_yyyy",
                        wrapper_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html",
                        placeholder=_("Year"),
                    ),
                ),
                "nof_employees",
                bootstrap.FormActions(
                    layout.Button('cancel', _('Cancel'), css_class="cancel"),
                    layout.Submit('submit', _('Save')),
                    css_class = "button-group form-buttons"
                ),
                
                css_class = "switch on"
            ),
        )

    def save(self):
        institution = self.institution
        institution.legal_form_id = self.cleaned_data.get('legal_form', None)
        institution.establishment_yyyy = self.cleaned_data.get('establishment_yyyy') or None
        institution.establishment_mm = self.cleaned_data.get('establishment_mm') or None
        institution.nof_employees = self.cleaned_data['nof_employees']
        institution.calculate_completeness()
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
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Payment"),
                layout.MultiField(
                    ' ',
                    layout.Field(
                        "is_cash_ok",
                        wrapper_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "is_card_visa_ok",
                        wrapper_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html"
                    ),
                ),
                layout.MultiField(
                    ' ',
                    layout.Field(
                        "is_invoice_ok",
                        wrapper_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "is_card_mastercard_ok",
                        wrapper_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html"
                    ),
                ),
                layout.MultiField(
                    ' ',
                    layout.Field(
                        "is_on_delivery_ok",
                        wrapper_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "is_card_americanexpress_ok",
                        wrapper_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html"
                    ),
                ),
                layout.MultiField(
                    ' ',
                    layout.Field(
                        "is_ec_maestro_ok",
                        wrapper_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "is_giropay_ok",
                        wrapper_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html"
                    ),
                ),
                layout.MultiField(
                    ' ',
                    layout.Field(
                        "is_prepayment_ok",
                        wrapper_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "is_paypal_ok",
                        wrapper_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html"
                    ),
                ),
                bootstrap.FormActions(
                    layout.Button('cancel', _('Cancel'), css_class="cancel"),
                    layout.Submit('submit', _('Save')),
                    css_class = "button-group form-buttons"
                ),
                css_class = "no-label switch on"
            ),
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
        institution.calculate_completeness()
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
        widget=forms.TimeInput(format = '%H:%M'),
    )
    mon_close0 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    mon_open1 = forms.TimeField(
        label=_("opens again"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    mon_close1 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    mon_is_closed = forms.BooleanField(
        label=_("Closed"),
        required=False,
        initial=False,
    )

    tue_open0 = forms.TimeField(
        label=_("opens"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    tue_close0 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    tue_open1 = forms.TimeField(
        label=_("opens again"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    tue_close1 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    tue_is_closed = forms.BooleanField(
        label=_("Closed"),
        required=False,
        initial=False,
    )

    wed_open0 = forms.TimeField(
        label=_("opens"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    wed_close0 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    wed_open1 = forms.TimeField(
        label=_("opens again"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    wed_close1 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    wed_is_closed = forms.BooleanField(
        label=_("Closed"),
        required=False,
        initial=False,
    )

    thu_open0 = forms.TimeField(
        label=_("opens"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    thu_close0 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    thu_open1 = forms.TimeField(
        label=_("opens again"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    thu_close1 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    thu_is_closed = forms.BooleanField(
        label=_("Closed"),
        required=False,
        initial=False,
    )

    fri_open0 = forms.TimeField(
        label=_("opens"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    fri_close0 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    fri_open1 = forms.TimeField(
        label=_("opens again"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    fri_close1 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    fri_is_closed = forms.BooleanField(
        label=_("Closed"),
        required=False,
        initial=False,
    )

    sat_open0 = forms.TimeField(
        label=_("opens"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    sat_close0 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    sat_open1 = forms.TimeField(
        label=_("opens again"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    sat_close1 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    sat_is_closed = forms.BooleanField(
        label=_("Closed"),
        required=False,
        initial=False,
    )

    sun_open0 = forms.TimeField(
        label=_("opens"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    sun_close0 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    sun_open1 = forms.TimeField(
        label=_("opens again"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    sun_close1 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
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
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Opening hours"),
                layout.MultiField(
                    _("Monday"),
                    layout.Field(
                        "mon_open0",
                        wrapper_class="col-xs-6 col-sm-3 col-md-3 col-lg-3 closed_mon",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "mon_close0",
                        wrapper_class="col-xs-6 col-sm-3 col-md-3 col-lg-3 closed_mon",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "mon_is_closed",
                        wrapper_class="col-xs-12 col-sm-6 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html",
                        css_class = "closed mon"
                    ),
                    css_class = "show-labels"
                ),
                layout.MultiField(
                    ' ',
                    layout.Field(
                        "mon_open1",
                        wrapper_class="col-xs-6 col-sm-3 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "mon_close1",
                        wrapper_class="col-xs-6 col-sm-3 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                    css_class = "show-labels break closed_mon"
                ),
                
                "show_breaks",
                layout.HTML("""{% load i18n %}
                    <dt></dt><dd><p><a id="apply_to_all_days" href="#">{% trans "Apply to all days" %}</a></p></dd>
                    <dd class="clearfix">&nbsp;</dd>
                """),
                
                layout.MultiField(
                    _("Tuesday"),
                    layout.Field(
                        "tue_open0",
                        wrapper_class="col-xs-6 col-sm-3 col-md-3 col-lg-3 closed_tue",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "tue_close0",
                        wrapper_class="col-xs-6 col-sm-3 col-md-3 col-lg-3 closed_tue",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "tue_is_closed",
                        wrapper_class="col-xs-12 col-sm-6 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html",
                        css_class = "closed tue"
                    ),
                    css_class = "show-labels"
                ),
                layout.MultiField(
                    ' ',
                    layout.Field(
                        "tue_open1",
                        wrapper_class="col-xs-6 col-sm-3 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "tue_close1",
                        wrapper_class="col-xs-6 col-sm-3 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                    css_class = "show-labels break closed_tue"
                ),
                
                layout.HTML("""<dd class="clearfix">&nbsp;</dd>"""),
                
                layout.MultiField(
                    _("Wednesday"),
                    layout.Field(
                        "wed_open0",
                        wrapper_class="col-xs-6 col-sm-3 col-md-3 col-lg-3 closed_wed",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "wed_close0",
                        wrapper_class="col-xs-6 col-sm-3 col-md-3 col-lg-3 closed_wed",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "wed_is_closed",
                        wrapper_class="col-xs-12 col-sm-6 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html",
                        css_class = "closed wed"
                    ),
                    css_class = "show-labels"
                ),
                layout.MultiField(
                    ' ',
                    layout.Field(
                        "wed_open1",
                        wrapper_class="col-xs-6 col-sm-3 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "wed_close1",
                        wrapper_class="col-xs-6 col-sm-3 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                    css_class = "show-labels break closed_wed"
                ),
                
                layout.HTML("""<dd class="clearfix">&nbsp;</dd>"""),
                
                layout.MultiField(
                    _("Thursday"),
                    layout.Field(
                        "thu_open0",
                        wrapper_class="col-xs-6 col-sm-3 col-md-3 col-lg-3 closed_thu",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "thu_close0",
                        wrapper_class="col-xs-6 col-sm-3 col-md-3 col-lg-3 closed_thu",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "thu_is_closed",
                        wrapper_class="col-xs-12 col-sm-6 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html",
                        css_class = "closed thu"
                    ),
                    css_class = "show-labels"
                ),
                layout.MultiField(
                    ' ',
                    layout.Field(
                        "thu_open1",
                        wrapper_class="col-xs-6 col-sm-3 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "thu_close1",
                        wrapper_class="col-xs-6 col-sm-3 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                    css_class = "show-labels break closed_thu"
                ),
                
                layout.HTML("""<dd class="clearfix">&nbsp;</dd>"""),
                
                layout.MultiField(
                    _("Friday"),
                    layout.Field(
                        "fri_open0",
                        wrapper_class="col-xs-6 col-sm-3 col-md-3 col-lg-3 closed_fri",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "fri_close0",
                        wrapper_class="col-xs-6 col-sm-3 col-md-3 col-lg-3 closed_fri",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "fri_is_closed",
                        wrapper_class="col-xs-12 col-sm-6 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html",
                        css_class = "closed fri"
                    ),
                    css_class = "show-labels"
                ),
                layout.MultiField(
                    ' ',
                    layout.Field(
                        "fri_open1",
                        wrapper_class="col-xs-6 col-sm-3 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "fri_close1",
                        wrapper_class="col-xs-6 col-sm-3 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                    css_class = "show-labels break closed_fri"
                ),
                
                layout.HTML("""<dd class="clearfix">&nbsp;</dd>"""),
                
                layout.MultiField(
                    _("Saturday"),
                    layout.Field(
                        "sat_open0",
                        wrapper_class="col-xs-6 col-sm-3 col-md-3 col-lg-3 closed_sat",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "sat_close0",
                        wrapper_class="col-xs-6 col-sm-3 col-md-3 col-lg-3 closed_sat",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "sat_is_closed",
                        wrapper_class="col-xs-12 col-sm-6 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html",
                        css_class = "closed sat"
                    ),
                    css_class = "show-labels"
                ),
                layout.MultiField(
                    ' ',
                    layout.Field(
                        "sat_open1",
                        wrapper_class="col-xs-6 col-sm-3 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "sat_close1",
                        wrapper_class="col-xs-6 col-sm-3 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                    css_class = "show-labels break closed_sat"
                ),
                
                layout.HTML("""<dd class="clearfix">&nbsp;</dd>"""),
                
                layout.MultiField(
                    _("Sunday"),
                    layout.Field(
                        "sun_open0",
                        wrapper_class="col-xs-6 col-sm-3 col-md-3 col-lg-3 closed_sun",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "sun_close0",
                        wrapper_class="col-xs-6 col-sm-3 col-md-3 col-lg-3 closed_sun",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "sun_is_closed",
                        wrapper_class="col-xs-12 col-sm-6 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html",
                        css_class = "closed sun"
                    ),
                    css_class = "show-labels"
                ),
                layout.MultiField(
                    ' ',
                    layout.Field(
                        "sun_open1",
                        wrapper_class="col-xs-6 col-sm-3 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "sun_close1",
                        wrapper_class="col-xs-6 col-sm-3 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                    css_class = "show-labels break closed_sun"
                ),
                
                layout.HTML("""<dd class="clearfix">&nbsp;</dd>"""),

                "exceptions_de",
                "exceptions_en",
                "is_appointment_based",
                
                bootstrap.FormActions(
                    layout.Button('cancel', _('Cancel'), css_class="cancel"),
                    layout.Submit('submit', _('Save')),
                    css_class = "button-group form-buttons"
                ),
                
                css_class = "opening-hours switch on"
            ),
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

        institution.calculate_completeness()
        institution.save()
        return institution

    def get_extra_context(self):
        return {}


class CategoriesForm(dynamicforms.Form):
    categories = ModelMultipleChoiceTreeField(
        label=_("Categories"),
        queryset=get_related_queryset(Institution, "categories"),
        required=True,
    )

    institution_types = ModelMultipleChoiceTreeField(
        label=_("Types"),
        queryset=get_related_queryset(Institution, "institution_types"),
        required=True,
    )

    def __init__(self, institution, index, *args, **kwargs):
        super(CategoriesForm, self).__init__(*args, **kwargs)
        self.institution = institution

        self.fields['categories'].initial = self.institution.categories.all()
        self.fields['institution_types'].initial = self.institution.institution_types.all()

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Categories"),
                
                layout.HTML(string_concat('<dt>', _("Categories"), '</dt>')),
                layout.Field("categories", template="ccb_form/custom_widgets/checkboxselectmultipletree.html"),
                
                layout.HTML("""<dd class="clearfix"></dd>"""),
                
                layout.HTML(string_concat('<dt>', _("Institution Types"), '</dt>')),
                layout.Field("institution_types", template="ccb_form/custom_widgets/checkboxselectmultipletree.html"),
                
                bootstrap.FormActions(
                    layout.Button('cancel', _('Cancel'), css_class="cancel"),
                    layout.Submit('submit', _('Save')),
                    css_class = "button-group form-buttons"
                ),
                
                css_class = "switch on"
            ),
        )

    def save(self, *args, **kwargs):
        institution = self.institution
        cleaned = self.cleaned_data

        institution.categories.clear()
        institution.categories.add(*cleaned['categories'])

        institution.institution_types.clear()
        institution.institution_types.add(*cleaned['institution_types'])

        institution.calculate_completeness()
        institution.save()
        # ContextItem.objects.update_for(institution)
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

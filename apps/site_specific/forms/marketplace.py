# -*- coding: UTF-8 -*-
import datetime

from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat
from django.conf import settings
from django.utils.dates import MONTHS
from base_libs.forms import dynamicforms
from base_libs.utils.misc import get_related_queryset, XChoiceList
from base_libs.forms.fields import AutocompleteField
from base_libs.middleware import get_current_user
from tagging.forms import TagField
from tagging_autocomplete.widgets import TagAutocomplete
from jetson.apps.location.models import Address
from jetson.apps.optionset.models import PhoneType
from jetson.apps.utils.forms import ModelMultipleChoiceTreeField
from ccb.apps.marketplace.models import JobOffer
from ccb.apps.marketplace.models import URL_ID_JOB_OFFER
from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

image_mods = models.get_app("image_mods")

Institution = models.get_model("institutions", "Institution")

YEARS_CHOICES = [("", _("Year"))] + [(i, i) for i in range(2008, 2040)]
MONTHS_CHOICES = [("", _("Month"))] + MONTHS.items()
DAYS_CHOICES = [("", _("Day"))] + [(i, i) for i in range(1, 32)]
HOURS_CHOICES = [("", _("HH"))] + [(i, u"%02d" % i) for i in range(0, 24)]
MINUTES_CHOICES = [("", _("MM"))] + [(i, u"%02d" % i) for i in range(0, 60, 5)]

# prexixes of fields to guarantee uniqueness
PREFIX_CI = 'CI_'  # Creative Sector aka Creative Industry
PREFIX_BC = 'BC_'  # Context Category aka Business Category
PREFIX_OT = 'OT_'  # Object Type
PREFIX_LT = 'LT_'  # Location Type
PREFIX_JS = 'JS_'  # Job Sector

URL_TYPE_CHOICES = XChoiceList(get_related_queryset(JobOffer, 'url0_type'))
IM_TYPE_CHOICES = XChoiceList(get_related_queryset(JobOffer, 'im0_type'))

CONTACT_PERSON_CHOICES = [
    (0, _("I am the contact person")),
    (1, _("I am not the contact person")),
]

LOGO_SIZE = getattr(settings, "LOGO_SIZE", (100, 100))
MIN_LOGO_SIZE = getattr(settings, "MIN_LOGO_SIZE", (100, 100))
STR_LOGO_SIZE = "%sx%s" % LOGO_SIZE
STR_MIN_LOGO_SIZE = "%sx%s" % MIN_LOGO_SIZE

# Collect translatable strings
_("Not listed? Enter manually")
_("Back to selection")


# TODO: each form could be ModelForm. Each formset could be ModelFormSet.
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
        widget=forms.Textarea(attrs={'class': 'vSystemTextField'}),
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
        super(DetailsForm, self).__init__(*args, **kwargs)
        self.job_offer = job_offer
        self.index = index
        if not args and not kwargs:  # if nothing is posted
            self.fields['position'].initial = job_offer.position
            self.fields['job_type'].initial = job_offer.job_type_id
            self.fields['qualifications'].initial = [q.pk for q in job_offer.qualifications.all()]
            self.fields['description'].initial = job_offer.description
            if job_offer.published_till:
                self.fields['end_yyyy'].initial = job_offer.published_till.year
                self.fields['end_mm'].initial = job_offer.published_till.month
                self.fields['end_dd'].initial = job_offer.published_till.day

        self.helper = FormHelper()
        self.helper.form_action = "/helper/edit-%(URL_ID_JOB_OFFER)s-profile/%(slug)s/details/" % {
            'URL_ID_JOB_OFFER': URL_ID_JOB_OFFER,
            'slug': self.job_offer.get_secure_id(),
        }
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Details"),
                "position",
                "job_type",
                "qualifications",
                "description",
                layout.MultiField(
                    _("Publish until"),
                    layout.Field(
                        "end_dd",
                        wrapper_class="col-xs-6 col-sm-3 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "end_mm",
                        wrapper_class="col-xs-6 col-sm-5 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "end_yyyy",
                        wrapper_class="col-xs-12 col-sm-4 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html",
                    ),
                ),
                bootstrap.FormActions(
                    layout.Button('cancel', _('Cancel'), css_class="cancel"),
                    layout.Submit('submit', _('Save')),
                    css_class = "button-group form-buttons"
                ),
                css_class="switch on",
            ),
        )

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
            except Exception:
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
    """
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
            "highlight": False,
        },
    )
    """
    offering_institution = forms.CharField(
        required=False,
        label=_("Offering institution"),
        help_text=_("Please enter a letter to display a list of available institutions"),
        widget=forms.Select(choices=[]),
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
        super(ContactForm, self).__init__(*args, **kwargs)
        self.job_offer = job_offer
        self.index = index
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
                
            # add option of choosen selections for autoload fields
            if job_offer.offering_institution_id:
                institution = Institution.objects.get(pk=job_offer.offering_institution_id)
                self.fields['offering_institution'].widget.choices=[(institution.id, institution.title)]   
            
        # add option of choosen selections for autoload fields on error reload of page
        if self.data.get('offering_institution', None):
            institution = Institution.objects.get(pk=self.data.get('offering_institution', None))
            self.fields['offering_institution'].widget.choices=[(institution.id, institution.title)]

        self.helper = FormHelper()
        self.helper.form_action = "/helper/edit-%(URL_ID_JOB_OFFER)s-profile/%(slug)s/contact/" % {
            'URL_ID_JOB_OFFER': URL_ID_JOB_OFFER,
            'slug': self.job_offer.get_secure_id(),
        }
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Contact Data"),
                layout.HTML(
                    string_concat('<dd class="no-label"><h3>', _("Institution/Company"), '</h3></dd>')),
                layout.Field(
                    "offering_institution", 
                    data_load_url="/helper/autocomplete/marketplace/get_institutions/title/get_address_string/",
                    data_load_start="1",
                    data_load_max="20",
                    wrapper_class="institution-select",
                    css_class="autoload"
                ),
                layout.HTML("""{% load i18n %}
                    <dt class="institution-select"> </dt><dd class="institution-select"><a href="javascript:void(0);" class="toggle-visibility" data-toggle-show=".institution-input" data-toggle-hide=".institution-select">{% trans "Not listed? Enter manually" %}</a></dd>
                """),
                layout.Field("offering_institution_title", wrapper_class="institution-input hidden", css_class="toggle-check"),
                layout.HTML("""{% load i18n %}
                    <dt class="institution-input hidden"> </dt><dd class="institution-input hidden"><a href="javascript:void(0);" class="toggle-visibility" data-toggle-show=".institution-select" data-toggle-hide=".institution-input">{% trans "Back to selection" %}</a></dd>
                    <dd class="clearfix"></dd>
                """),

                layout.HTML(
                    string_concat('<dd class="no-label"><h3 class="section">', _("Contact person"), '</h3></dd>')),
                "contact_person_ind",
                "contact_person_name",
                layout.HTML(string_concat('<dd class="no-label"><h3 class="section">', _("Address"), '</h3></dd>')),
                "latitude",  # hidden field
                "longitude",  # hidden field
                "district",  # hidden field
                "street_address",
                "street_address2",
                layout.MultiField(
                    string_concat(_('ZIP'), "*, ", _('City'), "*"),
                    layout.Field(
                        "postal_code",
                        wrapper_class="col-xs-4 col-sm-5 col-md-3 col-lg-3",
                        template="ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "city",
                        wrapper_class="col-xs-8 col-sm-7 col-md-9 col-lg-9",
                        template="ccb_form/multifield.html"
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
                    ' ',
                    layout.Field(
                        "url0_type",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "url0_link",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                ),
                layout.MultiField(
                    ' ',
                    layout.Field(
                        "url1_type",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "url1_link",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                ),
                layout.MultiField(
                    ' ',
                    layout.Field(
                        "url2_type",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "url2_link",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                ),
                layout.HTML(
                    string_concat('<dd class="no-label"><h3 class="section">', _("Instant Messengers"), '</h3></dd>')),
                layout.MultiField(
                    ' ',
                    layout.Field(
                        "im0_type",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "im0_address",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                ),
                layout.MultiField(
                    ' ',
                    layout.Field(
                        "im1_type",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "im1_address",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                ),
                layout.MultiField(
                    ' ',
                    layout.Field(
                        "im2_type",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "im2_address",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                ),
                bootstrap.FormActions(
                    layout.Button('cancel', _('Cancel'), css_class="cancel"),
                    layout.Submit('submit', _('Save')),
                    css_class = "button-group form-buttons"
                ),
                css_class="switch on",
            ),
        )

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
    job_sectors = forms.ModelMultipleChoiceField(
        queryset=get_related_queryset(JobOffer, "job_sectors"),
        required=True,
        widget=forms.CheckboxSelectMultiple,
        help_text="",
        label="",
    )

    tags = TagField(
        label=_("Tags"),
        help_text=_("Separate tags with commas"),
        max_length=200,
        required=False,
        widget=TagAutocomplete,
    )

    categories = ModelMultipleChoiceTreeField(
        label=_("Categories"),
        queryset=get_related_queryset(JobOffer, "categories").filter(level=0),
        required=True,
    )

    def __init__(self, job_offer, index, *args, **kwargs):
        super(CategoriesForm, self).__init__(*args, **kwargs)
        self.job_offer = job_offer
        self.fields['job_sectors'].initial = job_offer.job_sectors.all()
        self.fields['categories'].initial = job_offer.categories.all()
        self.fields['tags'].initial = job_offer.tags

        self.helper = FormHelper()
        self.helper.form_action = "/helper/edit-%(URL_ID_JOB_OFFER)s-profile/%(slug)s/categories/" % {
            'URL_ID_JOB_OFFER': URL_ID_JOB_OFFER,
            'slug': self.job_offer.get_secure_id(),
        }
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Categories"),
                layout.HTML(string_concat('<dt>', _("Job Sectors"), '</dt>')),
                "job_sectors",
                "tags",
                layout.HTML(string_concat('<dt>', _("Categories"), '</dt>')),
                layout.Field("categories", template="ccb_form/custom_widgets/checkboxselectmultipletree.html"),
                bootstrap.FormActions(
                    layout.Button('cancel', _('Cancel'), css_class="cancel"),
                    layout.Submit('submit', _('Save')),
                    css_class = "button-group form-buttons"
                ),
                css_class="switch on",
            ),
        )

    def save(self, *args, **kwargs):
        job_offer = self.job_offer
        cleaned = self.cleaned_data
        job_offer.tags = cleaned['tags']
        job_offer.save()

        job_offer.job_sectors.clear()
        job_offer.job_sectors.add(*cleaned['job_sectors'])

        job_offer.categories.clear()
        job_offer.categories.add(*cleaned['categories'])

        return job_offer

    def get_extra_context(self):
        return {}


profile_forms = {
    'details': DetailsForm,
    'contact': ContactForm,
    'categories': CategoriesForm,
}

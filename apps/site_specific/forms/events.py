# -*- coding: UTF-8 -*-
import datetime

from django.db import models
from django import forms
from django.forms.formsets import formset_factory
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat
from django.utils.dates import MONTHS
from django.forms.formsets import BaseFormSet
from django.conf import settings

from base_libs.forms import dynamicforms
from base_libs.forms.fields import ImageField
from base_libs.utils.misc import get_related_queryset, XChoiceList
from base_libs.forms.fields import AutocompleteField
from base_libs.middleware import get_current_user

from tagging.forms import TagField
from tagging_autocomplete.widgets import TagAutocomplete

from jetson.apps.location.models import Address
from jetson.apps.optionset.models import PhoneType

from ccb.apps.institutions.models import Institution
from ccb.apps.events.models import Event, EventTime
from ccb.apps.site_specific.models import ContextItem
from ccb.apps.events.models import URL_ID_EVENT

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

image_mods = models.get_app("image_mods")

WEEK_DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

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

URL_TYPE_CHOICES = XChoiceList(get_related_queryset(Event, 'url0_type'))
IM_TYPE_CHOICES = XChoiceList(get_related_queryset(Event, 'im0_type'))

EVENT_TYPE_CHOICES = XChoiceList(get_related_queryset(Event, "event_type"))

LOGO_SIZE = getattr(settings, "LOGO_SIZE", (100, 100))
MIN_LOGO_SIZE = getattr(settings, "MIN_LOGO_SIZE", (100, 100))
STR_LOGO_SIZE = "%sx%s" % LOGO_SIZE
STR_MIN_LOGO_SIZE = "%sx%s" % MIN_LOGO_SIZE

# Collect translatable strings
_("Remove from map")
_("Apply to all days")


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
# noinspection PyClassHasNoInit
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
        super(IdentityForm, self).__init__(*args, **kwargs)
        self.event = event
        self.index = index
        if not args and not kwargs:  # if nothing is posted
            self.fields['title_de'].initial = event.title_de
            self.fields['title_en'].initial = event.title_en
            self.fields['event_type'].initial = event.event_type_id

        self.helper = FormHelper()
        self.helper.form_action = "/helper/edit-%(URL_ID_EVENT)s-profile/%(slug)s/identity/" % {
            'URL_ID_EVENT': URL_ID_EVENT,
            'slug': self.event.slug,
        }
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'target': "hidden_iframe",
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Name"),
                "title_en",
                "title_de",
                "event_type",
            ),
            bootstrap.FormActions(
                layout.Button('cancel', _('Cancel')),
                layout.Submit('submit', _('Save')),
            )
        )

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
        super(DescriptionForm, self).__init__(*args, **kwargs)
        self.event = event
        self.index = index
        if not args and not kwargs:  # if nothing is posted
            self.fields['description_en'].initial = event.description_en
            self.fields['description_de'].initial = event.description_de

        self.helper = FormHelper()
        self.helper.form_action = "/helper/edit-%(URL_ID_EVENT)s-profile/%(slug)s/description/" % {
            'URL_ID_EVENT': URL_ID_EVENT,
            'slug': self.event.slug,
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
        event = self.event
        event.description_en = self.cleaned_data['description_en']
        event.description_de = self.cleaned_data['description_de']
        event.save()
        return event

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

    def __init__(self, event, index, *args, **kwargs):
        super(AvatarForm, self).__init__(*args, **kwargs)
        self.event = event
        self.index = index

        self.helper = FormHelper()
        self.helper.form_action = "/helper/edit-%(URL_ID_EVENT)s-profile/%(slug)s/avatar/" % {
            'URL_ID_EVENT': URL_ID_EVENT,
            'slug': self.event.slug,
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
                        <img src="{{ DEFAULT_FORM_LOGO_4_EVENT }}" alt="{{ object.get_title|escape }}"/>
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
        event = self.event
        if "media_file" in self.files:
            media_file = self.files['media_file']
            image_mods.FileManager.save_file_for_object(
                event,
                media_file.name,
                media_file,
                subpath="avatar/"
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
            "highlight": False,
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

    def __init__(self, event, index, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.event = event
        self.index = index
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

        self.helper = FormHelper()
        self.helper.form_action = "/helper/edit-%(URL_ID_EVENT)s-profile/%(slug)s/contact/" % {
            'URL_ID_EVENT': URL_ID_EVENT,
            'slug': self.event.slug,
        }
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'target': "hidden_iframe",
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Institution"),
                "venue",
                "venue_title",
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
                        layout.HTML(_("Fax")),
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
                layout.Submit('submit', _('Save')),
            )
        )

    def clean(self):
        # if venue is selected, the venue_title etc need not to be filled in and vice versa!
        data = super(ContactForm, self).clean()
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
            except Exception:
                return
                # venue_title = venue.get_title()
        # else:
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
            "highlight": False,
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
        super(OrganizerForm, self).__init__(*args, **kwargs)
        self.event = event
        self.index = index
        self.fields['organizing_institution'].initial = event.organizing_institution_id
        self.fields['organizer_title'].initial = event.organizer_title
        self.fields['organizer_url_link'].initial = event.organizer_url_link
        current_user = get_current_user()
        self.fields['is_organized_by_myself'].initial = bool(event.organizing_person)
        if event.creator and current_user != event.creator:
            self.fields['is_organized_by_myself'].label = _(
                "Organized by %s") % event.creator.profile.get_title()

        self.helper = FormHelper()
        self.helper.form_action = "/helper/edit-%(URL_ID_EVENT)s-profile/%(slug)s/organizer/" % {
            'URL_ID_EVENT': URL_ID_EVENT,
            'slug': self.event.slug,
        }
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'target': "hidden_iframe",
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Organizer"),
                "organizing_institution",
                "organizer_title",
                "organizer_url_link",
                "is_organized_by_myself",
            ),
            bootstrap.FormActions(
                layout.Button('cancel', _('Cancel')),
                layout.Submit('submit', _('Save')),
            )
        )

    def save(self):
        event = self.event
        data = self.cleaned_data

        event.organizing_person = (
            None,
            not event.creator and get_current_user().profile or event.creator.profile,
        )[data.get("is_organized_by_myself", False)]
        event.organizing_institution_id = data['organizing_institution'] or None
        event.organizer_title = data.get('organizer_title', None)
        event.organizer_url_link = data.get('organizer_url_link', None)
        event.save()
        return event

    def get_extra_context(self):
        return {}


class AdditionalInfoForm(dynamicforms.Form):
    additional_info_en = forms.CharField(
        label=_("Additional Info English (Max 500 Characters)"),
        required=False,
        widget=forms.Textarea(),
        max_length=500,
    )
    additional_info_de = forms.CharField(
        label=_("Additional Info German (Max 500 Characters)"),
        required=False,
        widget=forms.Textarea(),
        max_length=500,
    )

    related_events = forms.ModelMultipleChoiceField(
        label=_("Related Events"),
        queryset=get_related_queryset(Event, "related_events").all(),
        required=False,
        help_text="",
    )

    def __init__(self, event, index, *args, **kwargs):
        super(AdditionalInfoForm, self).__init__(*args, **kwargs)
        self.event = event
        self.index = index
        self.fields['related_events'].initial = event.related_events.values_list("pk", flat=True)
        self.fields['related_events'].help_text = ""
        self.fields['additional_info_en'].initial = event.additional_info_en
        self.fields['additional_info_de'].initial = event.additional_info_de

        self.helper = FormHelper()
        self.helper.form_action = "/helper/edit-%(URL_ID_EVENT)s-profile/%(slug)s/additional_info/" % {
            'URL_ID_EVENT': URL_ID_EVENT,
            'slug': self.event.slug,
        }
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'target': "hidden_iframe",
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Additional Info"),
                "additional_info_de",
                "additional_info_en",
                "related_events",
            ),
            bootstrap.FormActions(
                layout.Button('cancel', _('Cancel')),
                layout.Submit('submit', _('Save')),
            )
        )

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
    # TODO: ensure that empty form is also provided and implement JavaScripts

    def __init__(self, event, index, *args, **kwargs):
        super(EventTimesForm, self).__init__(*args, **kwargs)
        self.event = event
        self.index = index

        self.helper = FormHelper()
        self.helper.form_action = "/helper/edit-%(URL_ID_EVENT)s-profile/%(slug)s/event_times/" % {
            'URL_ID_EVENT': URL_ID_EVENT,
            'slug': self.event.slug,
        }
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'target': "hidden_iframe",
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Event Times"),
                layout.HTML("""{% load crispy_forms_tags i18n %}
                {{ formsets.event_times.management_form }}
                <div id="event_times">
                    {% for event_time_form in formsets.event_times.forms %}
                        <div class="event_time formset-form tabular-inline">
                            {% crispy event_time_form %}
                        </div>
                    {% endfor %}
                </div>
                <!-- used by javascript -->
                <div id="event_times_empty_form" class="event_time formset-form tabular-inline" style="display: none">
                    {% with formsets.event_times.empty_form as event_time_form %}
                        {% if event_time_form %}
                            {% crispy event_time_form %}
                        {% endif %}
                    {% endwith %}
                </div>
                """),
                css_id="event_times_fieldset",
            ),
            bootstrap.FormActions(
                layout.Button('cancel', _('Cancel')),
                layout.Submit('submit', _('Save')),
            )
        )

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

    has_end_date = forms.BooleanField(
        required=False,
        label=_("Event has an end date")
    )

    def __init__(self, event, index, *args, **kwargs):
        super(EventTimeForm, self).__init__(*args, **kwargs)
        self.event = event
        self.index = index
        kwargs.setdefault('initial', {})
        kwargs['initial']['label'] = kwargs['initial'].get("label_id", None)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = layout.Layout(
            layout.Div(
                "label",
                layout.Row(
                    layout.Div(
                        layout.HTML(_("Start")),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "start_dd",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "start_mm",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "start_yyyy",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        layout.HTML("&nbsp;"),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "start_hh",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "start_ii",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        layout.HTML("&nbsp;"),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        layout.HTML("&nbsp;"),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "is_all_day",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "has_end_date",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        layout.HTML("&nbsp;"),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        layout.HTML(_("End")),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "end_dd",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "end_mm",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "end_yyyy",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        layout.HTML("&nbsp;"),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "end_hh",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "end_ii",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        layout.HTML("&nbsp;"),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
            )
        )

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
        except Exception:
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
            except Exception:
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
        is_valid = super(EventTimeForm, self).is_valid()
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

    def __init__(self, event, index, *args, **kwargs):
        self.event = event
        self.index = index
        kwargs['initial'] = {
            'fees_en': event.fees_en,
            'fees_de': event.fees_de,
        }
        super(FeesOpeningHoursForm, self).__init__(*args, **kwargs)
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

        self.helper = FormHelper()
        self.helper.form_action = "/helper/edit-%(URL_ID_EVENT)s-profile/%(slug)s/fees_opening_hours/" % {
            'URL_ID_EVENT': URL_ID_EVENT,
            'slug': self.event.slug,
        }
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'target': "hidden_iframe",
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Fees"),
                "fees_de",
                "fees_en",
            ),
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
            ),
            bootstrap.FormActions(
                layout.Button('cancel', _('Cancel')),
                layout.Submit('submit', _('Save')),
            )
        )

    def clean(self):

        for week_day in WEEK_DAYS:
            # here, we apply opening hours and do some checks
            if self.cleaned_data.get(week_day + '_open0', None) and \
                    self.cleaned_data.get(week_day + '_open1', None) and \
                    self.cleaned_data.get(week_day + '_close0', None) and \
                    self.cleaned_data.get(week_day + '_close1', None):

                if self.cleaned_data[week_day + '_open1'] < self.cleaned_data[week_day + '_close0']:
                    self._errors[week_day + '_open1'] = [
                        _("An opening time after break must not be before the closing time to break.")]

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

    tags = TagField(
        label=_("Tags"),
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
        super(CategoriesForm, self).__init__(*args, **kwargs)
        self.event = event
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

        self.helper = FormHelper()
        self.helper.form_action = "/helper/edit-%(URL_ID_EVENT)s-profile/%(slug)s/categories/" % {
            'URL_ID_EVENT': URL_ID_EVENT,
            'slug': self.event.slug,
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
                "tags",
            ),
            bootstrap.FormActions(
                layout.Button('cancel', _('Cancel')),
                layout.Submit('submit', _('Save')),
            )
        )

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
                        del (selected_cs[ancestor.id])
                # add current
                selected_cs[item.id] = item
        event.creative_sectors.clear()
        event.creative_sectors.add(*selected_cs.values())

        ContextItem.objects.update_for(event)

        return event

    def get_extra_context(self):
        return {}


profile_forms = {
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
profile_formsets = {
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

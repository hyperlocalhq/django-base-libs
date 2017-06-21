# -*- coding: UTF-8 -*-
import datetime

import os.path
from django import forms
from django.forms.formsets import formset_factory
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat
from django.utils.dates import MONTHS
from django.conf import settings
from django.db import models
from django.utils.encoding import force_unicode
from django.shortcuts import get_object_or_404
from base_libs.forms import dynamicforms
from base_libs.forms.fields import ImageField
from base_libs.middleware import get_current_user
from base_libs.middleware.threadlocals import get_current_language
from base_libs.utils.misc import get_related_queryset, XChoiceList
from base_libs.utils.misc import get_unique_value
from base_libs.utils.betterslugify import better_slugify
from tagging.forms import TagField
from tagging_autocomplete.widgets import TagAutocomplete
from jetson.apps.location.models import Address, LocalityType
from jetson.apps.optionset.models import PhoneType, EmailType, URLType
from jetson.apps.utils.forms import ModelMultipleChoiceTreeField
from jetson.apps.utils.forms import ModelChoiceTreeField
from kb.apps.site_specific.models import ContextItem
from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

image_mods = models.get_app("image_mods")

app = models.get_app("events")
Event, EventType, EventTime, EventTimeLabel, URL_ID_EVENT, URL_ID_EVENTS = (
    app.Event, app.EventType, app.EventTime, app.EventTimeLabel, app.URL_ID_EVENT, app.URL_ID_EVENTS,
)

Institution = models.get_model("institutions", "Institution")

EVENT_TYPE_CHOICES = XChoiceList(get_related_queryset(Event, "event_type"))
ORGANIZING_INSTITUTION_CHOICES = XChoiceList(get_related_queryset(Event, "organizing_institution"))
URL_TYPE_CHOICES = XChoiceList(get_related_queryset(Event, "url0_type"))

YEARS_CHOICES = [("", _("Year"))] + [(i, i) for i in range(2016, 2040)]
MONTHS_CHOICES = [("", _("Month"))] + MONTHS.items()
DAYS_CHOICES = [("", _("Day"))] + [(i, i) for i in range(1, 32)]
HOURS_CHOICES = [("", _("HH"))] + [(i, u"%02d" % i) for i in range(0, 24)]
MINUTES_CHOICES = [("", _("MM"))] + [(i, u"%02d" % i) for i in range(0, 60, 5)]

WEEK_DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

ORGANIZER_CHOICES = [
    (0, _("selected venue is an organizer")),
    (1, _("organized by other institution")),
    (2, _("organized by myself")),
]

# prexixes of fields to guarantee uniqueness
PREFIX_CI = 'CI_'  # Creative Sector aka Creative Industry
PREFIX_BC = 'BC_'  # Context Category aka Business Category
PREFIX_OT = 'OT_'  # Object Type
PREFIX_LT = 'LT_'  # Location Type

LOGO_SIZE = getattr(settings, "LOGO_SIZE", (100, 100))
STR_LOGO_SIZE = "%sx%s" % LOGO_SIZE

# Collect translatable strings
_("Not listed? Enter manually")
_("Address")
_("Change selection")
_("Back to selection")
_("Phone")
_("Fax")
_("URL")
_("Apply to all days")


class MainDataForm(dynamicforms.Form):
    """
    Form for event "main data"
    """
    title_de = forms.CharField(
        label=_("Title (German)"),
        required=True,
    )

    title_en = forms.CharField(
        label=_("Title (English)"),
        required=False,
    )

    event_type = forms.ChoiceField(
        required=True,
        choices=EVENT_TYPE_CHOICES,
        label=_("Event Type"),
    )

    # related_events = forms.ModelMultipleChoiceField(
    #    required=False,
    #   queryset=get_related_queryset(Event, "related_events").only("id", "title", "title_de", "title_en"),
    #    label=_("Related Events"),
    # )

    """
    venue:
    
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
    """
    venue = AutocompleteField(
        required=True,
        label=_("Venue"),
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
    """
    venue = forms.CharField(
        required=True,
        label=_("Venue"),
        help_text=_("Please enter a letter to display a list of available venues"),
        widget=forms.Select(choices=[]),
    )

    venue_title = forms.CharField(
        required=True,
        label=_("Name"),
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

    email0_address = forms.EmailField(
        required=False,
        label=_("Email"),
    )

    url0_link = forms.URLField(
        required=False,
        label=_("Website"),
    )

    organizer_ind = forms.ChoiceField(
        initial=0,
        choices=ORGANIZER_CHOICES,
        widget=forms.RadioSelect()
    )
    """
    organizing_institution = AutocompleteField(
        required=True,
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
    """
    organizing_institution = forms.CharField(
        required=False,
        label=_("Organizing institution"),
        help_text=_("Please enter a letter to display a list of available institutions"),
        widget=forms.Select(choices=[]),
    )

    organizer_title = forms.CharField(
        required=True,
        label=_("Name of Institution"),
    )

    organizer_url_link = forms.URLField(
        required=True,
        label=_("Website"),
    )

    def __init__(self, *args, **kwargs):
        # initial_related_events = kwargs.get(
        #    "initial",
        #    {},
        #    ).get(
        #        "related_events",
        #        (),
        #        )
        # if (
        #    initial_related_events and
        #    isinstance(initial_related_events, (list, tuple, QuerySet))
        #    ):
        #    if isinstance(initial_related_events[0], models.Model):
        #        kwargs['initial']['related_events'] = [
        #            force_unicode(obj.pk)
        #            for obj in initial_related_events
        #            ]
        super(MainDataForm, self).__init__(*args, **kwargs)

        # add option of already choosen selections on multistep forms for autoload fields
        initial = kwargs.get("initial", None)
        if initial:
            if initial.get('venue', None):
                institution = Institution.objects.get(pk=initial.get('venue', None))
                self.fields['venue'].widget.choices = [(institution.id, institution.title)]

            if initial.get('organizing_institution', None):
                institution = Institution.objects.get(pk=initial.get('organizing_institution', None))
                self.fields['organizing_institution'].widget.choices = [(institution.id, institution.title)]


        # add option of choosen selections for autoload fields on error reload of page
        if self.data.get('venue', None):
            institution = Institution.objects.get(pk=self.data.get('venue', None))
            self.fields['venue'].widget.choices = [(institution.id, institution.title)]

        if self.data.get('organizing_institution', None):
            institution = Institution.objects.get(pk=self.data.get('organizing_institution', None))
            self.fields['organizing_institution'].widget.choices = [(institution.id, institution.title)]

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Title"),
                "title_de",
                "title_en",
                "event_type",
            ),
            layout.Fieldset(
                _("Period"),
                layout.HTML("""{% load crispy_forms_tags i18n %}
                {{ formsets.event_times.management_form }}
                <div id="event_times" class="dynamic-entries">
                    {% for event_time_form in formsets.event_times.forms %}
                        {% crispy event_time_form "kb_form" %}
                    {% endfor %}
                </div>
                <!-- used by javascript -->
                <div id="event_times_empty" style="display: none" class="dont-add-form-functionality">
                    {% with formsets.event_times.empty_form as event_time_form %}
                        {% if event_time_form %}
                            {% crispy event_time_form "kb_form" %}
                        {% endif %}
                    {% endwith %}
                </div>
                """),
                css_class="event-times",
            ),
            layout.Fieldset(
                _("Venue"),
                layout.Field(
                    "venue",
                    data_load_url="/%s/helper/autocomplete/events/get_venues/title/get_address_string/" % get_current_language(),
                    data_load_start="1",
                    data_load_max="20",
                    wrapper_class="venue-select",
                    css_class="autoload"
                ),
                layout.HTML("""{% load i18n %}
                    <dt class="venue-select"> </dt><dd class="venue-select"><a href="javascript:void(0);" class="toggle-visibility" data-toggle-show=".venue-input" data-toggle-hide=".venue-select">{% trans "Not listed? Enter manually" %}</a></dd>
                """),
                layout.Field("venue_title", wrapper_class="venue-input hidden", css_class="toggle-check"),
                layout.HTML("""{% load i18n %}
                    <dt class="venue-input hidden"> </dt><dd class="venue-input hidden"><a href="javascript:void(0);" class="toggle-visibility" data-toggle-show=".venue-select" data-toggle-hide=".venue-input">{% trans "Back to selection" %}</a></dd>
                """),
            ),
            # layout.Fieldset(
            #    _("Venue"),
            # TODO: decide how to rework the markup for bootstrap
            #    layout.HTML("""{% load i18n %}
            #        <ul class="def_list">
            #            <li class="add_manually_list_label">
            #                <label>
            #                    {% trans "Address" %}:
            #                </label>
            #            </li>
            #            <li id="id_venue_address_title" class="add_manually_list">
            #                <strong></strong>
            #            </li>
            #            <li id="id_venue_address_street_address" class="add_manually_list">
            #                <strong></strong>
            #            </li>
            #            <li id="id_venue_address_street_address2" class="add_manually_list">
            #                <strong></strong>
            #            </li>
            #            <li id="id_venue_address_postal_code" class="add_manually_list">
            #                <strong></strong>
            #            </li>
            #            <li id="id_venue_address_city" class="add_manually_list">
            #                <strong></strong>
            #            </li>
            #            <li id="id_venue_address_country" class="add_manually_list">
            #                <strong></strong>
            #            </li>
            #            <li class="add_manually_list">
            #                <a id="id_venue_change" href="#">
            #                    {% trans "Change selection" %}
            #                </a>
            #            </li>
            #        </ul>
            #    """),
            #    css_id="id_block_venue_address_display",
            # ),
            layout.Fieldset(
                _("Address"),
                "street_address",
                "street_address2",
                layout.MultiField(
                    string_concat(_('ZIP'), "*, ", _('City'), "*"),
                    layout.Field(
                        "postal_code",
                        wrapper_class="col-xs-4 col-sm-5 col-md-3 col-lg-3",
                        template="kb_form/multifield.html"
                    ),
                    layout.Field(
                        "city",
                        wrapper_class="col-xs-8 col-sm-7 col-md-9 col-lg-9",
                        template="kb_form/multifield.html"
                    )
                ),
                "country",
                "latitude",  # hidden field
                "longitude",  # hidden field
                layout.HTML("""{% include "kb_form/custom_widgets/editable_map.html" %}"""),
            ),
            layout.Fieldset(
                _("Information about this Event"),
                layout.MultiField(
                    _("Phone"),
                    layout.Field(
                        "phone_country",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template="kb_form/multifield.html"
                    ),
                    layout.Field(
                        "phone_area",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template="kb_form/multifield.html"
                    ),
                    layout.Field(
                        "phone_number",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template="kb_form/multifield.html"
                    ),
                    css_class="show-labels"
                ),
                layout.MultiField(
                    _("Fax"),
                    layout.Field(
                        "fax_country",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template="kb_form/multifield.html"
                    ),
                    layout.Field(
                        "fax_area",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template="kb_form/multifield.html"
                    ),
                    layout.Field(
                        "fax_number",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template="kb_form/multifield.html"
                    ),
                    css_class="show-labels"
                ),
                css_id="id_block_venue_contact_input",
            ),
            layout.Fieldset(
                _("Organizer"),
                "organizer_ind",
            ),
            layout.Fieldset(
                _("Organizing institution"),
                layout.Field(
                    "organizing_institution",
                    data_load_url="/%s/helper/autocomplete/events/get_organizing_institutions/title/get_address_string/" % get_current_language(),
                    data_load_start="1",
                    data_load_max="20",
                    wrapper_class="institution-select",
                    css_class="autoload"
                ),
                layout.HTML("""{% load i18n %}
                    <dt class="institution-select"> </dt><dd class="institution-select"><a href="javascript:void(0);" class="toggle-visibility" data-toggle-show=".institution-input" data-toggle-hide=".institution-select">{% trans "Not listed? Enter manually" %}</a></dd>
                """),

                layout.Field("organizer_title", wrapper_class="institution-input hidden", css_class="toggle-check"),
                layout.Field("organizer_url_link", wrapper_class="institution-input hidden"),
                layout.HTML("""{% load i18n %}
                    <dt class="institution-input hidden"> </dt><dd class="institution-input hidden"><a href="javascript:void(0);" class="toggle-visibility" data-toggle-show=".institution-select" data-toggle-hide=".institution-input">{% trans "Back to selection" %}</a></dd>
                """),
                css_class="radio-toggle",
                data_radio_name="organizer_ind",
                data_radio_index="1",
            ),
            # layout.Fieldset(
            #    _("Organizer address"),
            #    layout.HTML("""{% load i18n %}
            #        <ul class="address def_list">
            #            <li class="add_manually_list_label">
            #                <label>{% trans "Address" %}:</label>
            #            </li>
            #            <li id="id_org_inst_address_title" class="add_manually_list">
            #                <strong></strong>
            #            </li>
            #            <li id="id_org_inst_address_street_address" class="add_manually_list">
            #                <strong></strong>
            #            </li>
            #            <li id="id_org_inst_address_street_address2" class="add_manually_list">
            #                <strong></strong>
            #            </li>
            #            <li id="id_org_inst_address_postal_code" class="add_manually_list">
            #                <strong></strong>
            #            </li>
            #            <li id="id_org_inst_address_city" class="add_manually_list">
            #                <strong></strong>
            #            </li>
            #            <li id="id_org_inst_address_country" class="add_manually_list">
            #                <strong></strong>
            #            </li>
            #        </ul>
            #        <ul class="def_list" id="id_org_inst_phone_container">
            #            <li class="add_manually_list_label">
            #                <label>
            #                    {% trans "Phone" %}:
            #                </label>
            #            </li>
            #            <li id="id_org_inst_phone" class="add_manually_list">
            #                <strong></strong>
            #            </li>
            #        </ul>
            #        <ul class="def_list" id="id_org_inst_fax_container">
            #            <li class="add_manually_list_label">
            #                <label>
            #                    {% trans "Fax" %}:
            #                </label>
            #            </li>
            #            <li id="id_org_inst_fax" class="add_manually_list">
            #                <strong></strong>
            #            </li>
            #        </ul>
            #        <ul class="def_list" id="id_org_inst_url0_link_container">
            #            <li class="add_manually_list_label">
            #                <label>
            #                    {% trans "URL" %}:
            #                </label>
            #            </li>
            #            <li id="id_org_inst_url0_link" class="add_manually_list">
            #                <strong></strong>
            #            </li>
            #        </ul>
            #        <p>
            #            <a id="id_org_inst_change" href="#">{% trans "Change selection" %}</a>
            #        </p>
            #    """),
            # ),
            bootstrap.FormActions(
                layout.HTML("""{% include "utils/step_buttons_reg.html" %}"""),
            )
        )

    def clean(self):
        """"
        Below, there is some (simple and complex) validation logic:
        for example, some fields are not required, if a venue is selected.
        the "_errors" stuff there is a bit of a hack, but there seems 
        to be no other possibility to simulate the "required" attribute after
        field validation, because the fields clean method is called
        before and there is some "field required error" raised, which
        we have to eliminate manually. We set all the fields "required", even
        if you can enter alternative data. (You have this nice "*" attached
        to the label of the field indicating that you must fill in!
        (TODO Aidas, maybe you know something better!)
        """

        # if venue is selected, the venue_title etc need not to be filled in and vice versa!
        if self.cleaned_data.get('venue_title', None):
            if 'venue' in self._errors:
                del self._errors['venue']
        else:
            if self.cleaned_data.get('venue', None):
                for field_name in [
                    'venue_title',
                    'street_address',
                    'postal_code',
                    'city',
                    'country',
                ]:
                    if self._errors.get(field_name, False):
                        del self._errors[field_name]

        # organizing institution logic
        organizer_ind = int(self.cleaned_data['organizer_ind'])
        if organizer_ind == 1:
            if self.cleaned_data.get('organizer_title', "") != "":
                if self._errors.get('organizing_institution', False):
                    del self._errors['organizing_institution']
            else:
                if self.cleaned_data.get('organizing_institution', "") != "":
                    for field_name in [
                        'organizer_title',
                        'organizer_url_link',
                    ]:
                        if self._errors.get(field_name, False):
                            del self._errors[field_name]
        else:
            for field_name in [
                'organizing_institution',
                'organizer_title',
                'organizer_url_link',
            ]:
                if self._errors.get(field_name, False):
                    del self._errors[field_name]

        return self.cleaned_data


class EventTimeForm(dynamicforms.Form):
    """
    Form for event "main data"
    """

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

    def __init__(self, *args, **kwargs):
        initial_label = kwargs.get("initial", {}).get("label", None)
        if initial_label and isinstance(initial_label, models.Model):
            kwargs['initial']['label'] = force_unicode(initial_label.pk)
        super(EventTimeForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = layout.Layout(
            layout.Div(
                "label",
                layout.MultiField(
                    _("Start"),
                    layout.Field(
                        "start_dd",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template="kb_form/multifield.html",
                        placeholder=_('Day')
                    ),
                    layout.Field(
                        "start_mm",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template="kb_form/multifield.html",
                        placeholder=_('Month')
                    ),
                    layout.Field(
                        "start_yyyy",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template="kb_form/multifield.html",
                        placeholder=_('Year')
                    ),
                ),
                layout.MultiField(
                    " ",
                    layout.Field(
                        "start_hh",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template="kb_form/multifield.html",
                        placeholder=_('Hour')
                    ),
                    layout.Field(
                        "start_ii",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template="kb_form/multifield.html",
                        placeholder=_("Minute")
                    ),
                    css_class="hours"
                ),
                layout.MultiField(
                    " ",
                    layout.Field(
                        "is_all_day",
                        wrapper_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                        template="kb_form/multifield.html",
                        css_class="is-all-day"
                    ),
                    layout.Field(
                        "has_end_date",
                        wrapper_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                        template="kb_form/multifield.html"
                    ),
                ),
                layout.MultiField(
                    _("End"),
                    layout.Field(
                        "end_dd",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template="kb_form/multifield.html",
                        placeholder=_("Day")
                    ),
                    layout.Field(
                        "end_mm",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template="kb_form/multifield.html",
                        placeholder=_("Month")
                    ),
                    layout.Field(
                        "end_yyyy",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template="kb_form/multifield.html",
                        placeholder=_("Year")
                    ),
                ),
                layout.MultiField(
                    " ",
                    layout.Field(
                        "end_hh",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template="kb_form/multifield.html",
                        placeholder=_("Hour")
                    ),
                    layout.Field(
                        "end_ii",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template="kb_form/multifield.html",
                        placeholder=_("Minute")
                    ),
                    css_class="hours"
                ),

                css_class="entry"
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


class ProfileForm(dynamicforms.Form):
    """
    Form for event profile
    """
    description_en = forms.CharField(
        label=_("Description (English)"),
        required=False,
        widget=forms.Textarea(attrs={'class': 'vSystemTextField'}),
    )
    description_de = forms.CharField(
        label=_("Description (German)"),
        required=False,
        widget=forms.Textarea(attrs={'class': 'vSystemTextField'}),
    )

    image = ImageField(
        label=_("Profile photo"),
        help_text=_(
            "You can upload GIF, JPG, PNG, TIFF, and BMP images. The minimal dimensions are %s px.") % STR_LOGO_SIZE,
        required=False,
        min_dimensions=LOGO_SIZE,
    )

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Description"),
                "description_de",
                "description_en",
            ),
            layout.Fieldset(
                _("Photo"),
                layout.HTML("""{% load image_modifications %}
                    {% if form_step_data.step_event_profile.image %}
                        <dt>""" + (_("Image") + "") + """</dt><dd><img class="avatar" src="/{{ LANGUAGE_CODE }}/helper/tmpimage/{{ form_step_data.step_event_profile.image.tmp_filename }}/{{ LOGO_PREVIEW_SIZE }}/" alt="{{ object.get_title|escape }}"/></dd>
                    {% else %}
                        <dt>""" + (_("Image") + "") + """</dt><dd><img src="{{ STATIC_URL }}site/img/placeholder/event.png" alt="{{ object.get_title|escape }}"/>
</dd>
                    {% endif %}
                """),
                "image",
            ),
            bootstrap.FormActions(
                layout.HTML("""{% include "utils/step_buttons_reg.html" %}"""),
            )
        )


class FeesForm(dynamicforms.Form):
    """
    Form for event fees and opening ours
    """

    fees_en = forms.CharField(
        label=_('Fees (English)'),
        required=False,
        widget=forms.Textarea,
    )
    fees_de = forms.CharField(
        label=_('Fees (German)'),
        required=False,
        widget=forms.Textarea,
    )

    show_breaks = forms.BooleanField(
        required=False,
        label=_("Morning/Afternoon"),
        initial=False,
    )

    is_appointment_based = forms.BooleanField(
        label=_("Visiting by Appointment"),
        required=False,
        initial=False,
    )

    mon_open0 = forms.TimeField(
        label=_("opens"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )
    mon_close0 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )
    mon_open1 = forms.TimeField(
        label=_("opens again"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )
    mon_close1 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )
    mon_is_closed = forms.BooleanField(
        label=_("Closed"),
        required=False,
        initial=False,
    )

    tue_open0 = forms.TimeField(
        label=_("opens"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )
    tue_close0 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )
    tue_open1 = forms.TimeField(
        label=_("opens again"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )
    tue_close1 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )
    tue_is_closed = forms.BooleanField(
        label=_("Closed"),
        required=False,
        initial=False,
    )

    wed_open0 = forms.TimeField(
        label=_("opens"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )
    wed_close0 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )
    wed_open1 = forms.TimeField(
        label=_("opens again"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )
    wed_close1 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )
    wed_is_closed = forms.BooleanField(
        label=_("Closed"),
        required=False,
        initial=False,
    )

    thu_open0 = forms.TimeField(
        label=_("opens"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )
    thu_close0 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )
    thu_open1 = forms.TimeField(
        label=_("opens again"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )
    thu_close1 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )
    thu_is_closed = forms.BooleanField(
        label=_("Closed"),
        required=False,
        initial=False,
    )

    fri_open0 = forms.TimeField(
        label=_("opens"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )
    fri_close0 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )
    fri_open1 = forms.TimeField(
        label=_("opens again"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )
    fri_close1 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )
    fri_is_closed = forms.BooleanField(
        label=_("Closed"),
        required=False,
        initial=False,
    )

    sat_open0 = forms.TimeField(
        label=_("opens"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )
    sat_close0 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )
    sat_open1 = forms.TimeField(
        label=_("opens again"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )
    sat_close1 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )
    sat_is_closed = forms.BooleanField(
        label=_("Closed"),
        required=False,
        initial=False,
    )

    sun_open0 = forms.TimeField(
        label=_("opens"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )
    sun_close0 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )
    sun_open1 = forms.TimeField(
        label=_("opens again"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )
    sun_close1 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
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

    def __init__(self, *args, **kwargs):
        super(FeesForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Fees"),
                "fees_de",
                "fees_en",
            ),
            layout.Fieldset(
                string_concat(_("Opening Time"), " - ", _("Closing Time")),
                layout.MultiField(
                    _("Monday"),
                    layout.Field(
                        "mon_open0",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3 closed_mon",
                        template="kb_form/multifield.html"
                    ),
                    layout.Field(
                        "mon_close0",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3 closed_mon",
                        template="kb_form/multifield.html"
                    ),
                    layout.Field(
                        "mon_is_closed",
                        wrapper_class="col-xs-12 col-sm-12 col-md-6 col-lg-6",
                        template="kb_form/multifield.html",
                        css_class="closed mon"
                    ),
                    css_class="show-labels"
                ),
                layout.MultiField(
                    ' ',
                    layout.Field(
                        "mon_open1",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3",
                        template="kb_form/multifield.html"
                    ),
                    layout.Field(
                        "mon_close1",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3",
                        template="kb_form/multifield.html"
                    ),
                    css_class="show-labels break closed_mon"
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
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3 closed_tue",
                        template="kb_form/multifield.html"
                    ),
                    layout.Field(
                        "tue_close0",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3 closed_tue",
                        template="kb_form/multifield.html"
                    ),
                    layout.Field(
                        "tue_is_closed",
                        wrapper_class="col-xs-12 col-sm-12 col-md-6 col-lg-6",
                        template="kb_form/multifield.html",
                        css_class="closed tue"
                    ),
                    css_class="show-labels"
                ),
                layout.MultiField(
                    ' ',
                    layout.Field(
                        "tue_open1",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3",
                        template="kb_form/multifield.html"
                    ),
                    layout.Field(
                        "tue_close1",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3",
                        template="kb_form/multifield.html"
                    ),
                    css_class="show-labels break closed_tue"
                ),

                layout.HTML("""<dd class="clearfix">&nbsp;</dd>"""),

                layout.MultiField(
                    _("Wednesday"),
                    layout.Field(
                        "wed_open0",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3 closed_wed",
                        template="kb_form/multifield.html"
                    ),
                    layout.Field(
                        "wed_close0",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3 closed_wed",
                        template="kb_form/multifield.html"
                    ),
                    layout.Field(
                        "wed_is_closed",
                        wrapper_class="col-xs-12 col-sm-12 col-md-6 col-lg-6",
                        template="kb_form/multifield.html",
                        css_class="closed wed"
                    ),
                    css_class="show-labels"
                ),
                layout.MultiField(
                    ' ',
                    layout.Field(
                        "wed_open1",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3",
                        template="kb_form/multifield.html"
                    ),
                    layout.Field(
                        "wed_close1",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3",
                        template="kb_form/multifield.html"
                    ),
                    css_class="show-labels break closed_wed"
                ),

                layout.HTML("""<dd class="clearfix">&nbsp;</dd>"""),

                layout.MultiField(
                    _("Thursday"),
                    layout.Field(
                        "thu_open0",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3 closed_thu",
                        template="kb_form/multifield.html"
                    ),
                    layout.Field(
                        "thu_close0",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3 closed_thu",
                        template="kb_form/multifield.html"
                    ),
                    layout.Field(
                        "thu_is_closed",
                        wrapper_class="col-xs-12 col-sm-12 col-md-6 col-lg-6",
                        template="kb_form/multifield.html",
                        css_class="closed thu"
                    ),
                    css_class="show-labels"
                ),
                layout.MultiField(
                    ' ',
                    layout.Field(
                        "thu_open1",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3",
                        template="kb_form/multifield.html"
                    ),
                    layout.Field(
                        "thu_close1",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3",
                        template="kb_form/multifield.html"
                    ),
                    css_class="show-labels break closed_thu"
                ),

                layout.HTML("""<dd class="clearfix">&nbsp;</dd>"""),

                layout.MultiField(
                    _("Friday"),
                    layout.Field(
                        "fri_open0",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3 closed_fri",
                        template="kb_form/multifield.html"
                    ),
                    layout.Field(
                        "fri_close0",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3 closed_fri",
                        template="kb_form/multifield.html"
                    ),
                    layout.Field(
                        "fri_is_closed",
                        wrapper_class="col-xs-12 col-sm-12 col-md-6 col-lg-6",
                        template="kb_form/multifield.html",
                        css_class="closed fri"
                    ),
                    css_class="show-labels"
                ),
                layout.MultiField(
                    ' ',
                    layout.Field(
                        "fri_open1",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3",
                        template="kb_form/multifield.html"
                    ),
                    layout.Field(
                        "fri_close1",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3",
                        template="kb_form/multifield.html"
                    ),
                    css_class="show-labels break closed_fri"
                ),

                layout.HTML("""<dd class="clearfix">&nbsp;</dd>"""),

                layout.MultiField(
                    _("Saturday"),
                    layout.Field(
                        "sat_open0",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3 closed_sat",
                        template="kb_form/multifield.html"
                    ),
                    layout.Field(
                        "sat_close0",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3 closed_sat",
                        template="kb_form/multifield.html"
                    ),
                    layout.Field(
                        "sat_is_closed",
                        wrapper_class="col-xs-12 col-sm-12 col-md-6 col-lg-6",
                        template="kb_form/multifield.html",
                        css_class="closed sat"
                    ),
                    css_class="show-labels"
                ),
                layout.MultiField(
                    ' ',
                    layout.Field(
                        "sat_open1",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3",
                        template="kb_form/multifield.html"
                    ),
                    layout.Field(
                        "sat_close1",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3",
                        template="kb_form/multifield.html"
                    ),
                    css_class="show-labels break closed_sat"
                ),

                layout.HTML("""<dd class="clearfix">&nbsp;</dd>"""),

                layout.MultiField(
                    _("Sunday"),
                    layout.Field(
                        "sun_open0",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3 closed_sun",
                        template="kb_form/multifield.html"
                    ),
                    layout.Field(
                        "sun_close0",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3 closed_sun",
                        template="kb_form/multifield.html"
                    ),
                    layout.Field(
                        "sun_is_closed",
                        wrapper_class="col-xs-12 col-sm-12 col-md-6 col-lg-6",
                        template="kb_form/multifield.html",
                        css_class="closed sun"
                    ),
                    css_class="show-labels"
                ),
                layout.MultiField(
                    ' ',
                    layout.Field(
                        "sun_open1",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3",
                        template="kb_form/multifield.html"
                    ),
                    layout.Field(
                        "sun_close1",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3",
                        template="kb_form/multifield.html"
                    ),
                    css_class="show-labels break closed_sun"
                ),

                layout.HTML("""<dd class="clearfix">&nbsp;</dd>"""),

                "exceptions_de",
                "exceptions_en",
                "is_appointment_based",

                css_class="opening-hours"
            ),
            bootstrap.FormActions(
                layout.HTML("""{% include "utils/step_buttons_reg.html" %}"""),
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


class CategoriesForm(dynamicforms.Form):
    categories = ModelMultipleChoiceTreeField(
        label=_("Categories"),
        queryset=get_related_queryset(Event, "categories").filter(level=0),
        required=True,
    )

    tags = TagField(
        label=_("Tags"),
        help_text=_("Separate tags with commas."),
        max_length=200,
        required=False,
        widget=TagAutocomplete,
    )

    def __init__(self, *args, **kwargs):
        super(CategoriesForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Categories"),
                layout.Field("categories", template="kb_form/custom_widgets/checkboxselectmultipletree.html"),
                css_class="no-label"
            ),
            layout.Fieldset(
                _("Tags"),
                "tags",
            ),
            bootstrap.FormActions(
                layout.HTML("""{% include "utils/step_buttons_reg.html" %}"""),
            )
        )


def step_main_data_initial_data(request, **kwargs):
    institution_slug = request.GET.get('institution', None)
    initial_data = {}
    if institution_slug:
        institution = get_object_or_404(Institution, slug=institution_slug)
        initial_data['venue'] = institution.pk
        initial_data['organizing_institution'] = institution.pk
    return initial_data


def submit_step(current_step, form_steps, form_step_data):
    return form_step_data


def save_data(form_steps, form_step_data):
    step_main_data = form_step_data['step_main_data']
    step_event_profile = form_step_data['step_event_profile']
    step_fees_opening_hours = form_step_data['step_fees_opening_hours']
    step_categories = form_step_data['step_categories']
    step_confirm_data = form_step_data['step_confirm_data']
    user = get_current_user()

    # venue data
    venue = None
    venue_title = ''
    if step_main_data.get('venue', None):
        venue = Institution.objects.get(pk=step_main_data['venue'])
        # venue_title = venue.get_title()
    else:
        venue_title = step_main_data.get('venue_title', None)

        venue = Institution(
            title=venue_title,
            slug=get_unique_value(Institution, better_slugify(venue_title).replace("-", "_"), separator="_"),
        )
        venue.status = "event_location"
        venue.save()
        institutional_contact = venue.institutionalcontact_set.create(
            is_primary=True,
            is_temporary=False,
            phone0_type=PhoneType.objects.get(slug='phone'),
            phone0_country=step_main_data.get('phone_country', ''),
            phone0_area=step_main_data.get('phone_area', ''),
            phone0_number=step_main_data.get('phone_number', ''),
            phone1_type=PhoneType.objects.get(slug='fax'),
            phone1_country=step_main_data.get('fax_country', ''),
            phone1_area=step_main_data.get('fax_area', ''),
            phone1_number=step_main_data.get('fax_number', ''),
            url0_type_id=step_main_data.get('url0_type', None),
            url0_link=step_main_data.get('url0_link', ''),
        )
        Address.objects.set_for(
            institutional_contact,
            "postal_address",
            country=step_main_data.get('country', None),
            city=step_main_data.get('city', None),
            street_address=step_main_data.get('street_address', None),
            street_address2=step_main_data.get('street_address2', None),
            postal_code=step_main_data.get('postal_code', None),
            latitude=step_main_data.get('latitude', None),
            longitude=step_main_data.get('longitude', None),
        )
        '''
        if hasattr(venue, "create_default_group"):
            person_group = venue.create_default_group()
            person_group.content_object = venue
            person_group.save()
            membership = person_group.groupmembership_set.create(
                user = user,
                role = "owners",
                inviter = user,
                confirmer = user,
                is_accepted = True,
                )
        '''

    # organizing institution
    organizing_institution = None
    organizing_person = None
    organizer_title = None
    organizer_url_link = None
    organizer_ind = int(step_main_data.get('organizer_ind', 0))
    # venue is organizer
    if organizer_ind == 0:
        if venue:
            organizing_institution = venue
        """
        TODO As Reinhard decided, that we do not create any institutions
        implicitly, so, if no venue is selcted (but only a venue title with
        poatal_address is entered, no institution is created).
        """
        # I am the organizer!
    elif organizer_ind == 2:
        organizing_person = get_current_user().profile
    # orgnaizer is selected separately
    else:
        if step_main_data.get('organizing_institution', None):
            organizing_institution = Institution.objects.get(
                pk=step_main_data['organizing_institution'],
            )
        else:
            organizer_title = step_main_data.get('organizer_title', None)
            organizer_url_link = step_main_data.get('organizer_url_link', None)

    event = Event()

    event.title_en = step_main_data.get('title_en', None)
    event.title_de = step_main_data.get('title_de', None)
    if not event.title_en:
        event.title_en = event.title_de

    event.description_en = step_event_profile.get('description_en', None)
    event.description_de = step_event_profile.get('description_de', None)

    event.event_type = EventType.objects.get(
        pk=step_main_data.get('event_type', None),
    )

    event.venue_title = venue_title
    event.venue = venue
    event.organizing_institution = organizing_institution
    event.organizing_person = organizing_person
    event.organizer_title = organizer_title
    event.organizer_url_link = organizer_url_link

    event.additional_info_en = ""  # TODO we do not have that in the mockups
    event.additional_info_de = ""  # TODO we do not have that in the mockups

    event.fees_en = step_fees_opening_hours.get('fees_en', '')
    event.fees_de = step_fees_opening_hours.get('fees_de', '')

    event.is_registration_required = False  # TODO we do not have that in the mockups

    event.phone0_type = PhoneType.objects.get(slug='phone')
    event.phone0_country = step_main_data.get('phone_country', '')
    event.phone0_area = step_main_data.get('phone_area', '')
    event.phone0_number = step_main_data.get('phone_number', '')

    event.phone1_type = PhoneType.objects.get(slug='fax')
    event.phone1_country = step_main_data.get('fax_country', '')
    event.phone1_area = step_main_data.get('fax_area', '')
    event.phone1_number = step_main_data.get('fax_number', '')

    event.email0_type = EmailType.objects.get(slug='email')
    event.email0_address = step_main_data.get('email0_address', '')

    event.url0_type = URLType.objects.get(slug='web')
    event.url0_link = step_main_data.get('url0_link', '')

    for f in ("open", "break_close", "break_open", "close"):
        for d in ("mon", "tue", "wed", "thu", "fri", "sat", "sun"):
            setattr(
                event,
                "%s_%s" % (d, f),
                step_fees_opening_hours.get('%s_%s' % (d, f), None)
            )

    event.exceptions_en = step_fees_opening_hours.get('exceptions_en', '')
    event.exceptions_de = step_fees_opening_hours.get('exceptions_de', '')
    event.is_appointment_based = step_fees_opening_hours.get('is_appointment_based', False)

    event.tags = step_categories.get('tags', '')

    # TODO should we really publish the event immediately?
    event.status = "published"

    event.save()

    if venue and venue.get_contacts():
        Address.objects.set_for(
            event,
            "postal_address",
            **venue.get_contacts()[0].postal_address.get_dict()
        )
    else:
        Address.objects.set_for(
            event,
            "postal_address",
            country=step_main_data.get('country', None),
            city=step_main_data.get('city', None),
            street_address=step_main_data.get('street_address', None),
            street_address2=step_main_data.get('street_address2', None),
            postal_code=step_main_data.get('postal_code', None),
            latitude=step_main_data.get('latitude', None),
            longitude=step_main_data.get('longitude', None),
        )

    # creative sectors and context categories
    cleaned = step_categories
    event.categories.add(*cleaned['categories'])

    media_file = step_event_profile.get('image', '')
    if media_file:
        tmp_path = os.path.join(settings.PATH_TMP, media_file['tmp_filename'])
        f = open(tmp_path, 'r')
        filename = tmp_path.rsplit("/", 1)[1]
        image_mods.FileManager.save_file_for_object(
            event,
            filename,
            f.read(),
            subpath="avatar/"
        )
        f.close()

    # save again without triggering any signals
    event.save_base(raw=True)

    # for ev in step_main_data.get('related_events', ()):
    #    event.related_events.add(ev)

    for time_data in step_main_data['sets'].get("event_times", ()):
        time = EventTime(event=event)
        label_id = time_data.get('label', None)
        if label_id:
            time.label = EventTimeLabel.objects.get(pk=label_id)

        time.start_yyyy = time_data.get('start_yyyy', None)
        time.start_mm = time_data.get('start_mm', None)
        time.start_dd = time_data.get('start_dd', None)
        time.start_hh = time_data.get('start_hh', None)
        if time.start_hh:
            start_ii_default = 0
        else:
            start_ii_default = None
        time.start_ii = time_data.get('start_ii', start_ii_default)

        time.end_yyyy = time_data.get('end_yyyy', None)
        time.end_mm = time_data.get('end_mm', None)
        time.end_dd = time_data.get('end_dd', None)
        time.end_hh = time_data.get('end_hh', None)
        if time.end_hh:
            end_ii_default = 0
        else:
            end_ii_default = None
        time.end_ii = time_data.get('end_ii', end_ii_default)
        time.is_all_day = time_data.get('is_all_day', False)

        time.save()

    form_steps['success_url'] = event.get_url_path()

    return form_step_data


ADD_EVENT_FORM_STEPS = {
    'step_main_data': {
        'title': _("main data"),
        'template': "events/add_event_main_data.html",
        'form': MainDataForm,
        'formsets': {
            'event_times': formset_factory(
                EventTimeForm,
                can_delete=True,
                min_num=1,
                extra=0,
            ),
        },
        'initial_data': step_main_data_initial_data,
    },
    'step_event_profile': {
        'title': _("event profile"),
        'template': "events/add_event_profile.html",
        'form': ProfileForm,
    },
    'step_fees_opening_hours': {
        'title': _("fees and opening hours"),
        'template': "events/add_event_fees.html",
        'form': FeesForm,
    },
    'step_categories': {
        'title': _("categories"),
        'template': "events/add_event_categories.html",
        'form': CategoriesForm,
    },
    'step_confirm_data': {
        'title': _("confirm data"),
        'template': "events/add_event_confirm.html",
        'form': forms.Form,  # dummy form
    },
    'onsubmit': submit_step,
    'onsave': save_data,
    'name': 'add_event',
    'success_url': "/%s/" % URL_ID_EVENTS,
    'default_path': [
        'step_main_data',
        'step_event_profile',
        'step_fees_opening_hours',
        'step_categories',
        'step_confirm_data',
    ],
}


class EventSearchForm(dynamicforms.Form):
    category = ModelChoiceTreeField(
        empty_label=_("All"),
        label=_("Category"),
        required=False,
        queryset=get_related_queryset(ContextItem, "categories").filter(level=0),
    )
    event_type = ModelChoiceTreeField(
        empty_label=_("All"),
        label=_("Event Type"),
        required=False,
        queryset=get_related_queryset(Event, "event_type"),
    )
    locality_type = ModelChoiceTreeField(
        empty_label=_("All"),
        label=_("Location Type"),
        required=False,
        queryset=LocalityType.objects.order_by("tree_id", "lft"),
    )
    # keywords = forms.CharField(
    #     label=_("Keyword(s)"),
    #     required=False,
    # )
    is_featured = forms.BooleanField(
        label=_("Featured events only"),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(EventSearchForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "GET"
        self.helper.form_id = "filter_form"
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Filter"),
                layout.Field("category", template="kb_form/custom_widgets/filter_field.html"),
                layout.Field("event_type", template="kb_form/custom_widgets/filter_field.html"),
                layout.Field("locality_type", template="kb_form/custom_widgets/locality_type_filter_field.html"),
                template="kb_form/custom_widgets/filter.html"
            ),
            # "keywords",
            "is_featured",
            bootstrap.FormActions(
                layout.Submit('submit', _('Search')),
            )
        )

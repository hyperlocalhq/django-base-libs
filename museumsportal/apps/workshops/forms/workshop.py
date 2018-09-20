# -*- coding: utf-8 -*-

import os
import shutil

from django.db import models
from django import forms
from django.forms.models import ModelForm
from django.forms.models import inlineformset_factory
from django.conf import settings
from django.utils.translation import ugettext_lazy as _, ugettext
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from babeldjango.templatetags.babel import decimalfmt

from base_libs.forms.fields import AutocompleteModelChoiceField, DecimalField
from base_libs.models.base_libs_settings import MARKUP_HTML_WYSIWYG, MARKUP_PLAIN_TEXT
from base_libs.middleware import get_current_user

from jetson.apps.image_mods.models import FileManager

Museum = models.get_model("museums", "Museum")
Exhibition = models.get_model("exhibitions", "Exhibition")
Workshop = models.get_model("workshops", "Workshop")
WorkshopTime = models.get_model("workshops", "WorkshopTime")
Organizer = models.get_model("workshops", "Organizer")

FRONTEND_LANGUAGES = getattr(settings, "FRONTEND_LANGUAGES", settings.LANGUAGES) 
EXCLUDED_LANGUAGES = set(dict(settings.LANGUAGES).keys()) - set(dict(FRONTEND_LANGUAGES).keys())

from museumsportal.utils.forms import PrimarySubmit
from museumsportal.utils.forms import SecondarySubmit
from museumsportal.utils.forms import SecondaryButton
from museumsportal.utils.forms import InlineFormSet


class BasicInfoForm(ModelForm):
    museum = AutocompleteModelChoiceField(
        required=False,
        label=_("Museum from the list <b>(active)</b> / <a href=\"#\">Free location</a>"),
        # help_text=_("If location doesn't exist in the database, please click <a href=\"#\">here</a> to enter it."),
        app="museums",
        qs_function="get_published_museums",
        display_attr="title_uni",
        add_display_attr="get_address",
        options={
            "minChars": 1,
            "max": 20,
            "mustMatch": 1,
            "highlight": False,
            "multipleSeparator": ",,, ",
        },
    )
    exhibition = AutocompleteModelChoiceField(
        required=False,
        label=_("Related exhibition"),
        # help_text=u"Bitte geben Sie einen Anfangsbuchstaben ein, um eine entsprechende Auswahl der verfügbaren Museums angezeigt zu bekommen.",
        app="exhibitions",
        qs_function="get_published_exhibitions",
        display_attr="title",
        add_display_attr="get_museum",
        options={
            "minChars": 1,
            "max": 20,
            "mustMatch": 1,
            "highlight": False,
            "multipleSeparator": ",,, ",
        },
    )
    pdf_document_de_path = forms.CharField(
        max_length=255,
        widget=forms.HiddenInput(),
        required=False,
    )
    delete_pdf_document_de = forms.BooleanField(
        label=_("Delete PDF Document in German"),
        required=False,
        widget=forms.HiddenInput(),
    )
    pdf_document_en_path = forms.CharField(
        max_length=255,
        widget=forms.HiddenInput(),
        required=False,
    )
    delete_pdf_document_en = forms.BooleanField(
        label=_("Delete PDF Document in English"),
        required=False,
        widget=forms.HiddenInput(),
    )

    class Meta:
        model = Workshop
        
        fields = [
            'tags', 'types', 'languages', 'other_languages',
            'is_for_preschool',
            'is_for_primary_school',
            'is_for_youth',
            'is_for_families',
            'is_for_wheelchaired',
            'is_for_deaf',
            'is_for_blind',
            'is_for_learning_difficulties',
            'is_for_dementia_sufferers',
            'museum', 'location_name', 'street_address', 'street_address2', 'postal_code',
            'city', 'latitude', 'longitude', 'exhibition',
        ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'title_%s' % lang_code,
                'subtitle_%s' % lang_code,
                'press_text_%s' % lang_code,
                'website_%s' % lang_code,
            ]

    def __init__(self, *args, **kwargs):
        super(BasicInfoForm, self).__init__(*args, **kwargs)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            self.fields['website_%s' % lang_code] = forms.URLField(
                label=_("Website"),
                required=False,
            )

        self.fields['street_address'].required = True
        self.fields['postal_code'].required = True
        self.fields['city'].required = True

        self.fields['tags'].widget = forms.TextInput()
        self.fields['tags'].help_text = ""
        
        self.fields['types'].widget = forms.CheckboxSelectMultiple()
        self.fields['types'].help_text = ""
        self.fields['types'].empty_label = None

        self.fields['languages'].widget = forms.CheckboxSelectMultiple()
        self.fields['languages'].help_text = ""
        self.fields['languages'].empty_label = None

        self.fields['location_name'].label = _("Free location <b>(active)</b> / <a href=\"#\">Museum from the list</a>")
        # self.fields['location_name'].help_text = _("If you want to select a location from the database, please click <a href=\"#\">here</a>.")

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'title_%s' % lang_code,
                'subtitle_%s' % lang_code,
                'press_text_%s' % lang_code,
                'website_%s' % lang_code,
            ]:
                self.fields[f].label += """ <span class="lang">%s</span>""" % lang_code.upper()

        self.fields['latitude'].widget = forms.HiddenInput()
        self.fields['longitude'].widget = forms.HiddenInput()

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        
        layout_blocks = []

        fieldset_content = []  # collect multilingual divs into one list...
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('title_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('subtitle_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(
            "types"
        )
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('press_text_%s' % lang_code, css_class="tinymce"),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('website_%s' % lang_code, placeholder="http://"),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))

        layout_blocks.append(layout.Fieldset(
            _("Basic Info"),
            css_class="fieldset-basic-info",
            *fieldset_content
        ))

        layout_blocks.append(layout.Fieldset(
            _("Location"),
            layout.Row(
                layout.Div(
                    layout.Field("museum", template="bootstrap3/field_marked_as_required.html"),
                    layout.Field("location_name", template="bootstrap3/field_marked_as_required.html"),
                    "street_address",
                    "street_address2",
                    "postal_code",
                    "city",
                    css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                ),
                layout.Div(
                    layout.HTML("""{% load i18n %}
                        <div id="dyn_set_map">
                            <label>{% trans "Location" %}</label>
                            <div class="workshop_map" id="gmap-wrapper">
                                <!-- THE GMAPS WILL BE INSERTED HERE DYNAMICALLY -->
                            </div>
                            <div class="form-actions">
                                <input id="dyn_locate_geo" type="button" class="btn btn-primary" value="{% trans "Relocate on map" %}" />&zwnj;
                                <!--<input id="dyn_remove_geo" type="button" class="btn btn-primary" value="{% trans "Remove from map" %}"/>&zwnj;-->
                            </div>
                        </div>
                    """),
                    "latitude",
                    "longitude",
                    css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"

                ),
                css_class="row-md",
            ),
            css_class="fieldset-where",
        ))
        layout_blocks.append(layout.Fieldset(
            _("Organizers (when differ from location)"),
            layout.HTML("""{% load crispy_forms_tags i18n %}
            {{ formsets.organizers.management_form }}
            <div id="organizers">
                {% for form in formsets.organizers.forms %}
                    <div class="organizer formset-form tabular-inline">
                        {% crispy form %}
                    </div>
                {% endfor %}
            </div>
            <!-- used by javascript -->
            <div id="organizers_empty_form" class="organizer formset-form tabular-inline" style="display: none">
                {% with formsets.organizers.empty_form as form %}
                    {% crispy form %}
                {% endwith %}
            </div>
            """),
            css_id="organizers_fieldset",
        ))
        layout_blocks.append(layout.Fieldset(
            _("Related exhibition"),
            "exhibition",
            css_class="fieldset-related-exhibition",
        ))
        layout_blocks.append(layout.Fieldset(
            _("PDF Documents"),
            layout.Div(
                layout.HTML(u"""{% load i18n image_modifications %}
                    <div class="pdf_upload" id="pdf_document_de_upload">
                        <div class="pdf_uploader">
                            <noscript>
                                <p>{% trans "Please enable JavaScript to use file uploader." %}</p>
                            </noscript>
                        </div>
                        <div class="messages"></div>
                        <div class="pdf_link">
                            <p class="lead">
                            {% if workshop.pdf_document_de %}
                                <a class="btn btn-primary" href="{{ MEDIA_URL }}{{ workshop.pdf_document_de.path }}" target="_blank">{{ workshop.pdf_document_de.filename }} ({% trans "Preview" %})</a>
                            {% endif %}
                            </p>
                        </div>
                    </div>
                """),
                layout.HTML(u"""{% load i18n image_modifications %}
                    <div class="pdf_upload" id="pdf_document_en_upload">
                        <div class="pdf_uploader">
                            <noscript>
                                <p>{% trans "Please enable JavaScript to use file uploader." %}</p>
                            </noscript>
                        </div>
                        <div class="messages"></div>
                        <div class="pdf_link">
                            <p class="lead">
                            {% if workshop.pdf_document_en %}
                                <a class="btn btn-primary" href="{{ MEDIA_URL }}{{ workshop.pdf_document_en.path }}" target="_blank">{{ workshop.pdf_document_en.filename }} ({% trans "Preview" %})</a>
                            {% endif %}
                            </p>
                        </div>
                    </div>
                """),
                css_class="cols-2",
            ),
            "pdf_document_de_path",
            "delete_pdf_document_de",
            "pdf_document_en_path",
            "delete_pdf_document_en",
            css_class="fieldset-pdf-files",
        ))
        layout_blocks.append(layout.Fieldset(
            _("Categories and Tags"),

            layout.Div(
                layout.Div("languages", css_class="min"),
                layout.Div("other_languages", css_class="max"),
                css_class="flex merge",
            ),

            layout.Div(
                "tags",
            ),

            layout.Div(
                layout.HTML("""{% load i18n %} <label>{% trans "Particularities" %}</label> """),
                'is_for_preschool',
                'is_for_primary_school',
                'is_for_youth',
                'is_for_families',
                'is_for_wheelchaired',
                'is_for_deaf',
                'is_for_blind',
                'is_for_learning_difficulties',
                'is_for_dementia_sufferers',
                css_class="checkbox-group"
            ),
                
            css_class="fieldset-categories-tags",
        ))
        if self.instance and self.instance.pk:
            layout_blocks.append(bootstrap.FormActions(
                PrimarySubmit('submit', _('Next')),
                SecondarySubmit('save_and_close', _('Close')),         
                SecondarySubmit('reset', _('Cancel')),
            ))
        else:
            layout_blocks.append(bootstrap.FormActions(
                PrimarySubmit('submit', _('Next')),
                SecondarySubmit('reset', _('Cancel')),
            ))
        
        self.helper.layout = layout.Layout(
            *layout_blocks
        )

    def clean_pdf_document_de_path(self):
        data = self.cleaned_data['pdf_document_de_path']
        if ".." in data:
            raise forms.ValidationError(_("Double dots are not allowed in the file name."))
        return data

    def clean_pdf_document_en_path(self):
        data = self.cleaned_data['pdf_document_en_path']
        if ".." in data:
            raise forms.ValidationError(_("Double dots are not allowed in the file name."))
        return data

    def clean(self):
        cleaned_data = super(BasicInfoForm, self).clean()
        if not cleaned_data.get("museum") and not cleaned_data.get("location_name"):
            self._errors['museum'] = self.error_class([_("This field is required.")])
            del cleaned_data['museum']
            del cleaned_data['location_name']
        return cleaned_data


class OrganizerForm(ModelForm):
    organizing_museum = AutocompleteModelChoiceField(
        required=False,
        label=_("Museum from the list <b>(active)</b> / <a href=\"#\">Other Organizer</a>"),
        # help_text=_("If organizer doesn't exist in the database, please click <a href=\"#\">here</a> to enter it."),
        app="museums",
        qs_function="get_published_museums",
        display_attr="title_uni",
        add_display_attr="get_address",
        options={
            "minChars": 1,
            "max": 20,
            "mustMatch": 1,
            "highlight": False,
            "multipleSeparator": ",,, ",
        },
    )
    
    class Meta:
        model = Organizer
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(OrganizerForm, self).__init__(*args, **kwargs)

        self.fields['organizer_title'].label = _("Other Organizer <b>(active)</b> / <a href=\"#\">Museum from the list</a>")
        self.fields['organizer_url_link'].label = _("Website")
        # self.fields['organizer_title'].help_text = _("If you want to select an organizer from the database, please click <a href=\"#\">here</a>.")

        self.helper = FormHelper()
        self.helper.form_tag = False
        layout_blocks = []

        layout_blocks.append(
            layout.Div(
                layout.Div(
                    bootstrap.PrependedText("organizing_museum", ""), 
                    css_class="toggle-option"
                ),
                layout.Row(
                    layout.Div("organizer_title", css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"),
                    layout.Div(bootstrap.PrependedText("organizer_url_link", "", placeholder="http://"), css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"),
                    css_class="row-xs toggle-option"
                ),
                layout.Div(
                    "DELETE",
                    css_class="hide"
                ),
                css_class="div_organizer"
            )
        )

        self.helper.layout = layout.Layout(
            *layout_blocks
        )

OrganizerFormset = inlineformset_factory(Workshop, Organizer, form=OrganizerForm, formset=InlineFormSet, extra=0)


class PricesForm(ModelForm):
    admission_price = DecimalField(
        label=_(u"Price (€)"),
        max_digits=5,
        decimal_places=2,
        required=False,
    )
    reduced_price = DecimalField(
        label=_(u"Reduced price (€)"),
        max_digits=5,
        decimal_places=2,
        required=False,
    )

    class Meta:
        model = Workshop
        fields = ['free_admission', 'admission_price', 'reduced_price']
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'admission_price_info_%s' % lang_code,
                'meeting_place_%s' % lang_code,
                'booking_info_%s' % lang_code,
                'shop_link_%s' % lang_code,
            ]

    def __init__(self, *args, **kwargs):
        super(PricesForm, self).__init__(*args, **kwargs)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            self.fields['shop_link_%s' % lang_code] = forms.URLField(
                label=self.fields['shop_link_%s' % lang_code].help_text,
                required=self.fields['shop_link_%s' % lang_code].required,
                widget=forms.TextInput(attrs={'class': 'vURLField'})
            )
            for f in [
                'admission_price_info_%s' % lang_code,
                'meeting_place_%s' % lang_code,
                'booking_info_%s' % lang_code,
                'shop_link_%s' % lang_code,
            ]:
                self.fields[f].label += """ <span class="lang">%s</span>""" % lang_code.upper()
                
        self.fields['free_admission'].label = _("Free offer")

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        
        layout_blocks = []

        fieldset_content = []  # collect multilingual divs into one list...
        fieldset_content.append(
            layout.Div('free_admission', css_class="inline")
        )
        fieldset_content.append(
            layout.Div(
                layout.Field('admission_price', placeholder=decimalfmt(0, "#,##0.00")),
                layout.Field('reduced_price', placeholder=decimalfmt(0, "#,##0.00")),
                css_class="cols-2",
            )
        )
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('admission_price_info_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('shop_link_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))

        layout_blocks.append(layout.Fieldset(
            _("Prices"),
            css_class="fieldset-prices",
            *fieldset_content
        ))

        fieldset_content = []  # collect multilingual divs into one list...
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('meeting_place_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('booking_info_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))

        layout_blocks.append(layout.Fieldset(
            _("Details"),
            css_class="fieldset-details",
            *fieldset_content
        ))

        if self.instance and self.instance.pk:
            layout_blocks.append(bootstrap.FormActions(
                PrimarySubmit('submit', _('Next')),
                SecondarySubmit('save_and_close', _('Close')),
                SecondarySubmit('reset', _('Cancel')),
            ))
        else:
            layout_blocks.append(bootstrap.FormActions(
                PrimarySubmit('submit', _('Next')),
                SecondarySubmit('reset', _('Cancel')),
            ))
        
        self.helper.layout = layout.Layout(
            *layout_blocks
        )


class TimesForm(ModelForm):

    class Meta:
        model = Workshop
        fields = [
            'has_group_offer',
        ]

    def __init__(self, *args, **kwargs):
        super(TimesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.form_id = "workshop_times_form"
        layout_blocks = []
        layout_blocks.append(layout.Fieldset(
            _("Booking"),
            layout.Div(
                'has_group_offer',
                css_class="inline",
            ),
        ))
        layout_blocks.append(layout.Fieldset(
            _("Date and Time"),
            layout.HTML("""{% load crispy_forms_tags i18n %}
            {{ formsets.workshop_times.management_form }}
            <div id="workshop_times">
                {% for form in formsets.workshop_times.forms %}
                    <div class="workshop_time formset-form tabular-inline">
                        {% crispy form %}
                    </div>
                {% endfor %}
            </div>
            <!-- used by javascript -->
            <div id="workshop_times_empty_form" class="workshop_time formset-form tabular-inline" style="display: none">
                {% with formsets.workshop_times.empty_form as form %}
                    {% crispy form %}
                {% endwith %}
            </div>
            """),
            css_id="workshop_times_fieldset",
        ))
        if self.instance and self.instance.pk:
            layout_blocks.append(bootstrap.FormActions(
                PrimarySubmit('submit', _('Next')),
                SecondarySubmit('save_and_close', _('Close')),
                SecondarySubmit('reset', _('Cancel')),
            ))
        else:
            layout_blocks.append(bootstrap.FormActions(
                PrimarySubmit('submit', _('Next')),
                SecondarySubmit('reset', _('Cancel')),
            ))
        self.helper.layout = layout.Layout(
            *layout_blocks
        )


class WorkshopTimeForm(ModelForm):

    class Meta:
        model = WorkshopTime
        fields = "__all__"
        
    def __init__(self, *args, **kwargs):
        super(WorkshopTimeForm, self).__init__(*args, **kwargs)
        self.fields['workshop_date'].widget = forms.DateInput(format='%d.%m.%Y')
        self.fields['workshop_date'].input_formats=('%d.%m.%Y',)
        self.fields['workshop_date'].label = _("Date")
        self.fields['start'].required = True
        self.fields['start'].widget = forms.TimeInput(format='%H:%M')
        self.fields['end'].widget = forms.TimeInput(format='%H:%M')
        
        self.helper = FormHelper()
        self.helper.form_tag = False
        layout_blocks = []
        layout_blocks.append(
            layout.Row(
                layout.Div(
                    bootstrap.PrependedText("workshop_date", "", placeholder="dd.mm.yyyy", autocomplete="off"),
                    css_class="col-xs-4 col-sm-4 col-md-4 col-lg-4"
                ),
                layout.Div(
                    bootstrap.PrependedText("start", "", placeholder="00:00"),
                    css_class="col-xs-4 col-sm-4 col-md-4 col-lg-4"
                ),
                layout.Div(
                    bootstrap.PrependedText("end", "", placeholder="00:00"),
                    css_class="col-xs-4 col-sm-4 col-md-4 col-lg-4"
                ),
                layout.Div(
                    "DELETE",
                    css_class="hide"
                ),

                css_class="row-xs",
            ),
        )

        self.helper.layout = layout.Layout(
            *layout_blocks
        )

WorkshopTimeFormset = inlineformset_factory(Workshop, WorkshopTime, form=WorkshopTimeForm, formset=InlineFormSet, extra=0)


class BatchWorkshopTimeForm(forms.Form):
    range_start = forms.DateField(
        label=_("Start"),
        required=True,
    )
    range_end = forms.DateField(
        label=_("End"),
        required=True,
    )
    repeat = forms.ChoiceField(
        label=_("Repeat"),
        required=True,
        choices=((1, _("Every week")), (2, _("Every second week"))),
    )
    mon_start = forms.TimeField(
        label=_("From"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )
    mon_end = forms.TimeField(
        label=_("till"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )
    tue_start = forms.TimeField(
        label="",
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )
    tue_end = forms.TimeField(
        label="",
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )
    wed_start = forms.TimeField(
        label="",
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )
    wed_end = forms.TimeField(
        label="",
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )
    thu_start = forms.TimeField(
        label="",
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )
    thu_end = forms.TimeField(
        label="",
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )
    fri_start = forms.TimeField(
        label="",
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )
    fri_end = forms.TimeField(
        label="",
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )
    sat_start = forms.TimeField(
        label="",
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )
    sat_end = forms.TimeField(
        label="",
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )
    sun_start = forms.TimeField(
        label="",
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )
    sun_end = forms.TimeField(
        label="",
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
    )

    def __init__(self, *args, **kwargs):
        super(BatchWorkshopTimeForm, self).__init__(*args, **kwargs)
        self.fields['range_start'].widget = forms.DateInput(format='%d.%m.%Y')
        self.fields['range_start'].input_formats=('%d.%m.%Y',)
        
        self.fields['range_end'].widget = forms.DateInput(format='%d.%m.%Y')
        self.fields['range_end'].input_formats=('%d.%m.%Y',)
        
        self.helper = FormHelper()
        self.helper.form_id = "batch_workshop_time_form"
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        layout_blocks = []
        layout_blocks.append(layout.Fieldset(
            _("Batch workshop time creation"),
            
            layout.Row(
                layout.Div(
                    bootstrap.PrependedText("range_start", "", placeholder="dd.mm.yyyy"), css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                ),
                layout.Div(
                    bootstrap.PrependedText("range_end", "", placeholder="dd.mm.yyyy"), css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                ),
                css_class="row-md",
            ),

            "repeat",

            layout.Div(
                layout.Row(
                    layout.Div(
                        bootstrap.PrependedText("mon_start", ugettext('Mo'), placeholder="00:00"), css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                    ),
                    layout.Div(
                        bootstrap.PrependedText("mon_end", "", placeholder="00:00"), css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                    ),
                    css_class="row-xs"
                ),
                layout.Row(
                    layout.Div(
                        bootstrap.PrependedText("tue_start", ugettext('Tu'), placeholder="00:00"), css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                    ),
                    layout.Div(
                        bootstrap.PrependedText("tue_end", "", placeholder="00:00"), css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                    ),
                    css_class="row-xs"
                ),
                layout.Row(
                    layout.Div(
                        bootstrap.PrependedText("wed_start", ugettext('We'), placeholder="00:00"), css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                    ),
                    layout.Div(
                        bootstrap.PrependedText("wed_end", "", placeholder="00:00"), css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                    ),
                    css_class="row-xs"
                ),
                layout.Row(
                    layout.Div(
                        bootstrap.PrependedText("thu_start", ugettext('Th'), placeholder="00:00"), css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                    ),
                    layout.Div(
                        bootstrap.PrependedText("thu_end", "", placeholder="00:00"), css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                    ),
                    css_class="row-xs"
                ),
                layout.Row(
                    layout.Div(
                        bootstrap.PrependedText("fri_start", ugettext('Fr'), placeholder="00:00"), css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                    ),
                    layout.Div(
                        bootstrap.PrependedText("fri_end", "", placeholder="00:00"), css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                    ),
                    css_class="row-xs"
                ),
                layout.Row(
                    layout.Div(
                        bootstrap.PrependedText("sat_start", ugettext('Sa'), placeholder="00:00"), css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                    ),
                    layout.Div(
                        bootstrap.PrependedText("sat_end", "", placeholder="00:00"), css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                    ),
                    css_class="row-xs"
                ),
                layout.Row(
                    layout.Div(
                        bootstrap.PrependedText("sun_start", ugettext('Su'), placeholder="00:00"), css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                    ),
                    layout.Div(
                        bootstrap.PrependedText("sun_end", "", placeholder="00:00"), css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                    ),
                    css_class="row-xs"
                ),
                css_id="batch_workshop_time",
            ),
        ))
        
        layout_blocks.append(bootstrap.FormActions(
            PrimarySubmit('submit', _('Create workshop times')),
            SecondaryButton('go_back', _('Go back')),
        ))

        self.helper.layout = layout.Layout(
            *layout_blocks
        )


class GalleryForm(ModelForm):

    class Meta:
        model = Workshop
        fields = []
        
    def __init__(self, *args, **kwargs):
        super(GalleryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        layout_blocks = []
        if self.instance and self.instance.pk:
            layout_blocks.append(bootstrap.FormActions(
                PrimarySubmit('save_and_close', _('Close')),
                SecondarySubmit('reset', _('Cancel')),
            ))
        else:
            layout_blocks.append(bootstrap.FormActions(
                PrimarySubmit('submit', _('Save')),
                SecondarySubmit('reset', _('Cancel')),
            ))
        self.helper.layout = layout.Layout(
            *layout_blocks
        )


def load_data(instance=None, request=None):
    form_step_data = {}
    if instance:
        form_step_data = {
            'basic': {'_filled': True, 'sets': {'organizers': []}},
            'times': {'_filled': True, 'sets': {'workshop_times': [],}},
            'prices': {'_filled': True},
            'gallery': {'_filled': True},
            '_pk': instance.pk,
            '_is_new': False,
        }
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            form_step_data['basic']['title_%s' % lang_code] = getattr(instance, 'title_%s' % lang_code)
            form_step_data['basic']['subtitle_%s' % lang_code] = getattr(instance, 'subtitle_%s' % lang_code)
            form_step_data['basic']['description_%s' % lang_code] = getattr(instance, 'description_%s' % lang_code)
            form_step_data['basic']['press_text_%s' % lang_code] = getattr(instance, 'press_text_%s' % lang_code)
            form_step_data['basic']['website_%s' % lang_code] = getattr(instance, 'website_%s' % lang_code)
        form_step_data['basic']['tags'] = instance.tags
        form_step_data['basic']['types'] = instance.types.all()
        form_step_data['basic']['languages'] = instance.languages.all()
        form_step_data['basic']['other_languages'] = instance.other_languages
        if instance.museum:
            form_step_data['basic']['museum'] = instance.museum.pk
        form_step_data['basic']['location_name'] = instance.location_name
        form_step_data['basic']['street_address'] = instance.street_address
        form_step_data['basic']['street_address2'] = instance.street_address2
        form_step_data['basic']['postal_code'] = instance.postal_code
        form_step_data['basic']['city'] = instance.city
        form_step_data['basic']['latitude'] = instance.latitude
        form_step_data['basic']['longitude'] = instance.longitude
        if instance.exhibition:
            form_step_data['basic']['exhibition'] = instance.exhibition.pk
        for f in [
            'is_for_preschool',
            'is_for_primary_school',
            'is_for_youth',
            'is_for_families',
            'is_for_wheelchaired',
            'is_for_deaf',
            'is_for_blind',
            'is_for_learning_difficulties',
            'is_for_dementia_sufferers',
        ]:
            form_step_data['basic'][f] = getattr(instance, f)

        for organizer in instance.organizer_set.all():
            organizer_dict = {}
            if organizer.organizing_museum:
                organizer_dict['organizing_museum'] = organizer.organizing_museum.pk
            organizer_dict['organizer_title'] = organizer.organizer_title
            organizer_dict['organizer_url_link'] = organizer.organizer_url_link
            form_step_data['basic']['sets']['organizers'].append(organizer_dict)
            
        form_step_data['times']['has_group_offer'] = instance.has_group_offer
        for workshop_time in instance.workshoptime_set.all():
            workshop_time_dict = {}
            workshop_time_dict['workshop_date'] = workshop_time.workshop_date
            workshop_time_dict['start'] = workshop_time.start
            workshop_time_dict['end'] = workshop_time.end
            form_step_data['times']['sets']['workshop_times'].append(workshop_time_dict)
    
        fields = ['free_admission', 'admission_price', 'reduced_price']
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'admission_price_info_%s' % lang_code,
                'meeting_place_%s' % lang_code,
                'booking_info_%s' % lang_code,
                'shop_link_%s' % lang_code,
            ]
        for f in fields:
            form_step_data['prices'][f] = getattr(instance, f)

    return form_step_data


def submit_step(current_step, form_steps, form_step_data, instance=None):
    if current_step == "basic":
        # save the entry
        if "_pk" in form_step_data:
            instance = Workshop.objects.get(pk=form_step_data['_pk'])
        else:
            instance = Workshop()
            form_step_data['_is_new'] = True

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            setattr(instance, 'title_%s' % lang_code, form_step_data['basic']['title_%s' % lang_code]) 
            setattr(instance, 'subtitle_%s' % lang_code, form_step_data['basic']['subtitle_%s' % lang_code])
            setattr(instance, 'press_text_%s' % lang_code, form_step_data['basic']['press_text_%s' % lang_code])
            setattr(instance, 'website_%s' % lang_code, form_step_data['basic']['website_%s' % lang_code])
            setattr(instance, 'press_text_%s_markup_type' % lang_code, MARKUP_HTML_WYSIWYG)
            if not instance.description_locked: 
                setattr(instance, 'description_%s' % lang_code, form_step_data['basic']['press_text_%s' % lang_code])
                setattr(instance, 'description_%s_markup_type' % lang_code, MARKUP_HTML_WYSIWYG)
        instance.other_languages = form_step_data['basic']['other_languages']
        if form_step_data['basic']['museum']:
            instance.museum = form_step_data['basic']['museum']
            instance.location_name = ""
        else:
            instance.museum = None
            instance.location_name = form_step_data['basic']['location_name']
        instance.street_address = form_step_data['basic']['street_address']
        instance.street_address2 = form_step_data['basic']['street_address2'] 
        instance.postal_code = form_step_data['basic']['postal_code']
        instance.city = form_step_data['basic']['city']
        instance.latitude = form_step_data['basic']['latitude']
        instance.longitude = form_step_data['basic']['longitude']
        if form_step_data['basic']['exhibition']:
            instance.exhibition = form_step_data['basic']['exhibition']
        else:
            instance.exhibition = None
        if form_step_data['basic']['tags'] and not form_step_data['basic']['tags'].endswith(","):
            form_step_data['basic']['tags'] = form_step_data['basic']['tags'] + ","
        instance.tags = form_step_data['basic']['tags']
        for f in [
            'is_for_preschool',
            'is_for_primary_school',
            'is_for_youth',
            'is_for_families',
            'is_for_wheelchaired',
            'is_for_deaf',
            'is_for_blind',
            'is_for_learning_difficulties',
            'is_for_dementia_sufferers',
        ]:
            setattr(instance, f, form_step_data['basic'][f])
            
        if not instance.status:
            instance.status = "draft"
        instance.save()
        
        rel_dir = "workshops/%s/" % instance.slug

        if form_step_data['basic']['delete_pdf_document_de'] and instance.pdf_document_de:
            FileManager.delete_file(instance.pdf_document_de.path)
            instance.pdf_document_de = ""
            form_step_data['basic']['delete_pdf_document_de'] = False

        if form_step_data['basic']["pdf_document_de_path"]:
            tmp_path = form_step_data['basic']["pdf_document_de_path"]
            abs_tmp_path = os.path.join(settings.MEDIA_ROOT, tmp_path)

            fname, fext = os.path.splitext(os.path.basename(tmp_path))
            filename = slugify(fname) + fext
            dest_path = "".join((rel_dir, filename))
            FileManager.path_exists(os.path.join(settings.MEDIA_ROOT, rel_dir))
            abs_dest_path = os.path.join(settings.MEDIA_ROOT, dest_path)

            shutil.move(abs_tmp_path, abs_dest_path)

            instance.pdf_document_de = dest_path
            form_step_data['basic']["pdf_document_de_path"] = ""

        if form_step_data['basic']['delete_pdf_document_en'] and instance.pdf_document_en:
            FileManager.delete_file(instance.pdf_document_en.path)
            instance.pdf_document_en = ""
            form_step_data['basic']['delete_pdf_document_en'] = False

        if form_step_data['basic']["pdf_document_en_path"]:
            tmp_path = form_step_data['basic']["pdf_document_en_path"]
            abs_tmp_path = os.path.join(settings.MEDIA_ROOT, tmp_path)

            fname, fext = os.path.splitext(os.path.basename(tmp_path))
            filename = slugify(fname) + fext
            dest_path = "".join((rel_dir, filename))
            FileManager.path_exists(os.path.join(settings.MEDIA_ROOT, rel_dir))
            abs_dest_path = os.path.join(settings.MEDIA_ROOT, dest_path)

            shutil.move(abs_tmp_path, abs_dest_path)

            instance.pdf_document_en = dest_path
            form_step_data['basic']["pdf_document_en_path"] = ""

        instance.save()

        if '_pk' not in form_step_data:
            user = get_current_user()
            instance.set_owner(user)
        
        instance.types.clear()
        for cat in form_step_data['basic']['types']:
            instance.types.add(cat)
        
        instance.languages.clear()
        for cat in form_step_data['basic']['languages']:
            instance.languages.add(cat)
        
        instance.organizer_set.all().delete()
        for organizer_dict in form_step_data['basic']['sets']['organizers']:
            organizer = Organizer(workshop=instance)
            if organizer_dict.get('organizing_museum', None):
                organizer.organizing_museum = Museum.objects.get(
                    pk=organizer_dict['organizing_museum'],
                )
                organizer.organizer_title = ""
                organizer.organizer_url_link = ""
            else:
                organizer.organizing_museum = None
                organizer.organizer_title = organizer_dict.get('organizer_title', "")
                organizer.organizer_url_link = organizer_dict.get('organizer_url_link', "")
            organizer.save()
        
        form_step_data['_pk'] = instance.pk

    if current_step == "times":
        if "_pk" in form_step_data:
            instance = Workshop.objects.get(pk=form_step_data['_pk'])
            instance.has_group_offer = form_step_data['times']['has_group_offer']
            instance.save()
            instance.workshoptime_set.all().delete()
            for workshop_time_dict in form_step_data['times']['sets']['workshop_times']:
                workshop_time = WorkshopTime(workshop=instance)
                workshop_time.workshop_date = workshop_time_dict['workshop_date'] 
                workshop_time.start = workshop_time_dict['start']
                workshop_time.end = workshop_time_dict['end']
                workshop_time.save()

            instance.update_closest_workshop_time()

    if current_step == "prices":
        if "_pk" in form_step_data:
            instance = Workshop.objects.get(pk=form_step_data['_pk'])
        
            fields = ['free_admission', 'admission_price', 'reduced_price']
            for lang_code, lang_name in FRONTEND_LANGUAGES:
                fields += [
                    'admission_price_info_%s' % lang_code,
                    'meeting_place_%s' % lang_code,
                    'booking_info_%s' % lang_code,
                    'shop_link_%s' % lang_code,
                ]
                setattr(instance, "admission_price_info_%s_markup_type" % lang_code, MARKUP_PLAIN_TEXT)
                setattr(instance, "meeting_place_%s_markup_type" % lang_code, MARKUP_PLAIN_TEXT)
                setattr(instance, "booking_info_%s_markup_type" % lang_code, MARKUP_PLAIN_TEXT)
                    
            for f in fields:
                setattr(instance, f, form_step_data['prices'][f])
            instance.save()

    return form_step_data


def set_extra_context(current_step, form_steps, form_step_data, instance=None, request=None):
    extra_context = {}
    if "_pk" in form_step_data:
        extra_context['workshop'] = Workshop.objects.get(pk=form_step_data['_pk'])
    if current_step == "times":
        extra_context['batch_workshop_time_form'] = BatchWorkshopTimeForm()
    return extra_context


def save_data(form_steps, form_step_data, instance=None):
    is_new = form_step_data.get('_is_new', False)

    if not instance:
        if '_pk' in form_step_data:
            instance = Workshop.objects.get(pk=form_step_data['_pk'])
        else:
            instance = Workshop()
            
    for lang_code, lang_name in FRONTEND_LANGUAGES:
        setattr(instance, 'title_%s' % lang_code, form_step_data['basic']['title_%s' % lang_code]) 
        setattr(instance, 'subtitle_%s' % lang_code, form_step_data['basic']['subtitle_%s' % lang_code])
        setattr(instance, 'press_text_%s' % lang_code, form_step_data['basic']['press_text_%s' % lang_code])
        setattr(instance, 'website_%s' % lang_code, form_step_data['basic']['website_%s' % lang_code])
        setattr(instance, 'press_text_%s_markup_type' % lang_code, MARKUP_HTML_WYSIWYG)
        if not instance.description_locked: 
            setattr(instance, 'description_%s' % lang_code, form_step_data['basic']['press_text_%s' % lang_code])
            setattr(instance, 'description_%s_markup_type' % lang_code, MARKUP_HTML_WYSIWYG)
    instance.other_languages = form_step_data['basic']['other_languages'] 
    if form_step_data['basic']['museum']:
        instance.museum = form_step_data['basic']['museum']
        instance.location_name = ""
    else:
        instance.museum = None
        instance.location_name = form_step_data['basic']['location_name']
    instance.street_address = form_step_data['basic']['street_address']
    instance.street_address2 = form_step_data['basic']['street_address2'] 
    instance.postal_code = form_step_data['basic']['postal_code']
    instance.city = form_step_data['basic']['city']
    instance.latitude = form_step_data['basic']['latitude']
    instance.longitude = form_step_data['basic']['longitude']
    if form_step_data['basic'].get('exhibition', None):
        try:
            instance.exhibition = Exhibition.objects.get(pk=form_step_data['basic']['exhibition'])
        except:
            pass
    for f in [
        'is_for_preschool',
        'is_for_primary_school',
        'is_for_youth',
        'is_for_families',
        'is_for_wheelchaired',
        'is_for_deaf',
        'is_for_blind',
        'is_for_learning_difficulties',
        'is_for_dementia_sufferers',
    ]:
        setattr(instance, f, form_step_data['basic'][f])
    if form_step_data['basic']['tags'] and not form_step_data['basic']['tags'].endswith(","):
        form_step_data['basic']['tags'] = form_step_data['basic']['tags'] + ","
    instance.tags = form_step_data['basic']['tags']

    instance.has_group_offer = form_step_data['times']['has_group_offer']

    fields = ['free_admission', 'admission_price', 'reduced_price']
    for lang_code, lang_name in FRONTEND_LANGUAGES:
        fields += [
            'admission_price_info_%s' % lang_code,
            'meeting_place_%s' % lang_code,
            'booking_info_%s' % lang_code,
            'shop_link_%s' % lang_code,
        ]
        setattr(instance, "admission_price_info_%s_markup_type" % lang_code, MARKUP_PLAIN_TEXT)
        setattr(instance, "meeting_place_%s_markup_type" % lang_code, MARKUP_PLAIN_TEXT)
        setattr(instance, "booking_info_%s_markup_type" % lang_code, MARKUP_PLAIN_TEXT)
            
    for f in fields:
        setattr(instance, f, form_step_data['prices'][f])

    if is_new:
        instance.status = "published"
    instance.save()
    
    #if is_new:
    #    user = get_current_user()
    #    instance.set_owner(user)
    
    instance.types.clear()
    for cat in form_step_data['basic']['types']:
        instance.types.add(cat)
    
    instance.languages.clear()
    for cat in form_step_data['basic']['languages']:
        instance.languages.add(cat)
    
    instance.organizer_set.all().delete()
    for organizer_dict in form_step_data['basic']['sets']['organizers']:
        organizer = Organizer(workshop=instance)
        if organizer_dict.get('organizing_museum', None):
            try:
                organizer.organizing_museum = Museum.objects.get(pk=organizer_dict['organizing_museum'])
            except:
                pass
        organizer.organizer_title = organizer_dict.get('organizer_title', "")
        organizer.organizer_url_link = organizer_dict.get('organizer_url_link', "")
        organizer.save()

    instance.workshoptime_set.all().delete()
    for workshop_time_dict in form_step_data['times']['sets']['workshop_times']:
        workshop_time = WorkshopTime(workshop=instance)
        workshop_time.workshop_date = workshop_time_dict['workshop_date'] 
        workshop_time.start = workshop_time_dict['start']
        workshop_time.end = workshop_time_dict['end']
        workshop_time.save()

    instance.update_closest_workshop_time()

    form_steps['success_url'] = reverse("dashboard") #instance.get_url_path()
    
    return form_step_data


def cancel_editing(request):
    return redirect("dashboard")


WORKSHOP_FORM_STEPS = {
    'basic': {
        'title': _("Basic Information"),
        'template': "workshops/forms/basic_info_form.html",
        'form': BasicInfoForm,
        'formsets': {
            'organizers': OrganizerFormset,
        }
    },
    'times': {
        'title': _("Times"),
        'template': "workshops/forms/times_form.html",
        'form': TimesForm,
        'formsets': {
            'workshop_times': WorkshopTimeFormset,
        }
    },
    'prices': {
        'title': _("Prices"),
        'template': "workshops/forms/prices_form.html",
        'form': PricesForm,
    },
    'gallery': {
        'title': _("Images"),
        'template': "workshops/forms/gallery_form.html",
        'form': GalleryForm, # dummy form
    },
    'oninit': load_data,
    'on_set_extra_context': set_extra_context,
    'onsubmit': submit_step,
    'onsave': save_data,
    'onreset': cancel_editing,
    'general_error_message': _("There are errors in this form. Please correct them and try to save again."),
    'name': 'workshop_registration',
    'default_path': ["basic", "times", "prices", "gallery"],
}

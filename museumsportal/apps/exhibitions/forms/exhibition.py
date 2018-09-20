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
ExhibitionCategory = models.get_model("exhibitions", "ExhibitionCategory")
Season = models.get_model("exhibitions", "Season")
Organizer = models.get_model("exhibitions", "Organizer")

FRONTEND_LANGUAGES = getattr(settings, "FRONTEND_LANGUAGES", settings.LANGUAGES) 
EXCLUDED_LANGUAGES = set(dict(settings.LANGUAGES).keys()) - set(dict(FRONTEND_LANGUAGES).keys())

from museumsportal.utils.forms import PrimarySubmit
from museumsportal.utils.forms import SecondarySubmit
from museumsportal.utils.forms import InlineFormSet
from museumsportal.utils.forms import SplitDateTimeWidget
from museumsportal.utils.forms import ModelMultipleChoiceTreeField

# translatable strings to collect
_("Particularities")
_("Add Individual Opening Hours")
_("Opening Hours")
_("Add Closing Time / Holiday")
_("Closing Times / Holidays")
_("Location")
_("Relocate on map")
_("Remove from map")
_("From %(time)s")
_("To %(time)s")
_("Mo")
_("Tu")
_("We")
_("Th")
_("Fr")
_("Sa")
_("Su")
_("Breaks")


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
    categories = ModelMultipleChoiceTreeField(
        label=_("Categories"),
        required=False,
        queryset=ExhibitionCategory.objects.all(),
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
        model = Exhibition
        
        fields = [
            'start', 'end', 'permanent', 'exhibition_extended',
            'museum', 'location_name', 'street_address', 'street_address2', 'postal_code',
            'city', 'latitude', 'longitude',  
            'vernissage', 'finissage', 'tags', 'categories', "is_for_children",
        ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'title_%s' % lang_code,
                'subtitle_%s' % lang_code,
                'press_text_%s' % lang_code,
                'website_%s' % lang_code,
                'catalog_%s' % lang_code,
                'catalog_ordering_%s' % lang_code,
            ]

    def __init__(self, *args, **kwargs):
        super(BasicInfoForm, self).__init__(*args, **kwargs)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            self.fields['website_%s' % lang_code] = forms.URLField(
                label=_("Website"),
                required=False,
            )

        self.fields['press_text_%s' % settings.LANGUAGE_CODE].required = True
        self.fields['start'].required = True
        self.fields['street_address'].required = True
        self.fields['postal_code'].required = True
        self.fields['city'].required = True

        self.fields['start'].widget = forms.DateInput(format='%d.%m.%Y')
        self.fields['start'].input_formats=('%d.%m.%Y',)
        
        self.fields['end'].widget = forms.DateInput(format='%d.%m.%Y')
        self.fields['end'].input_formats=('%d.%m.%Y',)
        
        self.fields['vernissage'].widget = SplitDateTimeWidget(date_format="%d.%m.%Y", time_format='%H:%M')
        self.fields['vernissage'].input_formats=('%d.%m.%Y %H:%M',)
        
        self.fields['finissage'].widget = SplitDateTimeWidget(date_format="%d.%m.%Y", time_format='%H:%M')
        self.fields['finissage'].input_formats=('%d.%m.%Y %H:%M',)

        self.fields['tags'].widget = forms.TextInput()
        self.fields['tags'].help_text = ""
        #self.fields['categories'].widget = forms.CheckboxSelectMultiple()
        self.fields['categories'].help_text = ""
        self.fields['categories'].empty_label = None
        self.fields['categories'].level_indicator = "/ "

        self.fields['location_name'].label = _("Free location <b>(active)</b> / <a href=\"#\">Museum from the list</a>")
        # self.fields['location_name'].help_text = _("If you want to select a location from the database, please click <a href=\"#\">here</a>.")

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'title_%s' % lang_code,
                'subtitle_%s' % lang_code,
                'press_text_%s' % lang_code,
                'website_%s' % lang_code,
                'catalog_%s' % lang_code,
                'catalog_ordering_%s' % lang_code,
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
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('catalog_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('catalog_ordering_%s' % lang_code, placeholder="http://"),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))

        layout_blocks.append(layout.Fieldset(
            _("Basic Info"),
            css_class="fieldset-basic-info",
            *fieldset_content  # ... then pass them to a fieldset
        ))

        layout_blocks.append(layout.Fieldset(
            _("Duration"),
            layout.Div(
                "permanent",
                "exhibition_extended",
                css_class="cols-2",
            ),
            layout.Row(
                layout.Div(
                    bootstrap.PrependedText("start", "", placeholder="dd.mm.yyyy", autocomplete="off"), css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                ),
                layout.Div(
                    bootstrap.PrependedText("end", "", placeholder="dd.mm.yyyy", autocomplete="off"), css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                ),
                css_class="row-sm",
            ),
            bootstrap.PrependedText("vernissage", "", autocomplete="off"),
            bootstrap.PrependedText("finissage", "", autocomplete="off"),
            css_class="fieldset-when",
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
                            <div class="exhibition_map" id="gmap-wrapper">
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
                            {% if exhibition.pdf_document_de %}
                                <a class="btn btn-primary" href="{{ MEDIA_URL }}{{ exhibition.pdf_document_de.path }}" target="_blank">{{ exhibition.pdf_document_de.filename }} ({% trans "Preview" %})</a>
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
                            {% if exhibition.pdf_document_en %}
                                <a class="btn btn-primary" href="{{ MEDIA_URL }}{{ exhibition.pdf_document_en.path }}" target="_blank">{{ exhibition.pdf_document_en.filename }} ({% trans "Preview" %})</a>
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
            layout.Div(layout.Field("categories", template="utils/checkboxselectmultipletree.html")),

            layout.Div(
                layout.HTML("""{% load i18n %} <label>{% trans "Particularities" %}</label> """),
                "is_for_children",
                css_class="inline"
            ),

            layout.Div("tags"),
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
        start = cleaned_data.get("start")
        end = cleaned_data.get("end")
        if start and end and start > end:
            self._errors['end'] = self.error_class([_("End date should be later than the start date.")])
            del cleaned_data['end']
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
            "highlight" : False,
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

OrganizerFormset = inlineformset_factory(Exhibition, Organizer, form=OrganizerForm, formset=InlineFormSet, extra=0)


class OpeningForm(ModelForm):
    class Meta:
        model = Exhibition
        fields = ['museum_opening_hours']
    
    def __init__(self, *args, **kwargs):
        super(OpeningForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        layout_blocks = []
        layout_blocks.append(layout.Fieldset(
            _("Museum's Opening Hours"),
            'museum_opening_hours',
            css_id="fieldset_museum_opening_hours",
        ))
        layout_blocks.append(layout.HTML("""{% load i18n crispy_forms_tags %}
            <div id="item_container">
                <fieldset>
                    <legend>{% trans "Opening Hours" %}</legend>
                    <a class="add btn btn-primary" id="add_season" href="#">{% trans "Add Individual Opening Hours" %}</a>
                    <ul id="season_list" class="list-unstyled">
                        <li class="hide"></li>
                    </ul>
                </fieldset>
            </div>
            
            {{ formsets.seasons.management_form }}
            {{ formsets.special_openings.management_form }}
            
            <div id="seasons">
                {% for form in formsets.seasons.forms %}
                    <div class="season formset-form" style="display: none">
                        {% crispy form %}
                    </div>
                {% endfor %}
            </div>
            <!-- used by javascript -->
            <div id="seasons_empty_form" class="season formset-form" style="display: none">
                {% with formsets.seasons.empty_form as form %}
                    {% crispy form %}
                {% endwith %}
            </div>
            
        """))
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


class SeasonForm(ModelForm):
    mon_is_closed = forms.BooleanField(label=_("Closed"), required=False)
    tue_is_closed = forms.BooleanField(label=_("Closed"), required=False)
    wed_is_closed = forms.BooleanField(label=_("Closed"), required=False)
    thu_is_closed = forms.BooleanField(label=_("Closed"), required=False)
    fri_is_closed = forms.BooleanField(label=_("Closed"), required=False)
    sat_is_closed = forms.BooleanField(label=_("Closed"), required=False)
    sun_is_closed = forms.BooleanField(label=_("Closed"), required=False)
    
    class Meta:
        model = Season
        exclude = []
        for lang_code, lang_name in settings.LANGUAGES:
            exclude.append("exceptions_%s_markup_type" % lang_code)
        for lang_code in EXCLUDED_LANGUAGES:
            exclude.append("last_entry_%s" % lang_code)
            exclude.append("exceptions_%s" % lang_code)

    def __init__(self, *args, **kwargs):
        super(SeasonForm, self).__init__(*args, **kwargs)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            self.fields['exceptions_%s' % lang_code].label = _("Additional Information")

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'last_entry_%s' % lang_code,
                'exceptions_%s' % lang_code,
            ]:
                self.fields[f].label += """ <span class="lang">%s</span>""" % lang_code.upper()

        # remove labels from opening and closing times 
        for weekday in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]:
            self.fields['%s_open' % weekday].widget = forms.TimeInput(format='%H:%M')
            self.fields['%s_open' % weekday].label = ""
            self.fields['%s_break_close' % weekday].widget = forms.TimeInput(format='%H:%M')
            self.fields['%s_break_close' % weekday].label = ""
            self.fields['%s_break_open' % weekday].widget = forms.TimeInput(format='%H:%M')
            self.fields['%s_break_open' % weekday].label = ""
            self.fields['%s_close' % weekday].widget = forms.TimeInput(format='%H:%M')
            self.fields['%s_close' % weekday].label = ""
        
        self.helper = FormHelper()
        self.helper.form_tag = False
        layout_blocks = []

        fieldset_content = []  # collect multilingual divs into one list...
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('last_entry_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('exceptions_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))

        layout_blocks.append(layout.Fieldset(
            _("Individual Opening Time of the Exhibition"),
            layout.Div(
                "is_appointment_based", 
                "is_open_24_7",
                css_class="checkbox-group"
            ),
        ))

        layout_blocks.append(layout.Fieldset(
            "",
            layout.HTML("""{% load i18n %}
                <div class="row row-md">
                    <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">
                        <fieldset>
                            <legend>{% trans "Opening Hours" %}</legend>
                            <div class="row row-xs">
                                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6"><label>{% blocktrans with time="" %}From {{ time }}{% endblocktrans %}</label></div>
                                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6"><label>{% blocktrans with time="" %}To {{ time }}{% endblocktrans %}</label></div>
                            </div>
                             <div class="row row-xs">
                                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">"""), bootstrap.PrependedText("mon_open", ugettext('Mo'), placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">"""), bootstrap.PrependedText("mon_close", "", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                                <div class="closed hide">"""), "mon_is_closed", layout.HTML("""</div>
                            </div>
                            {% load i18n %}
                            <div class="row row-xs">
                                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">"""), bootstrap.PrependedText("tue_open", ugettext('Tu'), placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">"""), bootstrap.PrependedText("tue_close", "", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                                <div class="closed hide">"""), "tue_is_closed", layout.HTML("""</div>
                            </div>
                            {% load i18n %}
                            <div class="row row-xs">
                                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">"""), bootstrap.PrependedText("wed_open", ugettext('We'), placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">"""), bootstrap.PrependedText("wed_close", "", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                                <div class="closed hide">"""), "wed_is_closed", layout.HTML("""</div>
                            </div>
                            {% load i18n %}
                            <div class="row row-xs">
                                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">"""), bootstrap.PrependedText("thu_open", ugettext('Th'), placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">"""), bootstrap.PrependedText("thu_close", "", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                                <div class="closed hide">"""), "thu_is_closed", layout.HTML("""</div>
                            </div>
                            {% load i18n %}
                            <div class="row row-xs">
                                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">"""), bootstrap.PrependedText("fri_open", ugettext('Fr'), placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">"""), bootstrap.PrependedText("fri_close", "", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                                <div class="closed hide">"""), "fri_is_closed", layout.HTML("""</div>
                            </div>
                            {% load i18n %}
                            <div class="row row-xs">
                                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">"""), bootstrap.PrependedText("sat_open", ugettext('Sa'), placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">"""), bootstrap.PrependedText("sat_close", "", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                                <div class="closed hide">"""), "sat_is_closed", layout.HTML("""</div>
                            </div>
                            {% load i18n %}
                            <div class="row row-xs">
                                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">"""), bootstrap.PrependedText("sun_open", ugettext('Su'), placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">"""), bootstrap.PrependedText("sun_close", "", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                                <div class="closed hide">"""), "sun_is_closed", layout.HTML("""</div>
                            </div>
                        </fieldset>
                    </div>
                    {% load i18n %}
                    <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">
                        <fieldset>
                            <legend>{% trans "Breaks" %}</legend>
                            <div class="row row-xs">
                                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6"><label>{% blocktrans with time="" %}From {{ time }}{% endblocktrans %}</label></div>
                                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6"><label>{% blocktrans with time="" %}To {{ time }}{% endblocktrans %}</label></div>
                            </div>
                            <div class="row row-xs">
                                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">"""), bootstrap.PrependedText("mon_break_close", ugettext('Mo'), placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">"""), bootstrap.PrependedText("mon_break_open", "", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            </div>
                                {% load i18n %}
                            <div class="row row-xs">
                                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">"""), bootstrap.PrependedText("tue_break_close", ugettext('Tu'), placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">"""), bootstrap.PrependedText("tue_break_open", "", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            </div>
                                {% load i18n %}
                            <div class="row row-xs">
                                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">"""), bootstrap.PrependedText("wed_break_close", ugettext('We'), placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">"""), bootstrap.PrependedText("wed_break_open", "", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            </div>
                                {% load i18n %}
                            <div class="row row-xs">
                                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">"""), bootstrap.PrependedText("thu_break_close", ugettext('Th'), placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">"""), bootstrap.PrependedText("thu_break_open", "", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            </div>
                                {% load i18n %}
                            <div class="row row-xs">
                                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">"""), bootstrap.PrependedText("fri_break_close", ugettext('Fr'), placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">"""), bootstrap.PrependedText("fri_break_open", "", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            </div>
                                {% load i18n %}
                            <div class="row row-xs">
                                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">"""), bootstrap.PrependedText("sat_break_close", ugettext('Sa'), placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">"""), bootstrap.PrependedText("sat_break_open", "", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            </div>
                                {% load i18n %}
                            <div class="row row-xs">
                                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">"""), bootstrap.PrependedText("sun_break_close", ugettext('Su'), placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">"""), bootstrap.PrependedText("sun_break_open", "", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            </div>
                        </fieldset>
                    </div>
                </div>
            """),
            css_class="fieldset-season no-legend",
        ))
        fieldset_content.append(
            layout.Field('id'),
        )
        layout_blocks.append(layout.Fieldset(
            _("Additional info"),
            css_class="fieldset-additional-info",
            *fieldset_content
        ))

        self.helper.layout = layout.Layout(
            *layout_blocks
        )

SeasonFormset = inlineformset_factory(Exhibition, Season, form=SeasonForm, formset=InlineFormSet, extra=0)


class PricesForm(ModelForm):
    admission_price = DecimalField(
        label=_(u"Admission price (€)"),
        max_digits=5,
        decimal_places=2,
        required=False,
    )
    reduced_price = DecimalField(
        label=_(u"Reduced admission price (€)"),
        max_digits=5,
        decimal_places=2,
        required=False,
    )

    class Meta:
        model = Exhibition
        fields = ['museum_prices', 'free_entrance', 'admission_price', 'reduced_price',]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'admission_price_info_%s' % lang_code,
                'reduced_price_info_%s' % lang_code,
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
                'reduced_price_info_%s' % lang_code,
                'shop_link_%s' % lang_code,
            ]:
                self.fields[f].label += """ <span class="lang">%s</span>""" % lang_code.upper()

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        
        layout_blocks = []

        fieldset_content = []  # collect multilingual divs into one list...
        fieldset_content.append(
            layout.Div('museum_prices', layout.Div('free_entrance', css_class="price-info"), css_class="inline")
        )
        fieldset_content.append(
            layout.Div(
                layout.Field('admission_price', placeholder=decimalfmt(0, "#,##0.00")), css_class="price-info"
            )
        )
        fieldset_content.append(layout.Row(
            css_class="row-md price-info",
            *[layout.Div(
                layout.Field('admission_price_info_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(
            layout.Div(
                layout.Field('reduced_price', placeholder=decimalfmt(0, "#,##0.00")), css_class="price-info"
            )
        )
        fieldset_content.append(layout.Row(
            css_class="row-md price-info",
            *[layout.Div(
                layout.Field('reduced_price_info_%s' % lang_code),
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


class AccessibilityForm(ModelForm):
    class Meta:
        model = Exhibition
        fields = ['suitable_for_disabled',]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'suitable_for_disabled_info_%s' % lang_code,
            ]

    def __init__(self, *args, **kwargs):
        super(AccessibilityForm, self).__init__(*args, **kwargs)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'suitable_for_disabled_info_%s' % lang_code,
            ]:
                self.fields[f].label += """ <span class="lang">%s</span>""" % lang_code.upper()

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        
        layout_blocks = []

        fieldset_content = []  # collect multilingual divs into one list...
        fieldset_content.append(
            'suitable_for_disabled'
        )
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('suitable_for_disabled_info_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))

        layout_blocks.append(layout.Fieldset(
            _("Accessibility"),
            css_class="fieldset-accessibility",
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


class GalleryForm(ModelForm):
    class Meta:
        model = Exhibition
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
            'opening': {'_filled': True, 'sets': {'seasons': [], 'special_openings': []}},
            'prices': {'_filled': True},
            'accessibility': {'_filled': True},
            '_pk': instance.pk,
            '_is_new': False,
        }
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            form_step_data['basic']['title_%s' % lang_code] = getattr(instance, 'title_%s' % lang_code)
            form_step_data['basic']['subtitle_%s' % lang_code] = getattr(instance, 'subtitle_%s' % lang_code)
            form_step_data['basic']['description_%s' % lang_code] = getattr(instance, 'description_%s' % lang_code)
            form_step_data['basic']['press_text_%s' % lang_code] = getattr(instance, 'press_text_%s' % lang_code)
            form_step_data['basic']['website_%s' % lang_code] = getattr(instance, 'website_%s' % lang_code)
            form_step_data['basic']['catalog_%s' % lang_code] = getattr(instance, 'catalog_%s' % lang_code)
            form_step_data['basic']['catalog_ordering_%s' % lang_code] = getattr(instance, 'catalog_ordering_%s' % lang_code)
        form_step_data['basic']['start'] = instance.start
        form_step_data['basic']['end'] = instance.end
        form_step_data['basic']['permanent'] = instance.permanent
        form_step_data['basic']['exhibition_extended'] = instance.exhibition_extended
        if instance.museum:
            form_step_data['basic']['museum'] = instance.museum.pk
        form_step_data['basic']['location_name'] = instance.location_name
        form_step_data['basic']['street_address'] = instance.street_address
        form_step_data['basic']['street_address2'] = instance.street_address2
        form_step_data['basic']['postal_code'] = instance.postal_code
        form_step_data['basic']['city'] = instance.city
        form_step_data['basic']['latitude'] = instance.latitude
        form_step_data['basic']['longitude'] = instance.longitude
        form_step_data['basic']['vernissage'] = instance.vernissage
        form_step_data['basic']['finissage'] = instance.finissage
        form_step_data['basic']['categories'] = instance.categories.all()
        form_step_data['basic']['tags'] = instance.tags
        form_step_data['basic']['is_for_children'] = instance.is_for_children
    
        for organizer in instance.organizer_set.all():
            organizer_dict = {}
            if organizer.organizing_museum:
                organizer_dict['organizing_museum'] = organizer.organizing_museum.pk
            organizer_dict['organizer_title'] = organizer.organizer_title
            organizer_dict['organizer_url_link'] = organizer.organizer_url_link
            form_step_data['basic']['sets']['organizers'].append(organizer_dict)
    
        form_step_data['opening']['museum_opening_hours'] = instance.museum_opening_hours
    
        for season in instance.season_set.all():
            season_dict = {}
            season_dict['id'] = season.pk
            season_dict['is_appointment_based'] = season.is_appointment_based
            season_dict['is_open_24_7'] = season.is_open_24_7
            season_dict['mon_open'] = season.mon_open
            season_dict['mon_break_close'] = season.mon_break_close
            season_dict['mon_break_open'] = season.mon_break_open
            season_dict['mon_close'] = season.mon_close
            season_dict['mon_is_closed'] = not season.mon_open
            season_dict['tue_open'] = season.tue_open
            season_dict['tue_break_close'] = season.tue_break_close
            season_dict['tue_break_open'] = season.tue_break_open
            season_dict['tue_close'] = season.tue_close
            season_dict['tue_is_closed'] = not season.tue_open
            season_dict['wed_open'] = season.wed_open
            season_dict['wed_break_close'] = season.wed_break_close
            season_dict['wed_break_open'] = season.wed_break_open
            season_dict['wed_close'] = season.wed_close
            season_dict['wed_is_closed'] = not season.wed_open
            season_dict['thu_open'] = season.thu_open
            season_dict['thu_break_close'] = season.thu_break_close
            season_dict['thu_break_open'] = season.thu_break_open
            season_dict['thu_close'] = season.thu_close
            season_dict['thu_is_closed'] = not season.thu_open
            season_dict['fri_open'] = season.fri_open
            season_dict['fri_break_close'] = season.fri_break_close
            season_dict['fri_break_open'] = season.fri_break_open
            season_dict['fri_close'] = season.fri_close
            season_dict['fri_is_closed'] = not season.fri_open
            season_dict['sat_open'] = season.sat_open
            season_dict['sat_break_close'] = season.sat_break_close
            season_dict['sat_break_open'] = season.sat_break_open
            season_dict['sat_close'] = season.sat_close
            season_dict['sat_is_closed'] = not season.sat_open
            season_dict['sun_open'] = season.sun_open
            season_dict['sun_break_close'] = season.sun_break_close
            season_dict['sun_break_open'] = season.sun_break_open
            season_dict['sun_close'] = season.sun_close
            season_dict['sun_is_closed'] = not season.sun_open
            for lang_code, lang_name in FRONTEND_LANGUAGES:
                season_dict['last_entry_%s' % lang_code] = getattr(season, 'last_entry_%s' % lang_code)
                season_dict['exceptions_%s' % lang_code] = getattr(season, 'exceptions_%s' % lang_code)
            form_step_data['opening']['sets']['seasons'].append(season_dict)
            
        fields = ['museum_prices', 'free_entrance', 'admission_price', 'reduced_price',]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'admission_price_info_%s' % lang_code,
                'reduced_price_info_%s' % lang_code,
                'shop_link_%s' % lang_code,
            ]
        for f in fields:
            form_step_data['prices'][f] = getattr(instance, f)
    
        form_step_data['accessibility']['suitable_for_disabled'] = instance.suitable_for_disabled
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            form_step_data['accessibility']['suitable_for_disabled_info_%s' % lang_code] = getattr(instance, 'suitable_for_disabled_info_%s' % lang_code)

    return form_step_data


def submit_step(current_step, form_steps, form_step_data, instance=None):
    if current_step == "basic":
        # save the entry
        if "_pk" in form_step_data:
            instance = Exhibition.objects.get(pk=form_step_data['_pk'])
        else:
            instance = Exhibition()
            form_step_data['_is_new'] = True

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            setattr(instance, 'title_%s' % lang_code, form_step_data['basic']['title_%s' % lang_code]) 
            setattr(instance, 'subtitle_%s' % lang_code, form_step_data['basic']['subtitle_%s' % lang_code])
            setattr(instance, 'press_text_%s' % lang_code, form_step_data['basic']['press_text_%s' % lang_code])
            setattr(instance, 'website_%s' % lang_code, form_step_data['basic']['website_%s' % lang_code])
            setattr(instance, 'catalog_%s' % lang_code, form_step_data['basic']['catalog_%s' % lang_code])
            setattr(instance, 'catalog_ordering_%s' % lang_code, form_step_data['basic']['catalog_ordering_%s' % lang_code])
            setattr(instance, 'press_text_%s_markup_type' % lang_code, MARKUP_HTML_WYSIWYG)
            setattr(instance, 'catalog_%s_markup_type' % lang_code, MARKUP_PLAIN_TEXT)
            if not instance.description_locked:
                setattr(instance, 'description_%s' % lang_code, form_step_data['basic']['press_text_%s' % lang_code])
                setattr(instance, 'description_%s_markup_type' % lang_code, MARKUP_HTML_WYSIWYG)
        instance.start = form_step_data['basic']['start'] 
        instance.end = form_step_data['basic']['end']
        instance.permanent = form_step_data['basic']['permanent'] 
        instance.exhibition_extended = form_step_data['basic']['exhibition_extended']
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
        instance.vernissage = form_step_data['basic']['vernissage']
        instance.finissage = form_step_data['basic']['finissage']
        if form_step_data['basic']['tags'] and not form_step_data['basic']['tags'].endswith(","):
            form_step_data['basic']['tags'] = form_step_data['basic']['tags'] + ","
        instance.tags = form_step_data['basic']['tags']
        instance.is_for_children = form_step_data['basic']['is_for_children']
        if not instance.status:
            instance.status = "draft"
        instance.save()

        rel_dir = "exhibitions/%s/" % instance.slug

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
        
        instance.categories.clear()
        for cat in form_step_data['basic']['categories']:
            instance.categories.add(cat)
        
        instance.organizer_set.all().delete()
        for organizer_dict in form_step_data['basic']['sets']['organizers']:
            organizer = Organizer(exhibition=instance)
            if organizer_dict.get('organizing_museum', None):
                organizer.organizing_museum = Museum.objects.get(
                    pk=organizer_dict['organizing_museum'],
                )
                organizer.organizer_title = ""
                organizer.organizer_url_link = ""
            else:
                organizer.organizer_title = organizer_dict.get('organizer_title', "")
                organizer.organizer_url_link = organizer_dict.get('organizer_url_link', "")
                organizer.organizing_museum = None
            organizer.save()
        
        form_step_data['_pk'] = instance.pk
        
        if instance.museum:
            # fill in Opening hours from museum
            if not form_step_data.get('opening', {}).get('_filled', False):
                form_step_data['opening'] = {'_filled': True, 'sets': {'seasons': [], 'special_openings': []}}

                # for season in museum.season_set.all():
                #     season_dict = {}
                #     season_dict['start'] = season.start
                #     season_dict['end'] = season.end
                #     season_dict['is_appointment_based'] = season.is_appointment_based
                #     season_dict['is_open_24_7'] = season.is_open_24_7
                #     season_dict['mon_open'] = season.mon_open
                #     season_dict['mon_break_close'] = season.mon_break_close
                #     season_dict['mon_break_open'] = season.mon_break_open
                #     season_dict['mon_close'] = season.mon_close
                #     season_dict['mon_is_closed'] = not season.mon_open
                #     season_dict['tue_open'] = season.tue_open
                #     season_dict['tue_break_close'] = season.tue_break_close
                #     season_dict['tue_break_open'] = season.tue_break_open
                #     season_dict['tue_close'] = season.tue_close
                #     season_dict['tue_is_closed'] = not season.tue_open
                #     season_dict['wed_open'] = season.wed_open
                #     season_dict['wed_break_close'] = season.wed_break_close
                #     season_dict['wed_break_open'] = season.wed_break_open
                #     season_dict['wed_close'] = season.wed_close
                #     season_dict['wed_is_closed'] = not season.wed_open
                #     season_dict['thu_open'] = season.thu_open
                #     season_dict['thu_break_close'] = season.thu_break_close
                #     season_dict['thu_break_open'] = season.thu_break_open
                #     season_dict['thu_close'] = season.thu_close
                #     season_dict['thu_is_closed'] = not season.thu_open
                #     season_dict['fri_open'] = season.fri_open
                #     season_dict['fri_break_close'] = season.fri_break_close
                #     season_dict['fri_break_open'] = season.fri_break_open
                #     season_dict['fri_close'] = season.fri_close
                #     season_dict['fri_is_closed'] = not season.fri_open
                #     season_dict['sat_open'] = season.sat_open
                #     season_dict['sat_break_close'] = season.sat_break_close
                #     season_dict['sat_break_open'] = season.sat_break_open
                #     season_dict['sat_close'] = season.sat_close
                #     season_dict['sat_is_closed'] = not season.sat_open
                #     season_dict['sun_open'] = season.sun_open
                #     season_dict['sun_break_close'] = season.sun_break_close
                #     season_dict['sun_break_open'] = season.sun_break_open
                #     season_dict['sun_close'] = season.sun_close
                #     season_dict['sun_is_closed'] = not season.sun_open
                #     for lang_code, lang_name in FRONTEND_LANGUAGES:
                #         season_dict['title_%s' % lang_code] = getattr(season, 'title_%s' % lang_code)
                #         season_dict['last_entry_%s' % lang_code] = getattr(season, 'last_entry_%s' % lang_code)
                #         season_dict['exceptions_%s' % lang_code] = getattr(season, 'exceptions_%s' % lang_code)
                #     form_step_data['opening']['sets']['seasons'].append(season_dict)
                #
                # for special_opening in museum.specialopeningtime_set.all():
                #     special_opening_dict = {}
                #     special_opening_dict['yyyy'] = special_opening.yyyy
                #     special_opening_dict['get_yyyy_display'] = special_opening.get_yyyy_display()
                #     special_opening_dict['mm'] = special_opening.mm
                #     special_opening_dict['get_mm_display'] = special_opening.get_mm_display()
                #     special_opening_dict['dd'] = special_opening.dd
                #     special_opening_dict['get_dd_display'] = special_opening.get_dd_display()
                #     for lang_code, lang_name in FRONTEND_LANGUAGES:
                #         special_opening_dict['day_label_%s' % lang_code] = getattr(special_opening, 'day_label_%s' % lang_code)
                #         special_opening_dict['exceptions_%s' % lang_code] = getattr(special_opening, 'exceptions_%s' % lang_code)
                #     special_opening_dict['is_closed'] = special_opening.is_closed
                #     special_opening_dict['is_regular'] = special_opening.is_regular
                #     special_opening_dict['opening'] = special_opening.opening
                #     special_opening_dict['break_close'] = special_opening.break_close
                #     special_opening_dict['break_open'] = special_opening.break_open
                #     special_opening_dict['closing'] = special_opening.closing
                #     form_step_data['opening']['sets']['special_openings'].append(special_opening_dict)

            # fill in prices from museum
            if not form_step_data.get('prices', {}).get('_filled', False):
                form_step_data['prices'] = {'_filled': True}
                fields = ['free_entrance', 'admission_price', 'reduced_price',]
                for lang_code, lang_name in FRONTEND_LANGUAGES:
                    fields += [
                        'admission_price_info_%s' % lang_code,
                        'reduced_price_info_%s' % lang_code,
                    ]
                for f in fields:
                    form_step_data['prices'][f] = getattr(instance.museum, f)
                form_step_data['prices']['museum_prices'] = True
    
    if current_step == "opening":
        if "_pk" in form_step_data:
            instance = Exhibition.objects.get(pk=form_step_data['_pk'])

            instance.museum_opening_hours = form_step_data['opening']['museum_opening_hours'] 
            instance.save()

            season_ids_to_keep = []
            for season_dict in form_step_data['opening']['sets']['seasons']:
                if season_dict['id']:
                    try:
                        season = Season.objects.get(
                            pk=season_dict['id'],
                            exhibition=instance,
                        )
                    except models.ObjectDoesNotExist:
                        continue
                else:
                    season = Season(exhibition=instance)
                season.is_appointment_based = season_dict['is_appointment_based']
                season.is_open_24_7 = season_dict['is_open_24_7'] 
                #if not season_dict['mon_is_closed']:
                season.mon_open = season_dict['mon_open'] 
                season.mon_break_close = season_dict['mon_break_close'] 
                season.mon_break_open = season_dict['mon_break_open']
                season.mon_close = season_dict['mon_close']
                #if not season_dict['tue_is_closed']:
                season.tue_open = season_dict['tue_open'] 
                season.tue_break_close = season_dict['tue_break_close'] 
                season.tue_break_open = season_dict['tue_break_open'] 
                season.tue_close = season_dict['tue_close'] 
                #if not season_dict['wed_is_closed']:
                season.wed_open = season_dict['wed_open']
                season.wed_break_close = season_dict['wed_break_close'] 
                season.wed_break_open = season_dict['wed_break_open'] 
                season.wed_close = season_dict['wed_close'] 
                #if not season_dict['thu_is_closed']:
                season.thu_open = season_dict['thu_open'] 
                season.thu_break_close = season_dict['thu_break_close'] 
                season.thu_break_open = season_dict['thu_break_open'] 
                season.thu_close = season_dict['thu_close'] 
                #if not season_dict['fri_is_closed']:
                season.fri_open = season_dict['fri_open'] 
                season.fri_break_close = season_dict['fri_break_close'] 
                season.fri_break_open = season_dict['fri_break_open'] 
                season.fri_close = season_dict['fri_close'] 
                #if not season_dict['sat_is_closed']:
                season.sat_open = season_dict['sat_open']
                season.sat_break_close = season_dict['sat_break_close'] 
                season.sat_break_open = season_dict['sat_break_open']
                season.sat_close = season_dict['sat_close']
                #if not season_dict['sun_is_closed']:
                season.sun_open = season_dict['sun_open'] 
                season.sun_break_close = season_dict['sun_break_close'] 
                season.sun_break_open = season_dict['sun_break_open'] 
                season.sun_close = season_dict['sun_close']
                for lang_code, lang_name in FRONTEND_LANGUAGES:
                    setattr(season, 'last_entry_%s' % lang_code, season_dict['last_entry_%s' % lang_code])
                    setattr(season, 'exceptions_%s' % lang_code, season_dict['exceptions_%s' % lang_code])
                    setattr(season, 'exceptions_%s_markup_type' % lang_code, MARKUP_PLAIN_TEXT)
                season.save()
                season_ids_to_keep.append(season.pk)
            instance.season_set.exclude(pk__in=season_ids_to_keep).delete()

    if current_step == "prices":
        if "_pk" in form_step_data:
            instance = Exhibition.objects.get(pk=form_step_data['_pk'])

            fields = ['museum_prices', 'free_entrance', 'admission_price', 'reduced_price',]
            for lang_code, lang_name in FRONTEND_LANGUAGES:
                fields += [
                    'admission_price_info_%s' % lang_code,
                    'reduced_price_info_%s' % lang_code,
                    'shop_link_%s' % lang_code,
                ]
            for f in fields:
                setattr(instance, f, form_step_data['prices'][f])
        
            for lang_code, lang_name in FRONTEND_LANGUAGES:
                for f in [
                    'admission_price_info_%s' % lang_code,
                    'reduced_price_info_%s' % lang_code,
                ]:
                    setattr(instance, f + "_markup_type", MARKUP_PLAIN_TEXT)

            instance.save()

    if current_step == "accessibility":
        if "_pk" in form_step_data:
            instance = Exhibition.objects.get(pk=form_step_data['_pk'])

            instance.suitable_for_disabled = form_step_data['accessibility']['suitable_for_disabled']
            for lang_code, lang_name in FRONTEND_LANGUAGES:
                setattr(instance, 'suitable_for_disabled_info_%s' % lang_code, form_step_data['accessibility']['suitable_for_disabled_info_%s' % lang_code])
            
            instance.save()

    # finally all exhibition will be saved and published by save_data()
    return form_step_data


def set_extra_context(current_step, form_steps, form_step_data, instance=None, request=None):
    if "_pk" in form_step_data:
        return {'exhibition': Exhibition.objects.get(pk=form_step_data['_pk'])}
    return {}


def save_data(form_steps, form_step_data, instance=None):
    is_new = form_step_data.get('_is_new', False)

    if not instance:
        if '_pk' in form_step_data:
            instance = Exhibition.objects.get(pk=form_step_data['_pk'])
        else:
            instance = Exhibition()
    for lang_code, lang_name in FRONTEND_LANGUAGES:
        setattr(instance, 'title_%s' % lang_code, form_step_data['basic']['title_%s' % lang_code]) 
        setattr(instance, 'subtitle_%s' % lang_code, form_step_data['basic']['subtitle_%s' % lang_code])
        setattr(instance, 'press_text_%s' % lang_code, form_step_data['basic']['press_text_%s' % lang_code])
        setattr(instance, 'website_%s' % lang_code, form_step_data['basic']['website_%s' % lang_code])
        setattr(instance, 'catalog_%s' % lang_code, form_step_data['basic']['catalog_%s' % lang_code])
        setattr(instance, 'catalog_ordering_%s' % lang_code, form_step_data['basic']['catalog_ordering_%s' % lang_code])
        setattr(instance, 'press_text_%s_markup_type' % lang_code, MARKUP_HTML_WYSIWYG)
        setattr(instance, 'catalog_%s_markup_type' % lang_code, MARKUP_PLAIN_TEXT)
        if not instance.description_locked: 
            setattr(instance, 'description_%s' % lang_code, form_step_data['basic']['press_text_%s' % lang_code])
            setattr(instance, 'description_%s_markup_type' % lang_code, MARKUP_HTML_WYSIWYG)
            
    instance.start = form_step_data['basic']['start'] 
    instance.end = form_step_data['basic']['end']
    instance.permanent = form_step_data['basic']['permanent'] 
    instance.exhibition_extended = form_step_data['basic']['exhibition_extended']
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
    instance.vernissage = form_step_data['basic']['vernissage']
    instance.finissage = form_step_data['basic']['finissage']
    if form_step_data['basic']['tags'] and not form_step_data['basic']['tags'].endswith(","):
        form_step_data['basic']['tags'] = form_step_data['basic']['tags'] + ","
    instance.tags = form_step_data['basic']['tags']
    instance.is_for_children = form_step_data['basic']['is_for_children']

    instance.museum_opening_hours = form_step_data['opening']['museum_opening_hours'] 

    fields = ['museum_prices', 'free_entrance', 'admission_price', 'reduced_price',]
    for lang_code, lang_name in FRONTEND_LANGUAGES:
        fields += [
            'admission_price_info_%s' % lang_code,
            'reduced_price_info_%s' % lang_code,
            'shop_link_%s' % lang_code,
        ]
    for f in fields:
        setattr(instance, f, form_step_data['prices'][f])

    for lang_code, lang_name in FRONTEND_LANGUAGES:
        for f in [
            'admission_price_info_%s' % lang_code,
            'reduced_price_info_%s' % lang_code,
        ]:
            setattr(instance, f + "_markup_type", MARKUP_PLAIN_TEXT)

    instance.suitable_for_disabled = form_step_data['accessibility']['suitable_for_disabled']
    for lang_code, lang_name in FRONTEND_LANGUAGES:
        setattr(instance, 'suitable_for_disabled_info_%s' % lang_code, form_step_data['accessibility']['suitable_for_disabled_info_%s' % lang_code])

    if is_new:
        instance.status = "published"
    instance.save()
    
    #if is_new:
    #    user = get_current_user()
    #    instance.set_owner(user)
    
    instance.categories.clear()
    for cat in form_step_data['basic']['categories']:
        instance.categories.add(cat)

    instance.organizer_set.all().delete()
    for organizer_dict in form_step_data['basic']['sets']['organizers']:
        organizer = Organizer(exhibition=instance)
        if organizer_dict.get('organizing_museum', None):
            try:
                organizer.organizing_museum = Museum.objects.get(pk=organizer_dict['organizing_museum'])
            except:
                pass
        organizer.organizer_title = organizer_dict.get('organizer_title', "")
        organizer.organizer_url_link = organizer_dict.get('organizer_url_link', "")
        organizer.save()

    season_ids_to_keep = []
    for season_dict in form_step_data['opening']['sets']['seasons']:
        if season_dict['id']:
            try:
                season = Season.objects.get(
                    pk=season_dict['id'],
                    exhibition=instance,
                )
            except models.ObjectDoesNotExist:
                continue
        else:
            season = Season(exhibition=instance)
        season.is_appointment_based = season_dict['is_appointment_based'] 
        season.is_open_24_7 = season_dict['is_open_24_7'] 
        #if not season_dict['mon_is_closed']:
        season.mon_open = season_dict['mon_open'] 
        season.mon_break_close = season_dict['mon_break_close'] 
        season.mon_break_open = season_dict['mon_break_open']
        season.mon_close = season_dict['mon_close']
        #if not season_dict['tue_is_closed']:
        season.tue_open = season_dict['tue_open'] 
        season.tue_break_close = season_dict['tue_break_close'] 
        season.tue_break_open = season_dict['tue_break_open'] 
        season.tue_close = season_dict['tue_close'] 
        #if not season_dict['wed_is_closed']:
        season.wed_open = season_dict['wed_open']
        season.wed_break_close = season_dict['wed_break_close'] 
        season.wed_break_open = season_dict['wed_break_open'] 
        season.wed_close = season_dict['wed_close'] 
        #if not season_dict['thu_is_closed']:
        season.thu_open = season_dict['thu_open'] 
        season.thu_break_close = season_dict['thu_break_close'] 
        season.thu_break_open = season_dict['thu_break_open'] 
        season.thu_close = season_dict['thu_close'] 
        #if not season_dict['fri_is_closed']:
        season.fri_open = season_dict['fri_open'] 
        season.fri_break_close = season_dict['fri_break_close'] 
        season.fri_break_open = season_dict['fri_break_open'] 
        season.fri_close = season_dict['fri_close'] 
        #if not season_dict['sat_is_closed']:
        season.sat_open = season_dict['sat_open']
        season.sat_break_close = season_dict['sat_break_close'] 
        season.sat_break_open = season_dict['sat_break_open']
        season.sat_close = season_dict['sat_close']
        #if not season_dict['sun_is_closed']:
        season.sun_open = season_dict['sun_open'] 
        season.sun_break_close = season_dict['sun_break_close'] 
        season.sun_break_open = season_dict['sun_break_open'] 
        season.sun_close = season_dict['sun_close']
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            setattr(season, 'last_entry_%s' % lang_code, season_dict['last_entry_%s' % lang_code])
            setattr(season, 'exceptions_%s' % lang_code, season_dict['exceptions_%s' % lang_code])
            setattr(season, 'exceptions_%s_markup_type' % lang_code, MARKUP_PLAIN_TEXT)
        season.save()
        season_ids_to_keep.append(season.pk)
    instance.season_set.exclude(pk__in=season_ids_to_keep).delete()

    form_steps['success_url'] = reverse("dashboard") #instance.get_url_path()
    
    return form_step_data


def cancel_editing(request):
    return redirect("dashboard")


EXHIBITION_FORM_STEPS = {
    'basic': {
        'title': _("Basic Information"),
        'template': "exhibitions/forms/basic_info_form.html",
        'form': BasicInfoForm,
        'formsets': {
            'organizers': OrganizerFormset,
        }
    },
    'opening': {
        'title': _("Opening hours"),
        'template': "exhibitions/forms/opening_form.html",
        'form': OpeningForm, # dummy form
        'formsets': {
            'seasons': SeasonFormset,
        }
    },
    'prices': {
        'title': _("Admission"),
        'template': "exhibitions/forms/prices_form.html",
        'form': PricesForm,
    },
    'accessibility': {
        'title': _("Accessibility"),
        'template': "exhibitions/forms/accessibility_form.html",
        'form': AccessibilityForm,
    },
    'gallery': {
        'title': _("Images"),
        'template': "exhibitions/forms/gallery_form.html",
        'form': GalleryForm, # dummy form
    },
    'oninit': load_data,
    'on_set_extra_context': set_extra_context,
    'onsubmit': submit_step,
    'onsave': save_data,
    'onreset': cancel_editing,
    'general_error_message': _("There are errors in this form. Please correct them and try to save again."),
    'name': 'exhibition_registration',
    'default_path': ["basic", "opening", "prices", "accessibility", 'gallery'],
}

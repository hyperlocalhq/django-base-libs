# -*- coding: utf-8 -*-

from django.db import models
from django import forms
from django.forms.models import ModelForm
from django.forms.models import inlineformset_factory
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from babeldjango.templatetags.babel import decimalfmt

from base_libs.forms.fields import AutocompleteModelChoiceField, DecimalField
from base_libs.models.settings import MARKUP_HTML_WYSIWYG, MARKUP_PLAIN_TEXT
from base_libs.middleware import get_current_user

Museum = models.get_model("museums", "Museum")
Exhibition = models.get_model("exhibitions", "Exhibition")
ExhibitionCategory = models.get_model("exhibitions", "ExhibitionCategory")
Season = models.get_model("exhibitions", "Season")
Organizer = models.get_model("exhibitions", "Organizer")

FRONTEND_LANGUAGES = getattr(settings, "FRONTEND_LANGUAGES", settings.LANGUAGES) 

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
        display_attr="title",
        add_display_attr="get_address",
        options={
            "minChars": 1,
            "max": 20,
            "mustMatch": 1,
            "highlight" : False,
            "multipleSeparator": ",,, ",
            },
        )
    categories = ModelMultipleChoiceTreeField(
        label=_("Categories"),
        required=False,
        queryset=ExhibitionCategory.objects.all(),
        )
    class Meta:
        model = Exhibition
        
        fields = ['start', 'end', 'permanent', 'exhibition_extended',
            'museum', 'location_name', 'street_address', 'street_address2', 'postal_code', 'district',
            'city', 'latitude', 'longitude',  
            'vernissage', 'finissage', 'tags', 'categories', "is_for_children",
            ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'title_%s' % lang_code,
                'subtitle_%s' % lang_code,
                'description_%s' % lang_code,
                'website_%s' % lang_code,
                'catalog_%s' % lang_code,
                'catalog_ordering_%s' % lang_code,
                ]
    def __init__(self, *args, **kwargs):
        super(BasicInfoForm, self).__init__(*args, **kwargs)

        self.fields['vernissage'].widget = SplitDateTimeWidget(time_format='%H:%M')
        self.fields['finissage'].widget = SplitDateTimeWidget(time_format='%H:%M')

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
                'description_%s' % lang_code,
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

        layout_blocks.append(layout.Fieldset(
            _("Basic Info"),
            layout.Row(
                css_class="div-title",
                *('title_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),
            layout.Row(
                css_class="div-subtitle",
                *('subtitle_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),
            layout.Row(
                css_class="div-description",
                *(layout.Field('description_%s' % lang_code, css_class="tinymce") for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),
            layout.Row(
                css_class="div-website",
                *(layout.Field('website_%s' % lang_code, placeholder="http://") for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),
            layout.Row(
                css_class="div-catalog",
                *('catalog_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),
            layout.Row(
                css_class="div-catalog",
                *(layout.Field('catalog_ordering_%s' % lang_code, placeholder="http://") for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),
            css_class="fieldset-basic-info",
            ))

        layout_blocks.append(layout.Fieldset(
            _("Duration"),
            layout.Row(
                layout.Field("start", placeholder="yyyy-mm-dd", autocomplete="off"),
                layout.Field("end", placeholder="yyyy-mm-dd", autocomplete="off"),
            ),
            layout.Field("vernissage", autocomplete="off"),
            layout.Field("finissage", autocomplete="off"),
            layout.Div(
                "permanent",
                "exhibition_extended",
                css_class="inline",
                ),
            css_class="fieldset-when",
            ))
        layout_blocks.append(layout.Fieldset(
            _("Location"),
            layout.Row(
                layout.Div(
                "museum",
                "location_name",
                "street_address",
                "street_address2",
                "postal_code",
                "district",
                "city",
                ),
                layout.HTML("""{% load i18n %}
                    <div id="dyn_set_map">
                        <label>{% trans "Location" %}</label>
                        <div class="exhibition_map" id="gmap_wrapper">
                            <!-- THE GMAPS WILL BE INSERTED HERE DYNAMICALLY -->
                        </div>
                        <div class="form-actions">
                            <input id="dyn_locate_geo" type="button" class="btn btn-small" value="{% trans "Relocate on map" %}" />&zwnj;
                            <!--<input id="dyn_remove_geo" type="button" class="btn btn-small" value="{% trans "Remove from map" %}"/>&zwnj;-->
                        </div>
                    </div>
                """),
                "latitude",
                "longitude",
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
            _("Categories and Tags"),
            layout.Div("categories"),

            layout.Div(
                layout.HTML("""{% load i18n %} <label>{% trans "Particularities" %}</label> """),
                "is_for_children", 
                css_class="inline"
                ),

            layout.Row("tags"),
            css_class="fieldset-categories-tags",
            ))
        if self.instance and self.instance.pk:
            layout_blocks.append(bootstrap.FormActions(
                layout.Submit('submit', _('Next')),
                SecondarySubmit('save_and_close', _('Close')),
                SecondarySubmit('reset', _('Cancel')),
                ))
        else:
            layout_blocks.append(bootstrap.FormActions(
                layout.Submit('submit', _('Next')),
                SecondarySubmit('reset', _('Cancel')),
                ))
        
        self.helper.layout = layout.Layout(
            *layout_blocks
            )

class OrganizerForm(ModelForm):
    organizing_museum = AutocompleteModelChoiceField(
        required=False,
        label=_("Museum from the list <b>(active)</b> / <a href=\"#\">Other Organizer</a>"),
        # help_text=_("If organizer doesn't exist in the database, please click <a href=\"#\">here</a> to enter it."),
        app="museums",
        qs_function="get_published_museums",
        display_attr="title",
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
                layout.Row(
                    layout.Div("organizing_museum", css_class="max"), 
                    css_class="flex",
                    ),
                layout.Row(
                    layout.Div("organizer_title"),
                    layout.Div(layout.Field("organizer_url_link", placeholder="http://"), css_class="max"),
                    css_class="flex",
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
                    <a class="add" id="add_season" href="#">{% trans "Add Individual Opening Hours" %}</a>
                    <legend>{% trans "Opening Hours" %}</legend>
                    <ul id="season_list">
                        <li> </li>
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
                layout.Submit('submit', _('Next')),
                SecondarySubmit('save_and_close', _('Close')),
                SecondarySubmit('reset', _('Cancel')),
                ))
        else:
            layout_blocks.append(bootstrap.FormActions(
                layout.Submit('submit', _('Next')),
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
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            exclude.append("exceptions_%s_markup_type" % lang_code)
        
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
        layout_blocks.append(layout.Fieldset(
            _("Season"),
            layout.Div(
                "is_appointment_based", 
                "is_open_24_7",
                css_class="inline",
                ),

            layout.HTML(
            """{% load i18n %}
            <div class="row">
                <div>
                    <fieldset>
                        <legend>{% trans "Opening Hours" %}</legend>
                        <div class="row">
                            <div><label>{% blocktrans with time="" %}From {{ time }}{% endblocktrans %}</label></div>
                            <div><label>{% blocktrans with time="" %}To {{ time }}{% endblocktrans %}</label></div>
                        </div>
                         <div class="row">
                            <div class="has_weekday"><label class="weekday">{% trans "Mo" %}</label>"""), layout.Field("mon_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div>"""), layout.Field("mon_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div class="closed">"""), "mon_is_closed", layout.HTML("""</div>
                        </div>
                        {% load i18n %}
                        <div class="row">
                            <div class="has_weekday"><label class="weekday">{% trans "Tu" %}</label>"""), layout.Field("tue_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div>"""), layout.Field("tue_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div class="closed">"""), "tue_is_closed", layout.HTML("""</div>
                        </div>
                        {% load i18n %}
                        <div class="row">
                            <div class="has_weekday"><label class="weekday">{% trans "We" %}</label>"""), layout.Field("wed_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div>"""), layout.Field("wed_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div class="closed">"""), "wed_is_closed", layout.HTML("""</div>
                        </div>
                        {% load i18n %}
                        <div class="row">
                            <div class="has_weekday"><label class="weekday">{% trans "Th" %}</label>"""), layout.Field("thu_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div>"""), layout.Field("thu_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div class="closed">"""), "thu_is_closed", layout.HTML("""</div>
                        </div>
                        {% load i18n %}
                        <div class="row">
                            <div class="has_weekday"><label class="weekday">{% trans "Fr" %}</label>"""), layout.Field("fri_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div>"""), layout.Field("fri_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div class="closed">"""), "fri_is_closed", layout.HTML("""</div>
                        </div>
                        {% load i18n %}
                        <div class="row">
                            <div class="has_weekday"><label class="weekday">{% trans "Sa" %}</label>"""), layout.Field("sat_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div>"""), layout.Field("sat_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div class="closed">"""), "sat_is_closed", layout.HTML("""</div>
                        </div>
                        {% load i18n %}
                        <div class="row">
                            <div class="has_weekday"><label class="weekday">{% trans "Su" %}</label>"""), layout.Field("sun_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div>"""), layout.Field("sun_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div class="closed">"""), "sun_is_closed", layout.HTML("""</div>
                        </div>
                    </fieldset>
                </div>
                {% load i18n %}
                <div>
                    <fieldset>
                        <legend>{% trans "Breaks" %}</legend>
                        <div class="row">
                            <div><label>{% blocktrans with time="" %}From {{ time }}{% endblocktrans %}</label></div>
                            <div><label>{% blocktrans with time="" %}To {{ time }}{% endblocktrans %}</label></div>
                        </div>
                        <div class="row">
                            <div class="has_weekday"><label class="weekday">{% trans "Mo" %}</label>"""), layout.Field("mon_break_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div>"""), layout.Field("mon_break_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                        </div>
                            {% load i18n %}
                        <div class="row">
                            <div class="has_weekday"><label class="weekday">{% trans "Tu" %}</label>"""), layout.Field("tue_break_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div>"""), layout.Field("tue_break_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                        </div>
                            {% load i18n %}
                        <div class="row">
                            <div class="has_weekday"><label class="weekday">{% trans "We" %}</label>"""), layout.Field("wed_break_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div>"""), layout.Field("wed_break_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                        </div>
                            {% load i18n %}
                        <div class="row">
                            <div class="has_weekday"><label class="weekday">{% trans "Th" %}</label>"""), layout.Field("thu_break_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div>"""), layout.Field("thu_break_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                        </div>
                            {% load i18n %}
                        <div class="row">
                            <div class="has_weekday"><label class="weekday">{% trans "Fr" %}</label>"""), layout.Field("fri_break_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div>"""), layout.Field("fri_break_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                        </div>
                            {% load i18n %}
                        <div class="row">
                            <div class="has_weekday"><label class="weekday">{% trans "Sa" %}</label>"""), layout.Field("sat_break_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div>"""), layout.Field("sat_break_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                        </div>
                            {% load i18n %}
                        <div class="row">
                            <div class="has_weekday"><label class="weekday">{% trans "Su" %}</label>"""), layout.Field("sun_break_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div>"""), layout.Field("sun_break_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                        </div>
                    </fieldset>
                </div>
            </div>
            """
            ),

            css_class="fieldset-season",
            ))

        layout_blocks.append(layout.Fieldset(
            _("Additional info"),
            layout.Row(
                css_class="div-accessibility-details",
                *('last_entry_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

            layout.Row(
                css_class="div-accessibility-details",
                *('exceptions_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

                css_class="fieldset-additional-info",
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
        fields = ['museum_prices', 'free_entrance', 'admission_price', 'reduced_price',
            ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'admission_price_info_%s' % lang_code,
                'reduced_price_info_%s' % lang_code,
                ]
    def __init__(self, *args, **kwargs):
        super(PricesForm, self).__init__(*args, **kwargs)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'admission_price_info_%s' % lang_code,
                'reduced_price_info_%s' % lang_code,
                ]:
                self.fields[f].label += """ <span class="lang">%s</span>""" % lang_code.upper()

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        
        layout_blocks = []
        layout_blocks.append(layout.Fieldset(
            _("Prices"),
            layout.Div('museum_prices', 'free_entrance', css_class="inline"), 
            layout.Field('admission_price', placeholder=decimalfmt(0, "#,##0.00")),
            layout.Row(
                *('admission_price_info_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),
            css_class="fieldset-prices",
            ))
        layout_blocks.append(layout.Fieldset(
            _("Reduced Prices"),
            layout.Field('reduced_price', placeholder=decimalfmt(0, "#,##0.00")),
            layout.Row(
                *('reduced_price_info_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),
            ))

        if self.instance and self.instance.pk:
            layout_blocks.append(bootstrap.FormActions(
                layout.Submit('submit', _('Next')),
                SecondarySubmit('save_and_close', _('Close')),
                SecondarySubmit('reset', _('Cancel')),
                ))
        else:
            layout_blocks.append(bootstrap.FormActions(
                layout.Submit('submit', _('Next')),
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

        layout_blocks.append(layout.Fieldset(
            _("Accessibility"),
            'suitable_for_disabled',

            layout.Row(
                css_class="div-accessibility-details",
                *('suitable_for_disabled_info_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),
            
            css_class="fieldset-accessibility",
            ))

        if self.instance and self.instance.pk:
            layout_blocks.append(bootstrap.FormActions(
                layout.Submit('submit', _('Next')),
                SecondarySubmit('save_and_close', _('Close')),
                SecondarySubmit('reset', _('Cancel')),
                ))
        else:
            layout_blocks.append(bootstrap.FormActions(
                layout.Submit('submit', _('Next')),
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
                layout.Submit('save_and_close', _('Close')),
                SecondarySubmit('reset', _('Cancel')),
                ))
        else:
            layout_blocks.append(bootstrap.FormActions(
                layout.Submit('submit', _('Save')),
                SecondarySubmit('reset', _('Cancel')),
                ))
        self.helper.layout = layout.Layout(
            *layout_blocks
            )


def load_data(instance=None):
    form_step_data = {}
    if instance:
        form_step_data = {
            'basic': {'_filled': True, 'sets': {'organizers': []}},
            'opening': {'_filled': True, 'sets': {'seasons': [], 'special_openings': []}},
            'prices': {'_filled': True},
            'accessibility': {'_filled': True},
            '_pk': instance.pk,
            }
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            form_step_data['basic']['title_%s' % lang_code] = getattr(instance, 'title_%s' % lang_code)
            form_step_data['basic']['subtitle_%s' % lang_code] = getattr(instance, 'subtitle_%s' % lang_code)
            form_step_data['basic']['description_%s' % lang_code] = getattr(instance, 'description_%s' % lang_code)
            form_step_data['basic']['website_%s' % lang_code] = getattr(instance, 'website_%s' % lang_code)
            form_step_data['basic']['catalog_%s' % lang_code] = getattr(instance, 'catalog_%s' % lang_code)
            form_step_data['basic']['catalog_ordering_%s' % lang_code] = getattr(instance, 'catalog_ordering_%s' % lang_code)
        form_step_data['basic']['start'] = instance.start
        form_step_data['basic']['end'] = instance.end
        form_step_data['basic']['permanent'] = instance.permanent
        form_step_data['basic']['exhibition_extended'] = instance.exhibition_extended
        form_step_data['basic']['museum'] = instance.museum
        form_step_data['basic']['location_name'] = instance.location_name
        form_step_data['basic']['street_address'] = instance.street_address
        form_step_data['basic']['street_address2'] = instance.street_address2
        form_step_data['basic']['postal_code'] = instance.postal_code
        form_step_data['basic']['district'] = instance.district
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
            organizer_dict['organizing_museum'] = organizer.organizing_museum
            organizer_dict['organizer_title'] = organizer.organizer_title
            organizer_dict['organizer_url_link'] = organizer.organizer_url_link
            form_step_data['basic']['sets']['organizers'].append(organizer_dict)
    
        form_step_data['opening']['museum_opening_hours'] = instance.museum_opening_hours
    
        for season in instance.season_set.all():
            season_dict = {}
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
            
        fields = ['museum_prices', 'free_entrance', 'admission_price', 'reduced_price', 
            ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'admission_price_info_%s' % lang_code,
                'reduced_price_info_%s' % lang_code,
                ]
        for f in fields:
            form_step_data['prices'][f] = getattr(instance, f)
    
        form_step_data['accessibility']['suitable_for_disabled'] = instance.suitable_for_disabled
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            form_step_data['accessibility']['suitable_for_disabled_info_%s' % lang_code] = getattr(instance, 'suitable_for_disabled_info_%s' % lang_code)

    return form_step_data

def submit_step(current_step, form_steps, form_step_data, instance=None):
    museum = form_step_data.get('basic', {}).get('museum', None)
    if current_step == "basic":
        # save the entry
        if "_pk" in form_step_data:
            instance = Exhibition.objects.get(pk=form_step_data['_pk'])
        else:
            instance = Exhibition()
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            setattr(instance, 'title_%s' % lang_code, form_step_data['basic']['title_%s' % lang_code]) 
            setattr(instance, 'subtitle_%s' % lang_code, form_step_data['basic']['subtitle_%s' % lang_code])
            setattr(instance, 'description_%s' % lang_code, form_step_data['basic']['description_%s' % lang_code])
            setattr(instance, 'website_%s' % lang_code, form_step_data['basic']['website_%s' % lang_code])
            setattr(instance, 'catalog_%s' % lang_code, form_step_data['basic']['catalog_%s' % lang_code])
            setattr(instance, 'catalog_ordering_%s' % lang_code, form_step_data['basic']['catalog_ordering_%s' % lang_code])
            setattr(instance, 'description_%s_markup_type' % lang_code, MARKUP_HTML_WYSIWYG)
            setattr(instance, 'catalog_%s_markup_type' % lang_code, MARKUP_PLAIN_TEXT)
        instance.start = form_step_data['basic']['start'] 
        instance.end = form_step_data['basic']['end']
        instance.permanent = form_step_data['basic']['permanent'] 
        instance.exhibition_extended = form_step_data['basic']['exhibition_extended'] 
        instance.museum = museum
        instance.location_name = form_step_data['basic']['location_name']
        instance.street_address = form_step_data['basic']['street_address']
        instance.street_address2 = form_step_data['basic']['street_address2'] 
        instance.postal_code = form_step_data['basic']['postal_code']
        instance.district = form_step_data['basic']['district']
        instance.city = form_step_data['basic']['city']
        instance.latitude = form_step_data['basic']['latitude']
        instance.longitude = form_step_data['basic']['longitude']
        instance.vernissage = form_step_data['basic']['vernissage']
        instance.finissage = form_step_data['basic']['finissage']
        instance.tags = form_step_data['basic']['tags']
        instance.is_for_children = form_step_data['basic']['is_for_children']
        if not instance.status:
            instance.status = "draft"
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
            organizer.organizing_museum = organizer_dict['organizing_museum'] 
            organizer.organizer_title = organizer_dict['organizer_title']
            organizer.organizer_url_link = organizer_dict['organizer_url_link']
            organizer.save()
        
        form_step_data['_pk'] = instance.pk
        
    if current_step == "basic" and museum:
        # fill in Opening hours from museum
        if not form_step_data.get('opening', {}).get('_filled', False):
            form_step_data['opening'] = {'_filled': True, 'sets': {'seasons': [], 'special_openings': []}}
            
            '''
            for season in museum.season_set.all():
                season_dict = {}
                season_dict['start'] = season.start
                season_dict['end'] = season.end
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
                    season_dict['title_%s' % lang_code] = getattr(season, 'title_%s' % lang_code)
                    season_dict['last_entry_%s' % lang_code] = getattr(season, 'last_entry_%s' % lang_code)
                    season_dict['exceptions_%s' % lang_code] = getattr(season, 'exceptions_%s' % lang_code)
                form_step_data['opening']['sets']['seasons'].append(season_dict)
                
            for special_opening in museum.specialopeningtime_set.all():
                special_opening_dict = {}
                special_opening_dict['yyyy'] = special_opening.yyyy
                special_opening_dict['get_yyyy_display'] = special_opening.get_yyyy_display()
                special_opening_dict['mm'] = special_opening.mm
                special_opening_dict['get_mm_display'] = special_opening.get_mm_display()
                special_opening_dict['dd'] = special_opening.dd
                special_opening_dict['get_dd_display'] = special_opening.get_dd_display()
                for lang_code, lang_name in FRONTEND_LANGUAGES:
                    special_opening_dict['day_label_%s' % lang_code] = getattr(special_opening, 'day_label_%s' % lang_code)
                    special_opening_dict['exceptions_%s' % lang_code] = getattr(special_opening, 'exceptions_%s' % lang_code)
                special_opening_dict['is_closed'] = special_opening.is_closed
                special_opening_dict['is_regular'] = special_opening.is_regular
                special_opening_dict['opening'] = special_opening.opening
                special_opening_dict['break_close'] = special_opening.break_close
                special_opening_dict['break_open'] = special_opening.break_open
                special_opening_dict['closing'] = special_opening.closing
                form_step_data['opening']['sets']['special_openings'].append(special_opening_dict)
        '''
        
        # fill in prices from museum
        if not form_step_data.get('prices', {}).get('_filled', False):
            form_step_data['prices'] = {'_filled': True}
            fields = ['free_entrance', 'admission_price', 'reduced_price', 
                ]
            for lang_code, lang_name in FRONTEND_LANGUAGES:
                fields += [
                    'admission_price_info_%s' % lang_code,
                    'reduced_price_info_%s' % lang_code,
                    ]
            for f in fields:
                form_step_data['prices'][f] = getattr(museum, f)
            form_step_data['prices']['museum_prices'] = True
    
    if current_step == "opening":
        if "_pk" in form_step_data:
            instance = Exhibition.objects.get(pk=form_step_data['_pk'])

            instance.museum_opening_hours = form_step_data['opening']['museum_opening_hours'] 
            instance.save()

            instance.season_set.all().delete()
            for season_dict in form_step_data['opening']['sets']['seasons']:
                season = Season(exhibition=instance)
                season.is_appointment_based = season_dict['is_appointment_based'] 
                season.is_open_24_7 = season_dict['is_open_24_7'] 
                if not season_dict['mon_is_closed']:
                    season.mon_open = season_dict['mon_open'] 
                    season.mon_break_close = season_dict['mon_break_close'] 
                    season.mon_break_open = season_dict['mon_break_open']
                    season.mon_close = season_dict['mon_close']
                if not season_dict['tue_is_closed']:
                    season.tue_open = season_dict['tue_open'] 
                    season.tue_break_close = season_dict['tue_break_close'] 
                    season.tue_break_open = season_dict['tue_break_open'] 
                    season.tue_close = season_dict['tue_close'] 
                if not season_dict['wed_is_closed']:
                    season.wed_open = season_dict['wed_open']
                    season.wed_break_close = season_dict['wed_break_close'] 
                    season.wed_break_open = season_dict['wed_break_open'] 
                    season.wed_close = season_dict['wed_close'] 
                if not season_dict['thu_is_closed']:
                    season.thu_open = season_dict['thu_open'] 
                    season.thu_break_close = season_dict['thu_break_close'] 
                    season.thu_break_open = season_dict['thu_break_open'] 
                    season.thu_close = season_dict['thu_close'] 
                if not season_dict['fri_is_closed']:
                    season.fri_open = season_dict['fri_open'] 
                    season.fri_break_close = season_dict['fri_break_close'] 
                    season.fri_break_open = season_dict['fri_break_open'] 
                    season.fri_close = season_dict['fri_close'] 
                if not season_dict['sat_is_closed']:
                    season.sat_open = season_dict['sat_open']
                    season.sat_break_close = season_dict['sat_break_close'] 
                    season.sat_break_open = season_dict['sat_break_open']
                    season.sat_close = season_dict['sat_close']
                if not season_dict['sun_is_closed']:
                    season.sun_open = season_dict['sun_open'] 
                    season.sun_break_close = season_dict['sun_break_close'] 
                    season.sun_break_open = season_dict['sun_break_open'] 
                    season.sun_close = season_dict['sun_close']
                for lang_code, lang_name in FRONTEND_LANGUAGES:
                    setattr(season, 'last_entry_%s' % lang_code, season_dict['last_entry_%s' % lang_code])
                    setattr(season, 'exceptions_%s' % lang_code, season_dict['exceptions_%s' % lang_code])
                    setattr(season, 'exceptions_%s_markup_type' % lang_code, MARKUP_PLAIN_TEXT)
                season.save()
                
    if current_step == "prices":
        if "_pk" in form_step_data:
            instance = Exhibition.objects.get(pk=form_step_data['_pk'])

            fields = ['museum_prices', 'free_entrance', 'admission_price', 'reduced_price', 
                ]
            for lang_code, lang_name in FRONTEND_LANGUAGES:
                fields += [
                    'admission_price_info_%s' % lang_code,
                    'reduced_price_info_%s' % lang_code,
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

def set_extra_context(current_step, form_steps, form_step_data, instance=None):
    if "_pk" in form_step_data:
        return {'exhibition': Exhibition.objects.get(pk=form_step_data['_pk'])}
    return {}

def save_data(form_steps, form_step_data, instance=None):
    is_new = not instance
    
    if not instance:
        if '_pk' in form_step_data:
            instance = Exhibition.objects.get(pk=form_step_data['_pk'])
        else:
            instance = Exhibition()
    for lang_code, lang_name in FRONTEND_LANGUAGES:
        setattr(instance, 'title_%s' % lang_code, form_step_data['basic']['title_%s' % lang_code]) 
        setattr(instance, 'subtitle_%s' % lang_code, form_step_data['basic']['subtitle_%s' % lang_code])
        setattr(instance, 'description_%s' % lang_code, form_step_data['basic']['description_%s' % lang_code])
        setattr(instance, 'website_%s' % lang_code, form_step_data['basic']['website_%s' % lang_code])
        setattr(instance, 'catalog_%s' % lang_code, form_step_data['basic']['catalog_%s' % lang_code])
        setattr(instance, 'catalog_ordering_%s' % lang_code, form_step_data['basic']['catalog_ordering_%s' % lang_code])
        setattr(instance, 'description_%s_markup_type' % lang_code, MARKUP_HTML_WYSIWYG)
        setattr(instance, 'catalog_%s_markup_type' % lang_code, MARKUP_PLAIN_TEXT)
    instance.start = form_step_data['basic']['start'] 
    instance.end = form_step_data['basic']['end']
    instance.permanent = form_step_data['basic']['permanent'] 
    instance.exhibition_extended = form_step_data['basic']['exhibition_extended']
    instance.museum = form_step_data['basic']['museum']
    instance.location_name = form_step_data['basic']['location_name']
    instance.street_address = form_step_data['basic']['street_address']
    instance.street_address2 = form_step_data['basic']['street_address2'] 
    instance.postal_code = form_step_data['basic']['postal_code']
    instance.district = form_step_data['basic']['district']
    instance.city = form_step_data['basic']['city']
    instance.latitude = form_step_data['basic']['latitude']
    instance.longitude = form_step_data['basic']['longitude']
    instance.vernissage = form_step_data['basic']['vernissage']
    instance.finissage = form_step_data['basic']['finissage']
    instance.tags = form_step_data['basic']['tags']
    instance.is_for_children = form_step_data['basic']['is_for_children']

    instance.museum_opening_hours = form_step_data['opening']['museum_opening_hours'] 

    fields = ['museum_prices', 'free_entrance', 'admission_price', 'reduced_price', 
        ]
    for lang_code, lang_name in FRONTEND_LANGUAGES:
        fields += [
            'admission_price_info_%s' % lang_code,
            'reduced_price_info_%s' % lang_code,
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
    
    instance.status = "published"
    instance.save()
    
    if is_new:
        user = get_current_user()
        instance.set_owner(user)    
    
    instance.categories.clear()
    for cat in form_step_data['basic']['categories']:
        instance.categories.add(cat)

    instance.organizer_set.all().delete()
    for organizer_dict in form_step_data['basic']['sets']['organizers']:
        organizer = Organizer(exhibition=instance)
        organizer.organizing_museum = organizer_dict['organizing_museum'] 
        organizer.organizer_title = organizer_dict['organizer_title']
        organizer.organizer_url_link = organizer_dict['organizer_url_link']
        organizer.save()

    instance.season_set.all().delete()
    for season_dict in form_step_data['opening']['sets']['seasons']:
        season = Season(exhibition=instance)
        season.is_appointment_based = season_dict['is_appointment_based'] 
        season.is_open_24_7 = season_dict['is_open_24_7'] 
        if not season_dict['mon_is_closed']:
            season.mon_open = season_dict['mon_open'] 
            season.mon_break_close = season_dict['mon_break_close'] 
            season.mon_break_open = season_dict['mon_break_open']
            season.mon_close = season_dict['mon_close']
        if not season_dict['tue_is_closed']:
            season.tue_open = season_dict['tue_open'] 
            season.tue_break_close = season_dict['tue_break_close'] 
            season.tue_break_open = season_dict['tue_break_open'] 
            season.tue_close = season_dict['tue_close'] 
        if not season_dict['wed_is_closed']:
            season.wed_open = season_dict['wed_open']
            season.wed_break_close = season_dict['wed_break_close'] 
            season.wed_break_open = season_dict['wed_break_open'] 
            season.wed_close = season_dict['wed_close'] 
        if not season_dict['thu_is_closed']:
            season.thu_open = season_dict['thu_open'] 
            season.thu_break_close = season_dict['thu_break_close'] 
            season.thu_break_open = season_dict['thu_break_open'] 
            season.thu_close = season_dict['thu_close'] 
        if not season_dict['fri_is_closed']:
            season.fri_open = season_dict['fri_open'] 
            season.fri_break_close = season_dict['fri_break_close'] 
            season.fri_break_open = season_dict['fri_break_open'] 
            season.fri_close = season_dict['fri_close'] 
        if not season_dict['sat_is_closed']:
            season.sat_open = season_dict['sat_open']
            season.sat_break_close = season_dict['sat_break_close'] 
            season.sat_break_open = season_dict['sat_break_open']
            season.sat_close = season_dict['sat_close']
        if not season_dict['sun_is_closed']:
            season.sun_open = season_dict['sun_open'] 
            season.sun_break_close = season_dict['sun_break_close'] 
            season.sun_break_open = season_dict['sun_break_open'] 
            season.sun_close = season_dict['sun_close']
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            setattr(season, 'last_entry_%s' % lang_code, season_dict['last_entry_%s' % lang_code])
            setattr(season, 'exceptions_%s' % lang_code, season_dict['exceptions_%s' % lang_code])
            setattr(season, 'exceptions_%s_markup_type' % lang_code, MARKUP_PLAIN_TEXT)
        season.save()
        
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


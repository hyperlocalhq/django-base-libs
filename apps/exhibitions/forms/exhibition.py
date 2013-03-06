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

from base_libs.forms.fields import AutocompleteModelChoiceField
from base_libs.models.settings import MARKUP_HTML_WYSIWYG, MARKUP_PLAIN_TEXT
from base_libs.middleware import get_current_user

Exhibition = models.get_model("exhibitions", "Exhibition")
Season = models.get_model("exhibitions", "Season")
SpecialOpeningTime = models.get_model("exhibitions", "SpecialOpeningTime")

FRONTEND_LANGUAGES = getattr(settings, "FRONTEND_LANGUAGES", settings.LANGUAGES) 

from museumsportal.utils.forms import SecondarySubmit
from museumsportal.utils.forms import InlineFormSet
from museumsportal.utils.forms import SplitDateTimeWidget

class BasicInfoForm(ModelForm):
    museum = AutocompleteModelChoiceField(
        required=False,
        label=u"Name",
        # help_text=u"Bitte geben Sie einen Anfangsbuchstaben ein, um eine entsprechende Auswahl der verfügbaren Museums angezeigt zu bekommen.",
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
    organizing_museum = AutocompleteModelChoiceField(
        required=False,
        label=u"Name",
        # help_text=u"Bitte geben Sie einen Anfangsbuchstaben ein, um eine entsprechende Auswahl der verfügbaren Museums angezeigt zu bekommen.",
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
        model = Exhibition
        
        fields = ['start', 'end', 'permanent', 'exhibition_extended',
            'museum', 'location_name', 'street_address', 'street_address2', 'postal_code', 'district',
            'city', 'latitude', 'longitude', 
            'organizing_museum', 'organizer_title', 'organizer_url_link', 'vernissage', 'finissage', 'tags', 'categories', "is_for_children",
            ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'title_%s' % lang_code,
                'subtitle_%s' % lang_code,
                'description_%s' % lang_code,
                'catalog_%s' % lang_code,
                ]
    def __init__(self, *args, **kwargs):
        super(BasicInfoForm, self).__init__(*args, **kwargs)

        self.fields['vernissage'].widget = SplitDateTimeWidget(time_format='%H:%M')
        self.fields['finissage'].widget = SplitDateTimeWidget(time_format='%H:%M')

        self.fields['tags'].widget = forms.TextInput()
        self.fields['tags'].help_text = ""
        self.fields['categories'].widget = forms.CheckboxSelectMultiple()
        self.fields['categories'].help_text = ""
        self.fields['categories'].empty_label = None

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'title_%s' % lang_code,
                'subtitle_%s' % lang_code,
                'description_%s' % lang_code,
                'catalog_%s' % lang_code,
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
                css_class="div-catalog",
                *('catalog_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

                css_class="fieldset-basic-info",
                ))

        layout_blocks.append(layout.Fieldset(
            _("When?"),
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
            _("Organizer"),
            "organizing_museum",
            "organizer_title",
            "organizer_url_link",
            css_class="fieldset-organizer",
            ))
        layout_blocks.append(layout.Fieldset(
            _("Categories and Tags"),
            layout.Div("categories"),
            layout.Div(layout.HTML("""<label>&nbsp;</label> """),"is_for_children", css_class="inline"),
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

class OpeningForm(ModelForm):
    class Meta:
        model = Exhibition
        fields = []
    
    def __init__(self, *args, **kwargs):
        super(OpeningForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        layout_blocks = []
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
            for f in [
                'title_%s' % lang_code,
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
            layout.Row(
                css_class="div-title",
                *('title_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),
            layout.Row(
                layout.Field("start", placeholder="yyyy-mm-dd", autocomplete="off"),
                layout.Field("end", placeholder="yyyy-mm-dd", autocomplete="off")
                ),
            "is_appointment_based",

            layout.HTML(
            """{% load i18n %}
            <div class="row">
                <div>
                    <fieldset>
                        <legend>{% trans "Opening Hours" %}</legend>
                        <div class="row">
                            <div><label>{% trans "From" %}</label></div>
                            <div><label>{% trans "To" %}</label></div>
                        </div>
                         <div class="row">
                            <div class="has_weekday"><label class="weekday">{% trans "Mon" %}</label>"""), layout.Field("mon_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div>"""), layout.Field("mon_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div class="closed">"""), "mon_is_closed", layout.HTML("""</div>
                        </div>
                        {% load i18n %}
                        <div class="row">
                            <div class="has_weekday"><label class="weekday">{% trans "Tue" %}</label>"""), layout.Field("tue_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div>"""), layout.Field("tue_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div class="closed">"""), "tue_is_closed", layout.HTML("""</div>
                        </div>
                        {% load i18n %}
                        <div class="row">
                            <div class="has_weekday"><label class="weekday">{% trans "Wed" %}</label>"""), layout.Field("wed_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div>"""), layout.Field("wed_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div class="closed">"""), "wed_is_closed", layout.HTML("""</div>
                        </div>
                        {% load i18n %}
                        <div class="row">
                            <div class="has_weekday"><label class="weekday">{% trans "Thu" %}</label>"""), layout.Field("thu_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div>"""), layout.Field("thu_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div class="closed">"""), "thu_is_closed", layout.HTML("""</div>
                        </div>
                        {% load i18n %}
                        <div class="row">
                            <div class="has_weekday"><label class="weekday">{% trans "Fri" %}</label>"""), layout.Field("fri_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div>"""), layout.Field("fri_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div class="closed">"""), "fri_is_closed", layout.HTML("""</div>
                        </div>
                        {% load i18n %}
                        <div class="row">
                            <div class="has_weekday"><label class="weekday">{% trans "Sat" %}</label>"""), layout.Field("sat_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div>"""), layout.Field("sat_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div class="closed">"""), "sat_is_closed", layout.HTML("""</div>
                        </div>
                        {% load i18n %}
                        <div class="row">
                            <div class="has_weekday"><label class="weekday">{% trans "Sun" %}</label>"""), layout.Field("sun_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
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
                        <div><label>{% trans "From" %}</label></div>
                        <div><label>{% trans "To" %}</label></div>
                    </div>
                    <div class="row">
                        <div class="has_weekday"><label class="weekday">{% trans "Mon" %}</label>"""), layout.Field("mon_break_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                        <div>"""), layout.Field("mon_break_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                    </div>
                        {% load i18n %}
                    <div class="row">
                        <div class="has_weekday"><label class="weekday">{% trans "Tue" %}</label>"""), layout.Field("tue_break_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                        <div>"""), layout.Field("tue_break_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                    </div>
                        {% load i18n %}
                    <div class="row">
                        <div class="has_weekday"><label class="weekday">{% trans "Wed" %}</label>"""), layout.Field("wed_break_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                        <div>"""), layout.Field("wed_break_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                    </div>
                        {% load i18n %}
                    <div class="row">
                        <div class="has_weekday"><label class="weekday">{% trans "Thu" %}</label>"""), layout.Field("thu_break_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                        <div>"""), layout.Field("thu_break_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                    </div>
                        {% load i18n %}
                    <div class="row">
                        <div class="has_weekday"><label class="weekday">{% trans "Fri" %}</label>"""), layout.Field("fri_break_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                        <div>"""), layout.Field("fri_break_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                    </div>
                        {% load i18n %}
                    <div class="row">
                        <div class="has_weekday"><label class="weekday">{% trans "Sat" %}</label>"""), layout.Field("sat_break_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                        <div>"""), layout.Field("sat_break_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                    </div>
                        {% load i18n %}
                    <div class="row">
                        <div class="has_weekday"><label class="weekday">{% trans "Sun" %}</label>"""), layout.Field("sun_break_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
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

class SpecialOpeningTimeForm(ModelForm):
    class Meta:
        model = SpecialOpeningTime
        exclude = []
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            exclude.append("exceptions_%s_markup_type" % lang_code)
    def __init__(self, *args, **kwargs):
        super(SpecialOpeningTimeForm, self).__init__(*args, **kwargs)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'day_label_%s' % lang_code,
                'exceptions_%s' % lang_code,
                ]:
                self.fields[f].label += """ <span class="lang">%s</span>""" % lang_code.upper()

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'day_label_%s' % lang_code,
                ]:
                self.fields[f].help_text = ""

        for fname in ["opening", "break_close", "break_open", "closing"]:
            self.fields[fname].widget = forms.TimeInput(format='%H:%M')
        self.fields['yyyy'].choices[0] = ("", _("Every year"))
        self.fields['yyyy'].help_text = ""

        # remove labels from Closing Time / Holiday  
        self.fields['opening'].widget = forms.TimeInput(format='%H:%M')
        self.fields['opening'].label = ""
        self.fields['break_close'].widget = forms.TimeInput(format='%H:%M')
        self.fields['break_close'].label = ""
        self.fields['break_open'].widget = forms.TimeInput(format='%H:%M')
        self.fields['break_open'].label = ""
        self.fields['closing'].widget = forms.TimeInput(format='%H:%M')
        self.fields['closing'].label = ""

        self.helper = FormHelper()
        self.helper.form_tag = False
        layout_blocks = []

        layout_blocks.append(layout.Fieldset(
            _("Closing Time / Holiday"),
            layout.Row(
                css_class="div-accessibility-details",
                *('day_label_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),
            
            layout.Row(
                "yyyy", "mm", "dd",
                ),

            layout.Div(
                layout.HTML("""{% load i18n %} <label>{% trans "Particularities" %}</label> """),
                "is_closed", "is_regular", 
                ),
            
            layout.HTML(
                """{% load i18n %}
                <div class="row">
                    <div>
                        <fieldset>
                            <legend>{% trans "Opening Hours" %}</legend>
                            <div class="row">
                                <div><label>{% trans "From" %}</label></div>
                                <div><label>{% trans "To" %}</label></div>
                            </div>
                             <div class="row">
                                <div>"""), layout.Field("opening", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                                <div>"""), layout.Field("closing", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            </div>
                        </fieldset>
                    </div>
                    {% load i18n %}
                    <div>
                        <fieldset>
                            <legend>{% trans "Breaks" %}</legend>
                            <div class="row">
                                <div><label>{% trans "From" %}</label></div>
                                <div><label>{% trans "To" %}</label></div>
                            </div>
                            <div class="row">
                                <div>"""), layout.Field("break_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                                <div>"""), layout.Field("break_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            </div>
                        </fieldset>
                    </div>
                </div>
                """
                ),
            

            css_class="fieldset-opening-times",
            ))

        layout_blocks.append(layout.Fieldset(
            _("Additional info"),
            layout.Row(
                css_class="div-accessibility-details",
                *('exceptions_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

                css_class="fieldset-additional-info",
                ))

        self.helper.layout = layout.Layout(
            *layout_blocks
            )

SpecialOpeningTimeFormset = inlineformset_factory(Exhibition, SpecialOpeningTime, form=SpecialOpeningTimeForm, formset=InlineFormSet, extra=0)

class PricesForm(ModelForm):
    class Meta:
        model = Exhibition
        fields = ['museum_prices', 'free_entrance', 'admission_price', 'reduced_price', 'member_of_museumspass',
            'show_family_ticket',
            'show_group_ticket',
            'show_yearly_ticket',
            ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'admission_price_info_%s' % lang_code,
                'reduced_price_info_%s' % lang_code,
                'group_ticket_%s' % lang_code,
                ]
    def __init__(self, *args, **kwargs):
        super(PricesForm, self).__init__(*args, **kwargs)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'admission_price_info_%s' % lang_code,
                'reduced_price_info_%s' % lang_code,
                'group_ticket_%s' % lang_code,
                ]:
                self.fields[f].label += """ <span class="lang">%s</span>""" % lang_code.upper()

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        
        layout_blocks = []
        layout_blocks.append(layout.Fieldset(
            _("Prices"),
            layout.Div('museum_prices', 'free_entrance', css_class="inline"), 
            'admission_price',
            layout.Row(
                *('admission_price_info_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),
            css_class="fieldset-prices",
            ))
        layout_blocks.append(layout.Fieldset(
            _("Reduced Prices"),
            'reduced_price',
            layout.Row(
                *('reduced_price_info_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),
            ))

        layout_blocks.append(layout.Fieldset(
            _("Details"),
            layout.Div(
                'member_of_museumspass', 
                'show_family_ticket',
                'show_group_ticket',
                'show_yearly_ticket',
                css_class="inline",
                ),

            layout.Row(
                css_class="div-group_ticket-details",
                *('group_ticket_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

                css_class="fieldset-details",
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
            'basic': {'_filled': True},
            'opening': {'_filled': True, 'sets': {'seasons': [], 'special_openings': []}},
            'prices': {'_filled': True},
            'accessibility': {'_filled': True},
            '_pk': instance.pk,
            }
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            form_step_data['basic']['title_%s' % lang_code] = getattr(instance, 'title_%s' % lang_code)
            form_step_data['basic']['subtitle_%s' % lang_code] = getattr(instance, 'subtitle_%s' % lang_code)
            form_step_data['basic']['description_%s' % lang_code] = getattr(instance, 'description_%s' % lang_code)
            form_step_data['basic']['catalog_%s' % lang_code] = getattr(instance, 'catalog_%s' % lang_code)
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
        form_step_data['basic']['organizing_museum'] = instance.organizing_museum
        form_step_data['basic']['organizer_title'] = instance.organizer_title
        form_step_data['basic']['organizer_url_link'] = instance.organizer_url_link
        form_step_data['basic']['vernissage'] = instance.vernissage
        form_step_data['basic']['finissage'] = instance.finissage
        form_step_data['basic']['categories'] = instance.categories.all()
        form_step_data['basic']['tags'] = instance.tags
        form_step_data['basic']['is_for_children'] = instance.is_for_children
    
        for season in instance.season_set.all():
            season_dict = {}
            season_dict['start'] = season.start
            season_dict['end'] = season.end
            season_dict['is_appointment_based'] = season.is_appointment_based
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
            
        for special_opening in instance.specialopeningtime_set.all():
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
    
        fields = ['museum_prices', 'free_entrance', 'admission_price', 'reduced_price', 'member_of_museumspass',
            'show_family_ticket',
            'show_group_ticket',
            'show_yearly_ticket',
            ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'admission_price_info_%s' % lang_code,
                'reduced_price_info_%s' % lang_code,
                'group_ticket_%s' % lang_code,
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
            getattr(instance, 'catalog_%s' % lang_code, form_step_data['basic']['catalog_%s' % lang_code])
            setattr(instance, 'description_%s_markup_type' % lang_code, MARKUP_HTML_WYSIWYG)
            getattr(instance, 'catalog_%s_markup_type' % lang_code, MARKUP_PLAIN_TEXT)
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
        instance.organizing_museum = form_step_data['basic']['organizing_museum']
        instance.organizer_title = form_step_data['basic']['organizer_title']
        instance.organizer_url_link = form_step_data['basic']['organizer_url_link']
        instance.vernissage = form_step_data['basic']['vernissage']
        instance.finissage = form_step_data['basic']['finissage']
        instance.tags = form_step_data['basic']['tags']
        instance.is_for_children = form_step_data['basic']['is_for_children']
        instance.status = "draft"
        instance.save()
        
        if '_pk' not in form_step_data:
            user = get_current_user()
            instance.set_owner(user)
        
        instance.categories.clear()
        for cat in form_step_data['basic']['categories']:
            instance.categories.add(cat)
        
        form_step_data['_pk'] = instance.pk
        
    if current_step == "basic" and museum:
        # fill in Opening hours from museum
        if not form_step_data.get('opening', {}).get('_filled', False):
            form_step_data['opening'] = {'_filled': True, 'sets': {'seasons': [], 'special_openings': []}}
            for season in museum.season_set.all():
                season_dict = {}
                season_dict['start'] = season.start
                season_dict['end'] = season.end
                season_dict['is_appointment_based'] = season.is_appointment_based
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
        
        # fill in prices from museum
        if not form_step_data.get('prices', {}).get('_filled', False):
            form_step_data['prices'] = {'_filled': True}
            fields = ['free_entrance', 'admission_price', 'reduced_price', 'member_of_museumspass',
                'show_family_ticket',
                'show_group_ticket',
                'show_yearly_ticket',
                ]
            for lang_code, lang_name in FRONTEND_LANGUAGES:
                fields += [
                    'admission_price_info_%s' % lang_code,
                    'reduced_price_info_%s' % lang_code,
                    'group_ticket_%s' % lang_code,
                    ]
            for f in fields:
                form_step_data['prices'][f] = getattr(museum, f)
            form_step_data['prices']['museum_prices'] = True
    
    if current_step == "opening":
        if "_pk" in form_step_data:
            instance = Exhibition.objects.get(pk=form_step_data['_pk'])

            instance.season_set.all().delete()
            for season_dict in form_step_data['opening']['sets']['seasons']:
                season = Season(exhibition=instance)
                season.start = season_dict['start'] 
                season.end = season_dict['end'] 
                season.is_appointment_based = season_dict['is_appointment_based'] 
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
                    setattr(season, 'title_%s' % lang_code, season_dict['title_%s' % lang_code])
                    setattr(season, 'last_entry_%s' % lang_code, season_dict['last_entry_%s' % lang_code])
                    setattr(season, 'exceptions_%s' % lang_code, season_dict['exceptions_%s' % lang_code])
                    setattr(season, 'exceptions_%s_markup_type' % lang_code, MARKUP_PLAIN_TEXT)
                season.save()
                
            instance.specialopeningtime_set.all().delete()
            for special_opening_dict in form_step_data['opening']['sets']['special_openings']:
                special_opening = SpecialOpeningTime(exhibition=instance)
                special_opening.yyyy = special_opening_dict['yyyy'] 
                special_opening.mm = special_opening_dict['mm']
                special_opening.dd = special_opening_dict['dd']
                for lang_code, lang_name in FRONTEND_LANGUAGES:
                    setattr(special_opening, 'day_label_%s' % lang_code, special_opening_dict['day_label_%s' % lang_code])
                    setattr(special_opening, 'exceptions_%s' % lang_code, special_opening_dict['exceptions_%s' % lang_code])
                    setattr(special_opening, 'exceptions_%s_markup_type' % lang_code, MARKUP_PLAIN_TEXT)
                special_opening.is_closed = special_opening_dict['is_closed'] 
                special_opening.is_regular = special_opening_dict['is_regular'] 
                special_opening.opening = special_opening_dict['opening'] 
                special_opening.break_close = special_opening_dict['break_close'] 
                special_opening.break_open = special_opening_dict['break_open'] 
                special_opening.closing = special_opening_dict['closing']
                special_opening.save()
        
    if current_step == "prices":
        if "_pk" in form_step_data:
            instance = Exhibition.objects.get(pk=form_step_data['_pk'])

            fields = ['museum_prices', 'free_entrance', 'admission_price', 'reduced_price', 'member_of_museumspass',
                'show_family_ticket',
                'show_group_ticket',
                'show_yearly_ticket',
                ]
            for lang_code, lang_name in FRONTEND_LANGUAGES:
                fields += [
                    'admission_price_info_%s' % lang_code,
                    'reduced_price_info_%s' % lang_code,
                    'group_ticket_%s' % lang_code,
                    ]
            for f in fields:
                setattr(instance, f, form_step_data['prices'][f])
        
            for lang_code, lang_name in FRONTEND_LANGUAGES:
                for f in [
                    'admission_price_info_%s' % lang_code,
                    'reduced_price_info_%s' % lang_code,
                    'group_ticket_%s' % lang_code,
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
        getattr(instance, 'catalog_%s' % lang_code, form_step_data['basic']['catalog_%s' % lang_code])
        setattr(instance, 'description_%s_markup_type' % lang_code, MARKUP_HTML_WYSIWYG)
        getattr(instance, 'catalog_%s_markup_type' % lang_code, MARKUP_PLAIN_TEXT)
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
    instance.organizing_museum = form_step_data['basic']['organizing_museum']
    instance.organizer_title = form_step_data['basic']['organizer_title']
    instance.organizer_url_link = form_step_data['basic']['organizer_url_link']
    instance.vernissage = form_step_data['basic']['vernissage']
    instance.finissage = form_step_data['basic']['finissage']
    instance.tags = form_step_data['basic']['tags']
    instance.is_for_children = form_step_data['basic']['is_for_children']

    fields = ['museum_prices', 'free_entrance', 'admission_price', 'reduced_price', 'member_of_museumspass',
        'show_family_ticket',
        'show_group_ticket',
        'show_yearly_ticket',
        ]
    for lang_code, lang_name in FRONTEND_LANGUAGES:
        fields += [
            'admission_price_info_%s' % lang_code,
            'reduced_price_info_%s' % lang_code,
            'group_ticket_%s' % lang_code,
            ]
    for f in fields:
        setattr(instance, f, form_step_data['prices'][f])

    for lang_code, lang_name in FRONTEND_LANGUAGES:
        for f in [
            'admission_price_info_%s' % lang_code,
            'reduced_price_info_%s' % lang_code,
            'group_ticket_%s' % lang_code,
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
    
    instance.season_set.all().delete()
    for season_dict in form_step_data['opening']['sets']['seasons']:
        season = Season(exhibition=instance)
        season.start = season_dict['start'] 
        season.end = season_dict['end'] 
        season.is_appointment_based = season_dict['is_appointment_based'] 
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
            setattr(season, 'title_%s' % lang_code, season_dict['title_%s' % lang_code])
            setattr(season, 'last_entry_%s' % lang_code, season_dict['last_entry_%s' % lang_code])
            setattr(season, 'exceptions_%s' % lang_code, season_dict['exceptions_%s' % lang_code])
            setattr(season, 'exceptions_%s_markup_type' % lang_code, MARKUP_PLAIN_TEXT)
        season.save()
        
    instance.specialopeningtime_set.all().delete()
    for special_opening_dict in form_step_data['opening']['sets']['special_openings']:
        special_opening = SpecialOpeningTime(exhibition=instance)
        special_opening.yyyy = special_opening_dict['yyyy'] 
        special_opening.mm = special_opening_dict['mm']
        special_opening.dd = special_opening_dict['dd']
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            setattr(special_opening, 'day_label_%s' % lang_code, special_opening_dict['day_label_%s' % lang_code])
            setattr(special_opening, 'exceptions_%s' % lang_code, special_opening_dict['exceptions_%s' % lang_code])
            setattr(special_opening, 'exceptions_%s_markup_type' % lang_code, MARKUP_PLAIN_TEXT)
        special_opening.is_closed = special_opening_dict['is_closed'] 
        special_opening.is_regular = special_opening_dict['is_regular'] 
        special_opening.opening = special_opening_dict['opening'] 
        special_opening.break_close = special_opening_dict['break_close'] 
        special_opening.break_open = special_opening_dict['break_open'] 
        special_opening.closing = special_opening_dict['closing']
        special_opening.save()

    form_steps['success_url'] = reverse("dashboard") #instance.get_url_path()
    
    return form_step_data
    
def cancel_editing(request):
    return redirect("dashboard")

EXHIBITION_FORM_STEPS = {
    'basic': {
        'title': _("Basic Information"),
        'template': "exhibitions/forms/basic_info_form.html",
        'form': BasicInfoForm,
    },
    'opening': {
        'title': _("Opening hours"),
        'template': "exhibitions/forms/opening_form.html",
        'form': OpeningForm, # dummy form
        'formsets': {
            'seasons': SeasonFormset,
            'special_openings': SpecialOpeningTimeFormset,
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
    'name': 'exhibition_registration',
    'default_path': ["basic", "opening", "prices", "accessibility", 'gallery'],
}


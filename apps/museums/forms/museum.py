# -*- coding: utf-8 -*-

from django.db import models
from django import forms
from django.forms.models import ModelForm
from django.forms.models import inlineformset_factory
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from django.utils.safestring import mark_safe

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from base_libs.models.settings import MARKUP_HTML_WYSIWYG, MARKUP_PLAIN_TEXT
from base_libs.middleware import get_current_user

Museum = models.get_model("museums", "Museum")
Season = models.get_model("museums", "Season")
SpecialOpeningTime = models.get_model("museums", "SpecialOpeningTime")

FRONTEND_LANGUAGES = getattr(settings, "FRONTEND_LANGUAGES", settings.LANGUAGES) 

from museumsportal.utils.forms import SecondarySubmit
from museumsportal.utils.forms import InlineFormSet

class BasicInfoForm(ModelForm):
    class Meta:
        model = Museum
        
        fields = []
        
        #fields = ['tags', 'categories']
        #for lang_code, lang_name in FRONTEND_LANGUAGES:
        #    fields += [
        #        'title_%s' % lang_code,
        #        'subtitle_%s' % lang_code,
        #        'description_%s' % lang_code,
        #        ]
    def __init__(self, *args, **kwargs):
        super(BasicInfoForm, self).__init__(*args, **kwargs)

        #self.fields['tags'].widget = forms.TextInput()
        #self.fields['tags'].help_text = ""
        #self.fields['categories'].widget = forms.CheckboxSelectMultiple()
        #self.fields['categories'].help_text = ""
        #self.fields['categories'].empty_label = None

        #for lang_code, lang_name in FRONTEND_LANGUAGES:
        #    for f in [
        #        'title_%s' % lang_code,
        #        'subtitle_%s' % lang_code,
        #        'description_%s' % lang_code,
        #        ]:
        #        self.fields[f].label += """ <span class="lang">%s</span>""" % lang_code.upper()

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        
        layout_blocks = []

        #layout_blocks.append(layout.Fieldset(
        #    _("Basic Info"),
        #    layout.Row(
        #        css_class="div-accessibility-details",
        #        *(layout.Field('title_%s' % lang_code, disabled="disabled") for lang_code, lang_name in FRONTEND_LANGUAGES)
        #        ),

        #    layout.Row(
        #        css_class="div-accessibility-details",
        #        *(layout.Field('subtitle_%s' % lang_code, disabled="disabled") for lang_code, lang_name in FRONTEND_LANGUAGES)
        #        ),

        #    layout.Row(
        #        css_class="div-accessibility-details",
        #        *(layout.Field('description_%s' % lang_code, css_class="tinymce") for lang_code, lang_name in FRONTEND_LANGUAGES)
        #        ),

        #        css_class="fieldset-basic-info",
        #        ))

        #layout_blocks.append(layout.Fieldset(
        #    _("Categories and Tags"),
        #    layout.Field("categories", disabled="disabled"),
        #    layout.Field("tags", disabled="disabled"),
        #    css_class="fieldset-categories-tags",
        #    ))
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
        model = Museum
        fields = []
        
    def __init__(self, *args, **kwargs):
        super(OpeningForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        layout_blocks = []
        if self.instance and self.instance.pk:
            layout_blocks.append(bootstrap.FormActions(
                layout.Submit('submit', _('Next')),
                SecondarySubmit('save_and_close', _('save')),
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
                            <div><label class="weekday">{% trans "Mon" %}</label>"""), layout.Field("mon_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div>"""), layout.Field("mon_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div class="closed">"""), "mon_is_closed", layout.HTML("""</div>
                        </div>
                        {% load i18n %}
                        <div class="row">
                            <div><label class="weekday">{% trans "Tue" %}</label>"""), layout.Field("tue_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div>"""), layout.Field("tue_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div class="closed">"""), "tue_is_closed", layout.HTML("""</div>
                        </div>
                        {% load i18n %}
                        <div class="row">
                            <div><label class="weekday">{% trans "Wed" %}</label>"""), layout.Field("wed_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div>"""), layout.Field("wed_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div class="closed">"""), "wed_is_closed", layout.HTML("""</div>
                        </div>
                        {% load i18n %}
                        <div class="row">
                            <div><label class="weekday">{% trans "Thu" %}</label>"""), layout.Field("thu_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div>"""), layout.Field("thu_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div class="closed">"""), "thu_is_closed", layout.HTML("""</div>
                        </div>
                        {% load i18n %}
                        <div class="row">
                            <div><label class="weekday">{% trans "Fri" %}</label>"""), layout.Field("fri_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div>"""), layout.Field("fri_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div class="closed">"""), "fri_is_closed", layout.HTML("""</div>
                        </div>
                        {% load i18n %}
                        <div class="row">
                            <div><label class="weekday">{% trans "Sat" %}</label>"""), layout.Field("sat_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div>"""), layout.Field("sat_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                            <div class="closed">"""), "sat_is_closed", layout.HTML("""</div>
                        </div>
                        {% load i18n %}
                        <div class="row">
                            <div><label class="weekday">{% trans "Sun" %}</label>"""), layout.Field("sun_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
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
                        <div><label class="weekday">{% trans "Mon" %}</label>"""), layout.Field("mon_break_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                        <div>"""), layout.Field("mon_break_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                    </div>
                        {% load i18n %}
                    <div class="row">
                        <div><label class="weekday">{% trans "Tue" %}</label>"""), layout.Field("tue_break_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                        <div>"""), layout.Field("tue_break_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                    </div>
                        {% load i18n %}
                    <div class="row">
                        <div><label class="weekday">{% trans "Wed" %}</label>"""), layout.Field("wed_break_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                        <div>"""), layout.Field("wed_break_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                    </div>
                        {% load i18n %}
                    <div class="row">
                        <div><label class="weekday">{% trans "Thu" %}</label>"""), layout.Field("thu_break_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                        <div>"""), layout.Field("thu_break_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                    </div>
                        {% load i18n %}
                    <div class="row">
                        <div><label class="weekday">{% trans "Fri" %}</label>"""), layout.Field("fri_break_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                        <div>"""), layout.Field("fri_break_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                    </div>
                        {% load i18n %}
                    <div class="row">
                        <div><label class="weekday">{% trans "Sat" %}</label>"""), layout.Field("sat_break_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                        <div>"""), layout.Field("sat_break_open", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
                    </div>
                        {% load i18n %}
                    <div class="row">
                        <div><label class="weekday">{% trans "Sun" %}</label>"""), layout.Field("sun_break_close", placeholder="00:00", autocomplete="off"), layout.HTML("""</div>
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
                css_class="div-last_entry",
                *('last_entry_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

            layout.Row(
                css_class="div-exceptions",
                *('exceptions_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

                css_class="fieldset-additional-info",
                ))

        self.helper.layout = layout.Layout(
            *layout_blocks
            )

SeasonFormset = inlineformset_factory(Museum, Season, form=SeasonForm, formset=InlineFormSet, extra=0)

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
        for fname in ["opening", "break_close", "break_open", "closing"]:
            self.fields[fname].widget = forms.TimeInput(format='%H:%M')
        self.fields['yyyy'].choices[0] = ("", _("Every year"))
        self.fields['yyyy'].help_text = ""

        self.helper = FormHelper()
        self.helper.form_tag = False
        layout_blocks = []

        layout_blocks.append(layout.Fieldset(
            _("Occasion"),
            layout.Row(
                css_class="div-accessibility-details",
                *('day_label_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

                css_class="fieldset-additional-info",
                ))

        layout_blocks.append(layout.Fieldset(
            _("Special date"),

            layout.Row("yyyy", "mm", "dd"),
            
            css_class="fieldset-special-date",
            ))

        layout_blocks.append(layout.Fieldset(
            _("Opening hours"),
            "is_closed",
            "is_regular",
            layout.Row(
                layout.Field("opening", placeholder="00:00", autocomplete="off"),
                layout.Field("break_close", placeholder="00:00", autocomplete="off"),
                layout.Field("break_open", placeholder="00:00", autocomplete="off"),
                layout.Field("closing", placeholder="00:00", autocomplete="off"),
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

SpecialOpeningTimeFormset = inlineformset_factory(Museum, SpecialOpeningTime, form=SpecialOpeningTimeForm, formset=InlineFormSet, extra=0)

class PricesForm(ModelForm):
    class Meta:
        model = Museum
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
            layout.Div('free_entrance', 'member_of_museumspass', css_class="inline"), 
            'admission_price',
            layout.Row(
                *('admission_price_info_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),
            'reduced_price',
            layout.Row(
                *('reduced_price_info_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),
            css_class="fieldset-prices",
            ))

        layout_blocks.append(layout.Fieldset(
            _("Details"),
            layout.Div(
                'show_family_ticket',
                'show_group_ticket',
                'show_yearly_ticket',
                css_class="inline",
                ),

            layout.Row(
                layout.HTML("""{% load infoblocks %}
                    {% infoblock "family_ticket_info" %}
                """),
                css_class="div-family_ticket-details",
                ),

            layout.Row(
                css_class="div-group_ticket-details",
                *('group_ticket_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

            layout.Row(
                layout.HTML("""{% load infoblocks %}
                    {% infoblock "yearly_ticket_info" %}
                """),
                css_class="div-yearly_ticket-details",
                ),

                css_class="fieldset-details",
                ))

        if self.instance and self.instance.pk:
            layout_blocks.append(bootstrap.FormActions(
                layout.Submit('submit', _('Next')),
                SecondarySubmit('save_and_close', _('save')),
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
                
        
class AddressForm(ModelForm):
    class Meta:
        model = Museum
        fields = ['street_address', 'street_address2', 'postal_code', 'district',
            'city', 'latitude', 'longitude',
            'phone_country', 'phone_area', 'phone_number', 
            'group_bookings_phone_country', 'group_bookings_phone_area', 'group_bookings_phone_number', 
            'service_phone_country', 'service_phone_area', 'service_phone_number', 
            'fax_country', 'fax_area', 'fax_number', 'email', 'website', 'twitter', 'facebook',
            ]
    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.fields['latitude'].widget = forms.HiddenInput()
        self.fields['longitude'].widget = forms.HiddenInput()
        
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        
        layout_blocks = []
        layout_blocks.append(layout.Fieldset(
            _("Location"),
            layout.Row(
                layout.Div(
                    'street_address', 
                    'street_address2',
                    'postal_code', 
                    'city',
                    'district',
                    ),
                layout.HTML("""{% load i18n %}
                    <div id="dyn_set_map">
                        <label>{% trans "Location" %}</label>
                        <div id="gmap_wrapper">
                            <!-- THE GMAPS WILL BE INSERTED HERE DYNAMICALLY -->
                        </div>
                        <div class="form-actions">
                            <input id="dyn_locate_geo" type="button" class="btn" value="{% trans "Relocate on map" %}" />&zwnj;
                            <!--<input id="dyn_remove_geo" type="button" class="btn" value="{% trans "Remove from map" %}"/>&zwnj;-->
                        </div>
                    </div>
                """),
                'latitude', 
                'longitude',
                ),
            css_class="fieldset-location",
            ))
            
        layout_blocks.append(layout.Fieldset(
            _("Contact"),

            layout.Row(
                'email', 'website'),

            layout.Row(
                layout.Div(
                    layout.Row(
                    layout.HTML('{% load i18n %}<div><label>{% trans "Phone" %}</label></div>'),
                    'phone_country', 'phone_area', 'phone_number'),
                ),
                layout.Div(
                    layout.Row(
                    layout.HTML('{% load i18n %}<div><label>{% trans "Fax" %}</label></div>'),
                    'fax_country', 'fax_area', 'fax_number'),
                ),
            ),

            layout.Row(
                layout.Div(
                    layout.Row(
                    layout.HTML('{% load i18n %}<div><label>{% trans "Booking Phone" %}</label></div>'),
                    'group_bookings_phone_country', 'group_bookings_phone_area', 'group_bookings_phone_number'),

                ),
                layout.Div(
                    layout.Row(
                    layout.HTML('{% load i18n %}<div><label>{% trans "Service Phone" %}</label></div>'),
                     'service_phone_country', 'service_phone_area', 'service_phone_number'),
                ),
            ),

            css_class="fieldset-other-contact-info",
            ))
        layout_blocks.append(layout.Fieldset(
            _("Social media"),
            layout.Row('twitter', 'facebook'),
            css_class="fieldset-social-media",
            ))
        if self.instance and self.instance.pk:
            layout_blocks.append(bootstrap.FormActions(
                layout.Submit('submit', _('Next')),
                SecondarySubmit('save_and_close', _('save')),
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
            
class ServicesForm(ModelForm):
    class Meta:
        model = Museum
        fields = ['service_shop', 'service_restaurant',
        'service_cafe', 'service_library', 'service_archive', 
        'service_diaper_changing_table']
    def __init__(self, *args, **kwargs):
        super(ServicesForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        
        layout_blocks = []
        layout_blocks.append(layout.Fieldset(
            _("Services"),
            layout.Div('service_shop',
                'service_restaurant',
                'service_cafe',
                'service_library',
                'service_archive',
                'service_diaper_changing_table',
                css_class="inline",
                ),
            css_class="fieldset-services",
            ))
        if self.instance and self.instance.pk:
            layout_blocks.append(bootstrap.FormActions(
                layout.Submit('submit', _('Next')),
                SecondarySubmit('save_and_close', _('save')),
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
        model = Museum
        fields = ['accessibility_options',]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'accessibility_%s' % lang_code,
                ]
    def __init__(self, *args, **kwargs):
        super(AccessibilityForm, self).__init__(*args, **kwargs)
        self.fields['accessibility_options'].widget = forms.CheckboxSelectMultiple()
        choices = []
        for access_opt in self.fields['accessibility_options'].queryset:
            choices.append((access_opt.pk, mark_safe("""
                <img src="%s%s" alt="" /> %s
                """ % (settings.MEDIA_URL, access_opt.image.path, access_opt.title) ))) 
        self.fields['accessibility_options'].choices = choices
        self.fields['accessibility_options'].help_text = ""
        self.fields['accessibility_options'].empty_label = None
        
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'accessibility_%s' % lang_code,
                ]:
                self.fields[f].label += """ <span class="lang">%s</span>""" % lang_code.upper()
        
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        
        layout_blocks = []
        layout_blocks.append(layout.Fieldset(
            _("Accessibility"),

            layout.Row(
                css_class="div-accessibility-details",
                *('accessibility_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

            'accessibility_options',

            css_class="fieldset-accessibility-options",
            ))
        if self.instance and self.instance.pk:
            layout_blocks.append(bootstrap.FormActions(
                layout.Submit('submit', _('Next')),
                SecondarySubmit('save_and_close', _('save')),
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

class MediationForm(ModelForm):
    class Meta:
        model = Museum
        fields = []
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'mediation_offer_%s' % lang_code,
                ]
    def __init__(self, *args, **kwargs):
        super(MediationForm, self).__init__(*args, **kwargs)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'mediation_offer_%s' % lang_code,
                ]:
                self.fields[f].label += """ <span class="lang">%s</span>""" % lang_code.upper()

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"

        layout_blocks = []
        
        layout_blocks.append(layout.Fieldset(
            _("Basic Info"),
            layout.Row(
                css_class="div-accessibility-details",
                *('mediation_offer_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

                css_class="fieldset-basic-info",
                ))

        if self.instance and self.instance.pk:
            layout_blocks.append(bootstrap.FormActions(
                layout.Submit('submit', _('Next')),
                SecondarySubmit('save_and_close', _('save')),
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
        model = Museum
        fields = []
        
    def __init__(self, *args, **kwargs):
        super(GalleryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        layout_blocks = []
        if self.instance and self.instance.pk:
            layout_blocks.append(bootstrap.FormActions(
                layout.Submit('save_and_close', _('save')),
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
            'address': {'_filled': True},
            'services': {'_filled': True},
            'accessibility': {'_filled': True},
            'mediation': {'_filled': True},
            'gallery': {'_filled': True},
            '_pk': instance.pk,
            }
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            form_step_data['basic']['title_%s' % lang_code] = getattr(instance, 'title_%s' % lang_code)
            form_step_data['basic']['subtitle_%s' % lang_code] = getattr(instance, 'subtitle_%s' % lang_code)
            form_step_data['basic']['description_%s' % lang_code] = getattr(instance, 'description_%s' % lang_code)
        form_step_data['basic']['categories'] = instance.categories.all()
        form_step_data['basic']['tags'] = instance.tags
    
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
            form_step_data['prices'][f] = getattr(instance, f)
        
        fields = ['street_address', 'street_address2', 'postal_code', 'district',
            'city', 'latitude', 'longitude',
            'phone_country', 'phone_area', 'phone_number',
            'group_bookings_phone_country', 'group_bookings_phone_area', 'group_bookings_phone_number',
            'service_phone_country', 'service_phone_area', 'service_phone_number',
            'fax_country', 'fax_area', 'fax_number',
            'email', 'website', 'twitter', 'facebook',
            ]
        for f in fields:
            form_step_data['address'][f] = getattr(instance, f)
        
        form_step_data['services']['service_shop'] = instance.service_shop
        form_step_data['services']['service_restaurant'] = instance.service_restaurant
        form_step_data['services']['service_cafe'] = instance.service_cafe
        form_step_data['services']['service_library'] = instance.service_library
        form_step_data['services']['service_archive'] = instance.service_archive
        form_step_data['services']['service_diaper_changing_table'] = instance.service_diaper_changing_table
        
        form_step_data['accessibility']['accessibility_options'] = instance.accessibility_options.all()
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            form_step_data['accessibility']['accessibility_%s' % lang_code] = getattr(instance, 'accessibility_%s' % lang_code)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            form_step_data['mediation']['mediation_offer_%s' % lang_code] = getattr(instance, 'mediation_offer_%s' % lang_code)

    return form_step_data
    
def submit_step(current_step, form_steps, form_step_data, instance=None):
    if current_step == "basic":
        # save the entry
        if "_pk" in form_step_data:
            instance = Museum.objects.get(pk=form_step_data['_pk'])
        else:
            instance = Museum()
        #for lang_code, lang_name in FRONTEND_LANGUAGES:
        #    setattr(instance, 'title_%s' % lang_code, form_step_data['basic']['title_%s' % lang_code])
        #    setattr(instance, 'subtitle_%s' % lang_code, form_step_data['basic']['subtitle_%s' % lang_code])
        #    setattr(instance, 'description_%s' % lang_code, form_step_data['basic']['description_%s' % lang_code])
        #    setattr(instance, 'description_%s_markup_type' % lang_code, MARKUP_HTML_WYSIWYG)
        #instance.tags = form_step_data['basic']['tags']
        #if not instance.pk:
        #    instance.status = "draft"
        #instance.save()
        
        #if '_pk' not in form_step_data:
        #    user = get_current_user()
        #    instance.set_owner(user)
        
        #instance.categories.clear()
        #for cat in form_step_data['basic']['categories']:
        #    instance.categories.add(cat)
        
        form_step_data['_pk'] = instance.pk
        
    if current_step == "address":
        if "_pk" in form_step_data:
            instance = Museum.objects.get(pk=form_step_data['_pk'])
            fields = ['street_address', 'street_address2', 'postal_code', 'district',
                'city', 'latitude', 'longitude',
                'phone_country', 'phone_area', 'phone_number',
                'group_bookings_phone_country', 'group_bookings_phone_area', 'group_bookings_phone_number',
                'service_phone_country', 'service_phone_area', 'service_phone_number',
                'fax_country', 'fax_area', 'fax_number',
                'email', 'website', 'twitter', 'facebook',
                ]
            for f in fields:
                setattr(instance, f, form_step_data['address'][f])
            instance.save()
            
    if current_step == "opening":
        if "_pk" in form_step_data:
            instance = Museum.objects.get(pk=form_step_data['_pk'])
        
            instance.season_set.all().delete()
            for season_dict in form_step_data['opening']['sets']['seasons']:
                season = Season(museum=instance)
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
                special_opening = SpecialOpeningTime(museum=instance)
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
            instance = Museum.objects.get(pk=form_step_data['_pk'])

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
                setattr(instance, f, form_step_data['prices'][f])
        
            for lang_code, lang_name in FRONTEND_LANGUAGES:
                for f in [
                    'admission_price_info_%s' % lang_code,
                    'reduced_price_info_%s' % lang_code,
                    'group_ticket_%s' % lang_code,
                    ]:
                    setattr(instance, f + "_markup_type", MARKUP_PLAIN_TEXT)
            instance.save()
            
    if current_step == "services":
        if "_pk" in form_step_data:
            instance = Museum.objects.get(pk=form_step_data['_pk'])

            instance.service_shop = form_step_data['services']['service_shop']
            instance.service_restaurant = form_step_data['services']['service_restaurant']
            instance.service_cafe = form_step_data['services']['service_cafe']
            instance.service_library = form_step_data['services']['service_library']
            instance.service_archive = form_step_data['services']['service_archive']
            instance.service_diaper_changing_table = form_step_data['services']['service_diaper_changing_table']
            
            instance.save()
            
    if current_step == "accessibility":
        if "_pk" in form_step_data:
            instance = Museum.objects.get(pk=form_step_data['_pk'])

            for lang_code, lang_name in FRONTEND_LANGUAGES:
                setattr(instance, 'accessibility_%s' % lang_code, form_step_data['accessibility']['accessibility_%s' % lang_code])

            instance.save()
            
            instance.accessibility_options.clear()
            for cat in form_step_data['accessibility']['accessibility_options']:
                instance.accessibility_options.add(cat)
            
    if current_step == "mediation":
        if "_pk" in form_step_data:
            instance = Museum.objects.get(pk=form_step_data['_pk'])

            for lang_code, lang_name in FRONTEND_LANGUAGES:
                setattr(instance, 'mediation_offer_%s' % lang_code, form_step_data['mediation']['mediation_offer_%s' % lang_code])
                setattr(instance, 'mediation_offer_%s_markup_type' % lang_code, MARKUP_PLAIN_TEXT)
                
            instance.save()

    # finally all museum will be saved and published by save_data()
    return form_step_data

def set_extra_context(current_step, form_steps, form_step_data, instance=None):
    if "_pk" in form_step_data:
        return {'museum': Museum.objects.get(pk=form_step_data['_pk'])}
    return {}

def save_data(form_steps, form_step_data, instance=None):
    is_new = not instance
    if not instance:
        if '_pk' in form_step_data:
            instance = Museum.objects.get(pk=form_step_data['_pk'])
        else:
            instance = Museum()

    #for lang_code, lang_name in FRONTEND_LANGUAGES:
    #    setattr(instance, 'title_%s' % lang_code, form_step_data['basic']['title_%s' % lang_code])
    #    setattr(instance, 'subtitle_%s' % lang_code, form_step_data['basic']['subtitle_%s' % lang_code])
    #    setattr(instance, 'description_%s' % lang_code, form_step_data['basic']['description_%s' % lang_code])
    #    setattr(instance, 'description_%s_markup_type' % lang_code, MARKUP_HTML_WYSIWYG)
    #instance.tags = form_step_data['basic']['tags'] 

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
        setattr(instance, f, form_step_data['prices'][f])

    for lang_code, lang_name in FRONTEND_LANGUAGES:
        for f in [
            'admission_price_info_%s' % lang_code,
            'reduced_price_info_%s' % lang_code,
            'group_ticket_%s' % lang_code,
            ]:
            setattr(instance, f + "_markup_type", MARKUP_PLAIN_TEXT)

    fields = ['street_address', 'street_address2', 'postal_code', 'district',
        'city', 'latitude', 'longitude',
        'phone_country', 'phone_area', 'phone_number',
        'group_bookings_phone_country', 'group_bookings_phone_area', 'group_bookings_phone_number',
        'service_phone_country', 'service_phone_area', 'service_phone_number',
        'fax_country', 'fax_area', 'fax_number',
        'email', 'website', 'twitter', 'facebook',
        ]
    for f in fields:
        setattr(instance, f, form_step_data['address'][f])
    
    
    instance.service_shop = form_step_data['services']['service_shop']
    instance.service_restaurant = form_step_data['services']['service_restaurant']
    instance.service_cafe = form_step_data['services']['service_cafe']
    instance.service_library = form_step_data['services']['service_library']
    instance.service_archive = form_step_data['services']['service_archive']
    instance.service_diaper_changing_table = form_step_data['services']['service_diaper_changing_table']
    
    for lang_code, lang_name in FRONTEND_LANGUAGES:
        setattr(instance, 'accessibility_%s' % lang_code, form_step_data['accessibility']['accessibility_%s' % lang_code])

    for lang_code, lang_name in FRONTEND_LANGUAGES:
        for f in [
            'accessibility_%s' % lang_code,
            ]:
            setattr(instance, f + "_markup_type", MARKUP_PLAIN_TEXT)


    for lang_code, lang_name in FRONTEND_LANGUAGES:
        setattr(instance, 'mediation_offer_%s' % lang_code, form_step_data['mediation']['mediation_offer_%s' % lang_code])
        setattr(instance, 'mediation_offer_%s_markup_type' % lang_code, MARKUP_PLAIN_TEXT)

    instance.status = "published"
    instance.save()
    
    if is_new:
        user = get_current_user()
        instance.set_owner(user)
    
    #instance.categories.clear()
    #for cat in form_step_data['basic']['categories']:
    #    instance.categories.add(cat)
        
    instance.accessibility_options.clear()
    for cat in form_step_data['accessibility']['accessibility_options']:
        instance.accessibility_options.add(cat)

    instance.season_set.all().delete()
    for season_dict in form_step_data['opening']['sets']['seasons']:
        season = Season(museum=instance)
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
        special_opening = SpecialOpeningTime(museum=instance)
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

    form_steps['success_url'] = instance.get_url_path()

    return form_step_data

def cancel_editing(request):
    return redirect("dashboard")

MUSEUM_FORM_STEPS = {
    'basic': {
        'title': _("Basic Information"),
        'template': "museums/forms/basic_info_form.html",
        'form': BasicInfoForm,
    },
    'opening': {
        'title': _("Opening hours"),
        'template': "museums/forms/opening_form.html",
        'form': OpeningForm, # dummy form
        'formsets': {
            'seasons': SeasonFormset,
            'special_openings': SpecialOpeningTimeFormset,
        }
    },
    'prices': {
        'title': _("Prices"),
        'template': "museums/forms/prices_form.html",
        'form': PricesForm,
    },
    'address': {
        'title': _("Address"),
        'template': "museums/forms/address_form.html",
        'form': AddressForm,
    },
    'services': {
        'title': _("Services"),
        'template': "museums/forms/services_form.html",
        'form': ServicesForm,
    },
    'accessibility': {
        'title': _("Accessibility"),
        'template': "museums/forms/accessibility_form.html",
        'form': AccessibilityForm,
    },
    'mediation': {
        'title': _("Mediation"),
        'template': "museums/forms/mediation_form.html",
        'form': MediationForm,
    },
    'gallery': {
        'title': _("Images"),
        'template': "museums/forms/gallery_form.html",
        'form': GalleryForm, # dummy form
    },
    'oninit': load_data,
    'on_set_extra_context': set_extra_context,
    'onsubmit': submit_step,
    'onsave': save_data,
    'onreset': cancel_editing,
    'name': 'museum_registration',
    'default_path': ["basic", "address", "opening", "prices", "services", "accessibility", "mediation", "gallery"],
}


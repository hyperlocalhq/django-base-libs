# -*- coding: utf-8 -*-

from django.db import models
from django import forms
from django.forms.models import ModelForm
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from base_libs.models.settings import MARKUP_HTML_WYSIWYG, MARKUP_PLAIN_TEXT

Museum = models.get_model("museums", "Museum")
Season = models.get_model("museums", "Season")
SpecialOpeningTime = models.get_model("museums", "SpecialOpeningTime")

FRONTEND_LANGUAGES = getattr(settings, "FRONTEND_LANGUAGES", settings.LANGUAGES) 

class SecondarySubmit(layout.Submit):
    field_classes = "btn"

class BasicInfoForm(ModelForm):
    class Meta:
        model = Museum
        
        fields = ['tags', 'categories']
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'title_%s' % lang_code,
                'subtitle_%s' % lang_code,
                'description_%s' % lang_code,
                ]
    def __init__(self, *args, **kwargs):
        super(BasicInfoForm, self).__init__(*args, **kwargs)
        
        self.fields['categories'].widget = forms.CheckboxSelectMultiple()
        self.fields['categories'].help_text = ""
        self.fields['categories'].empty_label = None

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'title_%s' % lang_code,
                'subtitle_%s' % lang_code,
                'description_%s' % lang_code,
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
                *('title_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

            layout.Row(
                css_class="div-accessibility-details",
                *('subtitle_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

            layout.Row(
                css_class="div-accessibility-details",
                *(layout.Field('description_%s' % lang_code, css_class="tinymce") for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

                css_class="fieldset-basic-info",
                ))

        layout_blocks.append(layout.Fieldset(
            _("Categories and Tags"),
            "categories",
            "tags",
            css_class="fieldset-categories-tags",
            ))
        if self.instance and self.instance.pk:
            layout_blocks.append(bootstrap.FormActions(
                layout.Submit('submit', _('Next')),
                layout.Submit('save_and_close', _('Save and close')),
                SecondarySubmit('reset', _('Reset')),
                ))
        else:
            layout_blocks.append(bootstrap.FormActions(
                layout.Submit('submit', _('Next')),
                SecondarySubmit('reset', _('Reset')),
                ))
        
        self.helper.layout = layout.Layout(
            *layout_blocks
            )        

class InlineFormSet(BaseInlineFormSet):
    """ Inline formset which accepts initial values for unsaved models """
    def __init__(self, data=None, files=None, instance=None, save_as_new=False, prefix=None, queryset=None, initial=[]):
        self._initial = initial
        super(InlineFormSet, self).__init__(data, files, instance, save_as_new, prefix, queryset)
        
    def _construct_form(self, i, **kwargs):
        """
        Instantiates and returns the i-th form instance in a formset.
        """
        defaults = {'auto_id': self.auto_id, 'prefix': self.add_prefix(i)}
        if self.is_bound:
            defaults['data'] = self.data
            defaults['files'] = self.files
        if self._initial:
            try:
                defaults['initial'] = self._initial[i]
            except IndexError:
                pass
        # Allow extra forms to be empty.
        if i >= self.initial_form_count():
            defaults['empty_permitted'] = True
        defaults.update(kwargs)
        form = self.form(**defaults)
        self.add_fields(form, i)
        return form

    def initial_form_count(self):
        """Returns the number of forms that are required in this FormSet."""
        if not (self.data or self.files):
            return len(self._initial)
        return super(InlineFormSet, self).initial_form_count()


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
                layout.Submit('save_and_close', _('Save and close')),
                SecondarySubmit('reset', _('Reset')),
                ))
        else:
            layout_blocks.append(bootstrap.FormActions(
                layout.Submit('submit', _('Next')),
                SecondarySubmit('reset', _('Reset')),
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
                'last_entry_%s' % lang_code,
                'exceptions_%s' % lang_code,
                ]:
                self.fields[f].label += """ <span class="lang">%s</span>""" % lang_code.upper()

        # remove labels from opening and closing times 
        for weekday in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]:
            self.fields['%s_open' % weekday].label = ""
            self.fields['%s_break_close' % weekday].label = ""
            self.fields['%s_break_open' % weekday].label = ""
            self.fields['%s_close' % weekday].label = ""
        
        self.helper = FormHelper()
        self.helper.form_tag = False
        layout_blocks = []
        layout_blocks.append(layout.Fieldset(
            _("Season"),
            layout.Row(
                layout.Field("start", placeholder="yyyy-mm-dd", autocomplete="off"),
                layout.Field("end", placeholder="yyyy-mm-dd", autocomplete="off")
                ),
            "is_appointment_based",

            layout.HTML(
            """{% load i18n %}
            <table>
                <tbody>
                    <tr>
                        <th><h2>{% trans "Monday" %}</h2>{% trans "From" %}</th>
                        <th>{% trans "Break starts" %}</th>
                        <th>{% trans "Break ends" %}</th>
                        <th>{% trans "Till" %}"""), "mon_is_closed", layout.HTML("""</th>
                    </tr>
                    <tr>
                        <td>"""), layout.Field("mon_open", placeholder="0:00", autocomplete="off"), layout.HTML("""</td>
                        <td>"""), layout.Field("mon_break_close", placeholder="0:00", autocomplete="off"), layout.HTML("""</td>
                        <td>"""), layout.Field("mon_break_open", placeholder="0:00", autocomplete="off"), layout.HTML("""</td>
                        <td>"""), layout.Field("mon_close", placeholder="0:00", autocomplete="off"), layout.HTML("""</td>{% load i18n %}
                    </tr>
                    <tr>
                        <th><h2>{% trans "Tuesday" %}</h2>{% trans "From" %}</th>
                        <th>{% trans "Break starts" %}</th>
                        <th>{% trans "Break ends" %}</th>
                        <th>{% trans "Till" %}"""), "tue_is_closed", layout.HTML("""</th>
                    </tr>
                    <tr>
                        <td>"""), layout.Field("tue_open", placeholder="0:00", autocomplete="off"), layout.HTML("""</td>
                        <td>"""), layout.Field("tue_break_close", placeholder="0:00", autocomplete="off"), layout.HTML("""</td>
                        <td>"""), layout.Field("tue_break_open", placeholder="0:00", autocomplete="off"), layout.HTML("""</td>
                        <td>"""), layout.Field("tue_close", placeholder="0:00", autocomplete="off"), layout.HTML("""</td>{% load i18n %}
                    </tr>
                    <tr>
                        <th><h2>{% trans "Wednesday" %}</h2>{% trans "From" %}</th>
                        <th>{% trans "Break starts" %}</th>
                        <th>{% trans "Break ends" %}</th>
                        <th>{% trans "Till" %}"""), "wed_is_closed", layout.HTML("""</th>
                    </tr>
                    <tr>
                        <td>"""), layout.Field("wed_open", placeholder="0:00", autocomplete="off"), layout.HTML("""</td>
                        <td>"""), layout.Field("wed_break_close", placeholder="0:00", autocomplete="off"), layout.HTML("""</td>
                        <td>"""), layout.Field("wed_break_open", placeholder="0:00", autocomplete="off"), layout.HTML("""</td>
                        <td>"""), layout.Field("wed_close", placeholder="0:00", autocomplete="off"), layout.HTML("""</td>{% load i18n %}
                    </tr>
                    <tr>
                        <th><h2>{% trans "Thursday" %}</h2>{% trans "From" %}</th>
                        <th>{% trans "Break starts" %}</th>
                        <th>{% trans "Break ends" %}</th>
                        <th>{% trans "Till" %}"""), "thu_is_closed", layout.HTML("""</th>
                    </tr>
                    <tr>
                        <td>"""), layout.Field("thu_open", placeholder="0:00", autocomplete="off"), layout.HTML("""</td>
                        <td>"""), layout.Field("thu_break_close", placeholder="0:00", autocomplete="off"), layout.HTML("""</td>
                        <td>"""), layout.Field("thu_break_open", placeholder="0:00", autocomplete="off"), layout.HTML("""</td>
                        <td>"""), layout.Field("thu_close", placeholder="0:00", autocomplete="off"), layout.HTML("""</td>{% load i18n %}
                    </tr>
                    <tr>
                        <th><h2>{% trans "Friday" %}</h2>{% trans "From" %}</th>
                        <th>{% trans "Break starts" %}</th>
                        <th>{% trans "Break ends" %}</th>
                        <th>{% trans "Till" %}"""), "fri_is_closed", layout.HTML("""</th>
                    </tr>
                    <tr>
                        <td>"""), layout.Field("fri_open", placeholder="0:00", autocomplete="off"), layout.HTML("""</td>
                        <td>"""), layout.Field("fri_break_close", placeholder="0:00", autocomplete="off"), layout.HTML("""</td>
                        <td>"""), layout.Field("fri_break_open", placeholder="0:00", autocomplete="off"), layout.HTML("""</td>
                        <td>"""), layout.Field("fri_close", placeholder="0:00", autocomplete="off"), layout.HTML("""</td>{% load i18n %}
                    </tr>
                    <tr>
                        <th><h2>{% trans "Saturday" %}</h2>{% trans "From" %}</th>
                        <th>{% trans "Break starts" %}</th>
                        <th>{% trans "Break ends" %}</th>
                        <th>{% trans "Till" %}"""), "sat_is_closed", layout.HTML("""</th>
                    </tr>
                    <tr>
                        <td>"""), layout.Field("sat_open", placeholder="0:00", autocomplete="off"), layout.HTML("""</td>
                        <td>"""), layout.Field("sat_break_close", placeholder="0:00", autocomplete="off"), layout.HTML("""</td>
                        <td>"""), layout.Field("sat_break_open", placeholder="0:00", autocomplete="off"), layout.HTML("""</td>
                        <td>"""), layout.Field("sat_close", placeholder="0:00", autocomplete="off"), layout.HTML("""</td>{% load i18n %}
                    </tr>
                    <tr>
                        <th><h2>{% trans "Sunday" %}</h2>{% trans "From" %}</th>
                        <th>{% trans "Break starts" %}</th>
                        <th>{% trans "Break ends" %}</th>
                        <th>{% trans "Till" %}"""), "sun_is_closed", layout.HTML("""</th>
                    </tr>
                    <tr>
                        <td>"""), layout.Field("sun_open", placeholder="0:00", autocomplete="off"), layout.HTML("""</td>
                        <td>"""), layout.Field("sun_break_close", placeholder="0:00", autocomplete="off"), layout.HTML("""</td>
                        <td>"""), layout.Field("sun_break_open", placeholder="0:00", autocomplete="off"), layout.HTML("""</td>
                        <td>"""), layout.Field("sun_close", placeholder="0:00", autocomplete="off"), layout.HTML("""</td>
                    </tr>
                </tbody>
            </table>
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
            _("Opening times"),
            "is_closed",
            "is_regular",
            layout.Row(
                layout.Field("opening", placeholder="0:00", autocomplete="off"),
                layout.Field("break_close", placeholder="0:00", autocomplete="off"),
                layout.Field("break_open", placeholder="0:00", autocomplete="off"),
                layout.Field("closing", placeholder="0:00", autocomplete="off"),
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
            'show_admission_price_info',
            'show_reduced_price_info',
            'show_arrangements_for_children',
            'show_free_entrance_for',
            'show_family_ticket',
            'show_group_ticket',
            'show_free_entrance_times',
            'show_yearly_ticket',
            'show_other_tickets',
            ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'admission_price_info_%s' % lang_code,
                'reduced_price_info_%s' % lang_code,
                'arrangements_for_children_%s' % lang_code,
                'free_entrance_for_%s' % lang_code,
                'family_ticket_%s' % lang_code,
                'group_ticket_%s' % lang_code,
                'free_entrance_times_%s' % lang_code,
                'yearly_ticket_%s' % lang_code,
                'other_tickets_%s' % lang_code,
                ]
    def __init__(self, *args, **kwargs):
        super(PricesForm, self).__init__(*args, **kwargs)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'admission_price_info_%s' % lang_code,
                'reduced_price_info_%s' % lang_code,
                'arrangements_for_children_%s' % lang_code,
                'free_entrance_for_%s' % lang_code,
                'family_ticket_%s' % lang_code,
                'group_ticket_%s' % lang_code,
                'free_entrance_times_%s' % lang_code,
                'yearly_ticket_%s' % lang_code,
                'other_tickets_%s' % lang_code,
                ]:
                self.fields[f].label += """ <span class="lang">%s</span>""" % lang_code.upper()

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        
        layout_blocks = []
        layout_blocks.append(layout.Fieldset(
            _("Prices"),
            'free_entrance', 'admission_price', 'reduced_price', 'member_of_museumspass',
            css_class="fieldset-prices",
            ))

        layout_blocks.append(layout.Fieldset(
            _("Details"),
            layout.Div(
                'show_admission_price_info',
                'show_reduced_price_info',
                'show_arrangements_for_children',
                'show_free_entrance_for',
                'show_family_ticket',
                'show_group_ticket',
                'show_free_entrance_times',
                'show_yearly_ticket',
                'show_other_tickets', 
                css_class="inline",
                ),
            layout.Row(
                css_class="div-admission_price_info-details",
                *('admission_price_info_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

            layout.Row(
                css_class="div-reduced_price_info-details",
                *('reduced_price_info_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

            layout.Row(
                css_class="div-arrangements_for_children-details",
                *('arrangements_for_children_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

            layout.Row(
                css_class="div-free_entrance_for-details",
                *('free_entrance_for_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

            layout.Row(
                css_class="div-family_ticket-details",
                *('family_ticket_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

            layout.Row(
                css_class="div-group_ticket-details",
                *('group_ticket_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

            layout.Row(
                css_class="div-free_entrance_times-details",
                *('free_entrance_times_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

            layout.Row(
                css_class="div-yearly_ticket-details",
                *('yearly_ticket_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

            layout.Row(
                css_class="div-other_tickets-details",
                *('other_tickets_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

                css_class="fieldset-details",
                ))

        if self.instance and self.instance.pk:
            layout_blocks.append(bootstrap.FormActions(
                layout.Submit('submit', _('Next')),
                layout.Submit('save_and_close', _('Save and close')),
                SecondarySubmit('reset', _('Reset')),
                ))
        else:
            layout_blocks.append(bootstrap.FormActions(
                layout.Submit('submit', _('Next')),
                SecondarySubmit('reset', _('Reset')),
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
            'contact_name', 'contact_phone_country', 'contact_phone_area', 'contact_phone_number', 'contact_email',
            'post_street_address', 'post_street_address2', 'post_postal_code', 'post_city',
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
            layout.Row('street_address', 'street_address2'),
            layout.Row('postal_code', 'city'),
            'district',
            'latitude', 'longitude',
            css_class="fieldset-location",
            ))
        layout_blocks.append(layout.Fieldset(
            _("Postal address (if differs from museum's address)"),
            layout.Row('post_street_address', 'post_street_address2'),
            layout.Row('post_postal_code', 'post_city'),
            css_class="fieldset-postal-address",
            ))
        layout_blocks.append(layout.Fieldset(
            _("Contact person"),
            'contact_name', 
            layout.Row(
                layout.HTML('{% load i18n %}<div><label>{% trans "Contact person phone" %}</label></div>'),
                'contact_phone_country', 'contact_phone_area', 'contact_phone_number',
                css_class="phone"),
            'contact_email',
            css_class="fieldset-contact-person",
            ))
        layout_blocks.append(layout.Fieldset(
            _("Other contact info"),
            layout.Row(
                layout.HTML('{% load i18n %}<label>{% trans "Phone" %}</label>'),
                'phone_country', 'phone_area', 'phone_number',
                css_class="phone"),
            layout.Row(
                layout.HTML('{% load i18n %}<div><label>{% trans "Fax" %}</label></div>'),
                'fax_country', 'fax_area', 'fax_number',
                css_class="phone"),
            layout.Row(
                layout.HTML('{% load i18n %}<div><label>{% trans "Group bookings phone" %}</label></div>'),
                'group_bookings_phone_country', 'group_bookings_phone_area', 'group_bookings_phone_number',
                css_class="phone"),
            layout.Row(
                layout.HTML('{% load i18n %}<div><label>{% trans "Service phone" %}</label></div>'),
                'service_phone_country', 'service_phone_area', 'service_phone_number',
                css_class="phone"),
                'email', 'website',
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
                layout.Submit('save_and_close', _('Save and close')),
                SecondarySubmit('reset', _('Reset')),
                ))
        else:
            layout_blocks.append(bootstrap.FormActions(
                layout.Submit('submit', _('Next')),
                SecondarySubmit('reset', _('Reset')),
                ))
        
        self.helper.layout = layout.Layout(
            *layout_blocks
            )        
            
class ServicesAccessibilityForm(ModelForm):
    class Meta:
        model = Museum
        fields = ['accessibility_options', 'service_shop', 'service_books', 'service_restaurant',
        'service_cafe', 'service_library', 'service_archive', 'service_studio', 'service_online', 
        'service_diaper_changing_table', 'service_birthdays', 'service_rent', 'service_other']
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'accessibility_%s' % lang_code,
                'service_shop_info_%s' % lang_code,
                'service_books_info_%s' % lang_code,
                'service_restaurant_info_%s' % lang_code,
                'service_cafe_info_%s' % lang_code,
                'service_library_info_%s' % lang_code,
                'service_archive_info_%s' % lang_code,
                'service_studio_info_%s' % lang_code,
                'service_online_info_%s' % lang_code,
                'service_birthdays_info_%s' % lang_code,
                'service_rent_info_%s' % lang_code,
                'service_other_info_%s' % lang_code,
                ]
    def __init__(self, *args, **kwargs):
        super(ServicesAccessibilityForm, self).__init__(*args, **kwargs)
        self.fields['accessibility_options'].widget = forms.CheckboxSelectMultiple()
        self.fields['accessibility_options'].help_text = ""
        self.fields['accessibility_options'].empty_label = None
        
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'accessibility_%s' % lang_code,
                'service_shop_info_%s' % lang_code,
                'service_books_info_%s' % lang_code,
                'service_restaurant_info_%s' % lang_code,
                'service_cafe_info_%s' % lang_code,
                'service_library_info_%s' % lang_code,
                'service_archive_info_%s' % lang_code,
                'service_studio_info_%s' % lang_code,
                'service_online_info_%s' % lang_code,
                'service_birthdays_info_%s' % lang_code,
                'service_rent_info_%s' % lang_code,
                'service_other_info_%s' % lang_code,
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
        layout_blocks.append(layout.Fieldset(
            _("Services"),
            layout.Div('service_shop',
                'service_books',
                'service_restaurant',
                'service_cafe',
                'service_library',
                'service_archive',
                'service_studio',
                'service_online',
                'service_diaper_changing_table',
                'service_birthdays',
                'service_rent',
                'service_other',
                css_class="inline",
                ),
            layout.Row(
                css_class="div-shop-details",
                *('service_shop_info_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),
            layout.Row(
                css_class="div-books-details",
                *('service_books_info_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),
            layout.Row(
                css_class="div-restaurant-details",
                *('service_restaurant_info_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),
            layout.Row(
                css_class="div-cafe-details",
                *('service_cafe_info_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),
            layout.Row(
                css_class="div-library-details",
                *('service_library_info_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),
            layout.Row(
                css_class="div-archive-details",
                *('service_archive_info_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),
            layout.Row(
                css_class="div-studio-details",
                *('service_studio_info_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),
            layout.Row(
                css_class="div-online-details",
                *('service_online_info_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),
            layout.Row(
                css_class="div-birthdays-details",
                *('service_birthdays_info_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),
            layout.Row(
                css_class="div-rent-details",
                *('service_rent_info_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),
            layout.Row(
                css_class="div-other-details",
                *('service_other_info_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),
            css_class="fieldset-services",
            ))
        if self.instance and self.instance.pk:
            layout_blocks.append(bootstrap.FormActions(
                layout.Submit('submit', _('Next')),
                layout.Submit('save_and_close', _('Save and close')),
                SecondarySubmit('reset', _('Reset')),
                ))
        else:
            layout_blocks.append(bootstrap.FormActions(
                layout.Submit('submit', _('Next')),
                SecondarySubmit('reset', _('Reset')),
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
                layout.Submit('submit', _('Save')),
                layout.Submit('save_and_close', _('Save and close')),
                SecondarySubmit('reset', _('Reset')),
                ))
        else:
            layout_blocks.append(bootstrap.FormActions(
                layout.Submit('submit', _('Save')),
                SecondarySubmit('reset', _('Reset')),
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
            'services_accessibility': {'_filled': True},
            'mediation': {'_filled': True},
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
            'show_admission_price_info',
            'show_reduced_price_info',
            'show_arrangements_for_children',
            'show_free_entrance_for',
            'show_family_ticket',
            'show_group_ticket',
            'show_free_entrance_times',
            'show_yearly_ticket',
            'show_other_tickets',
            ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'admission_price_info_%s' % lang_code,
                'reduced_price_info_%s' % lang_code,
                'arrangements_for_children_%s' % lang_code,
                'free_entrance_for_%s' % lang_code,
                'family_ticket_%s' % lang_code,
                'group_ticket_%s' % lang_code,
                'free_entrance_times_%s' % lang_code,
                'yearly_ticket_%s' % lang_code,
                'other_tickets_%s' % lang_code,
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
            'contact_name', 'contact_phone_country', 'contact_phone_area', 'contact_phone_number', 'contact_email',
            'post_street_address', 'post_street_address2', 'post_postal_code', 'post_city',
            ]
        for f in fields:
            form_step_data['address'][f] = getattr(instance, f)
        
        form_step_data['services_accessibility']['accessibility_options'] = instance.accessibility_options.all()
        form_step_data['services_accessibility']['service_shop'] = instance.service_shop
        form_step_data['services_accessibility']['service_books'] = instance.service_books
        form_step_data['services_accessibility']['service_restaurant'] = instance.service_restaurant
        form_step_data['services_accessibility']['service_cafe'] = instance.service_cafe
        form_step_data['services_accessibility']['service_library'] = instance.service_library
        form_step_data['services_accessibility']['service_archive'] = instance.service_archive
        form_step_data['services_accessibility']['service_studio'] = instance.service_studio
        form_step_data['services_accessibility']['service_online'] = instance.service_online
        form_step_data['services_accessibility']['service_diaper_changing_table'] = instance.service_diaper_changing_table
        form_step_data['services_accessibility']['service_birthdays'] = instance.service_birthdays
        form_step_data['services_accessibility']['service_rent'] = instance.service_rent
        form_step_data['services_accessibility']['service_other'] = instance.service_other
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            form_step_data['services_accessibility']['accessibility_%s' % lang_code] = getattr(instance, 'accessibility_%s' % lang_code)
            form_step_data['services_accessibility']['service_shop_info_%s' % lang_code] = getattr(instance, 'service_shop_info_%s' % lang_code)
            form_step_data['services_accessibility']['service_books_info_%s' % lang_code] = getattr(instance, 'service_books_info_%s' % lang_code)
            form_step_data['services_accessibility']['service_restaurant_info_%s' % lang_code] = getattr(instance, 'service_restaurant_info_%s' % lang_code)
            form_step_data['services_accessibility']['service_cafe_info_%s' % lang_code] = getattr(instance, 'service_cafe_info_%s' % lang_code)
            form_step_data['services_accessibility']['service_library_info_%s' % lang_code] = getattr(instance, 'service_library_info_%s' % lang_code)
            form_step_data['services_accessibility']['service_archive_info_%s' % lang_code] = getattr(instance, 'service_archive_info_%s' % lang_code)
            form_step_data['services_accessibility']['service_studio_info_%s' % lang_code] = getattr(instance, 'service_studio_info_%s' % lang_code)
            form_step_data['services_accessibility']['service_online_info_%s' % lang_code] = getattr(instance, 'service_online_info_%s' % lang_code)
            form_step_data['services_accessibility']['service_birthdays_info_%s' % lang_code] = getattr(instance, 'service_birthdays_info_%s' % lang_code)
            form_step_data['services_accessibility']['service_rent_info_%s' % lang_code] = getattr(instance, 'service_rent_info_%s' % lang_code)
            form_step_data['services_accessibility']['service_other_info_%s' % lang_code] = getattr(instance, 'service_other_info_%s' % lang_code)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            form_step_data['mediation']['mediation_offer_%s' % lang_code] = getattr(instance, 'mediation_offer_%s' % lang_code)

    return form_step_data
    
def submit_step(current_step, form_steps, form_step_data, instance=None):
    return form_step_data

def save_data(form_steps, form_step_data, instance=None):
    if not instance:
        instance = Museum()

    for lang_code, lang_name in FRONTEND_LANGUAGES:
        setattr(instance, 'title_%s' % lang_code, form_step_data['basic']['title_%s' % lang_code])
        setattr(instance, 'subtitle_%s' % lang_code, form_step_data['basic']['subtitle_%s' % lang_code])
        setattr(instance, 'description_%s' % lang_code, form_step_data['basic']['description_%s' % lang_code])
        setattr(instance, 'description_%s_markup_type' % lang_code, MARKUP_HTML_WYSIWYG)
    instance.tags = form_step_data['basic']['tags'] 

    fields = ['free_entrance', 'admission_price', 'reduced_price', 'member_of_museumspass',
        'show_admission_price_info',
        'show_reduced_price_info',
        'show_arrangements_for_children',
        'show_free_entrance_for',
        'show_family_ticket',
        'show_group_ticket',
        'show_free_entrance_times',
        'show_yearly_ticket',
        'show_other_tickets',
        ]
    for lang_code, lang_name in FRONTEND_LANGUAGES:
        fields += [
            'admission_price_info_%s' % lang_code,
            'reduced_price_info_%s' % lang_code,
            'arrangements_for_children_%s' % lang_code,
            'free_entrance_for_%s' % lang_code,
            'family_ticket_%s' % lang_code,
            'group_ticket_%s' % lang_code,
            'free_entrance_times_%s' % lang_code,
            'yearly_ticket_%s' % lang_code,
            'other_tickets_%s' % lang_code,
            ]
    for f in fields:
        setattr(instance, f, form_step_data['prices'][f])

    for lang_code, lang_name in FRONTEND_LANGUAGES:
        for f in [
            'admission_price_info_%s' % lang_code,
            'reduced_price_info_%s' % lang_code,
            'arrangements_for_children_%s' % lang_code,
            'free_entrance_for_%s' % lang_code,
            'family_ticket_%s' % lang_code,
            'group_ticket_%s' % lang_code,
            'free_entrance_times_%s' % lang_code,
            'yearly_ticket_%s' % lang_code,
            'other_tickets_%s' % lang_code,
            ]:
            setattr(instance, f + "_markup_type", MARKUP_PLAIN_TEXT)

    fields = ['street_address', 'street_address2', 'postal_code', 'district',
        'city', 'latitude', 'longitude',
        'phone_country', 'phone_area', 'phone_number',
        'group_bookings_phone_country', 'group_bookings_phone_area', 'group_bookings_phone_number',
        'service_phone_country', 'service_phone_area', 'service_phone_number',
        'fax_country', 'fax_area', 'fax_number',
        'email', 'website', 'twitter', 'facebook',
        'contact_name', 'contact_phone_country', 'contact_phone_area', 'contact_phone_number', 'contact_email',
        'post_street_address', 'post_street_address2', 'post_postal_code', 'post_city',
        ]
    for f in fields:
        setattr(instance, f, form_step_data['address'][f])
    
    
    instance.service_shop = form_step_data['services_accessibility']['service_shop']
    instance.service_books = form_step_data['services_accessibility']['service_books']
    instance.service_restaurant = form_step_data['services_accessibility']['service_restaurant']
    instance.service_cafe = form_step_data['services_accessibility']['service_cafe']
    instance.service_library = form_step_data['services_accessibility']['service_library']
    instance.service_archive = form_step_data['services_accessibility']['service_archive']
    instance.service_studio = form_step_data['services_accessibility']['service_studio']
    instance.service_online = form_step_data['services_accessibility']['service_online']
    instance.service_diaper_changing_table = form_step_data['services_accessibility']['service_diaper_changing_table']
    instance.service_birthdays = form_step_data['services_accessibility']['service_birthdays']
    instance.service_rent = form_step_data['services_accessibility']['service_rent'] 
    instance.service_other = form_step_data['services_accessibility']['service_other']
    
    for lang_code, lang_name in FRONTEND_LANGUAGES:
        setattr(instance, 'accessibility_%s' % lang_code, form_step_data['services_accessibility']['accessibility_%s' % lang_code])
        setattr(instance, 'service_shop_info_%s' % lang_code, form_step_data['services_accessibility']['service_shop_info_%s' % lang_code])
        setattr(instance, 'service_books_info_%s' % lang_code, form_step_data['services_accessibility']['service_books_info_%s' % lang_code]) 
        setattr(instance, 'service_restaurant_info_%s' % lang_code, form_step_data['services_accessibility']['service_restaurant_info_%s' % lang_code])
        setattr(instance, 'service_cafe_info_%s' % lang_code, form_step_data['services_accessibility']['service_cafe_info_%s' % lang_code])
        setattr(instance, 'service_library_info_%s' % lang_code, form_step_data['services_accessibility']['service_library_info_%s' % lang_code])
        setattr(instance, 'service_archive_info_%s' % lang_code, form_step_data['services_accessibility']['service_archive_info_%s' % lang_code])
        setattr(instance, 'service_studio_info_%s' % lang_code, form_step_data['services_accessibility']['service_studio_info_%s' % lang_code])
        setattr(instance, 'service_online_info_%s' % lang_code, form_step_data['services_accessibility']['service_online_info_%s' % lang_code])
        setattr(instance, 'service_birthdays_info_%s' % lang_code, form_step_data['services_accessibility']['service_birthdays_info_%s' % lang_code])
        setattr(instance, 'service_rent_info_%s' % lang_code, form_step_data['services_accessibility']['service_rent_info_%s' % lang_code])
        setattr(instance, 'service_other_info_%s' % lang_code, form_step_data['services_accessibility']['service_other_info_%s' % lang_code])

    for lang_code, lang_name in FRONTEND_LANGUAGES:
        for f in [
            'accessibility_%s' % lang_code,
            'service_shop_info_%s' % lang_code,
            'service_books_info_%s' % lang_code,
            'service_restaurant_info_%s' % lang_code,
            'service_cafe_info_%s' % lang_code,
            'service_library_info_%s' % lang_code,
            'service_archive_info_%s' % lang_code,
            'service_studio_info_%s' % lang_code,
            'service_online_info_%s' % lang_code,
            'service_birthdays_info_%s' % lang_code,
            'service_rent_info_%s' % lang_code,
            'service_other_info_%s' % lang_code,
            ]:
            setattr(instance, f + "_markup_type", MARKUP_PLAIN_TEXT)


    for lang_code, lang_name in FRONTEND_LANGUAGES:
        setattr(instance, 'mediation_offer_%s' % lang_code, form_step_data['mediation']['mediation_offer_%s' % lang_code])
        setattr(instance, 'mediation_offer_%s_markup_type' % lang_code, MARKUP_PLAIN_TEXT)

    instance.status = "published"
    instance.save()
    
    instance.categories.clear()
    for cat in form_step_data['basic']['categories']:
        instance.categories.add(cat)
        
    instance.accessibility_options.clear()
    for cat in form_step_data['services_accessibility']['accessibility_options']:
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

MUSEUM_FORM_STEPS = {
    'basic': {
        'title': _("Basic Information"),
        'template': "museums/forms/basic_info_form.html",
        'form': BasicInfoForm,
    },
    'opening': {
        'title': _("Opening times"),
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
    'services_accessibility': {
        'title': _("Services and Accessibility"),
        'template': "museums/forms/services_accessibility_form.html",
        'form': ServicesAccessibilityForm,
    },
    'mediation': {
        'title': _("Mediation"),
        'template': "museums/forms/mediation_form.html",
        'form': MediationForm,
    },
    'oninit': load_data,
    'onsubmit': submit_step,
    'onsave': save_data,
    'name': 'museum_registration',
    'default_path': ["basic", "opening", "prices", "address", "services_accessibility", "mediation"],
}


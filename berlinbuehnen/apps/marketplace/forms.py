# -*- coding: UTF-8 -*-
from datetime import datetime
try:
    from django.utils.timezone import now as tz_now
except:
    tz_now = datetime.now

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _, ugettext
from django.utils.safestring import mark_safe

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from .models import JobOffer, JobCategory, JobType

FRONTEND_LANGUAGES = getattr(settings, "FRONTEND_LANGUAGES", settings.LANGUAGES)
EXCLUDED_LANGUAGES = set(dict(settings.LANGUAGES).keys()) - set(dict(FRONTEND_LANGUAGES).keys())

from berlinbuehnen.utils.forms import PrimarySubmit
from berlinbuehnen.utils.forms import SecondarySubmit


class JobOfferForm(forms.ModelForm):

    class Meta:
        model = JobOffer
        fields = [
            'deadline',
            'street_address', 'street_address2', 'postal_code', 'city', 'latitude', 'longitude',
            'phone_country', 'phone_area', 'phone_number',
            'fax_country', 'fax_area', 'fax_number',
            'email', 'website',
            'categories', 'job_type',
        ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'title_%s' % lang_code,
                'subtitle_%s' % lang_code,
                'position_%s' % lang_code,
                'description_%s' % lang_code,
                'remarks_%s' % lang_code,
            ]

    def __init__(self, *args, **kwargs):
        super(JobOfferForm, self).__init__(*args, **kwargs)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'title_%s' % lang_code,
                'subtitle_%s' % lang_code,
                'description_%s' % lang_code,
                'teaser_%s' % lang_code,
                'tickets_calling_prices_%s' % lang_code,
                'tickets_additional_info_%s' % lang_code,
            ]:
                self.fields[f].label += """ <span class="lang">%s</span>""" % lang_code.upper()

        self.fields['latitude'].widget = forms.HiddenInput()
        self.fields['longitude'].widget = forms.HiddenInput()

        self.fields['districts'].widget = forms.CheckboxSelectMultiple()
        self.fields['districts'].help_text = ""
        self.fields['districts'].empty_label = None

        self.fields['categories'].widget = forms.CheckboxSelectMultiple()
        self.fields['categories'].help_text = ""
        self.fields['categories'].empty_label = None

        self.fields['services'].widget = forms.CheckboxSelectMultiple()
        self.fields['services'].help_text = ""
        self.fields['services'].empty_label = None

        self.fields['accessibility_options'].widget = forms.CheckboxSelectMultiple()
        choices = []
        for access_opt in self.fields['accessibility_options'].queryset:
            choices.append((access_opt.pk, mark_safe("""
                <img src="%s%s" alt="" /> %s
                """ % (settings.MEDIA_URL, access_opt.image.path, access_opt.title) )))
        self.fields['accessibility_options'].choices = choices
        self.fields['accessibility_options'].help_text = ""
        self.fields['accessibility_options'].empty_label = None

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
                layout.Field('description_%s' % lang_code, disabled="disabled"),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('teaser_%s' % lang_code, disabled="disabled"),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))

        layout_blocks.append(layout.Fieldset(
            _("Basic Info"),
            css_class="fieldset-basic-info",
            *fieldset_content  # ... then pass them to a fieldset
        ))

        layout_blocks.append(layout.Fieldset(
            _("Logo"),
            layout.Row(
                layout.Div(
                    layout.HTML("""{% load i18n %}
                        <div id="logo_upload_widget">
                            <div class="preview">
                                {% if location.logo %}
                                    <img src="{{ location.logo.url }}" alt="" class="img-responsive" />
                                {% endif %}
                            </div>
                            <div class="uploader">
                                <noscript>
                                    <p>{% trans "Please enable Javascript to use file uploader." %}</p>
                                </noscript>
                            </div>
                            <p class="help_text help-block">
                                {% trans "Available formats are JPG, GIF, and PNG." %}
                            </p>
                            <div class="messages"></div>
                        </div>
                    """),
                    "logo_path",
                    "delete_logo",
                    css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12"
                ),
            )
        ))

        layout_blocks.append(layout.Fieldset(
            _("Address"),
            layout.Row(
                layout.Div(
                    "street_address",
                    "street_address2",
                    "postal_code",
                    "city",
                    css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                ),
                layout.Div(
                    layout.HTML("""{% load i18n %}
                        <div class="dyn_set_map">
                            <label>{% trans "Location" %}</label>
                            <div class="map_canvas">
                            </div>
                            <div class="form-actions">
                                <input type="button" class="locate_address btn btn-primary" value="{% trans "Relocate on map" %}" />&zwnj;
                                <!--<input type="button" class="remove_geo btn btn-primary" value="{% trans "Remove from map" %}"/>&zwnj;-->
                            </div>
                            <div class="map_locations">
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
            _("Districts"),
            "districts",
            css_class="fieldset-services",
        ))

        layout_blocks.append(layout.Fieldset(
            _("Contact"),

            layout.Row(
                layout.Div(
                    'email', css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                ),
                layout.Div(
                    layout.Field('website', placeholder="http://"), css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                ),
                css_class="row-md"
            ),

            layout.Row(
                layout.Div(
                    layout.HTML('{% load i18n %}<div><label class="with">{% trans "Phone" %}</label></div>'),
                    layout.Row(
                        layout.Div(
                            'phone_country', css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                        ),
                        layout.Div(
                            'phone_area',  css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                        ),
                        layout.Div(
                            'phone_number', css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                        ),
                        css_class="row-xs"
                    ),
                     css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                ),
                layout.Div(
                    layout.HTML('{% load i18n %}<div><label class="with">{% trans "Fax" %}</label></div>'),
                    layout.Row(
                        layout.Div(
                            'fax_country', css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                        ),
                        layout.Div(
                            'fax_area', css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                        ),
                        layout.Div(
                            'fax_number', css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                        ),
                        css_class="row-xs"
                    ),
                    css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                ),
                css_class="row-md"
            ),

            css_class="fieldset-other-contact-info"
        ))

        layout_blocks.append(layout.Fieldset(
            _("Social media"),
            layout.HTML("""{% load crispy_forms_tags i18n %}
            {{ formsets.social.management_form }}
            <div id="social">
                {% for form in formsets.social.forms %}
                    <div class="social formset-form tabular-inline">
                        {% crispy form %}
                    </div>
                {% endfor %}
            </div>
            <!-- used by javascript -->
            <div id="social_empty_form" class="social formset-form tabular-inline" style="display: none">
                {% with formsets.social.empty_form as form %}
                    {% crispy form %}
                {% endwith %}
            </div>
            """),
            css_id="social_channels_fieldset",
        ))

        layout_blocks.append(layout.Fieldset(
            _("Tickets Box Office (when differs from location address)"),
            layout.Row(
                layout.Div(
                    "tickets_street_address",
                    "tickets_street_address2",
                    "tickets_postal_code",
                    "tickets_city",
                    css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                ),
                layout.Div(
                    "tickets_email",
                    "tickets_website",
                    layout.HTML('{% load i18n %}<div><label class="with">{% trans "Phone" %}</label></div>'),
                    layout.Row(
                        layout.Div(
                            'tickets_phone_country', css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                        ),
                        layout.Div(
                            'tickets_phone_area',  css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                        ),
                        layout.Div(
                            'tickets_phone_number', css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                        ),
                        css_class="row-xs"
                    ),
                    layout.HTML('{% load i18n %}<div><label class="with">{% trans "Fax" %}</label></div>'),
                    layout.Row(
                        layout.Div(
                            'tickets_fax_country', css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                        ),
                        layout.Div(
                            'tickets_fax_area', css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                        ),
                        layout.Div(
                            'tickets_fax_number', css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                        ),
                        css_class="row-xs"
                    ),
                    css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                ),
                css_class="row-md",
            ),
            layout.Row(
                css_class="row-md",
                *[layout.Div(
                    layout.Field('tickets_calling_prices_%s' % lang_code),
                    css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                ) for lang_code, lang_name in FRONTEND_LANGUAGES]
            ),
            layout.Row(
                css_class="row-md",
                *[layout.Div(
                    layout.Field('tickets_additional_info_%s' % lang_code),
                    css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                ) for lang_code, lang_name in FRONTEND_LANGUAGES]
            ),
            css_class="fieldset-tickets",
        ))

        layout_blocks.append(layout.Fieldset(
            _("Opening Hours of Tickets Box Office"),
            layout.Row(
                layout.Div(
                    'mon_open',
                    css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                ),
                layout.Div(
                    'mon_break_close',
                    css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                ),
                layout.Div(
                    'mon_break_open',
                    css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                ),
                layout.Div(
                    'mon_close',
                    css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                ),
                css_class="row-md",
            ),
            layout.Row(
                layout.Div(
                    'tue_open',
                    css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                ),
                layout.Div(
                    'tue_break_close',
                    css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                ),
                layout.Div(
                    'tue_break_open',
                    css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                ),
                layout.Div(
                    'tue_close',
                    css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                ),
                css_class="row-md",
            ),
            layout.Row(
                layout.Div(
                    'wed_open',
                    css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                ),
                layout.Div(
                    'wed_break_close',
                    css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                ),
                layout.Div(
                    'wed_break_open',
                    css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                ),
                layout.Div(
                    'wed_close',
                    css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                ),
                css_class="row-md",
            ),
            layout.Row(
                layout.Div(
                    'thu_open',
                    css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                ),
                layout.Div(
                    'thu_break_close',
                    css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                ),
                layout.Div(
                    'thu_break_open',
                    css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                ),
                layout.Div(
                    'thu_close',
                    css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                ),
                css_class="row-md",
            ),
            layout.Row(
                layout.Div(
                    'fri_open',
                    css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                ),
                layout.Div(
                    'fri_break_close',
                    css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                ),
                layout.Div(
                    'fri_break_open',
                    css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                ),
                layout.Div(
                    'fri_close',
                    css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                ),
                css_class="row-md",
            ),
            layout.Row(
                layout.Div(
                    'sat_open',
                    css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                ),
                layout.Div(
                    'sat_break_close',
                    css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                ),
                layout.Div(
                    'sat_break_open',
                    css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                ),
                layout.Div(
                    'sat_close',
                    css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                ),
                css_class="row-md",
            ),
            layout.Row(
                layout.Div(
                    'sun_open',
                    css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                ),
                layout.Div(
                    'sun_break_close',
                    css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                ),
                layout.Div(
                    'sun_break_open',
                    css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                ),
                layout.Div(
                    'sun_close',
                    css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                ),
                css_class="row-md",
            ),
            css_class="fieldset-tickets",
        ))

        layout_blocks.append(layout.Fieldset(
            _("Press Contact"),

            layout.Row(
                layout.Div(
                    'press_contact_name', css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12"
                ),
                css_class="row-md"
            ),

            layout.Row(
                layout.Div(
                    'press_email', css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                ),
                layout.Div(
                    layout.Field('press_website', placeholder="http://"), css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                ),
                css_class="row-md"
            ),

            layout.Row(
                layout.Div(
                    layout.HTML('{% load i18n %}<div><label class="with">{% trans "Phone" %}</label></div>'),
                    layout.Row(
                        layout.Div(
                            'press_phone_country', css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                        ),
                        layout.Div(
                            'press_phone_area',  css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                        ),
                        layout.Div(
                            'press_phone_number', css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                        ),
                        css_class="row-xs"
                    ),
                     css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                ),
                layout.Div(
                    layout.HTML('{% load i18n %}<div><label class="with">{% trans "Fax" %}</label></div>'),
                    layout.Row(
                        layout.Div(
                            'press_fax_country', css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                        ),
                        layout.Div(
                            'press_fax_area', css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                        ),
                        layout.Div(
                            'press_fax_number', css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                        ),
                        css_class="row-xs"
                    ),
                    css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                ),
                css_class="row-md"
            ),
            css_class="fieldset-press_contact",
        ))

        layout_blocks.append(layout.Fieldset(
            _("Categories"),
            "categories",
            css_class="fieldset-services",
        ))
        layout_blocks.append(layout.Fieldset(
            _("Service"),
            "services",
            css_class="fieldset-services",
        ))
        layout_blocks.append(layout.Fieldset(
            _("Accessibility"),
            "accessibility_options",
            css_class="fieldset-accessibility",
        ))

        if self.instance and self.instance.pk:
            layout_blocks.append(bootstrap.FormActions(
                PrimarySubmit('submit', _('Next')),
                SecondarySubmit('save_and_close', _('Save and close')),
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

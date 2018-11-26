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
EXCLUDED_LANGUAGES = set(dict(settings.LANGUAGES).keys()
                        ) - set(dict(FRONTEND_LANGUAGES).keys())

from ruhrbuehnen.utils.forms import PrimarySubmit
from ruhrbuehnen.utils.forms import SecondarySubmit


class JobOfferForm(forms.ModelForm):
    class Meta:
        model = JobOffer
        fields = [
            'deadline',
            'start_contract_on',
            'street_address',
            'street_address2',
            'postal_code',
            'city',
            'latitude',
            'longitude',
            'name',
            'phone_country',
            'phone_area',
            'phone_number',
            'fax_country',
            'fax_area',
            'fax_number',
            'email',
            'website',
            'company',
            'categories',
            'job_type',
        ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                #'title_%s' % lang_code,
                #'subtitle_%s' % lang_code,
                'position_%s' % lang_code,
                'description_%s' % lang_code,
                'remarks_%s' % lang_code,
            ]

    def __init__(self, *args, **kwargs):
        super(JobOfferForm, self).__init__(*args, **kwargs)

        self.fields['deadline'].widget = forms.DateInput(format='%Y-%m-%d')
        self.fields['deadline'].input_formats = ('%Y-%m-%d', )
        self.fields['start_contract_on'].widget = forms.DateInput(
            format='%Y-%m-%d'
        )
        self.fields['start_contract_on'].input_formats = ('%Y-%m-%d', )

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                #'title_%s' % lang_code,
                #'subtitle_%s' % lang_code,
                'position_%s' % lang_code,
                'description_%s' % lang_code,
                'remarks_%s' % lang_code,
            ]:
                self.fields[
                    f
                ].label += """ <span class="lang">%s</span>""" % lang_code.upper(
                )

        self.fields['latitude'].widget = forms.HiddenInput()
        self.fields['longitude'].widget = forms.HiddenInput()

        self.fields['categories'].widget = forms.CheckboxSelectMultiple()
        self.fields['categories'].help_text = ""
        self.fields['categories'].empty_label = None

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"

        layout_blocks = []

        fieldset_content = [
            layout.Row(
                css_class="row-md",
                *[
                    layout.Div(
                        layout.Field('position_%s' % lang_code),
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ) for lang_code, lang_name in FRONTEND_LANGUAGES
                ]
            ),
            layout.Row(
                css_class="row-md",
                *[
                    layout.Div(
                        layout.Field('description_%s' % lang_code),
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ) for lang_code, lang_name in FRONTEND_LANGUAGES
                ]
            )
        ]  # collect multilingual divs into one list...
        #fieldset_content.append(layout.Row(
        #    css_class="row-md",
        #    *[layout.Div(
        #        layout.Field('title_%s' % lang_code),
        #        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
        #    ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        #))
        #fieldset_content.append(layout.Row(
        #    css_class="row-md",
        #    *[layout.Div(
        #        layout.Field('subtitle_%s' % lang_code),
        #        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
        #    ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        #))
        layout_blocks.append(
            layout.Fieldset(
                _("Basic Info"),
                css_class="fieldset-basic-info",
                *fieldset_content  # ... then pass them to a fieldset
            )
        )

        layout_blocks.append(
            layout.Fieldset(
                _("Company"),
                layout.Row(
                    layout.Div(
                        "company",
                        "street_address",
                        "street_address2",
                        "postal_code",
                        "city",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                    ),
                    layout.Div(
                        layout.HTML(
                            """{% load i18n %}
                        <div class="dyn_set_map">
                            <label>{% trans "Company" %}</label>
                            <div class="map_canvas">
                            </div>
                            <div class="form-actions">
                                <input type="button" class="locate_address btn btn-primary" value="{% trans "Relocate on map" %}" />&zwnj;
                                <!--<input type="button" class="remove_geo btn btn-primary" value="{% trans "Remove from map" %}"/>&zwnj;-->
                            </div>
                            <div class="map_locations">
                            </div>
                        </div>
                    """
                        ),
                        "latitude",
                        "longitude",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                    ),
                    css_class="row-md",
                ),
                css_class="fieldset-where",
            )
        )

        layout_blocks.append(
            layout.Fieldset(
                _("Contact"),
                "name",
                layout.Row(
                    layout.Div(
                        'email',
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                    ),
                    layout.Div(
                        layout.Field('website', placeholder="http://"),
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                    ),
                    css_class="row-md"
                ),
                layout.Row(
                    layout.Div(
                        layout.HTML(
                            '{% load i18n %}<div><label class="with">{% trans "Phone" %}</label></div>'
                        ),
                        layout.Row(
                            layout.Div(
                                'phone_country',
                                css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                            ),
                            layout.Div(
                                'phone_area',
                                css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                            ),
                            layout.Div(
                                'phone_number',
                                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                            ),
                            css_class="row-xs"
                        ),
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                    ),
                    layout.Div(
                        layout.HTML(
                            '{% load i18n %}<div><label class="with">{% trans "Fax" %}</label></div>'
                        ),
                        layout.Row(
                            layout.Div(
                                'fax_country',
                                css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                            ),
                            layout.Div(
                                'fax_area',
                                css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                            ),
                            layout.Div(
                                'fax_number',
                                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                            ),
                            css_class="row-xs"
                        ),
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                    ),
                    css_class="row-md"
                ),
                css_class="fieldset-other-contact-info"
            )
        )

        layout_blocks.append(
            layout.Fieldset(
                _("Type"),
                "job_type",
                css_class="fieldset-services",
            )
        )

        layout_blocks.append(
            layout.Fieldset(
                _("Categories"),
                "categories",
                css_class="fieldset-services",
            )
        )

        layout_blocks.append(
            layout.Fieldset(
                _("Dates"),
                layout.Row(
                    layout.Div(
                        'deadline',
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                    ),
                    layout.Div(
                        'start_contract_on',
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                    ),
                    css_class="row-md"
                ),
                css_class="fieldset-services",
            )
        )

        fieldset_content = [
            layout.Row(
                css_class="row-md",
                *[
                    layout.Div(
                        layout.Field('remarks_%s' % lang_code),
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ) for lang_code, lang_name in FRONTEND_LANGUAGES
                ]
            )
        ]  # collect multilingual divs into one list...
        layout_blocks.append(
            layout.Fieldset(
                _("Remarks"),
                css_class="fieldset-basic-info",
                *fieldset_content  # ... then pass them to a fieldset
            )
        )

        if self.instance and self.instance.pk:
            layout_blocks.append(
                bootstrap.FormActions(
                    PrimarySubmit('submit', _('Save and close')),
                    SecondarySubmit('reset', _('Cancel')),
                )
            )
        else:
            layout_blocks.append(
                bootstrap.FormActions(
                    PrimarySubmit('submit', _('Save and close')),
                    SecondarySubmit('reset', _('Cancel')),
                )
            )

        self.helper.layout = layout.Layout(*layout_blocks)

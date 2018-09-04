# -*- coding: utf-8 -*-

from django.db import models
from django import forms
from django.forms.models import ModelForm
from django.forms.models import inlineformset_factory
from django.conf import settings
from django.utils.translation import ugettext_lazy as _, ugettext
from django.shortcuts import redirect
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from babeldjango.templatetags.babel import decimalfmt

from base_libs.forms.fields import AutocompleteModelChoiceField, DecimalField
from base_libs.models.base_libs_settings import MARKUP_HTML_WYSIWYG, MARKUP_PLAIN_TEXT
from base_libs.middleware import get_current_user

Museum = models.get_model("museums", "Museum")
Season = models.get_model("museums", "Season")
SpecialOpeningTime = models.get_model("museums", "SpecialOpeningTime")
SocialMediaChannel = models.get_model("museums", "SocialMediaChannel")

FRONTEND_LANGUAGES = getattr(settings, "FRONTEND_LANGUAGES", settings.LANGUAGES)
EXCLUDED_LANGUAGES = set(dict(settings.LANGUAGES).keys()) - set(dict(FRONTEND_LANGUAGES).keys())

from museumsportal.utils.forms import PrimarySubmit
from museumsportal.utils.forms import SecondarySubmit
from museumsportal.utils.forms import InlineFormSet

# translatable strings to collect
_("Name")
_("Subtitle")
_("Description")
_("Categories")
_("Tags")
_("Special for children")
_("Particularities")
_("Opening Hours")
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
_("Available Offers")
_("Location")
_("Relocate on map")
_("Remove from map")
_("Phone")
_("Fax")
_("Booking Phone")
_("Service Phone")
_("Available Services")
_("Languages")
_("Available Audioguides")


class BasicInfoForm(ModelForm):
    class Meta:
        model = Museum

        fields = []

    def __init__(self, *args, **kwargs):
        super(BasicInfoForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"

        layout_blocks = []

        layout_blocks.append(layout.Fieldset(
            _("Basic Info"),

            layout.HTML("""{% load i18n %}
                <div class="row row-md">
                    <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">
                        <div id="div_id_title_de" class="form-group">
                            <label for="id_title_de" class="control-label requiredField">{% trans "Name" %} <span class="lang">DE</span><span class="asteriskField">*</span></label>
                            <div class="controls">
                                <input disabled="disabled" name="title_de" value="{{ museum.title_de|escape }}" class="textinput textInput form-control form_text" maxlength="255" type="text" id="id_title_de">
                            </div>
                        </div>
                    </div>
                    <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">
                        <div id="div_id_title_en" class="form-group">
                            <label for="id_title_de" class="control-label requiredField">{% trans "Name" %} <span class="lang">EN</span><span class="asteriskField">*</span></label>
                            <div class="controls">
                                <input disabled="disabled" name="title_en" value="{{ museum.title_en|escape }}" class="textinput textInput form-control form_text" maxlength="255" type="text" id="id_title_en">
                            </div>
                        </div>
                    </div>
                </div>
                <div class="row row-md">
                    <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">
                        <div id="div_id_subtitle_de" class="form-group">
                            <label for="id_subtitle_de" class="control-label requiredField">{% trans "Subtitle" %} <span class="lang">DE</span><span class="asteriskField">*</span></label>
                            <div class="controls">
                                <input disabled="disabled" name="subtitle_de" value="{{ museum.subtitle_de|escape }}" class="textinput textInput form-control form_text" maxlength="255" type="text" id="id_subtitle_de">
                            </div>
                        </div>
                    </div>
                    <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">
                        <div id="div_id_subtitle_en" class="form-group">
                            <label for="id_subtitle_en" class="control-label requiredField">{% trans "Subtitle" %} <span class="lang">EN</span><span class="asteriskField">*</span></label>
                            <div class="controls">
                                <input disabled="disabled" name="subtitle_en" value="{{ museum.subtitle_en|escape }}" class="textinput textInput form-control form_text" maxlength="255" type="text" id="id_subtitle_en">
                            </div>
                        </div>
                    </div>
                </div>
                <div class="row row-md">
                    <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">
                        <div id="div_id_description_de" class="form-group">
                            <label for="id_description_de" class="control-label requiredField">{% trans "Description" %} <span class="lang">DE</span><span class="asteriskField">*</span></label>
                            <div class="controls">
                                <div id="id_description_de" name="description_de" class="form-control textarea" aria-hidden="true">
                                    {{ museum.description_de|safe }}
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">
                        <div id="div_id_description_en" class="form-group">
                            <label for="id_description_en" class="control-label requiredField">{% trans "Description" %} <span class="lang">EN</span><span class="asteriskField">*</span></label>
                            <div class="controls">
                                <div id="id_description_en" name="description_en" class="form-control textarea" aria-hidden="true">
                                    {{ museum.description_en|safe }}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            """),

            css_class="fieldset-basic-info",
        ))

        layout_blocks.append(layout.Fieldset(
            _("Categories and Tags"),
            layout.HTML("""{% load i18n base_tags %}
                <div id="div_id_categories" class="clearfix form-group">
                    <label for="id_categories_0" class="control-label requiredField">{% trans "Categories" %}<span class="asteriskField">*</span></label>
                    <div class="checkbox-group">
                        {% get_objects all museums.MuseumCategory as museum_categories %}
                        {% for cat in museum_categories %}
                            <div class="form-group level-{{ cat.level }}">
                                <div class="checkbox">
                                    <label><input type="checkbox" name="categories" id="id_categories_{{ forloop.counter }}" value="{{ cat.id }}" disabled="disabled"{% if cat in museum.categories.all %} checked="checked"{% endif %}> {{ cat.title }}</label>
                                </div>
                            </div>
                        {% endfor %}
                    </div>
                </div>
                {% if museum.get_tags %}
                    <div id="div_id_tags" class="clearfix form-group">
                        <label for="id_tags" class="control-label">{% trans "Tags" %} </label>
                        <div class="checkbox-group">
                            <div id="id_tags_tagsinput" class="tagsinput">
                                {% for tag in museum.get_tags %}
                                    <span class="btn btn-primary tag"><span>{{ tag.name }}</span></span>
                                {% endfor %}
                                <div class="tags_clear"></div>
                            </div>
                        </div>
                    </div>
                {% endif %}

                <div class="inline">
                    <div id="div_id_is_for_children" class="clearfix control-group">
                        <div class="controls">
                            <label for="id_is_for_children" class="checkbox">
                                <input id="id_is_for_children"{% if museum.is_for_children %} checked="checked"{% endif %} type="checkbox" class="checkboxinput form_checkbox" name="is_for_children" disabled="disabled" />
                                {% trans "Special for children" %}
                            </label>
                        </div>
                    </div>
                </div>

            """),
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
            exclude.append("title_%s" % lang_code)
            exclude.append("last_entry_%s" % lang_code)
            exclude.append("exceptions_%s" % lang_code)

    def __init__(self, *args, **kwargs):
        super(SeasonForm, self).__init__(*args, **kwargs)

        self.fields['start'].widget = forms.DateInput(format='%d.%m.%Y')
        self.fields['start'].input_formats=('%d.%m.%Y',)

        self.fields['end'].widget = forms.DateInput(format='%d.%m.%Y')
        self.fields['end'].input_formats=('%d.%m.%Y',)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            self.fields['title_%s' % lang_code].required = True
            self.fields['exceptions_%s' % lang_code].label = _("Additional Information")

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'title_%s' % lang_code,
                'last_entry_%s' % lang_code,
                'exceptions_%s' % lang_code,
            ]:
                self.fields[f].label += """ <span class="lang">%s</span>""" % lang_code.upper()

        self.fields["is_appointment_based"].label = _("Open by appointment only")
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
                layout.Field('title_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content += [
            layout.Row(
                layout.Div(
                    bootstrap.PrependedText("start", "", placeholder="dd.mm.yyyy", autocomplete="off"), css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                ),
                layout.Div(
                    bootstrap.PrependedText("end", "", placeholder="dd.mm.yyyy", autocomplete="off"), css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                ),
                css_class="row-md",
            ),
            layout.Div(
                layout.HTML("""{% load i18n %} <label>{% trans "Particularities" %}</label> """),
                'is_appointment_based',
            ),
        ]

        layout_blocks.append(layout.Fieldset(
            _("Season"),
            css_class="fieldset-season",
            *fieldset_content
        ))

        fieldset_content = [
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
            """)
        ]

        layout_blocks.append(layout.Fieldset(
            "",
            css_class="fieldset-season-opening-hours no-legend",
            *fieldset_content
        ))

        fieldset_content = []
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
        fieldset_content.append(
            layout.Field('id'),
        )
        fieldset_content.append(
            layout.Field('DELETE'),
        )

        layout_blocks.append(layout.Fieldset(
            _("Additional info"),
            css_class="fieldset-additional-info",
            *fieldset_content
        ))

        self.helper.layout = layout.Layout(
            *layout_blocks
        )

SeasonFormset = inlineformset_factory(Museum, Season, form=SeasonForm, formset=InlineFormSet, extra=0)


class SpecialOpeningTimeForm(ModelForm):
    class Meta:
        model = SpecialOpeningTime
        exclude = []
        for lang_code, lang_name in settings.LANGUAGES:
            exclude.append("exceptions_%s_markup_type" % lang_code)
        for lang_code in EXCLUDED_LANGUAGES:
            exclude.append("day_label_%s" % lang_code)
            exclude.append("exceptions_%s" % lang_code)

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

        self.fields['day_label_de'].help_text = u"e.g. Weihnachten, Ostern, etc."
        self.fields['day_label_de'].help_text = u"e.g. Christmas, Easter, etc."

        self.helper = FormHelper()
        self.helper.form_tag = False
        layout_blocks = []

        fieldset_content = []  # collect multilingual divs into one list...
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('day_label_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))

        layout_blocks.append(layout.Fieldset(
            _("Occasion"),
            css_class="fieldset-additional-info",
            *fieldset_content
        ))

        layout_blocks.append(layout.Fieldset(
            _("Special date"),

            layout.Row(
                layout.Div(
                    "yyyy", css_class="col-xs-4 col-sm-4 col-md-4 col-lg-4"
                ),
                layout.Div(
                    "mm", css_class="col-xs-4 col-sm-4 col-md-4 col-lg-4"
                ),
                layout.Div(
                    "dd", css_class="col-xs-4 col-sm-4 col-md-4 col-lg-4"
                ),
                css_class="row-md"
            ),

            css_class="fieldset-special-date",
        ))

        layout_blocks.append(layout.Fieldset(
            _("Opening hours"),
            "is_closed",
            "is_regular",
            layout.Row(
                layout.Div(
                    bootstrap.PrependedText("opening", "", placeholder="00:00", autocomplete="off"),
                    css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                ),
                layout.Div(
                    bootstrap.PrependedText("break_close", "", placeholder="00:00", autocomplete="off"),
                    css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                ),
                layout.Div(
                    bootstrap.PrependedText("break_open", "", placeholder="00:00", autocomplete="off"),
                    css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                ),
                layout.Div(
                    bootstrap.PrependedText("closing", "", placeholder="00:00", autocomplete="off"),
                    css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                ),
                css_class="row-md",
                ),
            css_class="fieldset-opening-times",
        ))

        fieldset_content = []  # collect multilingual divs into one list...
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('exceptions_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(
            layout.Field('id'),
        )
        fieldset_content.append(
            layout.Field('DELETE'),
        )

        layout_blocks.append(layout.Fieldset(
            _("Additional info"),
            css_class="fieldset-additional-info",
            *fieldset_content
        ))

        self.helper.layout = layout.Layout(
            *layout_blocks
        )

SpecialOpeningTimeFormset = inlineformset_factory(Museum, SpecialOpeningTime, form=SpecialOpeningTimeForm, formset=InlineFormSet, extra=0)


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

        fieldset_content = []  # collect multilingual divs into one list...
        fieldset_content.append(
            layout.Div('free_entrance')
        )
        fieldset_content.append(
            layout.Field('admission_price', placeholder=decimalfmt(0, "#,##0.00"))
        )
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('admission_price_info_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))

        layout_blocks.append(layout.Fieldset(
            _("Admission"),
            css_class="fieldset-prices",
            *fieldset_content
        ))

        fieldset_content = []
        fieldset_content.append(
            layout.Field('reduced_price', placeholder=decimalfmt(0, "#,##0.00"))
        )
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('reduced_price_info_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))

        layout_blocks.append(layout.Fieldset(
            _("Reduced Prices"),
            *fieldset_content
        ))

        fieldset_content = []
        fieldset_content.append(
            layout.Div(
                layout.HTML("""{% load i18n %} <label>{% trans "Available Offers" %}</label> """),
                'member_of_museumspass',
                'show_family_ticket',
                'show_yearly_ticket',
                'show_group_ticket',
                css_class="checkbox-group"
            )
        )
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('group_ticket_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))

        layout_blocks.append(layout.Fieldset(
            _("Offers"),
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


class AddressForm(ModelForm):
    parent = AutocompleteModelChoiceField(
        required=False,
        label=_("Parent museum"),
        # help_text=u"Bitte geben Sie einen Anfangsbuchstaben ein, um eine entsprechende Auswahl der verfügbaren Museums angezeigt zu bekommen.",
        app="museums",
        qs_function="get_published_museums",
        display_attr="title",
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
        model = Museum
        fields = ['parent', 'street_address', 'street_address2', 'postal_code',
            'city', 'latitude', 'longitude',
            'phone_country', 'phone_area', 'phone_number',
            'group_bookings_phone_country', 'group_bookings_phone_area', 'group_bookings_phone_number',
            'service_phone_country', 'service_phone_area', 'service_phone_number',
            'fax_country', 'fax_area', 'fax_number', 'email', 'website',
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
                    'parent',
                    'street_address',
                    'street_address2',
                    'postal_code',
                    'city',
                    css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                ),
                layout.Div(
                    layout.HTML("""{% load i18n %}
                        <div id="dyn_set_map">
                            <label>{% trans "Location" %}</label>
                            <div class="museum_map" id="gmap-wrapper">
                                <!-- THE GMAPS WILL BE INSERTED HERE DYNAMICALLY -->
                            </div>
                            <div class="form-actions">
                                <input id="dyn_locate_geo" type="button" class="btn btn-primary" value="{% trans "Relocate on map" %}" />&zwnj;
                                <!--<input id="dyn_remove_geo" type="button" class="btn btn-primary" value="{% trans "Remove from map" %}"/>&zwnj;-->
                            </div>
                        </div>
                    """),
                    'latitude',
                    'longitude',
                    css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                ),
                css_class="row-md"
            ),
            css_class="fieldset-location"
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

            layout.Row(
                layout.Div(
                    layout.HTML('{% load i18n %}<div><label>{% trans "Booking Phone" %}</label></div>'),
                    layout.Row(
                        layout.Div(
                            'group_bookings_phone_country', css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                        ),
                        layout.Div(
                            'group_bookings_phone_area', css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                        ),
                        layout.Div(
                            'group_bookings_phone_number', css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                        ),
                        css_class="row-xs"
                    ),
                     css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                ),
                layout.Div(
                    layout.HTML('{% load i18n %}<div><label>{% trans "Service Telephone" %}</label></div>'),
                    layout.Row(
                        layout.Div(
                            'service_phone_country', css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                        ),
                        layout.Div(
                            'service_phone_area', css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                        ),
                        layout.Div(
                            'service_phone_number', css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
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


class SocialMediaChannelForm(ModelForm):
    class Meta:
        model = SocialMediaChannel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SocialMediaChannelForm, self).__init__(*args, **kwargs)

        self.fields['channel_type'].help_text = ""

        self.helper = FormHelper()
        self.helper.form_tag = False
        layout_blocks = []

        layout_blocks.append(
            layout.Row(
                layout.Div(
                    "channel_type", css_class="col-xs-12 col-sm-4 col-md-4 col-lg-4"
                ),
                layout.Div(
                    layout.Field("url", placeholder="http://"), css_class="col-xs-12 col-sm-8 col-md-8 col-lg-8"
                ),
                css_class="row-sm"
            )
        )

        self.helper.layout = layout.Layout(
            *layout_blocks
        )

SocialMediaChannelFormset = inlineformset_factory(Museum, SocialMediaChannel, form=SocialMediaChannelForm, formset=InlineFormSet, extra=0)


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
            layout.Div(
                layout.HTML("""{% load i18n %} <label>{% trans "Available Services" %}</label> """),
                'service_shop',
                'service_restaurant',
                'service_cafe',
                'service_library',
                'service_archive',
                'service_diaper_changing_table',
                css_class="checkbox-group"
            ),
            css_class="fieldset-services",
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

        fieldset_content = []
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('accessibility_%s' % lang_code, css_class="tinymce"),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(
            "accessibility_options"
        )

        layout_blocks.append(layout.Fieldset(
            _("Accessibility"),
            css_class="fieldset-accessibility-options",
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


class MediationForm(ModelForm):
    class Meta:
        model = Museum
        fields = [
            'has_audioguide',
            'has_audioguide_de',
            'has_audioguide_en',
            'has_audioguide_fr',
            'has_audioguide_it',
            'has_audioguide_sp',
            'has_audioguide_pl',
            'has_audioguide_tr',
            'audioguide_other_languages',
            'has_audioguide_for_children',
            'has_audioguide_for_learning_difficulties',
        ]

    def __init__(self, *args, **kwargs):
        super(MediationForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        layout_blocks = []

        layout_blocks.append(layout.Fieldset(
            _("Audioguides"),

            layout.Div(
                layout.HTML("""{% load i18n %} <label>{% trans "Available Audioguides" %}</label> """),
                'has_audioguide',
                layout.Div(
                    layout.Div(
                        layout.HTML("""{% load i18n %} <label>{% trans "Languages" %}</label> """),
                        'has_audioguide_de',
                        'has_audioguide_en',
                        'has_audioguide_fr',
                        'has_audioguide_it',
                        'has_audioguide_sp',
                        'has_audioguide_pl',
                        'has_audioguide_tr',
                        css_class="checkbox-inline-group"
                    ),
                    layout.Div("audioguide_other_languages", css_class="form-group"),
                    css_id="div_audioguide_languages",
                ),
                'has_audioguide_for_children',
                'has_audioguide_for_learning_difficulties',
                css_class="checkbox-group"
            ),
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


def load_data(instance=None):
    form_step_data = {}
    if instance:
        form_step_data = {
            'basic': {'_filled': True},
            'opening': {'_filled': True, 'sets': {'seasons': [], 'special_openings': []}},
            'prices': {'_filled': True},
            'address': {'_filled': True, 'sets': {'social': []}},
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
            season_dict['id'] = season.pk
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
            special_opening_dict['id'] = special_opening.pk
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

        fields = ['street_address', 'street_address2', 'postal_code',
            'city', 'latitude', 'longitude',
            'phone_country', 'phone_area', 'phone_number',
            'group_bookings_phone_country', 'group_bookings_phone_area', 'group_bookings_phone_number',
            'service_phone_country', 'service_phone_area', 'service_phone_number',
            'fax_country', 'fax_area', 'fax_number',
            'email', 'website',
        ]
        for f in fields:
            form_step_data['address'][f] = getattr(instance, f)
        if instance.parent:
            form_step_data['address']['parent'] = instance.parent.pk

        for social_media_channel in instance.socialmediachannel_set.all():
            social_media_channel_dict = {}
            social_media_channel_dict['channel_type'] = social_media_channel.channel_type
            social_media_channel_dict['url'] = social_media_channel.url
            form_step_data['address']['sets']['social'].append(social_media_channel_dict)

        form_step_data['services']['service_shop'] = instance.service_shop
        form_step_data['services']['service_restaurant'] = instance.service_restaurant
        form_step_data['services']['service_cafe'] = instance.service_cafe
        form_step_data['services']['service_library'] = instance.service_library
        form_step_data['services']['service_archive'] = instance.service_archive
        form_step_data['services']['service_diaper_changing_table'] = instance.service_diaper_changing_table

        form_step_data['accessibility']['accessibility_options'] = instance.accessibility_options.all()
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            form_step_data['accessibility']['accessibility_%s' % lang_code] = getattr(instance, 'accessibility_%s' % lang_code)

        fields = [
            'has_audioguide',
            'has_audioguide_de',
            'has_audioguide_en',
            'has_audioguide_fr',
            'has_audioguide_it',
            'has_audioguide_sp',
            'has_audioguide_pl',
            'has_audioguide_tr',
            'audioguide_other_languages',
            'has_audioguide_for_children',
            'has_audioguide_for_learning_difficulties',
        ]
        for f in fields:
            form_step_data['mediation'][f] = getattr(instance, f)

    return form_step_data


def submit_step(current_step, form_steps, form_step_data, instance=None):
    if current_step == "basic":
        # save the entry
        if "_pk" in form_step_data:
            instance = Museum.objects.get(pk=form_step_data['_pk'])
        else:
            instance = Museum()

        form_step_data['_pk'] = instance.pk

    if current_step == "address":
        if "_pk" in form_step_data:
            instance = Museum.objects.get(pk=form_step_data['_pk'])
            fields = [
                'street_address', 'street_address2', 'postal_code',
                'city', 'latitude', 'longitude',
                'phone_country', 'phone_area', 'phone_number',
                'group_bookings_phone_country', 'group_bookings_phone_area', 'group_bookings_phone_number',
                'service_phone_country', 'service_phone_area', 'service_phone_number',
                'fax_country', 'fax_area', 'fax_number',
                'email', 'website',
            ]
            for f in fields:
                setattr(instance, f, form_step_data['address'][f])
            if form_step_data['address']['parent']:
                try:
                    instance.parent = Museum.objects.get(pk=form_step_data['address']['parent'])
                except:
                    pass
            instance.save()
            instance.socialmediachannel_set.all().delete()
            for social_dict in form_step_data['address']['sets']['social']:
                social = SocialMediaChannel(museum=instance)
                social.channel_type = social_dict['channel_type']
                social.url = social_dict['url']
                social.save()

    if current_step == "opening":
        if "_pk" in form_step_data:
            instance = Museum.objects.get(pk=form_step_data['_pk'])

            season_ids_to_keep = []
            for season_dict in form_step_data['opening']['sets']['seasons']:
                if season_dict['id']:
                    try:
                        season = Season.objects.get(
                            pk=season_dict['id'],
                            museum=instance,
                        )
                    except models.ObjectDoesNotExist:
                        continue
                else:
                    season = Season(museum=instance)
                season.start = season_dict['start']
                season.end = season_dict['end']
                season.is_appointment_based = season_dict['is_appointment_based']
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
                    setattr(season, 'title_%s' % lang_code, season_dict['title_%s' % lang_code])
                    setattr(season, 'last_entry_%s' % lang_code, season_dict['last_entry_%s' % lang_code])
                    setattr(season, 'exceptions_%s' % lang_code, season_dict['exceptions_%s' % lang_code])
                    setattr(season, 'exceptions_%s_markup_type' % lang_code, MARKUP_PLAIN_TEXT)
                season.save()
                season_ids_to_keep.append(season.pk)
            instance.season_set.exclude(pk__in=season_ids_to_keep).delete()

            special_opening_ids_to_keep = []
            for special_opening_dict in form_step_data['opening']['sets']['special_openings']:
                if special_opening_dict['id']:
                    try:
                        special_opening = SpecialOpeningTime.objects.get(
                            id=special_opening_dict['id'],
                            museum=instance,
                        )
                    except models.ObjectDoesNotExist:
                        continue
                else:
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
                special_opening_ids_to_keep.append(special_opening.pk)
            instance.specialopeningtime_set.exclude(pk__in=special_opening_ids_to_keep).delete()

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
                setattr(instance, 'accessibility_%s_markup_type' % lang_code, MARKUP_HTML_WYSIWYG)

            instance.save()

            instance.accessibility_options.clear()
            for cat in form_step_data['accessibility']['accessibility_options']:
                instance.accessibility_options.add(cat)

    if current_step == "mediation":
        if "_pk" in form_step_data:
            instance = Museum.objects.get(pk=form_step_data['_pk'])

            fields = [
                'has_audioguide',
                'has_audioguide_de',
                'has_audioguide_en',
                'has_audioguide_fr',
                'has_audioguide_it',
                'has_audioguide_sp',
                'has_audioguide_pl',
                'has_audioguide_tr',
                'audioguide_other_languages',
                'has_audioguide_for_children',
                'has_audioguide_for_learning_difficulties',
            ]
            for f in fields:
                setattr(instance, f, form_step_data['mediation'][f])

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

    fields = [
        'street_address', 'street_address2', 'postal_code',
        'city', 'latitude', 'longitude',
        'phone_country', 'phone_area', 'phone_number',
        'group_bookings_phone_country', 'group_bookings_phone_area', 'group_bookings_phone_number',
        'service_phone_country', 'service_phone_area', 'service_phone_number',
        'fax_country', 'fax_area', 'fax_number',
        'email', 'website',
    ]
    for f in fields:
        setattr(instance, f, form_step_data['address'][f])
    if form_step_data['address'].get('parent', None):
        try:
            instance.parent = Museum.objects.get(pk=form_step_data['address']['parent'])
        except:
            pass

    instance.service_shop = form_step_data['services']['service_shop']
    instance.service_restaurant = form_step_data['services']['service_restaurant']
    instance.service_cafe = form_step_data['services']['service_cafe']
    instance.service_library = form_step_data['services']['service_library']
    instance.service_archive = form_step_data['services']['service_archive']
    instance.service_diaper_changing_table = form_step_data['services']['service_diaper_changing_table']

    for lang_code, lang_name in FRONTEND_LANGUAGES:
        setattr(instance, 'accessibility_%s' % lang_code, form_step_data['accessibility']['accessibility_%s' % lang_code])
        setattr(instance, 'accessibility_%s_markup_type' % lang_code, MARKUP_HTML_WYSIWYG)

    fields = [
        'has_audioguide',
        'has_audioguide_de',
        'has_audioguide_en',
        'has_audioguide_fr',
        'has_audioguide_it',
        'has_audioguide_sp',
        'has_audioguide_pl',
        'has_audioguide_tr',
        'audioguide_other_languages',
        'has_audioguide_for_children',
        'has_audioguide_for_learning_difficulties',
    ]
    for f in fields:
        setattr(instance, f, form_step_data['mediation'][f])

    if not instance.status:
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

    season_ids_to_keep = []
    for season_dict in form_step_data['opening']['sets']['seasons']:
        if season_dict['id']:
            try:
                season = Season.objects.get(
                    pk=season_dict['id'],
                    museum=instance,
                )
            except models.ObjectDoesNotExist:
                continue
        else:
            season = Season(museum=instance)
        season.start = season_dict['start']
        season.end = season_dict['end']
        season.is_appointment_based = season_dict['is_appointment_based']
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
            setattr(season, 'title_%s' % lang_code, season_dict['title_%s' % lang_code])
            setattr(season, 'last_entry_%s' % lang_code, season_dict['last_entry_%s' % lang_code])
            setattr(season, 'exceptions_%s' % lang_code, season_dict['exceptions_%s' % lang_code])
            setattr(season, 'exceptions_%s_markup_type' % lang_code, MARKUP_PLAIN_TEXT)
        season.save()
        season_ids_to_keep.append(season.pk)
    instance.season_set.exclude(pk__in=season_ids_to_keep).delete()

    special_opening_ids_to_keep = []
    for special_opening_dict in form_step_data['opening']['sets']['special_openings']:
        if special_opening_dict['id']:
            try:
                special_opening = SpecialOpeningTime.objects.get(
                    id=special_opening_dict['id'],
                    museum=instance,
                )
            except models.ObjectDoesNotExist:
                continue
        else:
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
        special_opening_ids_to_keep.append(special_opening.pk)
    instance.specialopeningtime_set.exclude(pk__in=special_opening_ids_to_keep).delete()

    instance.socialmediachannel_set.all().delete()
    for social_dict in form_step_data['address']['sets']['social']:
        social = SocialMediaChannel(museum=instance)
        social.channel_type = social_dict['channel_type']
        social.url = social_dict['url']
        social.save()

    form_steps['success_url'] = reverse("dashboard") #instance.get_url_path()

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
        'title': _("Admission"),
        'template': "museums/forms/prices_form.html",
        'form': PricesForm,
    },
    'address': {
        'title': _("Address"),
        'template': "museums/forms/address_form.html",
        'form': AddressForm,
        'formsets': {
            'social': SocialMediaChannelFormset,
        }
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
        'title': _("Audioguides"),
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
    'general_error_message': _("There are errors in this form. Please correct them and try to save again."),
    'name': 'museum_registration',
    'default_path': ["basic", "address", "opening", "prices", "services", "accessibility", "mediation", "gallery"],
}

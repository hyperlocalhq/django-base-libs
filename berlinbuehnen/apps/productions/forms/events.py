# -*- coding: UTF-8 -*-

from datetime import time, timedelta
from dateutil.parser import parse as datetime_parse

from django import forms
from django.utils.translation import ugettext_lazy as _, ugettext
from django.forms.models import inlineformset_factory, formset_factory
from django.conf import settings

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

FRONTEND_LANGUAGES = getattr(settings, "FRONTEND_LANGUAGES", settings.LANGUAGES)
EXCLUDED_LANGUAGES = set(dict(settings.LANGUAGES).keys()) - set(dict(FRONTEND_LANGUAGES).keys())

from berlinbuehnen.utils.forms import PrimarySubmit
from berlinbuehnen.utils.forms import SecondarySubmit
from berlinbuehnen.utils.forms import InlineFormSet

from berlinbuehnen.apps.productions.models import Event, EventLeadership, EventAuthorship, EventInvolvement
from berlinbuehnen.apps.sponsors.models import Sponsor

import autocomplete_light

EVENTS_TYPE_CHOICES = (
    ('single', _('Single date')),
    ('range', _('Date range')),
    ('multiple', _('Multiple dates')),
)


class AddEventsForm(forms.Form):
    events_type = forms.ChoiceField(
        label=_("Events type"),
        widget=forms.RadioSelect(),
        choices=EVENTS_TYPE_CHOICES,
        initial='single',
    )
    dates = forms.CharField(
        required=True,
        widget=forms.HiddenInput(),
    )
    start_time = forms.TimeField(
        label=_("Start time"),
    )
    end_time = forms.TimeField(
        label=_("End time"),
        required=False,
    )
    duration = forms.TimeField(
        label=_("Duration"),
        required=False,
    )
    pauses = forms.IntegerField(
        label=_("Amount of pauses"),
        required=False,
        initial=0,
    )

    def __init__(self, production, *args, **kwargs):
        super(AddEventsForm, self).__init__(*args, **kwargs)

        self.production = production

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        layout_blocks = []

        layout_blocks.append(layout.Fieldset(
            _("Add events"),
            layout.Row(
                layout.Div(
                    "events_type",
                    "dates",
                    css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12"
                ),
                css_class="row-sm"
            ),
            layout.HTML("""{% load i18n %}
                <div class="row">
                    <div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">
                        <div class="form-group {% if form.dates.errors %}has-error{% endif %}">
                            <label class="control-label requiredField">{% trans "Dates" %}*</label>
                            <div class="controls">
                                <div id="calendar"></div>
                                {% if form.dates.errors %}<span class="help-block"><strong>{% trans "At least one date should be selected." %}</strong></span>{% endif %}
                            </div>
                        </div>
                    </div>
                </div>
            """),
            layout.Row(
                layout.Div(
                    layout.Field("start_time", placeholder="HH:MM"),
                    css_class="col-xs-12 col-sm-6 col-md-6 col-lg-6"
                ),
                layout.Div(
                    layout.Field("end_time", placeholder="HH:MM"),
                    css_class="col-xs-12 col-sm-6 col-md-6 col-lg-6"
                ),
                css_class="row-sm"
            ),
            layout.Row(
                layout.Div(
                    layout.Field("duration", placeholder="HH:MM"),
                    css_class="col-xs-12 col-sm-6 col-md-6 col-lg-6"
                ),
                layout.Div(
                    layout.Field("pauses"),
                    css_class="col-xs-12 col-sm-6 col-md-6 col-lg-6"
                ),
                css_class="row-sm"
            )
        ))
        layout_blocks.append(bootstrap.FormActions(
            PrimarySubmit('submit', _('Save')),
            SecondarySubmit('reset', _('Cancel')),
        ))

        self.helper.layout = layout.Layout(
            *layout_blocks
        )

    def clean_dates(self):
        dates_str = self.cleaned_data['dates'].split(',')
        try:
            return [datetime_parse(d).date() for d in dates_str]
        except ValueError:
            pass
        return []

    def clean_duration(self):
        duration = self.cleaned_data['duration']
        if duration is not None:
            hours, minutes = duration.hour, duration.minute
            return hours * 3600 + minutes * 60

    def save(self, *args, **kwargs):
        cleaned = self.cleaned_data
        saved_events = []
        dates = cleaned['dates']
        if cleaned['events_type'] == 'range':
            d1, d2 = dates
            delta = d2 - d1
            dates = []
            for i in range(delta.days + 1):
                dates.append(d1 + timedelta(days=i))
        for d in dates:
            ev = Event(production=self.production)
            ev.start_date = d
            ev.start_time = cleaned['start_time']
            ev.end_time = cleaned['end_time']
            ev.pauses = cleaned['pauses']
            ev.duration = cleaned['duration']
            ev.save()
            saved_events.append(ev)
        return saved_events


class BasicInfoForm(autocomplete_light.ModelForm):
    duration_as_time = forms.TimeField(
        label=_("Duration"),
        required=False,
    )

    class Meta:
        model = Event
        autocomplete_fields = ('play_locations', 'play_stages',)
        fields = [
            'start_date',
            'end_date',
            'start_time',
            'end_time',
            'pauses',
            'organizer_title',
            'play_locations', 'play_stages',
            'event_status', 'ticket_status',
        ]
        # for lang_code, lang_name in FRONTEND_LANGUAGES:
        #     fields += []

    def __init__(self, *args, **kwargs):
        super(BasicInfoForm, self).__init__(*args, **kwargs)

        if self.instance.duration:
            duration_in_minutes = self.instance.duration / 60
            hours = duration_in_minutes / 60
            minutes = duration_in_minutes % 60
            self.fields['duration_as_time'].initial = time(hours, minutes)

        # for lang_code, lang_name in FRONTEND_LANGUAGES:
        #     for f in []:
        #         self.fields[f].label += """ <span class="lang">%s</span>""" % lang_code.upper()

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"

        layout_blocks = []
        fieldset_content = []  # collect multilingual divs into one list...

        layout_blocks.append(layout.Fieldset(
            _("Date and time"),
            layout.Row(
                layout.Div(
                    layout.Field("start_date", placeholder="YYYY-MM-DD"),
                    css_class="col-xs-12 col-sm-6 col-md-6 col-lg-6"
                ),
                layout.Div(
                    layout.Field("end_date", placeholder="YYYY-MM-DD"),
                    css_class="col-xs-12 col-sm-6 col-md-6 col-lg-6"
                ),
                css_class="row-sm"
            ),
            layout.Row(
                layout.Div(
                    layout.Field("start_time", placeholder="HH:MM"),
                    css_class="col-xs-12 col-sm-6 col-md-6 col-lg-6"
                ),
                layout.Div(
                    layout.Field("end_time", placeholder="HH:MM"),
                    css_class="col-xs-12 col-sm-6 col-md-6 col-lg-6"
                ),
                css_class="row-sm"
            ),
            layout.Row(
                layout.Div(
                    layout.Field("duration_as_time", placeholder="HH:MM"),
                    css_class="col-xs-12 col-sm-6 col-md-6 col-lg-6"
                ),
                layout.Div(
                    "pauses",
                    css_class="col-xs-12 col-sm-6 col-md-6 col-lg-6"
                ),
                css_class="row-sm"
            ),
            css_class="fieldset-date-time",
        ))

        layout_blocks.append(layout.Fieldset(
            _("Venue"),
            layout.Row(
                layout.Div(
                    "play_locations",
                    "play_stages",
                    "organizer_title",
                    css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12"
                ),
            ),
            css_class="fieldset-venue",
        ))

        layout_blocks.append(layout.Fieldset(
            _("Status"),
            layout.Row(
                layout.Div(
                    layout.Field("event_status"),
                    css_class="col-xs-12 col-sm-6 col-md-6 col-lg-6"
                ),
                layout.Div(
                    layout.Field("ticket_status"),
                    css_class="col-xs-12 col-sm-6 col-md-6 col-lg-6"
                ),
                css_class="row-sm"
            ),
            css_class="fieldset-date-time",
        ))

        layout_blocks.append(bootstrap.FormActions(
            PrimarySubmit('submit', _('Save')),
            SecondarySubmit('reset', _('Cancel')),
        ))

        self.helper.layout = layout.Layout(
            *layout_blocks
        )

    def save(self, commit=True):
        event = super(BasicInfoForm, self).save(commit=False)
        duration_as_time = self.cleaned_data['duration_as_time']
        event.duration = None
        if duration_as_time is not None:
            hours, minutes = duration_as_time.hour, duration_as_time.minute
            event.duration = hours * 3600 + minutes * 60
        if commit:
            event.save()
            self.save_m2m()
        return event


class DescriptionForm(autocomplete_light.ModelForm):
    class Meta:
        model = Event
        fields = [
            'free_entrance', 'price_from', 'price_till', 'tickets_website',
            'characteristics',
        ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'description_%s' % lang_code,
                'teaser_%s' % lang_code,
                'work_info_%s' % lang_code,
                'contents_%s' % lang_code,
                'press_text_%s' % lang_code,
                'credits_%s' % lang_code,
                'concert_programm_%s' % lang_code,
                'supporting_programm_%s' % lang_code,
                'remarks_%s' % lang_code,
                'duration_text_%s' % lang_code,
                'subtitles_text_%s' % lang_code,
                'age_text_%s' % lang_code,
                'price_information_%s' % lang_code,
                'other_characteristics_%s' % lang_code,
            ]

    def __init__(self, *args, **kwargs):
        super(DescriptionForm, self).__init__(*args, **kwargs)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'description_%s' % lang_code,
                'teaser_%s' % lang_code,
                'work_info_%s' % lang_code,
                'contents_%s' % lang_code,
                'press_text_%s' % lang_code,
                'credits_%s' % lang_code,
                'concert_programm_%s' % lang_code,
                'supporting_programm_%s' % lang_code,
                'remarks_%s' % lang_code,
                'duration_text_%s' % lang_code,
                'subtitles_text_%s' % lang_code,
                'age_text_%s' % lang_code,
                'price_information_%s' % lang_code,
                'other_characteristics_%s' % lang_code,
            ]:
                self.fields[f].label += """ <span class="lang">%s</span>""" % lang_code.upper()

        self.fields['characteristics'].widget = forms.CheckboxSelectMultiple()
        self.fields['characteristics'].help_text = u""

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"

        layout_blocks = []

        layout_blocks.append(layout.Fieldset(
            _("Leaders"),
            layout.HTML("""{% load crispy_forms_tags i18n %}
            {{ formsets.leaderships.management_form }}
            <div id="leaderships">
                {% for form in formsets.leaderships.forms %}
                    <div class="leadership formset-form">
                        {% crispy form %}
                    </div>
                {% endfor %}
            </div>
            <!-- used by javascript -->
            <div id="leaderships_empty_form" class="leadership formset-form" style="display: none">
                {% with formsets.leaderships.empty_form as form %}
                    {% crispy form %}
                {% endwith %}
            </div>
            """),
            css_id="leaderships_fieldset",
        ))

        layout_blocks.append(layout.Fieldset(
            _("Authors"),
            layout.HTML("""{% load crispy_forms_tags i18n %}
            {{ formsets.authorships.management_form }}
            <div id="authorships">
                {% for form in formsets.authorships.forms %}
                    <div class="authorship formset-form">
                        {% crispy form %}
                    </div>
                {% endfor %}
            </div>
            <!-- used by javascript -->
            <div id="authorships_empty_form" class="authorship formset-form" style="display: none">
                {% with formsets.authorships.empty_form as form %}
                    {% crispy form %}
                {% endwith %}
            </div>
            """),
            css_id="authorships_fieldset",
        ))

        layout_blocks.append(layout.Fieldset(
            _("Other involved people"),
            layout.HTML("""{% load crispy_forms_tags i18n %}
            {{ formsets.involvements.management_form }}
            <div id="involvements">
                {% for form in formsets.involvements.forms %}
                    <div class="involvement formset-form">
                        {% crispy form %}
                    </div>
                {% endfor %}
            </div>
            <!-- used by javascript -->
            <div id="involvements_empty_form" class="involvement formset-form" style="display: none">
                {% with formsets.involvements.empty_form as form %}
                    {% crispy form %}
                {% endwith %}
            </div>
            """),
            css_id="involvements_fieldset",
        ))

        fieldset_content = []  # collect multilingual divs into one list...
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('description_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('teaser_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('work_info_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('contents_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('press_text_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('credits_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('concert_programm_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('supporting_programm_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('remarks_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('duration_text_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('subtitles_text_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('age_text_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        layout_blocks.append(layout.Fieldset(
            _("Description"),
            css_class="fieldset-basic-info",
            *fieldset_content  # ... then pass them to a fieldset
        ))

        fieldset_content = []
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('price_information_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))

        layout_blocks.append(layout.Fieldset(
            _("Tickets"),
            layout.Row(
                layout.Div(
                    layout.Field('price_from'),
                    css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                ),
                layout.Div(
                    layout.Field('price_till'),
                    css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                ),
                css_class="row-md",
            ),
            layout.Row(
                layout.Div(
                    "free_entrance",
                    layout.Field("tickets_website", placeholder="http://"),
                    css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12"
                ),
            ),
            css_class="fieldset-tickets",
            *fieldset_content
        ))

        layout_blocks.append(layout.Fieldset(
            _("Other Characteristics"),
            layout.Row(
                layout.Div(
                    "characteristics",
                    css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12"
                ),
            ),
            layout.Row(
                css_class="row-md",
                *[layout.Div(
                    layout.Field('other_characteristics_%s' % lang_code),
                    css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                ) for lang_code, lang_name in FRONTEND_LANGUAGES]
            ),
            css_class="fieldset-characteristics",
        ))

        layout_blocks.append(layout.Fieldset(
            _("Sponsors"),
            layout.HTML("""{% load crispy_forms_tags i18n %}
            {{ formsets.sponsors.management_form }}
            <div id="sponsors">
                {% for form in formsets.sponsors.forms %}
                    <div class="sponsor formset-form">
                        {% crispy form %}
                    </div>
                {% endfor %}
            </div>
            <!-- used by javascript -->
            <div id="sponsors_empty_form" class="sponsor formset-form" style="display: none">
                {% with formsets.sponsors.empty_form as form %}
                    {% crispy form %}
                {% endwith %}
            </div>
            """),
            css_id="sponsors_fieldset",
        ))

        layout_blocks.append(bootstrap.FormActions(
            PrimarySubmit('submit', _('Save')),
            SecondarySubmit('reset', _('Cancel')),
        ))

        self.helper.layout = layout.Layout(
            *layout_blocks
        )


class EventLeadershipForm(autocomplete_light.ModelForm):
    first_name = forms.CharField(
        label=_("First name"),
        required=False,
        max_length=255,
    )
    last_name = forms.CharField(
        label=_("Last name"),
        required=False,
        max_length=255,
    )

    class Meta:
        model = EventLeadership
        autocomplete_fields = ('person',)

    def __init__(self, *args, **kwargs):
        super(EventLeadershipForm, self).__init__(*args, **kwargs)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'function_%s' % lang_code,
            ]:
                self.fields[f].label += """ <span class="lang">%s</span>""" % lang_code.upper()

        self.fields['sort_order'].widget = forms.HiddenInput()
        self.fields['person'].required = False
        self.fields['person'].label += ' (' + ugettext('or') + ' <a href="" class="enter_person">' + ugettext('enter a new person') + '</a>)'
        self.fields['first_name'].label += ' (' + ugettext('or') + ' <a href="" class="choose_person">' + ugettext('choose a person from the database') + '</a>)'

        self.helper = FormHelper()
        self.helper.form_tag = False
        layout_blocks = []

        layout_blocks.append(
            layout.Row(
                layout.Div(
                    "person",
                    "sort_order",
                    "id",
                    "DELETE",
                    css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12"
                ),
                css_class="row-sm choosing_person"
            )
        )
        layout_blocks.append(
            layout.Row(
                layout.Div(
                    "first_name",
                    css_class="col-xs-12 col-sm-6 col-md-6 col-lg-6"
                ),
                layout.Div(
                    "last_name",
                    css_class="col-xs-12 col-sm-6 col-md-6 col-lg-6"
                ),
                css_class="row-sm entering_person hidden"
            )
        )
        layout_blocks.append(
            layout.Row(
                css_class="row-sm",
                *[layout.Div(
                    layout.Field('function_%s' % lang_code),
                    css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                ) for lang_code, lang_name in FRONTEND_LANGUAGES]
            )
        )

        self.helper.layout = layout.Layout(
            *layout_blocks
        )

EventLeadershipFormset = inlineformset_factory(Event, EventLeadership, form=EventLeadershipForm, formset=InlineFormSet, extra=0)


class EventAuthorshipForm(autocomplete_light.ModelForm):
    first_name = forms.CharField(
        label=_("First name"),
        required=False,
        max_length=255,
    )
    last_name = forms.CharField(
        label=_("Last name"),
        required=False,
        max_length=255,
    )

    class Meta:
        model = EventAuthorship
        autocomplete_fields = ('person',)

    def __init__(self, *args, **kwargs):
        super(EventAuthorshipForm, self).__init__(*args, **kwargs)

        self.fields['sort_order'].widget = forms.HiddenInput()
        self.fields['person'].required = False
        self.fields['person'].label += ' (' + ugettext('or') + ' <a href="" class="enter_person">' + ugettext('enter a new person') + '</a>)'
        self.fields['first_name'].label += ' (' + ugettext('or') + ' <a href="" class="choose_person">' + ugettext('choose a person from the database') + '</a>)'

        self.helper = FormHelper()
        self.helper.form_tag = False
        layout_blocks = []

        layout_blocks.append(
            layout.Row(
                layout.Div(
                    "person", css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12"
                ),
                css_class="row-sm choosing_person"
            )
        )
        layout_blocks.append(
            layout.Row(
                layout.Div(
                    "first_name",
                    css_class="col-xs-12 col-sm-6 col-md-6 col-lg-6"
                ),
                layout.Div(
                    "last_name",
                    css_class="col-xs-12 col-sm-6 col-md-6 col-lg-6"
                ),
                css_class="row-sm entering_person hidden"
            )
        )
        layout_blocks.append(
            layout.Row(
                layout.Div(
                    "authorship_type",
                    "sort_order",
                    "id",
                    "DELETE",
                    css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12"
                ),
                css_class="row-sm"
            )
        )

        self.helper.layout = layout.Layout(
            *layout_blocks
        )

EventAuthorshipFormset = inlineformset_factory(Event, EventAuthorship, form=EventAuthorshipForm, formset=InlineFormSet, extra=0)


class EventInvolvementForm(autocomplete_light.ModelForm):
    first_name = forms.CharField(
        label=_("First name"),
        required=False,
        max_length=255,
    )
    last_name = forms.CharField(
        label=_("Last name"),
        required=False,
        max_length=255,
    )

    class Meta:
        model = EventInvolvement
        autocomplete_fields = ('person',)

    def __init__(self, *args, **kwargs):
        super(EventInvolvementForm, self).__init__(*args, **kwargs)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'involvement_role_%s' % lang_code,
                'involvement_instrument_%s' % lang_code,
            ]:
                self.fields[f].label += """ <span class="lang">%s</span>""" % lang_code.upper()

        self.fields['sort_order'].widget = forms.HiddenInput()
        self.fields['person'].required = False
        self.fields['person'].label += ' (' + ugettext('or') + ' <a href="" class="enter_person">' + ugettext('enter a new person') + '</a>)'
        self.fields['first_name'].label += ' (' + ugettext('or') + ' <a href="" class="choose_person">' + ugettext('choose a person from the database') + '</a>)'

        self.helper = FormHelper()
        self.helper.form_tag = False
        layout_blocks = []

        layout_blocks.append(
            layout.Row(
                layout.Div(
                    "person",
                    "sort_order",
                    "id",
                    "DELETE",
                    css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12"
                ),
                css_class="row-sm choosing_person"
            )
        )
        layout_blocks.append(
            layout.Row(
                layout.Div(
                    "first_name",
                    css_class="col-xs-12 col-sm-6 col-md-6 col-lg-6"
                ),
                layout.Div(
                    "last_name",
                    css_class="col-xs-12 col-sm-6 col-md-6 col-lg-6"
                ),
                css_class="row-sm entering_person hidden"
            )
        )
        layout_blocks.append(
            layout.Row(
                layout.Div(
                    "involvement_type",
                    css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12"
                ),
                css_class="row-sm"
            )
        )
        layout_blocks.append(
            layout.Row(
                css_class="row-sm",
                *[layout.Div(
                    layout.Field('involvement_role_%s' % lang_code),
                    css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                ) for lang_code, lang_name in FRONTEND_LANGUAGES]
            )
        )
        layout_blocks.append(
            layout.Row(
                css_class="row-sm",
                *[layout.Div(
                    layout.Field('involvement_instrument_%s' % lang_code),
                    css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                ) for lang_code, lang_name in FRONTEND_LANGUAGES]
            )
        )

        self.helper.layout = layout.Layout(
            *layout_blocks
        )

EventInvolvementFormset = inlineformset_factory(Event, EventInvolvement, form=EventInvolvementForm, formset=InlineFormSet, extra=0)


class SponsorForm(autocomplete_light.ModelForm):
    id = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=False,
    )
    media_file_path = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
    )

    class Meta:
        model = Sponsor
        exclude = ['image']

    def __init__(self, *args, **kwargs):
        super(SponsorForm, self).__init__(*args, **kwargs)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'title_%s' % lang_code,
            ]:
                self.fields[f].label += """ <span class="lang">%s</span>""" % lang_code.upper()

        self.helper = FormHelper()
        self.helper.form_tag = False

        fieldset_content = []  # collect multilingual divs into one list...

        fieldset_content.append(
            layout.HTML(u"""{% load i18n base_tags image_modifications %}
            <div class="row row-md">
                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">
                    <div class="image_preview">
                        {% if form.instance.image %}
                            <img class="img-responsive" src="{{ MEDIA_URL }}{{ form.instance.image|modified_path:"medium" }}?now={% now "YmdHis" %}" alt="" />
                        {% endif %}
                    </div>
                    <div class="image_uploader">
                        <noscript>
                            <p>{% trans "Please enable JavaScript to use file uploader." %}</p>
                        </noscript>
                    </div>
                    <p class="image_help_text help-block">{% trans "Available formats are JPG, GIF, and PNG. Minimal size is 100 × 100 px. Optimal size is 1000 × 350 px (min)." %}</p>
                </div>
            </div>
            """)
        )

        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('title_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            layout.Div(
                "media_file_path",
                layout.Field("website", placeholder="http://"),
                "id",
                "DELETE",
                css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12"
            ),
            css_class="row-sm"
        ))

        self.helper.layout = layout.Layout(
            *fieldset_content
        )

SponsorFormset = formset_factory(form=SponsorForm, extra=0, can_delete=True)


class GalleryForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = []

    def __init__(self, *args, **kwargs):
        super(GalleryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        layout_blocks = []
        layout_blocks.append(bootstrap.FormActions(
            PrimarySubmit('submit', _('Save')),
            SecondarySubmit('reset', _('Cancel')),
        ))
        self.helper.layout = layout.Layout(
            *layout_blocks
        )



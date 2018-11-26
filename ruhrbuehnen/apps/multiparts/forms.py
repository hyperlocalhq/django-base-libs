# -*- coding: UTF-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _, ugettext
from django.forms.models import inlineformset_factory

import autocomplete_light

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from models import Parent, Part

from ruhrbuehnen.utils.forms import PrimarySubmit
from ruhrbuehnen.utils.forms import SecondarySubmit
from ruhrbuehnen.utils.forms import InlineFormSet


class ParentForm(autocomplete_light.ModelForm):
    class Meta:
        model = Parent
        autocomplete_fields = ('production', )
        fields = ['production']

    def __init__(self, *args, **kwargs):
        super(ParentForm, self).__init__(*args, **kwargs)

        self.fields['production'].label = _("Parent production")

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"

        layout_blocks = [
            layout.Fieldset(
                _("Multipart Production"),
                "production",
            ),
            layout.Fieldset(
                _("Parts"),
                layout.HTML(
                    """{% load crispy_forms_tags i18n %}
            {{ formsets.parts.management_form }}
            <div id="parts">
                {% for form in formsets.parts.forms %}
                    <div class="part formset-form">
                        {% crispy form %}
                    </div>
                {% endfor %}
            </div>
            <!-- used by javascript -->
            <div id="parts_empty_form" class="part formset-form" style="display: none">
                {% with formsets.parts.empty_form as form %}
                    {% crispy form %}
                {% endwith %}
            </div>
            """
                ),
                css_id="parts_fieldset",
            ),
            bootstrap.FormActions(
                PrimarySubmit('submit', _('Save')),
                SecondarySubmit('reset', _('Cancel')),
            )
        ]

        self.helper.layout = layout.Layout(*layout_blocks)


class PartForm(autocomplete_light.ModelForm):
    class Meta:
        model = Part
        autocomplete_fields = ('production', )
        fields = ['id', 'production', 'sort_order']

    def __init__(self, *args, **kwargs):
        super(PartForm, self).__init__(*args, **kwargs)

        self.fields['sort_order'].widget = forms.HiddenInput()

        self.helper = FormHelper()
        self.helper.form_tag = False

        self.helper.layout = layout.Layout(
            "production",
            layout.Div(
                "sort_order",
                "id",
                "DELETE",
                css_class="hidden",
            )
        )


PartFormset = inlineformset_factory(
    Parent, Part, form=PartForm, formset=InlineFormSet, extra=0
)

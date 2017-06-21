# -*- coding: UTF-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from base_libs.forms import dynamicforms
from base_libs.utils.misc import get_related_queryset

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from jetson.apps.location.models import LocalityType
from jetson.apps.utils.forms import ModelChoiceTreeField

Person = models.get_model("people", "Person")
Term = models.get_model("structure", "Term")


class PersonSearchForm(dynamicforms.Form):
    creative_sector = ModelChoiceTreeField(
        empty_label=_("All"),
        label=_("Creative Sector"),
        required=False,
        queryset=get_related_queryset(Person, "creative_sectors"),
    )
    context_category = ModelChoiceTreeField(
        empty_label=_("All"),
        label=_("Business Category"),
        required=False,
        queryset=get_related_queryset(Person, "context_categories"),
    )
    individual_type = ModelChoiceTreeField(
        empty_label=_("All"),
        label=_("Type"),
        required=False,
        queryset=get_related_queryset(Person, "individual_type"),
    )
    locality_type = ModelChoiceTreeField(
        empty_label=_("All"),
        label=_("Location Type"),
        required=False,
        queryset=LocalityType.objects.order_by("tree_id", "lft"),
    )

    def __init__(self, *args, **kwargs):
        super(PersonSearchForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "GET"
        self.helper.form_id = "filter_form"
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Filter"),
                layout.Field("creative_sector", template="kb_form/custom_widgets/filter_field.html"),
                layout.Field("context_category", template="kb_form/custom_widgets/filter_field.html"),
                layout.Field("individual_type", template="kb_form/custom_widgets/filter_field.html"),
                layout.Field("locality_type", template="kb_form/custom_widgets/locality_type_filter_field.html"),
                template="kb_form/custom_widgets/filter.html"
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Search')),
            )
        )

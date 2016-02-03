# -*- coding: UTF-8 -*-
from crispy_forms import layout, bootstrap
from crispy_forms.helper import FormHelper
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.forms import TreeNodeChoiceField

from jetson.apps.utils.forms import ModelChoiceTreeField

from base_libs.utils.misc import get_related_queryset
from base_libs.forms import dynamicforms

Document = models.get_model("resources", "Document")


class DocumentSearchForm(dynamicforms.Form):
    creative_sector = ModelChoiceTreeField(
        empty_label=_("All"),
        label=_("Creative Sector"),
        required=False,
        queryset=get_related_queryset(Document, "creative_sectors"),
    )
    context_category = ModelChoiceTreeField(
        empty_label=_("All"),
        label=_("Business Category"),
        required=False,
        queryset=get_related_queryset(Document, "context_categories"),
    )
    document_type = ModelChoiceTreeField(
        empty_label=_("All"),
        label=_("Type"),
        required=False,
        queryset=get_related_queryset(Document, "document_type"),
    )

    def __init__(self, *args, **kwargs):
        super(DocumentSearchForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "GET"
        self.helper.form_id = "object_list_filter_form"
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Filter"),
                "creative_sector",
                "context_category",
                "document_type",
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Search')),
            )
        )

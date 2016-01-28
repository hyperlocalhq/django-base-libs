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
    category = ModelChoiceTreeField(
        empty_label=_("All"),
        label=_("Category"),
        required=False,
        queryset=get_related_queryset(Document, "categories").filter(level=0),
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
        self.helper.form_id = "filter_form"
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Filter"),
                layout.Field("category", template="ccb_form/custom_widgets/category_filter_field.html"),
                layout.Field("document_type", template="ccb_form/custom_widgets/document_type_filter_field.html"),
                template="ccb_form/custom_widgets/filter.html"
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Search')),
            )
        )

    def get_query(self):
        from django.template.defaultfilters import urlencode
        if self.is_valid():
            cleaned = self.cleaned_data
            return "&".join([
                ("%s=%s" % (k, urlencode(isinstance(v, models.Model) and v.pk or v)))
                for (k, v) in cleaned.items()
                if v
            ])
        return ""

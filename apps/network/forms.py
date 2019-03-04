# -*- coding: UTF-8 -*-
from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _

from base_libs.forms import dynamicforms
from base_libs.utils.misc import get_related_queryset

from ccb.apps.site_specific.models import ContextItem

from mptt.forms import TreeNodeChoiceField

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from jetson.apps.utils.forms import ModelChoiceTreeField


OBJECT_TYPE_CHOICES = (
    ('', _("All")),
    ('person', _("People")),
    ('institution', _("Institutions"))
)

class MemberSearchForm(dynamicforms.Form):
    category = ModelChoiceTreeField(
        empty_label=_("All"),
        label=_("Category"),
        required=False,
        queryset=get_related_queryset(ContextItem, "categories"),
    )
    locality_type = ModelChoiceTreeField(
        empty_label=_("All"),
        label=_("Locality Type"),
        required=False,
        queryset=get_related_queryset(ContextItem, "locality_type").all(),
    )
    object_type = forms.ChoiceField(
        choices=OBJECT_TYPE_CHOICES,
        label=_("Object Type"),
        required=False,
    )

    def __init__(self, root_category, *args, **kwargs):
        super(MemberSearchForm, self).__init__(*args, **kwargs)
        self.root_category = root_category
        if root_category:
            self.fields['category'].queryset = self.fields['category'].queryset.filter(tree_id=root_category.tree_id)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "GET"
        self.helper.form_id = "filter_form"
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Filter"),
                layout.Field("category", template="ccb_form/custom_widgets/category_filter_field.html"),
                layout.Field("locality_type", template="ccb_form/custom_widgets/locality_type_filter_field.html"),
                layout.Field("object_type", template="ccb_form/custom_widgets/filter_field.html"),
                template="ccb_form/custom_widgets/filter.html"
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Search')),
            )
        )

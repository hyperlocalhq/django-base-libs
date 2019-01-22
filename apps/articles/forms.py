# -*- coding: UTF-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from base_libs.utils.misc import get_related_queryset

from jetson.apps.utils.forms import ModelChoiceTreeField

from ccb.apps.articles.models import Article

class ArticleSearchForm(forms.Form):
    category = ModelChoiceTreeField(
        empty_label=_("All"),
        label=_("Category"),
        required=False,
        queryset=get_related_queryset(Article, "categories").filter(level=0),
    )

    def __init__(self, *args, **kwargs):
        super(ArticleSearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "GET"
        self.helper.form_id = "filter_form"
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Filter"),
                layout.Field("category", template="ccb_form/custom_widgets/filter_field.html"),
                template="ccb_form/custom_widgets/filter.html"
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Search')),
            )
        )

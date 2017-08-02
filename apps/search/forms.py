# -*- coding: UTF-8 -*-

from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from haystack.forms import SearchForm as _SearchForm

from .functions import model_choices, get_model_from_short_name


class ModelSearchForm(_SearchForm):
    QUERY_PARAM_NAME = 'q'
    MODELS_PARAM_NAME = 't'

    def __init__(self, *args, **kwargs):
        super(ModelSearchForm, self).__init__(*args, **kwargs)
        self.fields[self.QUERY_PARAM_NAME].label = _('Search')
        self.fields[self.MODELS_PARAM_NAME] = forms.MultipleChoiceField(
            choices=model_choices(),
            required=False,
            label=_('Search In'),
            widget=forms.SelectMultiple
        )
        self.helper = FormHelper()
        self.helper.form_action = reverse("haystack_search")
        self.helper.form_method = "GET"
        self.helper.form_id = "search_form"

        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Inquiry"),
                layout.Field(self.QUERY_PARAM_NAME),
                layout.Field(self.MODELS_PARAM_NAME, placeholder=_('Narrow down your search ...')),
                layout.Div(
                    layout.Submit('submit', _('search')),
                    css_class="button-group form-buttons"
                ),
            ),
        )

    def get_models(self):
        """Return list of model classes in the index."""
        search_models = []

        if self.is_valid():
            for short_name in self.cleaned_data[self.MODELS_PARAM_NAME]:
                app_model = get_model_from_short_name(short_name)
                search_models.append(models.get_model(*app_model.split('.')))

        return search_models

    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        if not self.cleaned_data[self.QUERY_PARAM_NAME]:
            return self.no_query_found()

        self.clean()

        q = self.cleaned_data[self.QUERY_PARAM_NAME]
        model_list = self.get_models()

        # add models
        from haystack.query import SearchQuerySet
        sqs = SearchQuerySet().models(*model_list)

        sqs = sqs.auto_query(sqs.query.clean(q))

        # add highlight
        sqs = sqs.highlight()

        # add faceting by django_ct
        sqs = sqs.facet('django_ct')

        if self.load_all:
            sqs = sqs.load_all()

        return sqs

# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

from haystack.views import SearchView as SearchViewBase
from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

class SearchView(SearchViewBase):
    def extra_context(self):
        context = {}
        
        form_helper = FormHelper()
        form_helper.form_action = ""
        form_helper.form_method = "GET"
        layout_blocks = []
        layout_blocks.append(layout.Fieldset(
            _("Search"),
            "q",
            layout.Div(
                'models',
                css_class="inline",
                ),
            ))
        layout_blocks.append(bootstrap.FormActions(
            layout.Submit('submit', _('Search')),
            ))
        form_helper.layout = layout.Layout(
            *layout_blocks
            )        
        context['form_helper'] = form_helper
        return context

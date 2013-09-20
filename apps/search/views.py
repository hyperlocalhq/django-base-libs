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
            "",

            layout.Div(
                'models',
                css_class="inline",
                ),

            layout.Div(
                
                layout.Div(
                    layout.Div(layout.Field("q", css_class="form-control"), css_class="max"),
                    css_class="form-group",
                ),
                
                layout.Div(
                    layout.Div(layout.Submit('submit', _('Search')),),
                    css_class="input-group-btn",
                ),

            css_class="input-group",
            ),
            
            css_id="search_form",
            ))

        form_helper.layout = layout.Layout(
            *layout_blocks
            )        
        context['form_helper'] = form_helper
        return context

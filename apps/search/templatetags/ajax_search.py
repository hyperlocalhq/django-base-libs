# -*- coding: UTF-8 -*-
from django import template
from django.template import loader

from kb.apps.search.forms import AjaxSearchForm

register = template.Library()


def show_search_selections(parser, token):
    """ Prints the list of select fields for search
    
    Usage::
        
        {% show_search_selections %}
        
    Examples::
        
        {% show_search_selections %}
        
    """
    return SearchSelections()


URL_SLUG_2_OT_SYSNAME = {
    "people": "person",
    "institutions": "institution",
    "documents": "document",
    "events": "event",
    "groups": "person_group",
}


class SearchSelections(template.Node):
    def render(self, context):
        request = context['request']

        data = request.GET.copy()
        if "search-cs" not in data and context.get("creative_sector", False):
            data["search-cs"] = str(context["creative_sector"].id)

        form = AjaxSearchForm(initial=data, prefix="search")
        form.data = data
        form.is_bound = True

        context['search_form'] = form
        return loader.render_to_string(
            "search/search_selection_list.html",
            context,
        )


register.tag('show_search_selections', show_search_selections)

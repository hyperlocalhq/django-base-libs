# -*- coding: UTF-8 -*-
import re

from django.db import models
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.http import Http404
from django.utils.encoding import force_unicode
from django.template.defaultfilters import urlencode
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.cache import never_cache
from django.core.paginator import Paginator, InvalidPage

from jetson.apps.utils.views import object_list, get_abc_list, filter_abc
from jetson.apps.structure.models import Term, ContextCategory

from ccb.apps.site_specific.models import ContextItem

Person = models.get_model("people", "Person")
Institution = models.get_model("institutions", "Institution")
Event = models.get_model("events", "Event")
Document = models.get_model("resources", "Document")

numeric = re.compile(r"^\d+$")

"""
context_item_type_mapper maps object types to url parts.
We need that for finding the correct redirections URL
in  "simplesearch" (see below). 
"""
object_type_mapper = {
    'person': 'people',
    'institution': 'institutions',
    'person_group': 'groups',
    'document': 'documents',
    'event': 'events',
}
"""
We also need the other way for mapping. 
Also we need different templates. 
"""
object_type_inverse_mapper = {
    'people': ('person', "people/person_simplesearchresults.html"),
    'institutions': ('institution', "institutions/institution_simplesearchresults.html"),
    'groups': ('person_group', "groups_networks/persongroups/group_simplesearchresults.html"),
    'documents': ('document', "resources/documents/document_simplesearchresults.html"),
    'events': ('event', "events/event_simplesearchresults.html"),
}

"""
maps a term sysname to a model...
"""
term_sysname_model_mapper = {
    'person': Person,
    'institution': Institution,
    'event': Event,
    'document': Document,
}


def map_ct(sysname):
    """ 
    just a helper function to map sysnames getting
    from object types to relating ContentTypes.
    """
    if sysname in term_sysname_model_mapper:
        model = term_sysname_model_mapper[sysname]
        return ContentType.objects.get_for_model(model)
    return None


@never_cache
def simplesearch(request, ot_url_part=None, **kwargs):
    """
    performs the 'database search'
    """

    abc_list = None
    abc_filter = request.GET.get('by-abc', None)

    """
    template_name and initial queryset.
    We apply an 'initial queryset' for the case,
    that a user will select the (f.e.) 
    '/people/simplesearch/' (Search) tab. In that
    case, all persons should be displayed, even,
    if no query parameters are specified.
    """
    queryset = ContextItem.objects.search(None)
    queryset = queryset.filter()
    if ot_url_part:
        template_name = object_type_inverse_mapper[ot_url_part][1]
        ot = Term.objects.get(
            sysname=object_type_inverse_mapper[ot_url_part][0]
        )
        ct = map_ct(ot.sysname)
        if ct:
            queryset = queryset.filter(content_type=ct)
    else:
        template_name = "search/simplesearchresults.html"

    # first, a redirection is done to the appropriate "type", if available.
    if request.GET:

        data = request.GET.copy()

        if data.has_key('search-ot') and numeric.match(data['search-ot']):
            ot = Term.objects.get(id=data['search-ot'])
            url_part = object_type_mapper[ot.sysname]
            if url_part != ot_url_part:
                return HttpResponseRedirect("/%s/simplesearch/?%s" % (
                    url_part,
                    request.META['QUERY_STRING'],
                ))
        else:
            if data.has_key('search-ot') and ot_url_part:
                return HttpResponseRedirect("/simplesearch/?%s" % (
                    request.META['QUERY_STRING'],
                ))

                # ok, redirection is done now, we can do filtering ...

        if data.has_key('search-cs_d') and numeric.match(data['search-cs_d']):
            cs = Term.objects.get(pk=data['search-cs_d'])
            queryset = queryset.filter(
                creative_sectors__lft__gte=cs.lft,
                creative_sectors__rght__lte=cs.rght,
                creative_sectors__tree_id=cs.tree_id,
            )
        elif data.has_key('search-cs') and numeric.match(data['search-cs']):
            cs = Term.objects.get(pk=data['search-cs'])
            queryset = queryset.filter(
                creative_sectors__lft__gte=cs.lft,
                creative_sectors__rght__lte=cs.rght,
                creative_sectors__tree_id=cs.tree_id,
            )

        if data.has_key('search-cc_d') and numeric.match(data['search-cc_d']):
            cc = ContextCategory.objects.get(pk=data['search-cc_d'])
            queryset = queryset.filter(
                context_categories__lft__gte=cc.lft,
                context_categories__rght__lte=cc.rght,
                context_categories__tree_id=cc.tree_id,
            )
        elif data.has_key('search-cc') and numeric.match(data['search-cc']):
            cc = ContextCategory.objects.get(pk=data['search-cc'])
            queryset = queryset.filter(
                context_categories__lft__gte=cc.lft,
                context_categories__rght__lte=cc.rght,
                context_categories__tree_id=cc.tree_id,
            )

        if data.has_key('search-lt_d') and numeric.match(data['search-lt_d']):
            lt = Term.objects.get(pk=data['search-lt_d'])
            queryset = queryset.filter(
                location_type__lft__gte=lt.lft,
                location_type__rght__lte=lt.rght,
                location_type__tree_id=lt.tree_id,
            )
        elif data.has_key('search-lt') and numeric.match(data['search-lt']):
            lt = Term.objects.get(pk=data['search-lt'])
            queryset = queryset.filter(
                location_type__lft__gte=lt.lft,
                location_type__rght__lte=lt.rght,
                location_type__tree_id=lt.tree_id,
            )

        if data.has_key('search-status') and len(data['search-status']) > 0:
            queryset = queryset.filter(status=data['search-status'])

    queryset = queryset.filter(
        status__in=("published", "published_commercial"),
    ).distinct()

    if kwargs.has_key("extra_context"):
        extra_context = kwargs["extra_context"]
    else:
        extra_context = {}

    if ot_url_part:
        abc_list = get_abc_list(queryset, "title", abc_filter)
        if abc_filter:
            queryset = filter_abc(queryset, "title", abc_filter)
        extra_context["abc_list"] = abc_list

    extra_context['source_list'] = "simplesearch"
    # this one indicates that the content object should be used for the prev-next prcessors
    extra_context['prev_next_use_content_object'] = True

    kwargs['extra_context'] = extra_context
    kwargs['queryset'] = queryset
    kwargs['template_name'] = template_name
    kwargs['httpstate_prefix'] = "search"

    return object_list(request, **kwargs)


def simplesearch_ical(request, ot_url_part=None, **kwargs):
    return simplesearch(request, ot_url_part, ical=True, **kwargs)


import haystack.views as haystack_views
from ccb.apps.search.forms import model_choices, ModelSearchForm, get_dictionaries


class SearchView(haystack_views.SearchView):
    def __init__(self, template=None, load_all=True, form_class=ModelSearchForm, searchqueryset=None,
                 context_class=RequestContext, results_per_page=None, limit=None):
        super(SearchView, self).__init__(template, load_all, form_class, searchqueryset, context_class,
                                         results_per_page)
        self.limit = limit

    def create_response(self):
        """
        Generates the actual HttpResponse to send back to the user.
        """
        # sort by default order
        app_models, indexes = get_dictionaries()

        result_groups = []
        for short_name, verbose_name in model_choices():
            app_model = indexes[short_name]
            # results = self.results.models(models.get_model(*app_model.split(".")))
            results = self.results.filter(django_ct=app_model)
            length = results.count()
            if length:
                d = {
                    'short_name': short_name,
                    'verbose_name': verbose_name,
                    'count': length,
                    'results': results[:self.limit] if self.limit else results,
                }
                if self.limit is None and self.request.GET.get('t', "") == short_name:
                    paginator = Paginator(results, self.results_per_page)
                    try:
                        page = paginator.page(self.request.GET.get('page', 1))
                    except:
                        raise Http404
                    d['paginator'] = paginator
                    d['page'] = page
                result_groups.append(d)

        context = {
            'query': self.query,
            'form': self.form,
            'full': self.limit is None,
            'result_groups': result_groups
        }
        context.update(self.extra_context())

        return render_to_response(self.template, context, context_instance=self.context_class(self.request))

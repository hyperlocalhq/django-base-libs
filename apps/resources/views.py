# -*- coding: UTF-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.apps import apps

from jetson.apps.utils.decorators import login_required
from jetson.apps.utils.views import object_list, object_detail, get_abc_list, filter_abc, get_year_list, filter_year
Document = apps.get_model("resources", "Document")
URL_ID_DOCUMENT = apps.get_app("resources").URL_ID_DOCUMENT
URL_ID_DOCUMENTS = apps.get_app("resources").URL_ID_DOCUMENTS

def _document_list_filter(request, queryset, show):
    return queryset.filter(
        status__in=("published", "published_commercial"),
        )

@never_cache
def document_list(
    request, 
    criterion="",
    slug="",
    show="",
    list_filter=_document_list_filter,
    **kwargs
    ):
    """Displays the list of documents"""
    
    abc_list = None
    abc_filter = request.GET.get('by-abc', None)
    
    kwargs['queryset'] = list_filter(request, kwargs['queryset'], show)
        
    document_filters = {}
    
    # DEPRECATED, but left as a possible solution
    # multiple filters can be collected from GET params like this:
    # for var in ("type", "commerciality", "actuality"):
    #    if var in request.GET:
    #        document_filters[var] = request.GET[var]
    
    if not document_filters:
        document_filters = request.httpstate.get('document_filters', {})
        
    if slug=="all":
        try:
            del(document_filters[criterion])
        except:
            pass
    else:
        if document_filters.get('criterion', '') != slug:
            document_filters[criterion] = slug
    request.httpstate['document_filters'] = document_filters
    
    if len(document_filters) == 0 and criterion:
        return HttpResponseRedirect('/%s/' % URL_ID_DOCUMENTS)
    elif len(document_filters) == 1 and criterion != document_filters.keys()[0]:
        for k, v in document_filters.items():
            page = 'page' in request.GET and "?page=%s" % request.GET.get("page", "") or ""
            return HttpResponseRedirect('/%s/by-%s/%s/%s' % (URL_ID_DOCUMENTS, k, v, page))
    elif not len(request.GET) and len(document_filters) > 1:
        query_vars = "?" + "&".join(["%s=%s" % (k, v) for k, v in document_filters.items()])
        page = 'page' in request.GET and "?page=%s" % request.GET.get("page") or ""
        return HttpResponseRedirect('/%s/%s%s' % (URL_ID_DOCUMENTS, page, query_vars))
    else:
        queryset = kwargs['queryset']
        
        # DEPRECATED, but left as a possible solution
        # the queryset might be filtered by different document_filters here
        # e.g.
        # if document_filters['type'] == "own":
        #     queryset.filter(owner=get_current_user())
        
        abc_list = get_abc_list(queryset, "title", abc_filter)
        if abc_filter:
            queryset = filter_abc(queryset, "title", abc_filter)

        extra_context = {'abc_list': abc_list, 'show': ("", "/%s" % show)[bool(show)], 'source_list': URL_ID_DOCUMENTS}
        if request.is_ajax():
            extra_context['base_template'] = "base_ajax.html"
        kwargs['extra_context'] = extra_context  
        kwargs['httpstate_prefix'] = URL_ID_DOCUMENTS        
        kwargs['queryset'] = queryset  
        return object_list(request, **kwargs)



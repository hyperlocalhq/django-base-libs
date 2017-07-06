# -*- coding: UTF-8 -*-
from django.db import models
from django.views.decorators.cache import never_cache
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from base_libs.utils.misc import get_installed
from jetson.apps.utils.views import object_list
from jetson.apps.utils.views import get_abc_list
from jetson.apps.utils.views import filter_abc

URL_ID_PEOPLE = get_installed("people.models.URL_ID_PEOPLE")
Person = models.get_model("people", "Person")
Institution = models.get_model("institutions", "Institution")


def _person_list_filter(request, queryset, show):
    return queryset.filter(
        status="published",
        )

@never_cache
def person_list(
    request,
    criterion="",
    slug="",
    show="",
    list_filter=_person_list_filter,
    **kwargs
    ):
    """Displays the list of people"""
    
    abc_list = None
    abc_filter = request.GET.get('by-abc', None)
    
    kwargs['queryset'] = list_filter(request, kwargs['queryset'], show)

    person_filters = {}
    for var in ("type", "commerciality", "location-type", "actuality", "neighborhood"):
        if var in request.GET:
            person_filters[var] = request.GET[var]
    if not person_filters:
        person_filters = request.httpstate.get('person_filters', {})
        
    if slug=="all":
        try:
            del(person_filters[criterion])
        except:
            pass
    else:
        if person_filters.get('criterion', '') != slug:
            person_filters[criterion] = slug
    request.httpstate['person_filters'] = person_filters
    
    if len(person_filters) == 0 and criterion:
        return HttpResponseRedirect('/%s/' % URL_ID_PEOPLE)
    elif len(person_filters) == 1 and criterion != person_filters.keys()[0]:
        for k, v in person_filters.items():
            page = 'page' in request.GET and "?page=%s" % request.GET.get("page", "") or ""
            return HttpResponseRedirect('/%s/by-%s/%s/%s' % (URL_ID_PEOPLE, k, v, page))
    elif not len(request.GET) and len(person_filters) > 1:
        query_vars = "?" + "&".join(["%s=%s" % (k, v) for k, v in person_filters.items()])
        page = 'page' in request.GET and "?page=%s" % request.GET.get("page", "") or ""
        return HttpResponseRedirect('/%s/%s%s' % (URL_ID_PEOPLE, page, query_vars))
    else:
        queryset = kwargs['queryset']
        for k, v in person_filters.items():
            if k=="type":
                pass
            elif k=="commerciality":
                queryset = queryset.filter(is_non_profit = True)
            elif k=="location-type" and request.user.is_authenticated():
                q = None
                for n in request.user.get_person().get_neighborhoods():
                    if not q:
                        q = models.Q(neighborhoods__icontains=n)
                    else:
                        q |= models.Q(neighborhoods__icontains=n)
                if q:
                    queryset = queryset.filter(q)
            elif k=="actuality":
                if v=="activity":
                    queryset = queryset.order_by("-last_activity_timestamp")
                elif v=="rating":
                    queryset = queryset.order_by("rating")
                elif v=="new":
                    queryset = queryset.order_by("-creation_date")
                elif v=="my-contacts":
                    person_ids = [p.id for p in Person.objects.filter(user__to_user__user=request.user).distinct()]
                    person_ctype = ContentType.objects.get_for_model(Person)
                    institution_ids = [i.id for i in Institution.objects.filter(persongroup__groupmembership__user=request.user).distinct()]
                    institution_ctype = ContentType.objects.get_for_model(Institution)
                    queryset = queryset.filter(models.Q(object_id__in=person_ids) & models.Q(content_type=person_ctype) | models.Q(object_id__in=institution_ids) & models.Q(content_type=institution_ctype))
            
        abc_list = get_abc_list(queryset, "user__last_name", abc_filter)
        if abc_filter:
            queryset = filter_abc(queryset, "user__last_name", abc_filter)

        view_type = request.REQUEST.get('view_type', request.httpstate.get(
            "%s_view_type" % URL_ID_PEOPLE,
            "icons",
            ))
        if view_type == "map":
            queryset = queryset.filter(
                individualcontact__postal_address__geoposition__latitude__gte=-90,
                ).distinct()
        
        extra_context = {'abc_list': abc_list, 'show': ("", "/%s" % show)[bool(show)], 'source_list': URL_ID_PEOPLE}
        if request.is_ajax():
            extra_context['base_template'] = "base_ajax.html"

        kwargs['extra_context'] = extra_context  
        kwargs['httpstate_prefix'] = URL_ID_PEOPLE
        kwargs['queryset'] = queryset
              
        return object_list(request, **kwargs)

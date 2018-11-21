# -*- coding: UTF-8 -*-
from django.utils.translation import ugettext_lazy as _, ugettext
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db import transaction
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.apps import apps

from base_libs.utils.misc import get_installed

from jetson.apps.utils.decorators import login_required
from jetson.apps.utils.views import object_list, object_detail, show_form_step, get_abc_list, filter_abc

app = models.get_app("institutions")
Institution, URL_ID_INSTITUTION, URL_ID_INSTITUTIONS = (
    app.Institution,
    app.URL_ID_INSTITUTION,
    app.URL_ID_INSTITUTIONS,
)

PersonGroup = apps.get_model("groups_networks", "PersonGroup")

ADD_INSTITUTION_FORM_STEPS = get_installed(
    "institutions.forms.ADD_INSTITUTION_FORM_STEPS"
)


@never_cache
@transaction.atomic
@login_required
def add_institution(request):
    return show_form_step(request, ADD_INSTITUTION_FORM_STEPS, extra_context={})


def _institution_list_filter(request, queryset, show):
    return queryset.filter(status__in=("published", "published_commercial"), )


@never_cache
def institution_list(
    request,
    criterion="",
    slug="",
    show="",
    list_filter=_institution_list_filter,
    **kwargs
):
    """Displays the list of institutions"""

    abc_list = None
    abc_filter = request.GET.get('by-abc', None)

    kwargs['queryset'] = list_filter(request, kwargs['queryset'], show)

    institution_filters = {}
    for var in (
        "type", "commerciality", "location-type", "actuality", "neighborhood"
    ):
        if var in request.GET:
            institution_filters[var] = request.GET[var]
    if not institution_filters:
        institution_filters = request.httpstate.get('institution_filters', {})

    if slug == "all":
        try:
            del (institution_filters[criterion])
        except:
            pass
    else:
        if institution_filters.get('criterion', '') != slug:
            institution_filters[criterion] = slug
    request.httpstate['institution_filters'] = institution_filters

    if len(institution_filters) == 0 and criterion:
        return HttpResponseRedirect('/%s/' % URL_ID_INSTITUTIONS)
    elif len(institution_filters
            ) == 1 and criterion != institution_filters.keys()[0]:
        for k, v in institution_filters.items():
            page = 'page' in request.GET and "?page=%s" % request.GET.get(
                "page", ""
            ) or ""
            return HttpResponseRedirect(
                '/%s/by-%s/%s/%s' % (URL_ID_INSTITUTIONS, k, v, page)
            )
    elif not len(request.GET) and len(institution_filters) > 1:
        query_vars = "?" + "&".join(
            ["%s=%s" % (k, v) for k, v in institution_filters.items()]
        )
        page = 'page' in request.GET and "?page=%s" % request.GET.get(
            "page", ""
        ) or ""
        return HttpResponseRedirect(
            '/%s/%s%s' % (URL_ID_INSTITUTIONS, page, query_vars)
        )
    else:
        queryset = kwargs['queryset']
        for k, v in institution_filters.items():
            if k == "type":
                pass
            elif k == "commerciality":
                queryset = queryset.filter(is_non_profit=True)
            elif k == "location-type" and request.user.is_authenticated():
                q = None
                for n in request.user.get_institution().get_neighborhoods():
                    if not q:
                        q = models.Q(neighborhoods__icontains=n)
                    else:
                        q |= models.Q(neighborhoods__icontains=n)
                if q:
                    queryset = queryset.filter(q)
            elif k == "actuality":
                if v == "activity":
                    queryset = queryset.order_by("-last_activity_timestamp")
                elif v == "rating":
                    queryset = queryset.order_by("rating")
                elif v == "new":
                    queryset = queryset.order_by("-creation_date")
                elif v == "my-contacts":
                    institution_ids = [
                        p.id for p in Institution.objects.
                        filter(user__to_user__user=request.user).distinct()
                    ]
                    institution_ctype = ContentType.objects.get_for_model(
                        Institution
                    )
                    institution_ids = [
                        i.id for i in Institution.objects.filter(
                            persongroup__groupmembership__user=request.user
                        ).distinct()
                    ]
                    institution_ctype = ContentType.objects.get_for_model(
                        Institution
                    )
                    queryset = queryset.filter(
                        models.Q(object_id__in=institution_ids
                                ) & models.Q(content_type=institution_ctype) |
                        models.Q(object_id__in=institution_ids
                                ) & models.Q(content_type=institution_ctype)
                    )

        abc_list = get_abc_list(queryset, "title", abc_filter)
        if abc_filter:
            queryset = filter_abc(queryset, "title", abc_filter)

        view_type = request.REQUEST.get(
            'view_type',
            request.httpstate.get(
                "%s_view_type" % URL_ID_INSTITUTIONS,
                "icons",
            )
        )
        if view_type == "map":
            queryset = queryset.filter(
                institutionalcontact__postal_address__geoposition__latitude__gte
                =-90,
            ).distinct()

        extra_context = {
            'abc_list': abc_list,
            'show': ("", "/%s" % show)[bool(show)],
            'source_list': URL_ID_INSTITUTIONS
        }
        if request.is_ajax():
            extra_context['base_template'] = "base_ajax.html"

        kwargs['extra_context'] = extra_context
        kwargs['httpstate_prefix'] = URL_ID_INSTITUTIONS
        kwargs['queryset'] = queryset

        return object_list(request, **kwargs)

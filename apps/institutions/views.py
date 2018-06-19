# -*- coding: UTF-8 -*-
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from base_libs.views import access_denied
from jetson.apps.institutions.views import *
from ccb.apps.events.views import event_list
from ccb.apps.marketplace.views import job_offer_list
from ccb.apps.institutions.forms import InstitutionSearchForm


class AccessDenied(Warning):
    pass


def _institution_list_filter(request, queryset, show):
    queryset = queryset.defer(
        "description", "description_de", "description_en",
        "description_de_markup_type", "description_en_markup_type",
        "exceptions", "exceptions_de", "exceptions_en",
        "exceptions_de_markup_type", "exceptions_en_markup_type",
    )

    if show == "favorites":
        from ccb.apps.site_specific.models import ContextItem

        if not request.user.is_authenticated():
            raise AccessDenied

        tables = ["favorites_favorite"]
        condition = [
            "favorites_favorite.user_id = %d" % request.user.id,
            "favorites_favorite.object_id::integer = system_contextitem.id",
        ]
        ct = ContentType.objects.get_for_model(queryset.model)
        fav_inst_ids = [
            int(el['object_id']) for el in ContextItem.objects.filter(
                content_type=ct
            ).extra(
                tables=tables,
                where=condition,
            ).distinct().values("object_id")
        ]
        queryset = queryset.filter(pk__in=fav_inst_ids)
    elif show == "memos":
        from jetson.apps.memos.models import Memo, MEMO_TOKEN_NAME

        ct = ContentType.objects.get_for_model(queryset.model)
        memos_ids = map(int, Memo.objects.filter(
            collection__token=request.COOKIES.get(MEMO_TOKEN_NAME, None),
            content_type=ct,
        ).values_list("object_id", flat=True))
        queryset = queryset.filter(
            pk__in=memos_ids,
        )
    elif show == "own-%s" % URL_ID_INSTITUTIONS:
        if not request.user.is_authenticated():
            raise AccessDenied
        from ccb.apps.groups_networks.models import PersonGroup

        ct = ContentType.objects.get_for_model(queryset.model)
        owned_inst_ids = [
            int(el['object_id']) for el in PersonGroup.objects.filter(
                groupmembership__user=request.user,
                content_type=ct,
            ).distinct().values("object_id")
            ]
        queryset = queryset.filter(pk__in=owned_inst_ids)
    else:
        queryset = queryset.filter(
            status__in=("published", "published_commercial"),
        )
    return queryset


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

    try:
        kwargs['queryset'] = list_filter(request, kwargs['queryset'], show)
    except AccessDenied:
        return access_denied(request)

    institution_filters = {}
    for var in ("type", "commerciality", "location-type", "actuality", "neighborhood"):
        if var in request.GET:
            institution_filters[var] = request.GET[var]
    if not institution_filters:
        institution_filters = request.httpstate.get('institution_filters', {})

    if slug == "all":
        try:
            del (institution_filters[criterion])
        except Exception:
            pass
    else:
        if institution_filters.get('criterion', '') != slug:
            institution_filters[criterion] = slug
    request.httpstate['institution_filters'] = institution_filters

    if len(institution_filters) == 0 and criterion:
        return HttpResponseRedirect('/%s/' % URL_ID_INSTITUTIONS)
    elif len(institution_filters) == 1 and criterion != institution_filters.keys()[0]:
        for k, v in institution_filters.items():
            page = 'page' in request.GET and "?page=%s" % request.GET.get("page", "") or ""
            return HttpResponseRedirect('/%s/by-%s/%s/%s' % (URL_ID_INSTITUTIONS, k, v, page))
    elif not len(request.GET) and len(institution_filters) > 1:
        query_vars = "?" + "&".join(["%s=%s" % (k, v) for k, v in institution_filters.items()])
        page = 'page' in request.GET and "?page=%s" % request.GET.get("page", "") or ""
        return HttpResponseRedirect('/%s/%s%s' % (URL_ID_INSTITUTIONS, page, query_vars))
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
                    institution_ids = [p.id for p in
                                       Institution.objects.filter(user__to_user__user=request.user).distinct()]
                    institution_ctype = ContentType.objects.get_for_model(Institution)
                    institution_ids = [force_text(i.id) for i in Institution.objects.filter(
                        persongroup__groupmembership__user=request.user).distinct()]
                    institution_ctype = ContentType.objects.get_for_model(Institution)
                    queryset = queryset.filter(
                        models.Q(object_id__in=institution_ids) & models.Q(content_type=institution_ctype) | models.Q(
                            object_id__in=institution_ids) & models.Q(content_type=institution_ctype))

        abc_list = get_abc_list(queryset, "title", abc_filter)
        if abc_filter:
            queryset = filter_abc(queryset, "title", abc_filter)

        view_type = request.REQUEST.get('view_type', request.httpstate.get(
            "%s_view_type" % URL_ID_INSTITUTIONS,
            "icons",
        ))
        if view_type == "map":
            queryset = queryset.filter(
                institutionalcontact__postal_address__geoposition__latitude__gte=-90,
            ).distinct()

        form = InstitutionSearchForm(data=request.REQUEST)
        if form.is_valid():
            cs = form.cleaned_data['creative_sector']
            if cs:
                queryset = queryset.filter(
                    creative_sectors__lft__gte=cs.lft,
                    creative_sectors__rght__lte=cs.rght,
                    creative_sectors__tree_id=cs.tree_id,
                ).distinct()
            cc = form.cleaned_data['context_category']
            if cc:
                queryset = queryset.filter(
                    context_categories__lft__gte=cc.lft,
                    context_categories__rght__lte=cc.rght,
                    context_categories__tree_id=cc.tree_id,
                ).distinct()
            it = form.cleaned_data['institution_type']
            if it:
                queryset = queryset.filter(
                    institution_types=it,
                )

            lt = form.cleaned_data['locality_type']
            if lt:
                ContextItem = models.get_model("site_specific", "ContextItem")
                context_item_qs = ContextItem.objects.filter(
                    content_type__app_label="events",
                    content_type__model="event",
                )
                if lt:
                    context_item_qs = context_item_qs.filter(
                        locality_type__lft__gte=lt.lft,
                        locality_type__rght__lte=lt.rght,
                        locality_type__tree_id=lt.tree_id,
                    ).distinct()

                institutions_pks = map(int, context_item_qs.values_list("object_id", flat=True))

                queryset = queryset.filter(
                    pk__in=institutions_pks,
                )

        extra_context = {'form': form, 'abc_list': abc_list, 'show': ("", "/%s" % show)[bool(show)],
                         'source_list': URL_ID_INSTITUTIONS}
        if request.is_ajax():
            extra_context['base_template'] = "base_ajax.html"

        kwargs['extra_context'] = extra_context
        kwargs['httpstate_prefix'] = URL_ID_INSTITUTIONS
        kwargs['queryset'] = queryset

        return object_list(request, **kwargs)


@never_cache
def institution_staff_list(request, slug, **kwargs):
    """
    Lists the institution's staff
    """
    institution = get_object_or_404(Institution, slug=slug)
    staff = institution.get_contact_persons()
    kwargs['queryset'] = kwargs['queryset'].filter(
        pk__in=[person.id for person in staff],
    )

    kwargs.setdefault("extra_context", {})
    kwargs['extra_context']['object'] = institution
    return object_list(request, **kwargs)


@never_cache
def institution_partners_list(request, slug, **kwargs):
    """
    Lists the institution's partners
    """
    raise Http404


@never_cache
def institution_groups_list(request, slug, **kwargs):
    """
    Lists the institution's groups
    """
    institution = get_object_or_404(Institution, slug=slug)

    # TODO maybe there is a better solution for this:
    # Here we need a queryset but have a list. So we make a queryset from the list...
    groups = institution.get_groups()
    extra_clause = "id in (%s)" % ", ".join(["%d" % group.id for group in groups])
    kwargs['queryset'] = kwargs['queryset'].extra(where=[extra_clause])

    kwargs.setdefault("extra_context", {})
    kwargs['extra_context']['object'] = institution

    return object_list(request, **kwargs)


@never_cache
def institution_events_list(request, slug, **kwargs):
    """
    Lists the institution's events
    """
    institution = get_object_or_404(Institution, slug=slug)
    kwargs['queryset'] = kwargs['queryset'].filter(
        models.Q(organizing_institution=institution) |
        models.Q(venue=institution),
    ).order_by('-creation_date')
    kwargs.setdefault("extra_context", {})
    kwargs['extra_context']['object'] = institution
    kwargs['title'] = _("Events by/at %s") % institution.get_title()
    return event_list(request, show="related", **kwargs)


@never_cache
def institution_events_list_ical(request, slug, **kwargs):
    return institution_events_list(request, slug, ical=True, **kwargs)


@never_cache
def institution_events_list_feed(request, slug, **kwargs):
    return institution_events_list(request, slug, feed=True, **kwargs)


@never_cache
def institution_job_offer_list(request, slug, **kwargs):
    """
    Lists the institution's job offers
    """
    institution = get_object_or_404(Institution, slug=slug)
    kwargs['queryset'] = kwargs['queryset'].filter(
        offering_institution=institution,
    ).order_by('-creation_date')
    kwargs.setdefault("extra_context", {})
    kwargs['extra_context']['object'] = institution
    kwargs['title'] = _("Job offers by %s") % institution.get_title()
    return job_offer_list(request, show="related", **kwargs)


@never_cache
def institution_job_offer_list_feed(request, slug, **kwargs):
    return institution_job_offer_list(request, slug, feed=True, **kwargs)

# -*- coding: UTF-8 -*-
from jetson.apps.resources.views import *

from base_libs.views import access_denied
from ccb.apps.resources.forms import DocumentSearchForm


class AccessDenied(Warning):
    pass


def _document_list_filter(request, queryset, show):
    queryset = queryset.defer(
        "description", "description_de", "description_en",
        "description_de_markup_type", "description_en_markup_type",
    )

    if show == "favorites":
        if not request.user.is_authenticated():
            raise AccessDenied

        from ccb.apps.site_specific.models import ContextItem

        tables = ["favorites_favorite"]
        condition = ["favorites_favorite.user_id = %d" % request.user.id,
                     "favorites_favorite.object_id::integer = system_contextitem.id"]
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
    elif show == "cultural-funding":
        queryset = queryset.filter(
            document_type__slug="cultural-funding",
        )
    elif show == "scholarship":
        queryset = queryset.filter(
            document_type__slug="scholarship",
        )
    elif show == "support-programme":
        queryset = queryset.filter(
            document_type__slug="support-programme",
        )
    elif show == "information-founders":
        queryset = queryset.filter(
            document_type__slug="information-founders",
        )
    elif show == "other":
        queryset = queryset.exclude(
            document_type__slug__in=[
                "cultural-funding",
                "scholarship",
                "support-programme",
                "information-founders",
            ],
        )
    else:
        queryset = queryset.filter(
            status__in=("published", "published_commercial"),
        )
    return queryset


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

    try:
        kwargs['queryset'] = list_filter(request, kwargs['queryset'], show)
    except AccessDenied:
        return access_denied(request)

    document_filters = {}

    # DEPRECATED, but left as a possible solution
    # multiple filters can be collected from GET params like this:
    # for var in ("type", "commerciality", "actuality"):
    #    if var in request.GET:
    #        document_filters[var] = request.GET[var]

    if not document_filters:
        document_filters = request.httpstate.get('document_filters', {})

    if slug == "all":
        try:
            del (document_filters[criterion])
        except Exception:
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

        form = DocumentSearchForm(data=request.REQUEST)
        if form.is_valid():
            cat = form.cleaned_data['category']
            if cat:
                queryset = queryset.filter(
                    categories__tree_id=cat.tree_id,
                ).distinct()
            dt = form.cleaned_data['document_type']
            if dt:
                queryset = queryset.filter(
                    document_type__lft__gte=dt.lft,
                    document_type__rght__lte=dt.rght,
                    document_type__tree_id=dt.tree_id,
                )

        extra_context = {'form': form, 'abc_list': abc_list, 'show': ("", "/%s" % show)[bool(show)],
                         'source_list': URL_ID_DOCUMENTS}
        if request.is_ajax():
            extra_context['base_template'] = "base_ajax.html"
        kwargs['extra_context'] = extra_context
        kwargs['httpstate_prefix'] = URL_ID_DOCUMENTS
        kwargs['queryset'] = queryset
        return object_list(request, **kwargs)

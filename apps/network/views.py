# -*- coding: UTF-8 -*-

from django.db import models
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

from base_libs.views import access_denied

from jetson.apps.structure.models import Category
from jetson.apps.utils.views import object_list, object_detail
from jetson.apps.utils.views import get_abc_list
from jetson.apps.utils.views import filter_abc

from ccb.apps.people.models import Person
from ccb.apps.institutions.models import Institution
from ccb.apps.site_specific.models import ContextItem

from .forms import MemberSearchForm


class AccessDenied(Warning):
    pass


def _member_list_filter(request, queryset, show):
    queryset = queryset.defer(
        # "description", "description_de", "description_en",
        # "description_markup_type", "description_de_markup_type", "description_en_markup_type",
        # "birthname", "gender", "birthday_yyyy", "birthday_mm", "birthday_dd",
        # "nationality", "degree", "interests", "preferred_language",
        # "timezone", "completeness", "user__password",
    )
    print(show)
    if show == "contacts":
        from ccb.apps.site_specific.models import ContextItem

        if not request.user.is_authenticated():
            pass
            # raise Http404
        tables = ["favorites_favorite"]
        condition = [
            "favorites_favorite.user_id = %d" % request.user.id,
            "favorites_favorite.object_id = system_contextitem.id"]
        ct = ContentType.objects.get_for_model(queryset.model)
        fav_person_ids = [
            el['object_id'] for el in ContextItem.objects.filter(
                content_type=ct
            ).extra(
                tables=tables,
                where=condition,
            ).distinct().values("object_id")
            ]
        queryset = queryset.filter(
            pk__in=fav_person_ids,
        )
    elif show == "relationships":
        if not request.user.is_authenticated():
            raise Http404
        queryset = queryset.filter(
            user__to_user__user=request.user,
            user__to_user__status="confirmed",
        )
    elif show == "memos":
        from jetson.apps.memos.models import Memo, MEMO_TOKEN_NAME

        ct = ContentType.objects.get_for_model(queryset.model)
        memos_ids = Memo.objects.filter(
            collection__token=request.COOKIES.get(MEMO_TOKEN_NAME, None),
            content_type=ct,
        ).values_list("object_id", flat=True)
        queryset = queryset.filter(
            pk__in=memos_ids,
        )
    elif show == "favorites":
        from ccb.apps.site_specific.models import ContextItem

        if not request.user.is_authenticated():
            raise AccessDenied

        tables = ["favorites_favorite"]
        condition = ["favorites_favorite.user_id = %d" % request.user.id,
                     "favorites_favorite.object_id = system_contextitem.id"]
        ct = ContentType.objects.get_for_model(queryset.model)
        fav_inst_ids = [
            el['object_id'] for el in ContextItem.objects.filter(
                content_type=ct
            ).extra(
                tables=tables,
                where=condition,
            ).distinct().values("object_id")
            ]
        queryset = queryset.filter(pk__in=fav_inst_ids)
    elif show == "own-institutions":
        if not request.user.is_authenticated():
            raise AccessDenied
        from ccb.apps.groups_networks.models import PersonGroup

        ct = ContentType.objects.get_for_model(queryset.model)
        owned_inst_ids = [
            el['object_id'] for el in PersonGroup.objects.filter(
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


def member_list(request, creative_sector_slug="", show="", list_filter=_member_list_filter, **kwargs):
    if creative_sector_slug:
        kwargs['queryset'] = kwargs['queryset'].filter(
            creative_sectors__slug=creative_sector_slug,
        )
    try:
        kwargs['queryset'] = list_filter(request, kwargs['queryset'], show)
    except AccessDenied:
        return access_denied(request)

    abc_list = None
    abc_filter = request.GET.get('by-abc', None)

    view_type = request.REQUEST.get('view_type', request.httpstate.get(
        "context_item_view_type",
        "icons",
    ))
    if view_type == "map":
        people_ids = Person.objects.filter(
            individualcontact__postal_address__geoposition__latitude__gte=-90,
        ).distinct().values_list("id", flat=True)
        institutions_ids = Institution.objects.filter(
            institutionalcontact__postal_address__geoposition__latitude__gte=-90,
        ).distinct().values_list("id", flat=True)
        kwargs['queryset'] = kwargs['queryset'].filter(
            models.Q(content_type__model="person", object_id__in=people_ids)
            | models.Q(content_type__model="institution", object_id__in=institutions_ids)
        )

    form = MemberSearchForm(data=request.REQUEST)

    facets = {
        'selected': {},
        'categories': {
            'categories': Category.objects.all(),
            'object_types': form.fields['object_type'].choices,
            'locality_types': form.fields['locality_type'].queryset,
        },
    }


    if form.is_valid():

        cat = form.cleaned_data['category']
        if cat:
            facets['selected']['category'] = cat
            kwargs['queryset'] = kwargs['queryset'].filter(
                categories__lft__gte=cat.lft,
                categories__rght__lte=cat.rght,
                categories__tree_id=cat.tree_id,
            ).distinct()

        lt = form.cleaned_data['locality_type']
        if lt:
            facets['selected']['locality_type'] = lt
            kwargs['queryset'] = kwargs['queryset'].filter(
                locality_type__lft__gte=lt.lft,
                locality_type__rght__lte=lt.rght,
                locality_type__tree_id=lt.tree_id,
            )

        ot = form.cleaned_data['object_type']
        if ot:
            facets['selected']['object_type'] = ot
            kwargs['queryset'] = kwargs['queryset'].filter(
                content_type__model=ot,
            )

    abc_list = get_abc_list(kwargs['queryset'], "title", abc_filter)
    if abc_filter:
        kwargs['queryset'] = filter_abc(kwargs['queryset'], "title", abc_filter)

    kwargs['queryset'] = kwargs['queryset'].distinct()

    extra_context = kwargs.setdefault("extra_context", {})
    extra_context['form'] = form
    extra_context['abc_list'] = abc_list
    facets['queryset'] = kwargs['queryset']
    extra_context['facets'] = facets

    if request.is_ajax():
        extra_context['base_template'] = "base_ajax.html"

    return object_list(request, **kwargs)


def member_detail(request, slug, creative_sector_slug="", **kwargs):
    ci = get_object_or_404(
        ContextItem,
        content_type__model__in=["person", "institution"],
        status="published",
        slug=slug,
    )
    if ci.is_person():
        kwargs['queryset'] = Person.objects.all()
        kwargs['template_name'] = 'people/person_details.html'
        kwargs['slug_field'] = 'user__username'
        kwargs['slug'] = slug
    else:
        kwargs['queryset'] = Institution.objects.all()
        kwargs['template_name'] = 'institutions/institution_details.html'
        kwargs['slug_field'] = 'slug'
        kwargs['slug'] = slug

    if creative_sector_slug:
        kwargs['queryset'] = kwargs['queryset'].filter(
            creative_sectors__slug=creative_sector_slug,
        )
    return object_detail(request, **kwargs)

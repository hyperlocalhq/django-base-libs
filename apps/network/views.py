# -*- coding: UTF-8 -*-

from django.db import models
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.cache import never_cache
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from base_libs.views import access_denied

from jetson.apps.structure.models import Category
from jetson.apps.utils.views import object_list, object_detail
from jetson.apps.utils.views import get_abc_list
from jetson.apps.utils.views import filter_abc

from ccb.apps.people.models import Person
from ccb.apps.institutions.models import Institution
from ccb.apps.site_specific.models import ContextItem
from ccb.apps.events.views import event_list

from actstream.models import following

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
    if show in ("contacts", "favorites"):
        if not request.user.is_authenticated():
            raise AccessDenied
        tables = ["favorites_favorite"]
        condition = [
            "favorites_favorite.user_id = %d" % request.user.id,
            "favorites_favorite.object_id = system_contextitem.id"]
        queryset = queryset.filter(
            content_type__model__in=("person", "institution")
        ).extra(
            tables=tables,
            where=condition,
        ).distinct()
    elif show == "following":
        if not request.user.is_authenticated():
            raise Http404
        followees = following(request.user)
        conditions = models.Q()
        institution_ct = ContentType.objects.get_for_model(Institution)
        person_ct = ContentType.objects.get_for_model(Person)
        if followees:
            for followee in followees:
                if isinstance(followee, Institution):
                    ct = institution_ct
                    object_id = followee.pk
                elif isinstance(followee, User):
                    ct = person_ct
                    object_id = followee.profile.pk
                else:
                    continue
                conditions |= models.Q(
                    content_type=ct,
                    object_id=object_id,
                )
            queryset = queryset.filter(conditions)
        else:
            queryset = queryset.none()
    elif show == "relationships":
        if not request.user.is_authenticated():
            raise Http404
        related_people_pks = Person.objects.filter(
            user__to_user__user=request.user,
            user__to_user__status="confirmed",
        ).values_list("id", flat=True)
        ct = ContentType.objects.get_for_model(Person)
        queryset = queryset.filter(
            object_id__in=related_people_pks,
            content_type=ct,
        )
    elif show == "memos":
        # DEPRECATED
        from jetson.apps.memos.models import Memo, MEMO_TOKEN_NAME
        ct = ContentType.objects.get_for_model(queryset.model)
        memos_ids = Memo.objects.filter(
            collection__token=request.COOKIES.get(MEMO_TOKEN_NAME, None),
            content_type__model__in=("person", "institution"),
        ).values_list("object_id", flat=True)
        # the following should check object_id and content_type pairs
        queryset = queryset.filter(
            content_type__model__in=("person", "institution"),
            object_id__in=memos_ids,
        )
    elif show == "own-institutions":
        if not request.user.is_authenticated():
            raise AccessDenied
        from ccb.apps.groups_networks.models import PersonGroup

        ct = ContentType.objects.get_for_model(Institution)
        owned_inst_ids = [
            el['object_id'] for el in PersonGroup.objects.filter(
                groupmembership__user=request.user,
                content_type=ct,
            ).distinct().values("object_id")
            ]
        queryset = queryset.filter(object_id__in=owned_inst_ids, content_type=ct)
    else:
        queryset = queryset.filter(
            status__in=("published", "published_commercial"),
        )
    return queryset


def member_list(request, creative_sector_slug="", show="", list_filter=_member_list_filter, category_slug=None, **kwargs):
    if creative_sector_slug:
        kwargs['queryset'] = kwargs['queryset'].filter(
            creative_sectors__slug=creative_sector_slug,
        )

    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        kwargs['queryset'] = kwargs['queryset'].filter(categories__tree_id=category.tree_id)

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

    form = MemberSearchForm(category, data=request.REQUEST)

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
    extra_context['category'] = category
    facets['queryset'] = kwargs['queryset']
    extra_context['facets'] = facets

    if request.is_ajax():
        extra_context['base_template'] = "base_ajax.html"

    return object_list(request, **kwargs)


def member_detail(request, slug, creative_sector_slug="", **kwargs):
    item = get_object_or_404(
        ContextItem,
        content_type__model__in=("person", "institution"),
        slug=slug,
    )
    if item.is_person():
        if not request.user.has_perm("people.change_person", item.content_object) and item.status not in ("published", "published_commercial"):
            return access_denied(request)
        kwargs['queryset'] = Person.objects.all()
        kwargs['template_name'] = 'people/person_details.html'
        kwargs['slug_field'] = 'user__username'
        kwargs['slug'] = slug
    else:
        if not request.user.has_perm("institutions.change_institution", item.content_object) and item.status not in ("published", "published_commercial"):
            return access_denied(request)
        kwargs['queryset'] = Institution.objects.all()
        kwargs['template_name'] = 'institutions/institution_details.html'
        kwargs['slug_field'] = 'slug'
        kwargs['slug'] = slug

    if creative_sector_slug:
        kwargs['queryset'] = kwargs['queryset'].filter(
            creative_sectors__slug=creative_sector_slug,
        )

    return object_detail(request, **kwargs)


@never_cache
def member_events_list(request, slug, **kwargs):
    """
    Lists the institution's events
    """
    item = get_object_or_404(
        ContextItem,
        content_type__model__in=("person", "institution"),
        slug=slug,
    )
    if item.is_person():
        if not request.user.has_perm("people.change_person", item.content_object) and item.status not in ("published", "published_commercial"):
            return access_denied(request)
        person = item.content_object
        kwargs['queryset'] = kwargs['queryset'].filter(
            models.Q(organizing_person=person)
        ).order_by('start')
        kwargs['template_name'] = 'people/person_events.html'
    else:
        if not request.user.has_perm("institutions.change_institution", item.content_object) and item.status not in ("published", "published_commercial"):
            return access_denied(request)
        institution = item.content_object
        kwargs['queryset'] = kwargs['queryset'].filter(
            models.Q(organizing_institution=institution) |
            models.Q(venue=institution),
        ).order_by('start')
        kwargs['template_name'] = 'institutions/institution_events.html'

    kwargs.setdefault("extra_context", {})
    kwargs['extra_context']['object'] = item.content_object
    kwargs['title'] = _("Events by/at %s") % item.content_object.get_title()
    return event_list(request, show="related", **kwargs)


@never_cache
def member_events_list_ical(request, slug, **kwargs):
    return member_events_list(request, slug, ical=True, **kwargs)


@never_cache
def member_events_list_feed(request, slug, **kwargs):
    return member_events_list(request, slug, feed=True, **kwargs)


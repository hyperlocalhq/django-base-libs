# -*- coding: UTF-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib.auth.models import User

from jetson.apps.utils.decorators import login_required
from jetson.apps.people.views import *
from ccb.apps.events.views import event_list
from ccb.apps.marketplace.views import job_offer_list
from ccb.apps.people.forms import PersonSearchForm


def _person_list_filter(request, queryset, show):
    queryset = queryset.defer(
        # "description", "description_de", "description_en",
        # "description_markup_type", "description_de_markup_type", "description_en_markup_type",
        # "birthname", "gender", "birthday_yyyy", "birthday_mm", "birthday_dd",
        # "nationality", "degree", "interests", "preferred_language",
        # "timezone", "completeness", "user__password",
    )

    if show == "contacts":
        from ccb.apps.site_specific.models import ContextItem

        if not request.user.is_authenticated():
            raise Http404
        tables = ["favorites_favorite"]
        condition = [
            "favorites_favorite.user_id = %d" % request.user.id,
            "favorites_favorite.object_id::integer = system_contextitem.id"]
        ct = ContentType.objects.get_for_model(queryset.model)
        fav_person_ids = [
            int(el['object_id']) for el in ContextItem.objects.filter(
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
        memos_ids = map(int, Memo.objects.filter(
            collection__token=request.COOKIES.get(MEMO_TOKEN_NAME, None),
            content_type=ct,
        ).values_list("object_id", flat=True))
        queryset = queryset.filter(
            pk__in=memos_ids,
        )
    else:
        queryset = queryset.filter(
            status="published",
        )
    return queryset


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

    Institution = models.get_model("institutions", "Institution")

    abc_list = None
    abc_filter = request.GET.get('by-abc', None)

    kwargs['queryset'] = list_filter(request, kwargs['queryset'], show)

    person_filters = {}
    for var in ("type", "commerciality", "location-type", "actuality", "neighborhood"):
        if var in request.GET:
            person_filters[var] = request.GET[var]
    if not person_filters:
        person_filters = request.httpstate.get('person_filters', {})

    if slug == "all":
        try:
            del (person_filters[criterion])
        except Exception:
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
            if k == "type":
                pass
            elif k == "commerciality":
                queryset = queryset.filter(is_non_profit=True)
            elif k == "location-type" and request.user.is_authenticated():
                q = None
                for n in request.user.get_person().get_neighborhoods():
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
                    person_ids = [p.id for p in Person.objects.filter(user__to_user__user=request.user).distinct()]
                    person_ctype = ContentType.objects.get_for_model(Person)
                    institution_ids = [i.id for i in Institution.objects.filter(
                        persongroup__groupmembership__user=request.user).distinct()]
                    institution_ctype = ContentType.objects.get_for_model(Institution)
                    queryset = queryset.filter(
                        models.Q(object_id__in=person_ids) & models.Q(content_type=person_ctype) | models.Q(
                            object_id__in=institution_ids) & models.Q(content_type=institution_ctype))

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

        form = PersonSearchForm(data=request.REQUEST)
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
            it = form.cleaned_data['individual_type']
            if it:
                queryset = queryset.filter(
                    individual_type=it,
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

                people_pks = list(context_item_qs.values_list("object_id", flat=True))

                queryset = queryset.filter(
                    pk__in=people_pks,
                )

        extra_context = {'form': form, 'abc_list': abc_list, 'show': ("", "/%s" % show)[bool(show)],
                         'source_list': URL_ID_PEOPLE}
        if request.is_ajax():
            extra_context['base_template'] = "base_ajax.html"

        kwargs['extra_context'] = extra_context
        kwargs['httpstate_prefix'] = URL_ID_PEOPLE
        kwargs['queryset'] = queryset

        return object_list(request, **kwargs)


def person_invitation_list(request, show="", **kwargs):
    """
    Rupert, 18032008
    I've created a separate view for the invitations lists. We do not need the
    filter stuff for the invitiation lists and login is required here.
    I think, that is cleaner this way ...
    
    here we filter for "pending or denied" (let us call it status_filter)
    also abc filters are allowed ...
    
    The default (indicated by url "invitations" is requests!
    """
    extra_context = kwargs.setdefault("extra_context", {})

    abc_list = None
    abc_filter = request.GET.get('by-abc', None)

    status_filter = request.GET.get('by-status', None)
    if status_filter:
        extra_context['active_status_filter'] = status_filter

    if show == "invitations":
        if not status_filter:
            status_filter = "pending"
        # TODO: change the hardcoded URL to a named one, specialized for network app
        return HttpResponseRedirect('/%s/requests/?by-status=%s' % (URL_ID_PEOPLE, status_filter))

    elif show == "requested":
        extra_context['active_link'] = "requested"

        if status_filter == "pending":
            filter_by = ['inviting']
        elif status_filter == "denied":
            filter_by = ['denied']
        else:
            filter_by = None

        queryset = request.user.profile.get_person_invitation_requested(filter_by)

    elif show == "requests":
        extra_context['active_link'] = 'requests'

        if status_filter == "pending":
            filter_by = ['invited']
        elif status_filter == "denied":
            filter_by = ['denying']
        else:
            filter_by = None

        queryset = request.user.profile.get_person_invitation_requests(filter_by)

    else:
        raise Http404

    abc_list = get_abc_list(queryset, "user__last_name", abc_filter)
    if abc_filter:
        queryset = filter_abc(queryset, "user__last_name", abc_filter)

    extra_context['abc_list'] = abc_list
    extra_context['show'] = "/%s" % show
    # Ruper20032008 that show stuff gives anb error in the produced pagination url ...
    # extra_context["show"] = ("", "/%s" % show)[bool(show)]
    extra_context['source_list'] = URL_ID_PEOPLE
    kwargs['extra_context'] = extra_context
    kwargs['queryset'] = queryset
    return object_list(request, **kwargs)


person_invitation_list = login_required(never_cache(person_invitation_list))


@never_cache
def person_person_contacts_list(request, slug, **kwargs):
    """
    Lists a person's individual contacts
    """
    user = get_object_or_404(User, username=slug)
    person = user.profile
    kwargs['queryset'] = kwargs['queryset'].filter(
        user__to_user__user=user,
        user__to_user__status="confirmed",
    )

    kwargs.setdefault("extra_context", {})
    kwargs['extra_context']['object'] = person

    return object_list(request, **kwargs)


@never_cache
def person_institution_contacts_list(request, slug, **kwargs):
    """
    Lists a person's institutional contacts
    """
    user = get_object_or_404(User, username=slug)
    person = user.profile

    institutions = person.get_institutions()
    kwargs['queryset'] = kwargs['queryset'].filter(id__in=[institution.id for institution in institutions])

    kwargs.setdefault("extra_context", {})
    kwargs['extra_context']['object'] = person

    return object_list(request, **kwargs)


@never_cache
def person_groups_list(request, slug, **kwargs):
    """
    Lists a person's groups
    """
    user = get_object_or_404(User, username=slug)
    person = user.profile

    groups = person.get_groups()
    kwargs['queryset'] = kwargs['queryset'].filter(id__in=[group.id for group in groups])

    kwargs.setdefault("extra_context", {})
    kwargs['extra_context']['object'] = person

    return object_list(request, **kwargs)


@never_cache
def person_events_list(request, slug, **kwargs):
    """
    Lists the person's events
    """
    user = get_object_or_404(User, username=slug)
    person = user.profile
    kwargs['queryset'] = kwargs['queryset'].filter(
        models.Q(organizing_person=person)
        | models.Q(creator=user)
    ).order_by('-creation_date')
    kwargs.setdefault("extra_context", {})
    kwargs['extra_context']['object'] = person
    kwargs['title'] = _("Events by %s") % person.get_title()
    return event_list(request, show="related", **kwargs)


@never_cache
def person_events_list_ical(request, slug, **kwargs):
    return person_events_list(request, slug, ical=True, **kwargs)


@never_cache
def person_events_list_feed(request, slug, **kwargs):
    return person_events_list(request, slug, feed=True, **kwargs)


@never_cache
def person_job_offer_list(request, slug, **kwargs):
    """
    Lists the person's job offers
    """
    user = get_object_or_404(User, username=slug)
    person = user.profile
    kwargs['queryset'] = kwargs['queryset'].filter(
        contact_person=person,
    ).order_by('-creation_date')
    kwargs.setdefault("extra_context", {})
    kwargs['extra_context']['object'] = person
    kwargs['title'] = _("Job offers by %s") % person.get_title()
    return job_offer_list(request, show="related", **kwargs)


@never_cache
def person_job_offer_list_feed(request, slug, **kwargs):
    return person_job_offer_list(request, slug, feed=True, **kwargs)

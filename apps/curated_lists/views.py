# -*- coding: UTF-8 -*-
from django.contrib.contenttypes.models import ContentType
from hashids import Hashids
from django.db import models
from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse

from jetson.apps.utils.decorators import login_required
from jetson.apps.utils.views import object_list

from base_libs.views.views import access_denied


from .forms import CuratedListForm, CuratedListFilterForm
from .models import CuratedList


def curated_list_detail(request, token, **kwargs):
    """
    Displays the list of favorite objects
    """
    hashids = Hashids(min_length=6)

    try:
        curated_list_id = hashids.decode(token)[0]
    except IndexError:
        raise Http404

    try:
        curated_list = CuratedList.objects.filter(pk=curated_list_id)[0]
    except IndexError:
        raise Http404

    other_curated_lists = []
    if curated_list.is_featured:
        other_curated_lists = CuratedList.objects.filter(is_featured=True).exclude(pk=curated_list_id)

    return render(request, "curated_lists/curated_list_detail.html", {
        'curated_list': curated_list,
        'other_curated_lists': other_curated_lists,
    })


@login_required
def change_curated_list(request, token, **kwargs):
    """
    Displays the list of favorite objects
    """
    hashids = Hashids(min_length=6)

    try:
        curated_list_id = hashids.decode(token)[0]
    except IndexError:
        raise Http404

    try:
        curated_list = CuratedList.objects.filter(pk=curated_list_id)[0]
    except IndexError:
        raise Http404

    if request.user != curated_list.user and not request.user.is_staff:
        return access_denied(request)

    if request.method == "POST":
        form = CuratedListForm(data=request.POST, instance=curated_list)
        if form.is_valid():
            opts = form.save(commit=False)
            opts.save()
            return render(request, "curated_lists/change_curated_list_done.html", {})

    else:
        form = CuratedListForm(instance=curated_list)

    return render(request, "curated_lists/change_curated_list.html", {
        'form': form,
        'curated_list': curated_list,
    })


def featured_curated_lists(request, **kwargs):
    qs = CuratedList.objects.filter(is_featured=True)
    form = CuratedListFilterForm(data=request.GET)

    facets = {
        'selected': {},
        'categories': {
            'owners': form.fields['owner'].queryset,
            'categories': form.fields['category'].queryset,
        },
    }

    if form.is_valid():
        owner = form.cleaned_data.get("owner")
        if owner:
            facets['selected']['owner'] = owner
            qs = qs.filter(
                listowner__owner_content_type=owner.content_type,
                listowner__owner_object_id=owner.object_id,
            )
        cat = form.cleaned_data.get("category")
        if cat:
            facets['selected']['category'] = cat
            qs = qs.filter(
                categories__tree_id=cat.tree_id,
            )

    context = {
        'facets': facets,
        'object_list': qs,
        'form': form,
    }

    kwargs['template_name'] = "curated_lists/featured_curated_lists.html"
    kwargs['queryset'] = qs.distinct()

    extra_context = kwargs.setdefault("extra_context", {})
    extra_context['form'] = form
    extra_context['facets'] = facets

    return object_list(request, **kwargs)


@login_required
def user_curated_lists_json(request):
    """
    Returns a list of curated lists created by the currently logged in user or their institutions

    If content_type_id and object_id are passed as query parameters,
    also checks each list if an item with that content_type_id and object_id exists in that list.

    :param request:
    :return: Example: [
        {
            "owner": {"id": 123, "title": "Joe Smith", "type": "person"}
            "lists": [
                {"token": "sdfgbyx", "title": "Best Companies", "item_included": false}, 
                {"token": "nbyasf", "title": "Best Galleries", "item_included": true}]
        },
        {
            "owner": {"id": 124, "title": "Joe & Co", "type": "institution"}
            "lists": [
                {"token": "sdfbsdf", "title": "Geniuses", "item_included": false},
                {"token": "dfbddss", "title": "Best Galleries", "item_included": false}]
        },
        {
            "owner": {"id": 124, "title": "The Smiths", "type": "institution"}
            "lists": [
                {"token": "bjdfsms", "title": "Favorites", "item_included": false}
            ]
        },
    ]
    """
    item_content_type = item_object_id = None
    if request.GET:
        item_content_type = ContentType.objects.get(pk=request.GET.get('content_type_id'))
        item_object_id = request.GET.get('object_id')
    data = []
    data_item = {}
    person = request.user.profile
    data_item['owner'] = {
        'id': person.pk,
        'title': person.get_title(),
        'type': 'people.person',
    }
    curated_lists = CuratedList.objects.filter(
        listowner__owner_content_type=ContentType.objects.get_for_model(person),
        listowner__owner_object_id=person.pk,
    )
    if item_content_type and item_object_id:
        curated_lists = curated_lists.annotate(
            item_included=models.Sum(
                models.Case(
                    models.When(
                        listitem__content_type=item_content_type,
                        listitem__object_id=item_object_id,
                        then=1,
                    ),
                    default=0,
                    output_field=models.IntegerField()
                )
            )
        )
    data_item['lists'] = [{
        'token': curated_list.get_token(),
        'title': curated_list.title,
        'item_included': bool(getattr(curated_list, "item_included", False)),
    } for curated_list in curated_lists]
    data.append(data_item)

    for contact in person.individualcontact_set.exclude(institution=None).only("institution"):
        data_item = {}
        institution = contact.institution
        curated_lists = CuratedList.objects.filter(
            listowner__owner_content_type=ContentType.objects.get_for_model(institution),
            listowner__owner_object_id=institution.pk,
        )
        if item_content_type and item_object_id:
            curated_lists = curated_lists.annotate(
                item_included=models.Sum(
                    models.Case(
                        models.When(
                            listitem__content_type=item_content_type,
                            listitem__object_id=item_object_id,
                            then=1,
                        ),
                        default=0,
                        output_field=models.IntegerField()
                    )
                )
            )
        data_item['owner'] = {
            'id': institution.pk,
            'title': institution.get_title(),
            'type': 'institutions.institution',
        }
        data_item['lists'] = [{
            'token': curated_list.get_token(),
            'title': curated_list.title,
            'item_included': bool(getattr(curated_list, "item_included", False)),
        } for curated_list in curated_lists]
        data.append(data_item)

    return JsonResponse(data, safe=False)


@login_required
def add_user_curated_list_json(request):
    data = {}
    return JsonResponse(data)


@login_required
def change_user_curated_list_json(request, token):
    data = {}
    return JsonResponse(data)


@login_required
def delete_user_curated_list_json(request, token):
    data = {}
    return JsonResponse(data)

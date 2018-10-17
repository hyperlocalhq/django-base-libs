# -*- coding: UTF-8 -*-
from django.contrib.contenttypes.models import ContentType
from django import forms
from django.db import models
from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse

from jetson.apps.utils.decorators import login_required
from jetson.apps.utils.views import object_list

from base_libs.views.views import access_denied


from .forms import (
    CuratedListForm, CuratedListItemForm, CuratedListFilterForm, OwnerInvitationForm,
    CuratedListDeletionForm, CuratedListItemRemovalForm, CuratedListOwnerRemovalForm
)
from .models import CuratedList


def curated_list_detail(request, token, **kwargs):
    """
    Displays the list of favorite objects
    """
    curated_list = CuratedList.objects.get_by_token(token=token)
    if not curated_list:
        raise Http404

    other_curated_lists = []
    if curated_list.is_featured:
        other_curated_lists = CuratedList.objects.filter(is_featured=True).exclude(pk=curated_list.pk)

    editable = curated_list.is_editable(user=request.user)

    return render(request, "curated_lists/curated_list_detail.html", {
        'curated_list': curated_list,
        'other_curated_lists': other_curated_lists,
        'editable': editable,
    })


@login_required
def change_curated_list(request, token, **kwargs):
    """
    Displays the list of favorite objects
    """
    curated_list = CuratedList.objects.get_by_token(token=token)
    if not curated_list:
        raise Http404

    if not curated_list.is_editable(user=request.user):
        return access_denied(request)

    if request.method == "POST":
        form = CuratedListForm(request=request, instance=curated_list, data=request.POST)
        if form.is_valid():
            opts = form.save(commit=False)
            opts.save()
            return redirect('curated_list_detail', token=token)

    else:
        form = CuratedListForm(request=request, instance=curated_list)

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


### JSON views ###

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
    if request.method == "POST":
        form = CuratedListForm(request=request, instance=None, data=request.POST)
        if form.is_valid():
            curated_list = form.save()
            data = {
                'success': True,
                'token': curated_list.get_token(),
                'title': curated_list.title,
                'description': curated_list.description,
            }
            return JsonResponse(data)
        data = {
            'success': False,
            'errors': form.errors,
        }
        return JsonResponse(data)
    data = {}
    return JsonResponse(data)


@login_required
def change_user_curated_list_json(request, token):
    curated_list = CuratedList.objects.get_by_token(token=token)
    if not curated_list:
        raise Http404

    if not curated_list.is_editable(user=request.user):
        return access_denied(request)

    if request.method == "POST":
        form = CuratedListForm(request=request, instance=curated_list, data=request.POST)
        if form.is_valid():
            curated_list = form.save()
            data = {
                'success': True,
                'token': curated_list.get_token(),
                'title': curated_list.title,
                'description': curated_list.description,
            }
            return JsonResponse(data)
        data = {
            'success': False,
            'errors': form.errors,
        }
        return JsonResponse(data)
    data = {
        'token': curated_list.get_token(),
        'title': curated_list.title,
        'description': curated_list.description,
    }
    return JsonResponse(data)


@login_required
def delete_user_curated_list_json(request, token):
    curated_list = CuratedList.objects.get_by_token(token=token)
    if not curated_list:
        raise Http404

    if request.method == "POST":
        curated_list.delete()

    data = {
        'success': True,
    }
    return JsonResponse(data)


### Editing of curated lists, items, and owners ###

@login_required
def delete_curated_list(request, token):
    curated_list = CuratedList.objects.get_by_token(token=token)
    if not curated_list:
        raise Http404

    if not curated_list.is_editable(user=request.user):
        return access_denied(request)

    if request.method == 'POST':
        form = CuratedListDeletionForm(curated_list=curated_list, data=request.POST)
        if form.is_valid():
            form.delete()
            return redirect('featured_curated_lists')
    else:
        form = CuratedListDeletionForm(curated_list=curated_list)

    return render(request, "curated_lists/delete_curated_list.html", {
        'curated_list': curated_list,
        'form': form,
    })


@login_required
def change_curated_list_item(request, token, item_id):
    curated_list = CuratedList.objects.get_by_token(token=token)
    if not curated_list:
        raise Http404

    if not curated_list.is_editable(user=request.user):
        return access_denied(request)

    try:
        item = curated_list.listitem_set.filter(pk=item_id)[0]
    except IndexError:
        raise Http404

    if request.method == 'POST':
        form = CuratedListItemForm(instance=item, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("curated_list_details", token=token)
    else:
        form = CuratedListItemForm(instance=item)

    return render(request, "curated_lists/change_curated_list_item.html", {
        'curated_list': curated_list,
        'form': form,
    })


@login_required
def remove_curated_list_item(request, token, item_id):
    curated_list = CuratedList.objects.get_by_token(token=token)
    if not curated_list:
        raise Http404

    if not curated_list.is_editable(user=request.user):
        return access_denied(request)

    try:
        item = curated_list.listitem_set.filter(pk=item_id)[0]
    except IndexError:
        raise Http404

    if request.method == 'POST':
        form = CuratedListItemRemovalForm(curated_list=curated_list, item=item, data=request.POST)
        if form.is_valid():
            form.remove()
            return redirect('curated_list_detail', token=token)
    else:
        form = CuratedListItemRemovalForm(curated_list=curated_list, item=item)

    return render(request, "curated_lists/remove_curated_list_item.html", {
        'curated_list': curated_list,
        'form': form,
    })


@login_required
def curated_list_owners(request, token):
    curated_list = CuratedList.objects.get_by_token(token=token)
    if not curated_list:
        raise Http404

    if not curated_list.is_editable(user=request.user):
        return access_denied(request)

    return render(request, "curated_lists/curated_list_owners.html", {
        'curated_list': curated_list,
    })


@login_required
def invite_curated_list_owner(request, token):
    curated_list = CuratedList.objects.get_by_token(token=token)
    if not curated_list:
        raise Http404

    if not curated_list.is_editable(user=request.user):
        return access_denied(request)

    if request.method == 'POST':
        form = OwnerInvitationForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # TODO: do the saving and notification
            return redirect("curated_list_owners", token=token)
    else:
        form = OwnerInvitationForm()

    return render(request, "curated_lists/invite_curated_list_owner.html", {
        'curated_list': curated_list,
        'form': form,
    })


@login_required
def remove_curated_list_owner(request, token, owner_id):
    curated_list = CuratedList.objects.get_by_token(token=token)
    if not curated_list:
        raise Http404

    if not curated_list.is_editable(user=request.user):
        return access_denied(request)

    try:
        owner = curated_list.listowner_set.filter(pk=owner_id)[0]
    except IndexError:
        raise Http404

    if request.method == 'POST':
        form = CuratedListOwnerRemovalForm(curated_list=curated_list, owner=owner, data=request.POST)
        if form.is_valid():
            form.remove()
            return redirect('curated_list_owners', token=token)
    else:
        form = CuratedListOwnerRemovalForm(curated_list=curated_list, owner=owner)

    return render(request, "curated_lists/remove_curated_list_owner.html", {
        'curated_list': curated_list,
        'form': form,
    })

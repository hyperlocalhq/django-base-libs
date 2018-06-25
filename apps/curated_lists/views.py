# -*- coding: UTF-8 -*-
from hashids import Hashids
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404

from jetson.apps.utils.decorators import login_required

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


def featured_curated_lists(request):
    qs = CuratedList.objects.filter(is_featured=True)
    form = CuratedListFilterForm(data=request.GET)
    if form.is_valid():
        pass

    context = {
        'object_list': qs,
        'form': form,
    }

    return render(request, "curated_lists/featured_curated_lists.html", context)
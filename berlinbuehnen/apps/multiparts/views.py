# -*- coding: UTF-8 -*-
# -*- coding: utf-8 -*-
import os
import shutil
from datetime import datetime, date, timedelta

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from django.views.decorators.cache import never_cache
from django.db import models

from base_libs.views.views import access_denied

from jetson.apps.utils.views import object_list, object_detail
from jetson.apps.utils.views import get_abc_list
from jetson.apps.utils.views import filter_abc
from jetson.apps.utils.context_processors import prev_next_processor
from jetson.apps.utils.decorators import login_required

FRONTEND_LANGUAGES = getattr(settings, "FRONTEND_LANGUAGES", settings.LANGUAGES)

from berlinbuehnen.apps.locations.models import Location

from .forms import ParentForm, PartFormset
from .models import Parent, Part


class EventFilterForm(forms.Form):
    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        required=False,
    )


def multipart_list(request, year=None, month=None, day=None):
    #qs = Parent.objects.filter(production__status="published")
    qs = Parent.objects.all()

    form = EventFilterForm(data=request.REQUEST)

    facets = {
        'selected': {},
        'categories': {
            'locations': Location.objects.all(),
        },
    }

    if form.is_valid():
        cat = form.cleaned_data['location']
        if cat:
            facets['selected']['location'] = cat
            qs = qs.filter(
                models.Q(production__in_program_of=cat) |
                models.Q(production__play_locations=cat)
            ).distinct()


    abc_filter = request.GET.get('abc', None)
    if abc_filter:
        facets['selected']['abc'] = abc_filter
    abc_list = get_abc_list(qs, "production__title_%s" % request.LANGUAGE_CODE, abc_filter)
    if abc_filter:
        qs = filter_abc(qs, "production__title_%s" % request.LANGUAGE_CODE, abc_filter)

    extra_context = {}
    extra_context['form'] = form
    extra_context['abc_list'] = abc_list
    extra_context['facets'] = facets

    return object_list(
        request,
        queryset=qs,
        template_name="multiparts/multipart_list.html",
        paginate_by=24,
        extra_context=extra_context,
        httpstate_prefix="multipart_list",
        context_processors=(prev_next_processor,),
    )


@never_cache
@login_required
def add_multipart(request):
    if not request.user.has_perm("multiparts.add_parent"):
        return access_denied(request)

    if request.REQUEST.get('reset'):
        return redirect("dashboard")

    if request.method == "POST":
        form = ParentForm(data=request.POST)
        part_formset = PartFormset(
            data=request.POST,
            prefix="parts",
        )

        if form.is_valid() and part_formset.is_valid():
            multipart = form.save(commit=False)
            multipart.save()
            form.save_m2m()

            ids_to_keep = []
            for frm in part_formset.forms:
                if (
                    frm.has_changed()
                    and hasattr(frm, "cleaned_data")
                    and not frm.cleaned_data.get('DELETE', False)
                ):
                    # frm.instance = multipart
                    obj = frm.save(commit=False)
                    obj.parent = multipart
                    obj.save()
                    ids_to_keep.append(obj.pk)
            multipart.part_set.exclude(pk__in=ids_to_keep).delete()

            if not multipart.get_owners():
                multipart.set_owner(request.user)

            return redirect("dashboard")
    else:
        form = ParentForm()
        part_formset = PartFormset(
            prefix="parts",
        )

    return render(request, "multiparts/forms/multipart_form.html", {
        'form': form,
        'formsets': {
            'parts': part_formset,
        },
    })


def change_multipart(request, slug):
    parent = get_object_or_404(Parent, production__slug=slug)
    if not parent.is_editable():
        return access_denied(request)

    if request.REQUEST.get('reset'):
        return redirect("dashboard")

    if request.method == "POST":
        form = ParentForm(data=request.POST, instance=parent)
        part_formset = PartFormset(
            data=request.POST,
            prefix="parts",
            instance=parent,
        )

        if form.is_valid() and part_formset.is_valid():
            parent = form.save(commit=False)
            parent.save()
            form.save_m2m()

            ids_to_keep = []
            for frm in part_formset.forms:
                if (
                    frm.has_changed()
                    and hasattr(frm, "cleaned_data")
                    and not frm.cleaned_data.get('DELETE', False)
                ):
                    obj = frm.save()
                    ids_to_keep.append(obj.pk)
            parent.part_set.exclude(pk__in=ids_to_keep).delete()

            return redirect("dashboard")
    else:
        form = ParentForm(instance=parent)
        part_formset = PartFormset(
            prefix="parts",
            instance=parent,
            initial=[{
                'id': part.pk,
                'sort_order': part.sort_order,
                'production': part.production,
            } for part in parent.part_set.all()],
        )

    return render(request, "multiparts/forms/multipart_form.html", {
        'multipart': parent,
        'form': form,
        'formsets': {
            'parts': part_formset,
        },
    })


@never_cache
@login_required
def delete_multipart(request, slug):
    parent = get_object_or_404(Parent, production__slug=slug)
    if not parent.is_deletable():
        return access_denied(request)
    if request.method == "POST" and request.is_ajax():
        parent.delete()
        return HttpResponse("OK")
    return redirect("dashboard")

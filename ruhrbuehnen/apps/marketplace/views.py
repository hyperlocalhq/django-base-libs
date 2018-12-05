# -*- coding: utf-8 -*-
import os
import shutil
from datetime import datetime

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.views.decorators.cache import never_cache
from django.db import models
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect

from base_libs.views.views import access_denied

from jetson.apps.utils.views import object_list, object_detail
from jetson.apps.utils.views import get_abc_list
from jetson.apps.utils.views import filter_abc
from jetson.apps.utils.context_processors import prev_next_processor
from jetson.apps.utils.views import show_form_step
from jetson.apps.utils.decorators import login_required

FRONTEND_LANGUAGES = getattr(settings, "FRONTEND_LANGUAGES", settings.LANGUAGES)

from .models import JobOffer, JobType, JobCategory
from .models import SECURITY_SUMMAND

from .forms import JobOfferForm

from jetson.apps.image_mods.models import FileManager
from filebrowser.models import FileDescription


class JobOfferFilterForm(forms.Form):
    categories = forms.ModelMultipleChoiceField(
        required=False,
        queryset=JobCategory.objects.all(),
    )
    job_type = forms.ModelChoiceField(
        required=False,
        queryset=JobType.objects.all(),
    )


def job_offer_list(request, year=None, month=None, day=None):
    from ruhrbuehnen.apps.advertising.templatetags.advertising_tags import not_empty_ad_zone
    qs = JobOffer.objects.filter(status="published").filter(
        models.Q(deadline=None) | models.Q(deadline__gte=datetime.today())
    )
    qs = qs.filter(status="published").filter(
        models.Q(start_contract_on=None) |
        models.Q(start_contract_on__gte=datetime.today())
    )

    form = JobOfferFilterForm(data=request.REQUEST)

    facets = {
        'selected': {},
        'categories':
            {
                'categories': JobCategory.objects.all(),
                'job_types': JobType.objects.all(),
            },
    }

    abc_list = get_abc_list(qs, "position_%s" % request.LANGUAGE_CODE)

    if form.is_valid():
        cats = form.cleaned_data['categories']
        if cats:
            facets['selected']['categories'] = cats
            qs = qs.filter(categories__in=cats, ).distinct()

        job_type = form.cleaned_data['job_type']
        if job_type:
            facets['selected']['job_type'] = job_type
            qs = qs.filter(job_type=job_type, ).distinct()

    abc_filter = request.GET.get('abc', None)
    if abc_filter:
        facets['selected']['abc'] = abc_filter
        for letter in abc_filter:
            qs = filter_abc(qs, "position_%s" % request.LANGUAGE_CODE, letter)

    # qs = qs.extra(select={
    #     'title_uni': "IF (events_event.title_%(lang_code)s = '', events_event.title_de, events_event.title_%(lang_code)s)" % {
    #         'lang_code': request.LANGUAGE_CODE,
    #     }
    # }).order_by("title_uni")

    #qs = qs.prefetch_related("season_set", "mediafile_set", "categories", "accessibility_options").defer("tags")

    qs = qs.order_by("deadline")

    extra_context = {'form': form, 'abc_list': abc_list, 'facets': facets}

    first_page_delta = 0
    if not_empty_ad_zone('marketplace'):
        first_page_delta = 1
        extra_context['show_ad'] = True

    return object_list(
        request,
        queryset=qs,
        template_name="marketplace/job_offer_list.html",
        paginate_by=24,
        extra_context=extra_context,
        httpstate_prefix="job_offer_list",
        context_processors=(prev_next_processor, ),
        first_page_delta=first_page_delta,
    )


def job_offer_detail(request, secure_id):
    secure_id = int(secure_id)
    if "preview" in request.REQUEST:
        qs = JobOffer.objects.all()
        obj = get_object_or_404(qs, pk=secure_id - SECURITY_SUMMAND)
        if not obj.is_editable():
            return access_denied(request)
    else:
        qs = JobOffer.objects.filter(status__in=("published", "not_listed"))
    return object_detail(
        request,
        queryset=qs,
        object_id=secure_id - SECURITY_SUMMAND,
        template_name="marketplace/job_offer_detail.html",
        context_processors=(prev_next_processor, ),
    )


@never_cache
@login_required
def add_job_offer(request):
    if not request.user.has_perm("marketplace.add_joboffer"):
        return access_denied(request)

    if request.method == "POST":
        form = JobOfferForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.status = "published"
            instance.save()
            form.save_m2m()
            instance.set_owner(request.user)
            return redirect("dashboard")
    else:
        form = JobOfferForm()
    return render(
        request, "marketplace/forms/basic_info_form.html", {"form": form}
    )


@never_cache
@login_required
def change_job_offer(request, secure_id):
    secure_id = int(secure_id)
    instance = get_object_or_404(JobOffer, pk=secure_id - SECURITY_SUMMAND)
    if not instance.is_editable():
        return access_denied(request)

    if request.method == "POST":
        form = JobOfferForm(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save()
            return redirect("dashboard")
    else:
        form = JobOfferForm(instance=instance)
    return render(
        request, "marketplace/forms/basic_info_form.html", {
            "form": form,
            "job_offer": instance
        }
    )


@never_cache
@login_required
def delete_job_offer(request, secure_id):
    secure_id = int(secure_id)
    instance = get_object_or_404(JobOffer, pk=secure_id - SECURITY_SUMMAND)
    if not instance.is_deletable():
        return access_denied(request)
    if request.method == "POST" and request.is_ajax():
        instance.status = "trashed"
        instance.save()
        return HttpResponse("OK")
    return redirect(instance.get_url_path())


@never_cache
@login_required
def change_job_offer_status(request, secure_id):
    secure_id = int(secure_id)
    instance = get_object_or_404(JobOffer, pk=secure_id - SECURITY_SUMMAND)
    if not instance.is_editable():
        return access_denied(request)
    if request.method == "POST" and request.is_ajax(
    ) and request.POST['status'] in ("draft", "published", "not_listed"):
        instance.status = request.POST['status']
        instance.save()
        return HttpResponse("OK")
    return redirect(instance.get_url_path())

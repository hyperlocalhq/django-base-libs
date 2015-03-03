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
from django.core.urlresolvers import reverse

from base_libs.views.views import access_denied

from jetson.apps.utils.views import object_list, object_detail
from jetson.apps.utils.views import get_abc_list
from jetson.apps.utils.views import filter_abc
from jetson.apps.utils.context_processors import prev_next_processor
from jetson.apps.utils.views import show_form_step
from jetson.apps.utils.decorators import login_required

FRONTEND_LANGUAGES = getattr(settings, "FRONTEND_LANGUAGES", settings.LANGUAGES)

from berlinbuehnen.apps.productions.forms.productions import PRODUCTION_FORM_STEPS
from berlinbuehnen.apps.productions.forms.gallery import VideoForm, VideoDeletionForm
from berlinbuehnen.apps.productions.forms.gallery import StreamingForm, StreamingDeletionForm
from berlinbuehnen.apps.productions.forms.gallery import ImageForm, ImageDeletionForm
from berlinbuehnen.apps.productions.forms.gallery import PDFForm, PDFDeletionForm
from berlinbuehnen.apps.productions.forms.events import AddEventsForm
from berlinbuehnen.apps.productions.forms.events import BasicInfoForm as EventBasicInfoForm
from berlinbuehnen.apps.productions.forms.events import DescriptionForm as EventDescriptionForm, EventLeadershipFormset, EventAuthorshipFormset, EventInvolvementFormset, SocialMediaChannelFormset, SponsorFormset
from berlinbuehnen.apps.productions.forms.events import GalleryForm

from jetson.apps.image_mods.models import FileManager
from filebrowser.models import FileDescription

from berlinbuehnen.apps.locations.models import Location
from berlinbuehnen.apps.sponsors.models import Sponsor
from berlinbuehnen.apps.productions.models import Production, ProductionImage
from berlinbuehnen.apps.productions.models import Event, ProductionVideo, ProductionLiveStream, EventImage, ProductionPDF
from berlinbuehnen.apps.productions.models import EventLeadership, EventAuthorship, EventInvolvement, EventSocialMediaChannel


class EventFilterForm(forms.Form):
    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        required=False,
    )


def event_list(request, year=None, month=None, day=None):
    #qs = Event.objects.filter(production__status="published")
    qs = Event.objects.all()

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
                models.Q(play_locations=cat) |
                models.Q(production__play_locations=cat)
            ).distinct()


    abc_filter = request.GET.get('abc', None)
    if abc_filter:
        facets['selected']['abc'] = abc_filter
    abc_list = get_abc_list(qs, "production__title_%s" % request.LANGUAGE_CODE, abc_filter)
    if abc_filter:
        qs = filter_abc(qs, "production__title_%s" % request.LANGUAGE_CODE, abc_filter)

    # qs = qs.extra(select={
    #     'title_uni': "IF (events_event.title_%(lang_code)s = '', events_event.title_de, events_event.title_%(lang_code)s)" % {
    #         'lang_code': request.LANGUAGE_CODE,
    #     }
    # }).order_by("title_uni")

    #qs = qs.prefetch_related("season_set", "mediafile_set", "categories", "accessibility_options").defer("tags")
    
    extra_context = {}
    extra_context['form'] = form
    extra_context['abc_list'] = abc_list
    extra_context['facets'] = facets

    return object_list(
        request,
        queryset=qs,
        template_name="events/event_list.html",
        paginate_by=24,
        extra_context=extra_context,
        httpstate_prefix="event_list",
        context_processors=(prev_next_processor,),
    )


def event_detail(request, slug, event_id):
    if "preview" in request.REQUEST:
        qs = Event.objects.all()
        obj = get_object_or_404(qs, production__slug=slug, pk=event_id)
        if not request.user.has_perm("events.change_event", obj):
            return access_denied(request)
    else:
        #qs = Event.objects.filter(production__status="published")
        qs = Event.objects.all()
    return object_detail(
        request,
        queryset=qs,
        object_id=event_id,
        template_name="events/event_detail.html",
        context_processors=(prev_next_processor,),
    )


@never_cache
@login_required
def add_production(request):
    if not request.user.has_perm("productions.add_production"):
        return access_denied(request)
    return show_form_step(request, PRODUCTION_FORM_STEPS, extra_context={});


@never_cache
@login_required
def change_production(request, slug):
    instance = get_object_or_404(Production, slug=slug)
    if not request.user.has_perm("productions.change_production", instance):
        return access_denied(request)
    return show_form_step(request, PRODUCTION_FORM_STEPS, extra_context={'production': instance}, instance=instance);


@never_cache
@login_required
def delete_production(request, slug):
    instance = get_object_or_404(Production, slug=slug)
    if not request.user.has_perm("productions.delete_production", instance):
        return access_denied(request)
    if request.method == "POST" and request.is_ajax():
        instance.status = "trashed"
        instance.save()
        return HttpResponse("OK")
    return redirect(instance.get_url_path())


@never_cache
@login_required
def change_production_status(request, slug):
    instance = get_object_or_404(Production, slug=slug)
    if not request.user.has_perm("productions.change_production", instance):
        return access_denied(request)
    if request.method == "POST" and request.is_ajax() and request.POST['status'] in ("draft", "published", "not_listed"):
        instance.status = request.POST['status']
        instance.save()
        return HttpResponse("OK")
    return redirect(instance.get_url_path())

### EVENTS MANAGEMENT ###

@never_cache
@login_required
def events_overview(request, slug):
    production = get_object_or_404(Production, slug=slug)
    if not request.user.has_perm("productions.change_production", production):
        return access_denied(request)

    return render(request, "productions/events/overview.html", {'production': production})


@never_cache
@login_required
def add_events(request, slug):
    production = get_object_or_404(Production, slug=slug)
    if not request.user.has_perm("productions.change_production", production):
        return access_denied(request)

    if request.REQUEST.get('reset'):
        return redirect(reverse("change_production", kwargs={'slug': production.slug}) + '?step=4')

    if request.method == "POST":
        form = AddEventsForm(production, data=request.POST)
        if form.is_valid():
            # create new events
            form.save()
            return redirect(reverse("change_production", kwargs={'slug': production.slug}) + '?step=4')
    else:
        form = AddEventsForm(production)

    return render(request, "productions/events/add_events.html", {'production': production, 'form': form})


@never_cache
@login_required
def change_event_basic_info(request, slug, event_id):
    production = get_object_or_404(Production, slug=slug)
    event = get_object_or_404(Event, pk=event_id, production=production)
    if not request.user.has_perm("productions.change_production", production):
        return access_denied(request)

    if request.REQUEST.get('reset'):
        return redirect(reverse("change_production", kwargs={'slug': production.slug}) + '?step=4')

    if request.method == "POST":
        form = EventBasicInfoForm(data=request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect(reverse("change_production", kwargs={'slug': production.slug}) + '?step=4')
    else:
        form = EventBasicInfoForm(instance=event)

    return render(request, "productions/events/basic_info_form.html", {'production': production, 'event': event, 'form': form})


@never_cache
@login_required
def change_event_description(request, slug, event_id):
    production = get_object_or_404(Production, slug=slug)
    event = get_object_or_404(Event, pk=event_id, production=production)
    if not request.user.has_perm("productions.change_production", production):
        return access_denied(request)

    if request.REQUEST.get('reset'):
        return redirect(reverse("change_production", kwargs={'slug': production.slug}) + '?step=4')

    if request.method == "POST":
        form = EventDescriptionForm(data=request.POST, instance=event)
        leadership_formset = EventLeadershipFormset(
            data=request.POST,
            prefix="leaderships",
            instance=event,
        )
        authorship_formset = EventAuthorshipFormset(
            data=request.POST,
            prefix="authorships",
            instance=event,
        )
        involvement_formset = EventInvolvementFormset(
            data=request.POST,
            prefix="involvements",
            instance=event,
        )
        social_formset = SocialMediaChannelFormset(
            data=request.POST,
            prefix="social",
            instance=event,
        )
        sponsor_formset = SponsorFormset(
            data=request.POST,
            prefix="sponsors",
            initial=[s.__dict__ for s in Sponsor.objects.filter(event=event)],
        )

        if form.is_valid() and leadership_formset.is_valid() and authorship_formset.is_valid() and involvement_formset.is_valid() and social_formset.is_valid() and sponsor_formset.is_valid():
            # save description fields
            event = form.save(commit=False)
            event.save()
            form.save_m2m()

            ids_to_keep = []
            for frm in leadership_formset.forms:
                if (
                    hasattr(frm, "cleaned_data")
                    and not frm.cleaned_data.get('DELETE', False)
                ):
                    obj = frm.save()
                    ids_to_keep.append(obj.pk)
            event.eventleadership_set.exclude(pk__in=ids_to_keep).delete()

            ids_to_keep = []
            for frm in authorship_formset.forms:
                if (
                    hasattr(frm, "cleaned_data")
                    and not frm.cleaned_data.get('DELETE', False)
                ):
                    obj = frm.save()
                    ids_to_keep.append(obj.pk)
            event.eventauthorship_set.exclude(pk__in=ids_to_keep).delete()

            ids_to_keep = []
            for frm in involvement_formset.forms:
                if (
                    hasattr(frm, "cleaned_data")
                    and not frm.cleaned_data.get('DELETE', False)
                ):
                    obj = frm.save()
                    ids_to_keep.append(obj.pk)
            event.eventinvolvement_set.exclude(pk__in=ids_to_keep).delete()

            ids_to_keep = []
            for frm in social_formset.forms:
                if (
                    hasattr(frm, "cleaned_data")
                    and not frm.cleaned_data.get('DELETE', False)
                ):
                    obj = frm.save()
                    ids_to_keep.append(obj.pk)
            event.eventsocialmediachannel_set.exclude(pk__in=ids_to_keep).delete()

            event.sponsors.clear()
            for frm in sponsor_formset.forms:
                if (
                    hasattr(frm, "cleaned_data")
                    and not frm.cleaned_data.get('DELETE', False)
                ):
                    obj = frm.save(commit=False)
                    sponsor_dict = frm.cleaned_data
                    if sponsor_dict['id']:
                        # ensure that image is saved to the updated instance
                        sponsor = Sponsor.objects.get(pk=sponsor_dict['id'])
                        obj.id = sponsor_dict['id']
                        obj.image = sponsor.image
                    if sponsor_dict['media_file_path'] and obj.image:
                        # delete the old file
                        try:
                            FileManager.delete_file(obj.image.path)
                        except OSError:
                            pass
                    rel_dir = "sponsors/"
                    if sponsor_dict['media_file_path']:
                        tmp_path = sponsor_dict['media_file_path']
                        abs_tmp_path = os.path.join(settings.MEDIA_ROOT, tmp_path)

                        fname, fext = os.path.splitext(tmp_path)
                        filename = datetime.now().strftime("%Y%m%d%H%M%S") + fext
                        dest_path = "".join((rel_dir, filename))
                        FileManager.path_exists(os.path.join(settings.MEDIA_ROOT, rel_dir))
                        abs_dest_path = os.path.join(settings.MEDIA_ROOT, dest_path)

                        shutil.copy2(abs_tmp_path, abs_dest_path)

                        os.remove(abs_tmp_path)
                        obj.image = dest_path
                        sponsor_dict['media_file_path'] = u""

                    obj.save()
                    event.sponsors.add(obj)

            return redirect(reverse("change_production", kwargs={'slug': production.slug}) + '?step=4')
    else:
        form = EventDescriptionForm(instance=event)

        initial = [{
            'id': obj.id,
            'person': obj.person,
            'function_de': obj.function_de,
            'function_en': obj.function_en,
            'sort_order': obj.sort_order,
        } for obj in EventLeadership.objects.filter(event=event)]
        leadership_formset = EventLeadershipFormset(
            prefix="leaderships",
            instance=event,
            initial=initial,
        )
        initial = [{
            'id': obj.id,
            'person': obj.person,
            'authorship_type': obj.authorship_type,
            'sort_order': obj.sort_order,
        } for obj in EventAuthorship.objects.filter(event=event)]
        authorship_formset = EventAuthorshipFormset(
            prefix="authorships",
            instance=event,
            initial=initial,
        )
        initial = [{
            'id': obj.id,
            'person': obj.person,
            'involvement_type': obj.involvement_type,
            'involvement_role_de': obj.involvement_role_de,
            'involvement_role_en': obj.involvement_role_en,
            'involvement_instrument_de': obj.involvement_instrument_de,
            'involvement_instrument_en': obj.involvement_instrument_en,
            'sort_order': obj.sort_order,
        } for obj in EventInvolvement.objects.filter(event=event)]
        involvement_formset = EventInvolvementFormset(
            prefix="involvements",
            instance=event,
            initial=initial,
        )

        initial = [{
            'id': obj.id,
            'channel_type': obj.channel_type,
            'url': obj.url,
        } for obj in EventSocialMediaChannel.objects.filter(event=event)]
        social_formset = SocialMediaChannelFormset(
            prefix="social",
            instance=event,
            initial=initial,
        )

        sponsors = list(Sponsor.objects.filter(event=event))
        initial = []
        for obj in sponsors:
            initial.append({
                'id': obj.id,
                'title_de': obj.title_de,
                'title_en': obj.title_en,
                'website': obj.website,
            })
        sponsor_formset = SponsorFormset(
            prefix="sponsors",
            initial=initial,
        )
        for obj, frm in zip(sponsors, sponsor_formset.forms):
            frm.instance = obj

    return render(request, "productions/events/description_form.html", {
        'production': production,
        'event': event,
        'form': form,
        'formsets': {
            'leaderships': leadership_formset,
            'authorships': authorship_formset,
            'involvements': involvement_formset,
            'social': social_formset,
            'sponsors': sponsor_formset,
        }
    })


@never_cache
@login_required
def change_event_gallery(request, slug, event_id):
    production = get_object_or_404(Production, slug=slug)
    event = get_object_or_404(Event, pk=event_id, production=production)
    if not request.user.has_perm("productions.change_production", production):
        return access_denied(request)

    if request.REQUEST.get('reset'):
        return redirect(reverse("change_production", kwargs={'slug': production.slug}) + '?step=4')

    if request.method == "POST":
        # TODO: exchange the form with some gallery form
        form = GalleryForm(data=request.POST, instance=event)
        if form.is_valid():
            return redirect(reverse("change_production", kwargs={'slug': production.slug}) + '?step=4')
    else:
        form = GalleryForm(instance=event)

    return render(request, "productions/events/gallery_form.html", {'production': production, 'event': event, 'form': form})


@never_cache
@login_required
def delete_event(request, slug, event_id):
    production = get_object_or_404(Production, slug=slug)
    event = get_object_or_404(Event, pk=event_id, production=production)
    if not request.user.has_perm("productions.delete_event", event):
        return access_denied(request)
    if request.method == "POST" and request.is_ajax():
        event.delete()
        return HttpResponse("OK")
    return redirect(reverse("change_production", kwargs={'slug': production.slug}) + '?step=4')

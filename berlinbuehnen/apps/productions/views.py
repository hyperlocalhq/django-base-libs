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
from jetson.apps.utils.views import show_form_step
from jetson.apps.utils.decorators import login_required

FRONTEND_LANGUAGES = getattr(settings, "FRONTEND_LANGUAGES", settings.LANGUAGES)

from forms.production import PRODUCTION_FORM_STEPS
from forms.gallery import ImageFileForm, ImageDeletionForm
from forms.events import AddEventsForm
from forms.events import BasicInfoForm as EventBasicInfoForm
from forms.events import DescriptionForm as EventDescriptionForm
from forms.events import EventLeadershipFormset, EventAuthorshipFormset, EventInvolvementFormset, SponsorFormset

from jetson.apps.image_mods.models import FileManager
from filebrowser.models import FileDescription

from berlinbuehnen.apps.locations.models import Location
from models import Production, ProductionImage, Event


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


### MEDIA FILE MANAGEMENT ###


def update_mediafile_ordering(tokens, production):
    # tokens is in this format:
    # "<mediafile1_token>,<mediafile2_token>,<mediafile3_token>"
    mediafiles = []
    for mediafile_token in tokens.split(u","):
        mediafile = get_object_or_404(
            ProductionImage,
            production=production,
            pk=ProductionImage.token_to_pk(mediafile_token)
        )
        mediafiles.append(mediafile)
    sort_order = 0
    for mediafile in mediafiles:
        mediafile.sort_order = sort_order
        mediafile.save()
        sort_order += 1


@never_cache
@login_required
def gallery_overview(request, slug):
    instance = get_object_or_404(Production, slug=slug)
    if not request.user.has_perm("productions.change_production", instance):
        return access_denied(request)

    if "ordering" in request.POST and request.is_ajax():
        tokens = request.POST['ordering']
        update_mediafile_ordering(tokens, instance)
        return HttpResponse("OK")

    return render(request, "productions/gallery/overview.html", {'production': instance})


@never_cache
@login_required
def create_update_mediafile(request, slug, mediafile_token="", media_file_type="", **kwargs):
    instance = get_object_or_404(Production, slug=slug)
    if not request.user.has_perm("productions.change_production", instance):
        return access_denied(request)

    media_file_type = media_file_type or "image"
    if media_file_type not in ("image",):
        raise Http404

    if not "extra_context" in kwargs:
        kwargs["extra_context"] = {}

    rel_dir = "productions/%s/" % instance.slug

    filters = {}
    if mediafile_token:
        media_file_obj = get_object_or_404(
            ProductionImage,
            production=instance,
            pk=ProductionImage.token_to_pk(mediafile_token),
        )
    else:
        media_file_obj = None

    form_class = ImageFileForm

    if request.method == "POST":
        # just after submitting data
        form = form_class(media_file_obj, request.POST, request.FILES)
        if form.is_valid():
            cleaned = form.cleaned_data
            path = ""
            if media_file_obj and media_file_obj.path:
                path = media_file_obj.path.path
            if cleaned.get("media_file_path", None):
                if path:
                    # delete the old file
                    try:
                        FileManager.delete_file(path)
                    except OSError:
                        pass
                    path = ""

            if not media_file_obj:
                media_file_obj = ProductionImage(
                    production=instance
                )
            media_file_obj.copyright_restrictions = cleaned['copyright_restrictions']

            media_file_path = ""
            if cleaned.get("media_file_path", None):
                tmp_path = cleaned['media_file_path']
                abs_tmp_path = os.path.join(settings.MEDIA_ROOT, tmp_path)

                fname, fext = os.path.splitext(tmp_path)
                filename = datetime.now().strftime("%Y%m%d%H%M%S") + fext
                dest_path = "".join((rel_dir, filename))
                FileManager.path_exists(os.path.join(settings.MEDIA_ROOT, rel_dir))
                abs_dest_path = os.path.join(settings.MEDIA_ROOT, dest_path)

                shutil.copy2(abs_tmp_path, abs_dest_path)

                os.remove(abs_tmp_path);
                media_file_obj.path = media_file_path = dest_path
                media_file_obj.save()


            from filebrowser.base import FileObject

            try:
                file_description = FileDescription.objects.filter(
                    file_path=FileObject(media_file_path or path),
                ).order_by("pk")[0]
            except:
                file_description = FileDescription(file_path=media_file_path or path)

            for lang_code, lang_name in FRONTEND_LANGUAGES:
                setattr(file_description, 'title_%s' % lang_code, cleaned['title_%s' % lang_code])
                setattr(file_description, 'description_%s' % lang_code, cleaned['description_%s' % lang_code])
            setattr(file_description, 'author', cleaned['author'])
            #setattr(file_description, 'copyright_limitations', cleaned['copyright_limitations'])

            file_description.save()

            if not media_file_obj.pk:
                media_file_obj.sort_order = ProductionImage.objects.filter(
                    production=instance,
                ).count()
            else:
                # trick not to reorder media files on save
                media_file_obj.sort_order = media_file_obj.sort_order
            media_file_obj.save()

            if "hidden_iframe" in request.REQUEST:
                return render(
                    request,
                    "productions/gallery/success.html",
                    {},
                )
            else:
                if cleaned['goto_next']:
                    return redirect(cleaned['goto_next'])
                else:
                    return redirect("production_gallery_overview", slug=instance.slug)
    else:
        if media_file_obj:
            # existing media file
            try:
                file_description = FileDescription.objects.filter(
                    file_path=media_file_obj.path,
                ).order_by("pk")[0]
            except:
                file_description = FileDescription(file_path=media_file_obj.path)
            initial = {}
            initial.update(media_file_obj.__dict__)
            initial.update(file_description.__dict__)
            form = form_class(media_file_obj, initial=initial)
        else:
            # new media file
            form = form_class(media_file_obj)

    form.helper.form_action = request.path + "?hidden_iframe=1"

    base_template = "base.html"
    if "hidden_iframe" in request.REQUEST:
        base_template = "base_iframe.html"

    context_dict = {
        'base_template': base_template,
        'media_file': media_file_obj,
        'media_file_type': media_file_type,
        'form': form,
        'production': instance,
    }

    return render(
        request,
        "productions/gallery/create_update_mediafile.html",
        context_dict,
    )


@never_cache
@login_required
def delete_mediafile(request, slug, mediafile_token="", **kwargs):
    instance = get_object_or_404(Production, slug=slug)
    if not request.user.has_perm("productions.change_production", instance):
        return access_denied(request)

    filters = {
        'id': ProductionImage.token_to_pk(mediafile_token),
    }
    if instance:
        filters['production'] = instance
    try:
        media_file_obj = ProductionImage.objects.get(**filters)
    except:
        raise Http404

    if "POST" == request.method:
        form = ImageDeletionForm(request.POST)
        if media_file_obj:
            if media_file_obj.path:
                try:
                    FileManager.delete_file(media_file_obj.path.path)
                except OSError:
                    pass
                FileDescription.objects.filter(
                    file_path=media_file_obj.path,
                ).delete()
            media_file_obj.delete()

            return HttpResponse("OK")
    else:
        form = ImageDeletionForm()

    form.helper.form_action = request.path

    context_dict = {
        'media_file': media_file_obj,
        'form': form,
        'production': instance,
    }

    return render(
        request,
        "locations/gallery/delete_mediafile.html",
        context_dict,
    )


### EVENTS MANAGEMENT ###

@never_cache
@login_required
def events_overview(request, slug):
    instance = get_object_or_404(Production, slug=slug)
    if not request.user.has_perm("productions.change_production", instance):
        return access_denied(request)

    return render(request, "productions/events/overview.html", {'production': instance})


@never_cache
@login_required
def add_events(request, slug):
    instance = get_object_or_404(Production, slug=slug)
    if not request.user.has_perm("productions.change_production", instance):
        return access_denied(request)

    if request.method == "POST":
        form = AddEventsForm(data=request.POST)
        if form.is_valid():
            # TODO: create new events
            return redirect(instance.get_url_path())
    else:
        form = AddEventsForm()

    return render(request, "productions/events/add_events.html", {'production': instance, 'form': form})


@never_cache
@login_required
def change_event_basic_info(request, slug, event_id):
    production = get_object_or_404(Production, slug=slug)
    event = get_object_or_404(Event, pk=event_id, production=production)
    if not request.user.has_perm("productions.change_production", production):
        return access_denied(request)

    if request.method == "POST":
        form = EventBasicInfoForm(data=request.POST, instance=event)
        if form.is_valid():
            # TODO: save basic info fields
            return redirect(production.get_url_path())
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

    if request.method == "POST":
        form = EventDescriptionForm(data=request.POST, instance=event)
        leadership_formset = EventLeadershipFormset(data=request.POST, prefix="leaderships")
        authorship_formset = EventAuthorshipFormset(data=request.POST, prefix="authorships")
        involvement_formset = EventInvolvementFormset(data=request.POST, prefix="involvements")
        sponsor_formset = SponsorFormset(data=request.POST, prefix="sponsors")

        if form.is_valid() and leadership_formset.is_valid() and authorship_formset.is_valid() and involvement_formset.is_valid() and sponsor_formset.is_valid():
            # TODO: save description fields
            return redirect(production.get_url_path())
    else:
        form = EventDescriptionForm(instance=event)
        leadership_formset = EventLeadershipFormset(prefix="leaderships")
        authorship_formset = EventAuthorshipFormset(prefix="authorships")
        involvement_formset = EventInvolvementFormset(prefix="involvements")
        sponsor_formset = SponsorFormset(prefix="sponsors")

    return render(request, "productions/events/description_form.html", {
        'production': production,
        'event': event,
        'form': form,
        'formsets': {
            'leaderships': leadership_formset,
            'authorships': authorship_formset,
            'involvements': involvement_formset,
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

    if request.method == "POST":
        # TODO: exchange the form with some gallery form
        form = EventDescriptionForm(data=request.POST, instance=event)
        if form.is_valid():
            return redirect(production.get_url_path())
    else:
        form = EventDescriptionForm(instance=event)

    return render(request, "productions/events/gallery_form.html", {'production': production, 'event': event, 'form': form})

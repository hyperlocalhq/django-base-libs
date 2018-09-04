# -*- coding: utf-8 -*-
import os
import shutil
import json
from datetime import datetime, date, timedelta

from django.db import models
from django.http import HttpResponse
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from django.http import Http404

from base_libs.forms import dynamicforms
from base_libs.utils.misc import ExtendedJSONEncoder
from base_libs.utils.misc import get_related_queryset
from base_libs.utils.html import decode_entities
from base_libs.views.views import access_denied

from jetson.apps.utils.decorators import login_required
from jetson.apps.utils.views import object_list, object_detail
from jetson.apps.utils.views import get_abc_list
from jetson.apps.utils.views import filter_abc
from jetson.apps.utils.views import show_form_step
from jetson.apps.utils.context_processors import prev_next_processor

EventCategory = models.get_model("events", "EventCategory")
Event = models.get_model("events", "Event")
MediaFile = models.get_model("events", "MediaFile")

FRONTEND_LANGUAGES = getattr(settings, "FRONTEND_LANGUAGES", settings.LANGUAGES) 

from forms.event import EVENT_FORM_STEPS, BatchEventTimeForm
from forms.gallery import ImageFileForm, ImageDeletionForm

from jetson.apps.image_mods.models import FileManager
from filebrowser.models import FileDescription

CALENDAR_CHOICES = (
    ('today', _("Today")),
    ('tomorrow', _("Tomorrow")),
    ('within_7_days', _("7 Days")),
    ('within_30_days', _("30 Days")),
)


class EventFilterForm(dynamicforms.Form):
    category = forms.ModelChoiceField(
        required=False,
        queryset=get_related_queryset(Event, "categories"),
        to_field_name="slug",
    )
    suitable_for_children = forms.BooleanField(
        required=False,
    )
    free_admission = forms.BooleanField(
        required=False,
    )
    calendar = forms.ChoiceField(
        choices=CALENDAR_CHOICES,
        required=False,
    )
    selected_date = forms.DateField(
        required=False,
    )


def event_list(request):
    # qs = Event.objects.filter(status="published").extra(
    #     select={'no_closest_event_date': 'closest_event_date IS NULL'},
    #     order_by=["no_closest_event_date", "closest_event_date", "closest_event_time", "title_%s" % request.LANGUAGE_CODE],
    # )
    qs = Event.objects.filter(status="published").annotate(
        null_date=models.Count("closest_event_date")
    ).order_by("-null_date", "closest_event_date", "closest_event_time", "title_%s" % request.LANGUAGE_CODE)

    #if not request.REQUEST.keys():
    #    return redirect("/%s%s?status=newly_opened" % (request.LANGUAGE_CODE, request.path))
    
    form = EventFilterForm(data=request.REQUEST)
    
    facets = {
        'selected': {},
        'categories': {
            'categories': get_related_queryset(Event, "categories"),
            'suitable_for_children': _("Also suitable for children"),
            'free_admission': _("Free admission"),
            'calendar': CALENDAR_CHOICES,
        },
    }

    # status = None
    if form.is_valid():
        cat = form.cleaned_data['category']
        if cat:
            facets['selected']['category'] = cat
            qs = qs.filter(
                categories=cat,
            ).distinct()
        suitable_for_children = form.cleaned_data['suitable_for_children']
        if suitable_for_children:
            facets['selected']['suitable_for_children'] = True
            qs = qs.filter(
                suitable_for_children=True,
            )
        free_admission = form.cleaned_data['free_admission']
        if free_admission:
            facets['selected']['free_admission'] = True
            qs = qs.filter(
                free_admission=True,
            )
        cat = form.cleaned_data['calendar']
        if cat:
            facets['selected']['calendar'] = (cat, dict(CALENDAR_CHOICES)[cat])
            today = date.today()
            if cat == "today":
                qs = qs.filter(
                    eventtime__event_date=today,
                )
            if cat == "tomorrow":
                tomorrow = today + timedelta(days=1)
                qs = qs.filter(
                    eventtime__event_date=tomorrow,
                )
            if cat == "within_7_days":
                selected_start = today
                selected_end = selected_start + timedelta(days=7)
                qs = qs.filter(
                    eventtime__event_date__gte=selected_start,
                    eventtime__event_date__lte=selected_end,
                )
            if cat == "within_30_days":
                selected_start = today
                selected_end = selected_start + timedelta(days=30)
                qs = qs.filter(
                    eventtime__event_date__gte=selected_start,
                    eventtime__event_date__lte=selected_end,
                )
        selected_start = None
        selected_date = form.cleaned_data['selected_date']
        if selected_date:
            facets['selected']['selected_date'] = selected_date
            selected_start = selected_date

        if selected_start:
            qs = qs.filter(
                eventtime__event_date=selected_start,
            )

    qs = qs.distinct()

    abc_filter = request.GET.get('abc', None)
    if abc_filter:
        facets['selected']['abc'] = abc_filter
    abc_list = get_abc_list(qs, "title_%s" % request.LANGUAGE_CODE, abc_filter)
    if abc_filter:
        qs = filter_abc(qs, "title_%s" % request.LANGUAGE_CODE, abc_filter)

    #qs = qs.select_related("museum").defer("tags")

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
        httpstate_prefix="event_list_map",
        context_processors=(prev_next_processor,),
    )


def event_list_map(request):
    qs = Event.objects.filter(status="published").annotate(
        null_date=models.Count("closest_event_date")
    ).order_by("-null_date", "closest_event_date", "closest_event_time", "title_%s" % request.LANGUAGE_CODE)

    #if not request.REQUEST.keys():
    #    return redirect("/%s%s?status=newly_opened" % (request.LANGUAGE_CODE, request.path))

    form = EventFilterForm(data=request.REQUEST)

    facets = {
        'selected': {},
        'categories': {
            'categories': get_related_queryset(Event, "categories"),
            'suitable_for_children': _("Also suitable for children"),
            'free_admission': _("Free admission"),
            'calendar': CALENDAR_CHOICES,
        },
    }

    # status = None
    if form.is_valid():
        cat = form.cleaned_data['category']
        if cat:
            facets['selected']['category'] = cat
            qs = qs.filter(
                categories=cat,
            ).distinct()
        suitable_for_children = form.cleaned_data['suitable_for_children']
        if suitable_for_children:
            facets['selected']['suitable_for_children'] = True
            qs = qs.filter(
                suitable_for_children=True,
            )
        free_admission = form.cleaned_data['free_admission']
        if free_admission:
            facets['selected']['free_admission'] = True
            qs = qs.filter(
                free_admission=True,
            )
        cat = form.cleaned_data['calendar']
        if cat:
            facets['selected']['calendar'] = (cat, dict(CALENDAR_CHOICES)[cat])
            today = date.today()
            if cat == "today":
                qs = qs.filter(
                    eventtime__event_date=today,
                )
            if cat == "tomorrow":
                tomorrow = today + timedelta(days=1)
                qs = qs.filter(
                    eventtime__event_date=tomorrow,
                )
            if cat == "within_7_days":
                selected_start = today
                selected_end = selected_start + timedelta(days=7)
                qs = qs.filter(
                    eventtime__event_date__gte=selected_start,
                    eventtime__event_date__lte=selected_end,
                )
            if cat == "within_30_days":
                selected_start = today
                selected_end = selected_start + timedelta(days=30)
                qs = qs.filter(
                    eventtime__event_date__gte=selected_start,
                    eventtime__event_date__lte=selected_end,
                )

    qs = qs.distinct()

    abc_filter = request.GET.get('abc', None)
    if abc_filter:
        facets['selected']['abc'] = abc_filter
    abc_list = get_abc_list(qs, "title_%s" % request.LANGUAGE_CODE, abc_filter)
    if abc_filter:
        qs = filter_abc(qs, "title_%s" % request.LANGUAGE_CODE, abc_filter)

    extra_context = {}
    extra_context['form'] = form
    extra_context['abc_list'] = abc_list
    extra_context['facets'] = facets

    return object_list(
        request,
        queryset=qs,
        template_name="events/event_list_map.html",
        paginate_by=200,
        extra_context=extra_context,
        httpstate_prefix="event_list",
        context_processors=(prev_next_processor,),
    )


def event_detail(request, slug):
    if "preview" in request.REQUEST:
        qs = Event.objects.all()
        obj = get_object_or_404(qs, slug=slug)
        if not request.user.has_perm("events.change_event", obj):
            return access_denied(request)
    else:
        qs = Event.objects.filter(status="published")
        
    form = EventFilterForm(data=request.REQUEST)
    
    if form.is_valid():
        selected_date = form.cleaned_data['selected_date']

    extra_context = {}
    extra_context['selected_date'] = selected_date
    
    return object_detail(
        request,
        queryset=qs,
        slug=slug,
        slug_field="slug",
        template_name="events/event_detail.html",
        extra_context=extra_context,
        context_processors=(prev_next_processor,),
    )


def event_detail_ajax(request, slug, template_name="events/event_detail_ajax.html"):
    if "preview" in request.REQUEST:
        qs = Event.objects.all()
        obj = get_object_or_404(qs, slug=slug)
        if not request.user.has_perm("events.change_event", obj):
            return access_denied(request)
    else:
        qs = Event.objects.filter(status="published")
    return object_detail(
        request,
        queryset=qs,
        slug=slug,
        slug_field="slug",
        template_name=template_name,
        context_processors=(prev_next_processor,),
    )


def event_detail_slideshow(request, slug):
    if "preview" in request.REQUEST:
        qs = Event.objects.all()
        obj = get_object_or_404(qs, slug=slug)
        if not request.user.has_perm("events.change_event", obj):
            return access_denied(request)
    else:
        qs = Event.objects.filter(status="published")
    return object_detail(
        request,
        queryset=qs,
        slug=slug,
        slug_field="slug",
        template_name="events/event_detail_slideshow.html",
        context_processors=(prev_next_processor,),
    )


def event_products(request, slug):
    qs = Event.objects.all()
    obj = get_object_or_404(qs, slug=slug)

    qs = obj.get_related_products()

    extra_context = {
        'object': obj,
    }
    return object_list(
        request,
        queryset=qs,
        template_name="events/event_products.html",
        paginate_by=24,
        extra_context=extra_context,
        httpstate_prefix="event_%s_products" % obj.pk,
        context_processors=(prev_next_processor,),
    )


@never_cache
@login_required
def add_event(request):
    if not request.user.has_perm("events.add_event"):
        return access_denied(request)
    return show_form_step(request, EVENT_FORM_STEPS, extra_context={});


@never_cache
@login_required
def change_event(request, slug):
    instance = get_object_or_404(Event, slug=slug)
    if not request.user.has_perm("events.change_event", instance):
        return access_denied(request)
    return show_form_step(request, EVENT_FORM_STEPS, extra_context={'event': instance}, instance=instance);


@never_cache
@login_required
def delete_event(request, slug):
    instance = get_object_or_404(Event, slug=slug)
    if not request.user.has_perm("events.delete_event", instance):
        return access_denied(request)
    if request.method == "POST" and request.is_ajax():
        instance.status = "trashed"
        instance.save()
        return HttpResponse("OK")
    return redirect(instance.get_url_path())


@never_cache
@login_required
def batch_event_times(request, slug):
    weekdays = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    instance = get_object_or_404(Event, slug=slug)
    if request.method == "POST" and request.is_ajax():
        form = BatchEventTimeForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            d1 = cleaned['range_start']
            ## start with the first Monday after this date
            #while d1.weekday() != 0:
            #    d1 = d1 + timedelta(days=1)
            d2 = cleaned['range_end']
            delta = d2 - d1
            event_times = []
            week_count = 0
            for i in range(delta.days + 1):
                d = d1 + timedelta(days=i)
                wd = d.weekday()
                
                is_closing_day = False
                if instance.museum:
                    is_closing_day = bool(instance.museum.specialopeningtime_set.filter(
                        models.Q(yyyy__isnull=True) | models.Q(yyyy=d.year), mm=d.month, dd=d.day, is_closed=True
                    ))
                    try:
                        is_closing_day = is_closing_day or not getattr(instance.museum.season_set.filter(
                            start__lte=d, end__gte=d
                        )[0], '%s_open' % weekdays[wd])
                    except:
                        pass
                
                if (cleaned['repeat'] == "1" or week_count % 2 == 0) and not is_closing_day:
                    start_time = cleaned['%s_start' % weekdays[wd]]
                    if start_time:
                        start_time = start_time.strftime("%H:%M")
                    
                    end_time = cleaned['%s_end' % weekdays[wd]]
                    if end_time:
                        end_time = end_time.strftime("%H:%M")
                    
                    if start_time:
                        event_times.append({
                            'event_date': d.strftime("%d.%m.%Y"),
                            'start': start_time,
                            'end': end_time,
                            })
                if wd == 6:
                    week_count += 1
            return HttpResponse(json.dumps(event_times))
        return HttpResponse(json.dumps([]))
    return redirect(instance.get_url_path())


@never_cache
@login_required
def change_event_status(request, slug):
    instance = get_object_or_404(Event, slug=slug)
    if not request.user.has_perm("events.change_event", instance):
        return access_denied(request)
    if request.method == "POST" and request.is_ajax():
        instance.status = request.POST['status']
        instance.save()
        return HttpResponse("OK")
    return redirect(instance.get_url_path())
    

### MEDIA FILE MANAGEMENT ###


def update_mediafile_ordering(tokens, event):
    # tokens is in this format:
    # "<mediafile1_token>,<mediafile2_token>,<mediafile3_token>"
    mediafiles = []
    for mediafile_token in tokens.split(u","):
        mediafile = get_object_or_404(
            MediaFile,
            event=event,
            pk=MediaFile.token_to_pk(mediafile_token)
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
    instance = get_object_or_404(Event, slug=slug)
    if not request.user.has_perm("events.change_event", instance):
        return access_denied(request)

    if "ordering" in request.POST and request.is_ajax():
        tokens = request.POST['ordering']
        update_mediafile_ordering(tokens, instance)
        return HttpResponse("OK")

    return render(request, "events/gallery/overview.html", {'event': instance})


@never_cache
@login_required
def create_update_mediafile(request, slug, mediafile_token="", media_file_type="", **kwargs):
    instance = get_object_or_404(Event, slug=slug)
    if not request.user.has_perm("events.change_event", instance):
        return access_denied(request)
    
    media_file_type = media_file_type or "image"
    if media_file_type not in ("image",):
        raise Http404
    
    if not "extra_context" in kwargs:
        kwargs["extra_context"] = {}

    rel_dir = "events/%s/" % instance.slug
    
    filters = {}
    if mediafile_token:
        media_file_obj = get_object_or_404(
            MediaFile,
            event=instance,
            pk=MediaFile.token_to_pk(mediafile_token),
        )
    else:
        media_file_obj = None
    
    form_class = ImageFileForm

    if request.method=="POST":
        # just after submitting data
        form = form_class(media_file_obj, request.POST, request.FILES)
        # Passing request.FILES to the form always breaks the form validation
        # WHY!?? As a workaround, let's validate just the POST and then 
        # manage FILES separately. 
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
                media_file_obj = MediaFile(
                    event=instance
                )
                    
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
            setattr(file_description, 'copyright_limitations', cleaned['copyright_limitations'])

            file_description.save()
            
            if not media_file_obj.pk:
                media_file_obj.sort_order = MediaFile.objects.filter(
                    event=instance,
                    ).count()
            else:
                # trick not to reorder media files on save
                media_file_obj.sort_order = media_file_obj.sort_order
            media_file_obj.save()
            
            if "hidden_iframe" in request.REQUEST:
                return render(
                    request,
                    "events/gallery/success.html",
                    {},
                )
            else:
                if cleaned['goto_next']:
                    return redirect(cleaned['goto_next'])
                else:
                    return redirect("event_gallery_overview", slug=instance.slug)
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
        'event': instance,
    }
    
    return render(
        request,
        "events/gallery/create_update_mediafile.html",
        context_dict,
    )


@never_cache
@login_required
def delete_mediafile(request, slug, mediafile_token="", **kwargs):
    instance = get_object_or_404(Event, slug=slug)
    if not request.user.has_perm("events.change_event", instance):
        return access_denied(request)
    
    filters = {
        'id': MediaFile.token_to_pk(mediafile_token),
    }
    if instance:
        filters['event'] = instance
    try:
        media_file_obj = MediaFile.objects.get(**filters)
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
        'event': instance,
    }
    
    return render(
        request,
        "events/gallery/delete_mediafile.html",
        context_dict,
    )


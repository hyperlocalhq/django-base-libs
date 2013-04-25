# -*- coding: utf-8 -*-
import os
import shutil
from datetime import datetime, date, timedelta

from django.db import models
from django.http import HttpResponse
from django import forms
from django.utils import simplejson
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from django.http import Http404

from base_libs.templatetags.base_tags import decode_entities
from base_libs.forms import dynamicforms
from base_libs.utils.misc import ExtendedJSONEncoder
from base_libs.utils.misc import get_related_queryset
from base_libs.views.views import access_denied

from jetson.apps.utils.decorators import login_required
from jetson.apps.utils.views import object_list, object_detail
from jetson.apps.utils.views import get_abc_list
from jetson.apps.utils.views import filter_abc
from jetson.apps.utils.views import show_form_step
from jetson.apps.utils.context_processors import prev_next_processor

WorkshopCategory = models.get_model("workshops", "WorkshopCategory")
Workshop = models.get_model("workshops", "Workshop")
MediaFile = models.get_model("workshops", "MediaFile")

FRONTEND_LANGUAGES = getattr(settings, "FRONTEND_LANGUAGES", settings.LANGUAGES) 

from forms.workshop import WORKSHOP_FORM_STEPS, BatchWorkshopTimeForm
from forms.gallery import ImageFileForm, ImageDeletionForm

from jetson.apps.image_mods.models import FileManager
from filebrowser.models import FileDescription

STATUS_CHOICES = (
    ("newly_opened", _("Newly opened")),
    ("closing_soon", _("Closing soon")),
    )

class WorkshopSearchForm(dynamicforms.Form):
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        )

def workshop_list(request):
    qs = Workshop.objects.filter(status="published")
    
    #if not request.REQUEST.keys():
    #    return redirect("/%s%s?status=newly_opened" % (request.LANGUAGE_CODE, request.path))
    
    form = WorkshopSearchForm(data=request.REQUEST)
    
    facets = {
        'selected': {},
        'categories': {
            'statuses': STATUS_CHOICES,
            },
        }

    status = None
    if form.is_valid():
        status = form.cleaned_data['status']
        if status:
            facets['selected']['status'] = status
            today = date.today()
            two_weeks = timedelta(days=14)
            if status == "newly_opened":
                # today - 2 weeks < WORKSHOP START <= today
                qs = qs.filter(
                    workshoptime__workshop_date__gt=today-two_weeks,
                    workshoptime__workshop_date__lte=today,
                    )
            elif status == "closing_soon":
                # today <= WORKSHOP END < today + two weeks
                qs = qs.filter(
                    workshoptime__workshop_date__gte=today,
                    workshoptime__workshop_date__lt=today+two_weeks,
                    )
    #if status == "closing_soon":
    #    qs = qs.order_by("workshoptime__workshop_date", "title_%s" % request.LANGUAGE_CODE)
    #else:
    #    qs = qs.order_by("-workshoptime__workshop_date", "title_%s" % request.LANGUAGE_CODE)
        
    qs = qs.order_by("closest_workshop_date", "closest_workshop_time", "title_%s" % request.LANGUAGE_CODE)

    qs = qs.distinct()
    
    abc_filter = request.GET.get('by-abc', None)
    abc_list = get_abc_list(qs, "title", abc_filter)
    if abc_filter:
        qs = filter_abc(qs, "title", abc_filter)
        
    extra_context = {}
    extra_context['form'] = form
    extra_context['abc_list'] = abc_list
    extra_context['facets'] = facets

    return object_list(
        request,
        queryset=qs,
        template_name="workshops/workshop_list.html",
        paginate_by=200,
        extra_context=extra_context,
        httpstate_prefix="workshop_list",
        context_processors=(prev_next_processor,),
        )

def workshop_detail(request, slug):
    if "preview" in request.REQUEST:
        qs = Workshop.objects.all()
        obj = get_object_or_404(qs, slug=slug)
        if not request.user.has_perm("workshops.change_workshop", obj):
            return access_denied(request)
    else:
        qs = Workshop.objects.filter(status="published")
    return object_detail(
        request,
        queryset=qs,
        slug=slug,
        slug_field="slug",
        template_name="workshops/workshop_detail.html",
        context_processors=(prev_next_processor,),
        )

@never_cache
@login_required
def add_workshop(request):
    if not request.user.has_perm("workshops.add_workshop"):
        return access_denied(request)
    return show_form_step(request, WORKSHOP_FORM_STEPS, extra_context={});
    
@never_cache
@login_required
def change_workshop(request, slug):
    instance = get_object_or_404(Workshop, slug=slug)
    if not request.user.has_perm("workshops.change_workshop", instance):
        return access_denied(request)
    return show_form_step(request, WORKSHOP_FORM_STEPS, extra_context={'workshop': instance}, instance=instance);

@never_cache
@login_required
def delete_workshop(request, slug):
    instance = get_object_or_404(Workshop, slug=slug)
    if not request.user.has_perm("workshops.delete_workshop", instance):
        return access_denied(request)
    if request.method == "POST" and request.is_ajax():
        instance.status = "trashed"
        instance.save()
        return HttpResponse("OK")
    return redirect(instance.get_url_path())

@never_cache
@login_required
def batch_workshop_times(request, slug):
    weekdays = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    instance = get_object_or_404(Workshop, slug=slug)
    if request.method == "POST" and request.is_ajax():
        form = BatchWorkshopTimeForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            d1 = cleaned['range_start']
            # start with the first Monday after this date
            while d1.weekday() != 0:
                d1 = d1 + timedelta(days=1)
            d2 = cleaned['range_end']
            delta = d2 - d1
            workshop_times = []
            week_count = 0
            for i in range(delta.days + 1):
                d = d1 + timedelta(days=i)
                wd = d.weekday()
                
                is_closing_day = False
                if instance.museum:
                    is_closing_day = bool(instance.museum.specialopeningtime_set.filter(
                        models.Q(yyyy=None) | models.Q(yyyy=d.year), mm=d.month, dd=d.day, is_closed=True
                        ))
                
                if (cleaned['repeat'] == 1 or week_count % 2 == 0) and not is_closing_day:
                    start_time = cleaned['%s_start' % weekdays[wd]]
                    if start_time:
                        start_time = start_time.strftime("%H:%M")
                    
                    end_time = cleaned['%s_end' % weekdays[wd]]
                    if end_time:
                        end_time = end_time.strftime("%H:%M")
                    
                    if start_time:
                        workshop_times.append({
                            'workshop_date': d.strftime("%Y-%m-%d"),
                            'start': start_time,
                            'end': end_time,
                            })
                if wd == 6:
                    week_count += 1
            return HttpResponse(simplejson.dumps(workshop_times))
        return HttpResponse(simplejson.dumps([]))
    return redirect(instance.get_url_path())

@never_cache
@login_required
def change_workshop_status(request, slug):
    instance = get_object_or_404(Workshop, slug=slug)
    if not request.user.has_perm("workshops.change_workshop", instance):
        return access_denied(request)
    if request.method == "POST" and request.is_ajax():
        instance.status = request.POST['status']
        instance.save()
        return HttpResponse("OK")
    return redirect(instance.get_url_path())

### MEDIA FILE MANAGEMENT ###

def update_mediafile_ordering(tokens, workshop):
    # tokens is in this format:
    # "<mediafile1_token>,<mediafile2_token>,<mediafile3_token>"
    mediafiles = []
    for mediafile_token in tokens.split(u","):
        mediafile = get_object_or_404(
            MediaFile,
            workshop=workshop,
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
    instance = get_object_or_404(Workshop, slug=slug)
    if not request.user.has_perm("workshops.change_workshop", instance):
        return access_denied(request)

    if "ordering" in request.POST and request.is_ajax():
        tokens = request.POST['ordering']
        update_mediafile_ordering(tokens, instance)
        return HttpResponse("OK")

    return render(request, "workshops/gallery/overview.html", {'workshop': instance})
    
@never_cache
@login_required
def create_update_mediafile(request, slug, mediafile_token="", media_file_type="", **kwargs):
    instance = get_object_or_404(Workshop, slug=slug)
    if not request.user.has_perm("workshops.change_workshop", instance):
        return access_denied(request)
    
    media_file_type = media_file_type or "image"
    if media_file_type not in ("image",):
        raise Http404
    
    if not "extra_context" in kwargs:
        kwargs["extra_context"] = {}

    rel_dir = "workshops/%s/" % instance.slug
    
    filters = {}
    if mediafile_token:
        media_file_obj = get_object_or_404(
            MediaFile,
            workshop=instance,
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
                    workshop=instance
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

            file_description.save()
            
            if not media_file_obj.pk:
                media_file_obj.sort_order = MediaFile.objects.filter(
                    workshop=instance,
                    ).count()
            else:
                # trick not to reorder media files on save
                media_file_obj.sort_order = media_file_obj.sort_order
            media_file_obj.save()
            
            if "hidden_iframe" in request.REQUEST:
                return render(
                    request,
                    "workshops/gallery/success.html",
                    {},
                    )
            else:
                if cleaned['goto_next']:
                    return redirect(cleaned['goto_next'])
                else:
                    return redirect("workshop_gallery_overview", slug=instance.slug)
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
        'workshop': instance,
        }
    
    return render(
        request,
        "workshops/gallery/create_update_mediafile.html",
        context_dict,
        )

@never_cache
@login_required
def delete_mediafile(request, slug, mediafile_token="", **kwargs):
    instance = get_object_or_404(Workshop, slug=slug)
    if not request.user.has_perm("workshops.change_workshop", instance):
        return access_denied(request)
    
    filters = {
        'id': MediaFile.token_to_pk(mediafile_token),
        }
    if instance:
        filters['workshop'] = instance
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
        'workshop': instance,
        }
    
    return render(
        request,
        "workshops/gallery/delete_mediafile.html",
        context_dict,
        )


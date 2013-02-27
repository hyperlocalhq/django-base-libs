# -*- coding: utf-8 -*-
import os
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

from base_libs.templatetags.base_tags import decode_entities
from base_libs.forms import dynamicforms
from base_libs.utils.misc import ExtendedJSONEncoder
from base_libs.utils.misc import get_related_queryset
from base_libs.views.views import access_denied

from jetson.apps.utils.decorators import login_required
from jetson.apps.utils.views import object_list, object_detail
from jetson.apps.utils.views import show_form_step
from jetson.apps.utils.context_processors import prev_next_processor

WorkshopCategory = models.get_model("workshops", "WorkshopCategory")
Workshop = models.get_model("workshops", "Workshop")
MediaFile = models.get_model("workshops", "MediaFile")

FRONTEND_LANGUAGES = getattr(settings, "FRONTEND_LANGUAGES", settings.LANGUAGES) 

from forms.workshop import WORKSHOP_FORM_STEPS
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
    if status == "closing_soon":
        qs = qs.order_by("workshoptime__workshop_date", "title_%s" % request.LANGUAGE_CODE)
    else:
        qs = qs.order_by("-workshoptime__workshop_date", "title_%s" % request.LANGUAGE_CODE)
        
    extra_context = {}
    extra_context['form'] = form
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
    return show_form_step(request, WORKSHOP_FORM_STEPS, extra_context={});
    
@never_cache
@login_required
def change_workshop(request, slug):
    instance = get_object_or_404(Workshop, slug=slug)
    if not request.user.has_perm("workshops.change_workshop", instance):
        return access_denied(request)
    return show_form_step(request, WORKSHOP_FORM_STEPS, extra_context={'workshop': instance}, instance=instance);


### MEDIA FILE MANAGEMENT ###

def update_mediafile_ordering(tokens, museum):
    # tokens is in this format:
    # "<mediafile1_token>,<mediafile2_token>,<mediafile3_token>"
    mediafiles = []
    for mediafile_token in tokens.split(u","):
        mediafile = get_object_or_404(
            MediaFile,
            museum=museum,
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

    rel_dir = "workshops/%s/gallery/" % instance.slug
    
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
        form = form_class(request.POST, request.FILES)
        # Passing request.FILES to the form always breaks the form validation
        # WHY!?? As a workaround, let's validate just the POST and then 
        # manage FILES separately. 
        if not media_file_obj and ("media_file" not in request.FILES):
            # new media file - media file required
            form.fields['media_file'].required = True
        if form.is_valid():
            cleaned = form.cleaned_data
            path = ""
            if media_file_obj and media_file_obj.path:
                path = media_file_obj.path.path
            if cleaned.get("media_file", None):
                if path:
                    # delete the old file
                    try:
                        FileManager.delete_file(path)
                    except OSError:
                        pass
                    path = ""
            media_file_path = ""
            if cleaned.get("media_file", None):
                fname, fext = os.path.splitext(cleaned['media_file'].name)
                filename = datetime.now().strftime("%Y%m%d%H%M%S") + fext
                path = "".join((rel_dir, filename)) 
                FileManager.save_file(
                    path=path,
                    content=cleaned['media_file'],
                    )
                media_file_path = path
            
            if not media_file_obj:
                media_file_obj = MediaFile(
                    workshop=instance
                    )
            
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
            
            file_description.save()
            
            if media_file_path: # update media_file path
                media_file_obj.path = media_file_path
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
            form = form_class(initial=initial)
        else:
            # new media file
            form = form_class()
            form.fields['media_file'].required = True

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


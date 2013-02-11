# -*- coding: utf-8 -*-
import os
from datetime import datetime

from django.db import models
from django.http import HttpResponse
from django import forms
from django.utils import simplejson
from django.utils.translation import ugettext_lazy as _
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
from jetson.apps.utils.views import get_abc_list
from jetson.apps.utils.views import filter_abc
from jetson.apps.utils.views import show_form_step
from jetson.apps.utils.context_processors import prev_next_processor

MuseumCategory = models.get_model("museums", "MuseumCategory")
Museum = models.get_model("museums", "Museum")
MediaFile = models.get_model("museums", "MediaFile")

FRONTEND_LANGUAGES = getattr(settings, "FRONTEND_LANGUAGES", settings.LANGUAGES) 

from forms.museum import MUSEUM_FORM_STEPS
from forms.gallery import ImageFileForm, ImageDeletionForm

from jetson.apps.image_mods.models import FileManager
from filebrowser.models import FileDescription

class MuseumSearchForm(dynamicforms.Form):
    category = forms.ModelChoiceField(
        required=False,
        queryset=get_related_queryset(Museum, "categories"),
        )
    open_on_mondays = forms.BooleanField(
        required=False,
        )
    free_entrance = forms.BooleanField(
        required=False,
        )

def museum_list(request):
    qs = Museum.objects.filter(status="published")

    form = MuseumSearchForm(data=request.REQUEST)
    
    facets = {
        'selected': {},
        'categories': {
            'categories': MuseumCategory.objects.all().order_by("title_%s" % request.LANGUAGE_CODE),
            'open_on_mondays': _("Open on Mondays"),
            'free_entrance': _("Free entrance"),
            },
        }
    
    if form.is_valid():
        cat = form.cleaned_data['category']
        if cat:
            facets['selected']['category'] = cat
            qs = qs.filter(
                categories=cat,
                ).distinct()
        open_on_mondays = form.cleaned_data['open_on_mondays']
        if open_on_mondays:
            facets['selected']['open_on_mondays'] = True
            qs = qs.filter(
                open_on_mondays=True,
                )
        free_entrance = form.cleaned_data['free_entrance']
        if free_entrance:
            facets['selected']['free_entrance'] = True
            qs = qs.filter(
                free_entrance=True,
                )
    
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
        template_name="museums/museum_list.html",
        paginate_by=200,
        extra_context=extra_context,
        httpstate_prefix="museum_list",
        context_processors=(prev_next_processor,),
        )

def museum_detail(request, slug):
    qs = Museum.objects.filter(status="published")
    return object_detail(
        request,
        queryset=qs,
        slug=slug,
        slug_field="slug",
        template_name="museums/museum_detail.html",
        context_processors=(prev_next_processor,),
        )

def export_json_museums(request):    
    #create queryset
    qs = Museum.objects.filter(status="published")
   
    museums = []
    for m in qs:        
        data ={
            'title': m.title,
            'subtitle': m.subtitle,
            'description': decode_entities(m.description),
            'image_caption': m.image_caption,
            'street_address': m.street_address,
            'street_address2': m.street_address2,
            'postal_code': m.postal_code,
            'city': m.city,
            'country': m.country,
            'latitude': m.latitude,
            'longitude': m.longitude,
            'phone': m.phone,
            'fax': m.fax,
            'email': m.email,
            'website': m.website,
            'open_on_mondays': m.open_on_mondays,
            'free_entrance': m.free_entrance,
            'status': m.status,
        }
        categories = []
        for cat in m.categories.all():
            categories.append({
                'id': cat.id,
                'title': cat.title,
            })
        data['categories'] = categories
        museums.append(data)
    
    json = simplejson.dumps(museums, ensure_ascii=False, cls=ExtendedJSONEncoder)
    return HttpResponse(json, mimetype='text/javascript; charset=utf-8')

@never_cache
@login_required
def add_museum(request):
    return show_form_step(request, MUSEUM_FORM_STEPS, extra_context={});
    
@never_cache
@login_required
def change_museum(request, slug):
    instance = get_object_or_404(Museum, slug=slug)
    if not request.user.has_perm("museums.change_museum", instance):
        return access_denied(request)
    return show_form_step(request, MUSEUM_FORM_STEPS, extra_context={'museum': instance}, instance=instance);


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
    instance = get_object_or_404(Museum, slug=slug)
    if not request.user.has_perm("museums.change_museum", instance):
        return access_denied(request)

    if "ordering" in request.POST and request.is_ajax():
        tokens = request.POST['ordering']
        update_mediafile_ordering(tokens, instance)
        return HttpResponse("OK")

    return render(request, "museums/gallery/overview.html", {'museum': instance})
    
@never_cache
@login_required
def create_update_mediafile(request, slug, mediafile_token="", media_file_type="", **kwargs):
    instance = get_object_or_404(Museum, slug=slug)
    if not request.user.has_perm("museums.change_museum", instance):
        return access_denied(request)
    
    media_file_type = media_file_type or "image"
    if media_file_type not in ("image",):
        raise Http404
    
    if not "extra_context" in kwargs:
        kwargs["extra_context"] = {}

    rel_dir = "museums/%s/gallery/" % instance.slug
    
    filters = {}
    if mediafile_token:
        media_file_obj = get_object_or_404(
            MediaFile,
            museum=instance,
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
                    museum=instance
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
                    museum=instance,
                    ).count()
            else:
                # trick not to reorder media files on save
                media_file_obj.sort_order = media_file_obj.sort_order
            media_file_obj.save()
            
            if "hidden_iframe" in request.REQUEST:
                return render(
                    request,
                    "museums/gallery/success.html",
                    {},
                    )
            else:
                if cleaned['goto_next']:
                    return redirect(cleaned['goto_next'])
                else:
                    return redirect("museum_gallery_overview", slug=instance.slug)
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
        'museum': instance,
        }
    
    return render(
        request,
        "museums/gallery/create_update_mediafile.html",
        context_dict,
        )

@never_cache
@login_required
def delete_mediafile(request, slug, mediafile_token="", **kwargs):
    instance = get_object_or_404(Museum, slug=slug)
    if not request.user.has_perm("museums.change_museum", instance):
        return access_denied(request)
    
    filters = {
        'id': MediaFile.token_to_pk(mediafile_token),
        }
    if instance:
        filters['museum'] = instance
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
        'museum': instance,
        }
    
    return render(
        request,
        "museums/gallery/delete_mediafile.html",
        context_dict,
        )


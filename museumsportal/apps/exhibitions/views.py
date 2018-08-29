# -*- coding: utf-8 -*-
import os
import shutil
import json
from datetime import datetime, date, timedelta

from django.db import models
from django.http import HttpResponse
from django import forms
from django.utils.translation import ugettext_lazy as _
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

ExhibitionCategory = models.get_model("exhibitions", "ExhibitionCategory")
Exhibition = models.get_model("exhibitions", "Exhibition")
MediaFile = models.get_model("exhibitions", "MediaFile")

FRONTEND_LANGUAGES = getattr(settings, "FRONTEND_LANGUAGES", settings.LANGUAGES) 

from forms.exhibition import EXHIBITION_FORM_STEPS
from forms.gallery import ImageFileForm, ImageDeletionForm

from jetson.apps.image_mods.models import FileManager
from filebrowser.models import FileDescription

SMART_LIST_CHOICES = (
    ('actual', _("Current")),
    ('upcoming', _("Upcoming")),
    ('newly_open', _("Newly open")),
    ('closing_soon', _("Closing soon")),
    ('special', _("Special Exhibitions")),
    ('permanent', _("Permanent Exhibitions")),
    ('suitable_for_disabled', _("Suitable for people with disabilities")),
    ('for_children', _("Special for children / families / youth")),
)

CALENDAR_CHOICES = (
    ('today', _("Today")),
    ('tomorrow', _("Tomorrow")),
    ('within_7_days', _("7 Days")),
    ('within_30_days', _("30 Days")),
)


class ExhibitionFilterForm(dynamicforms.Form):
    category = forms.ModelChoiceField(
        required=False,
        queryset=get_related_queryset(Exhibition, "categories").filter(parent=None),
        to_field_name="slug",
    )
    subcategory = forms.ModelChoiceField(
        required=False,
        queryset=get_related_queryset(Exhibition, "categories").exclude(parent=None),
        to_field_name="slug",
    )
    smart = forms.ChoiceField(
        choices=SMART_LIST_CHOICES,
        required=False,
    )
    calendar = forms.ChoiceField(
        choices=CALENDAR_CHOICES,
        required=False,
    )
    selected_date = forms.DateField(
        required=False,
    )
    from_date = forms.DateField(
        required=False,
    )
    till_date = forms.DateField(
        required=False,
    )


def exhibition_list(request):
    from museumsportal.apps.advertising.templatetags.advertising_tags import not_empty_ad_zone
    qs = Exhibition.objects.filter(status="published")
    
    #if not request.REQUEST.keys():
    #    return redirect("/%s%s?status=newly_opened" % (request.LANGUAGE_CODE, request.path))
    
    form = ExhibitionFilterForm(data=request.REQUEST)
    
    facets = {
        'selected': {},
        'categories': {
            'categories': get_related_queryset(Exhibition, "categories").all().order_by("title_%s" % request.LANGUAGE_CODE),
            'smart_list': SMART_LIST_CHOICES,
            'calendar': CALENDAR_CHOICES,
        },
    }

    closing_soon = False
    if form.is_valid():

        cat = form.cleaned_data['category']
        if cat:
            facets['selected']['category'] = cat
            qs = qs.filter(
                categories=cat,
            ).distinct()

        cat = form.cleaned_data['subcategory']
        if cat:
            facets['selected']['subcategory'] = cat
            qs = qs.filter(
                categories=cat,
            ).distinct()

        cat = form.cleaned_data['smart']
        if cat:
            facets['selected']['smart'] = (cat, dict(SMART_LIST_CHOICES)[cat])
            today = date.today()
            two_weeks = timedelta(days=14)
            if cat == "actual":
                qs = qs.filter(
                    start__lte=today,
                    end__gte=today,
                )
            elif cat == "upcoming":
                qs = qs.filter(
                    start__gt=today,
                )
            elif cat == "newly_open":
                # today - 2 weeks < EXHIBITION START <= today
                qs = qs.filter(
                    start__gt=today-two_weeks,
                    start__lte=today,
                )
            elif cat == "closing_soon":
                # today <= EXHIBITION END < today + two weeks
                qs = qs.filter(
                    end__gte=today,
                    end__lt=today+two_weeks,
                )
                closing_soon = True
            elif cat == "special":
                qs = qs.filter(
                    special=True,
                )
            elif cat == "permanent":
                qs = qs.filter(
                    permanent=True,
                )
            elif cat == "suitable_for_disabled":
                qs = qs.filter(
                    suitable_for_disabled=True,
                )
            elif cat == "for_children":
                qs = qs.filter(
                    is_for_children=True,
                )
        selected_start = None
        selected_end = None
        cat = form.cleaned_data['calendar']
        if cat:
            facets['selected']['calendar'] = (cat, dict(CALENDAR_CHOICES)[cat])
            today = date.today()
            if cat == "today":
                selected_start = today
            if cat == "tomorrow":
                selected_start = today + timedelta(days=1)
            if cat == "within_7_days":
                selected_start = today
                selected_end = selected_start + timedelta(days=7)
            if cat == "within_30_days":
                selected_start = today
                selected_end = selected_start + timedelta(days=30)
        selected_date = form.cleaned_data['selected_date']
        if selected_date:
            facets['selected']['selected_date'] = selected_date
            selected_start = selected_date
        from_date = form.cleaned_data['from_date']
        if from_date:
            facets['selected']['from_date'] = from_date
            selected_start = from_date
        till_date = form.cleaned_data['till_date']
        if till_date:
            facets['selected']['till_date'] = till_date
            selected_end = till_date

        if selected_start:
            if selected_end:
                # Get events which start date is within the selected range
                # -----[--selected range--]----- time ->
                #            [-event-]
                #                   [-event-]
                #                 [-event------
                conditions = models.Q(
                    start__gte=selected_start,
                    start__lte=selected_end,
                )
                # .. which started before and will end after the selected range
                # -----[-selected range-]------- time ->
                #    [------event---------]
                #    [------event------------
                conditions |= models.Q(
                    start__lte=selected_start,
                    end__gte=selected_end,
                )
                conditions |= models.Q(
                    start__lte=selected_start,
                    end=None,
                )
                # .. or which end date is within the selected range
                # -----[--selected range--]----- time ->
                #          [-event-]
                #   [-event-]
                conditions |= models.Q(
                    end__gte=selected_start,
                    end__lte=selected_end,
                )
                qs = qs.filter(conditions)
            else:
                qs = qs.filter(
                    models.Q(
                        start__lte=selected_start,
                        end__gte=selected_start,
                    ) | models.Q(
                        start__lte=selected_start,
                        end=None,
                    )
                )

    if closing_soon:
        qs = qs.order_by("end", "title_%s" % request.LANGUAGE_CODE)
    elif facets['selected'].get("smart", ("", ""))[0] == "upcoming":
        qs = qs.order_by("start", "title_%s" % request.LANGUAGE_CODE)
    else:
        qs = qs.order_by("-start", "title_%s" % request.LANGUAGE_CODE)

    abc_filter = request.GET.get('abc', None)
    if abc_filter:
        facets['selected']['abc'] = abc_filter
    abc_list = get_abc_list(qs, "title_%s" % request.LANGUAGE_CODE, abc_filter)
    if abc_filter:
        qs = filter_abc(qs, "title_%s" % request.LANGUAGE_CODE, abc_filter)

    qs = qs.prefetch_related("museum", "mediafile_set", "categories").defer("tags")

    extra_context = {}
    extra_context['form'] = form
    extra_context['abc_list'] = abc_list
    extra_context['facets'] = facets

    first_page_delta = 0
    if not_empty_ad_zone('exhibitions'):
        first_page_delta = 1
        extra_context['show_ad'] = True

    return object_list(
        request,
        queryset=qs,
        template_name="exhibitions/exhibition_list.html",
        paginate_by=24,
        extra_context=extra_context,
        httpstate_prefix="exhibition_list",
        context_processors=(prev_next_processor,),
        first_page_delta=first_page_delta,
    )


def exhibition_list_map(request):
    qs = Exhibition.objects.filter(status="published")

    #if not request.REQUEST.keys():
    #    return redirect("/%s%s?status=newly_opened" % (request.LANGUAGE_CODE, request.path))

    form = ExhibitionFilterForm(data=request.REQUEST)

    facets = {
        'selected': {},
        'categories': {
            'categories': get_related_queryset(Exhibition, "categories").all().order_by("title_%s" % request.LANGUAGE_CODE),
            'smart_list': SMART_LIST_CHOICES,
            'calendar': CALENDAR_CHOICES,
        },
    }

    closing_soon = False
    if form.is_valid():

        cat = form.cleaned_data['category']
        if cat:
            facets['selected']['category'] = cat
            qs = qs.filter(
                categories=cat,
            ).distinct()

        cat = form.cleaned_data['subcategory']
        if cat:
            facets['selected']['subcategory'] = cat
            qs = qs.filter(
                categories=cat,
            ).distinct()

        cat = form.cleaned_data['smart']
        if cat:
            facets['selected']['smart'] = (cat, dict(SMART_LIST_CHOICES)[cat])
            today = date.today()
            two_weeks = timedelta(days=14)
            if cat == "actual":
                qs = qs.filter(
                    start__lte=today,
                    end__gte=today,
                )
            elif cat == "upcoming":
                qs = qs.filter(
                    start__gt=today,
                )
            elif cat == "newly_opened":
                # today - 2 weeks < EXHIBITION START <= today
                qs = qs.filter(
                    start__gt=today-two_weeks,
                    start__lte=today,
                )
            elif cat == "closing_soon":
                # today <= EXHIBITION END < today + two weeks
                qs = qs.filter(
                    end__gte=today,
                    end__lt=today+two_weeks,
                )
                closing_soon = True
            elif cat == "special":
                qs = qs.filter(
                    special=True,
                )
            elif cat == "permanent":
                qs = qs.filter(
                    permanent=True,
                )
            elif cat == "suitable_for_disabled":
                qs = qs.filter(
                    suitable_for_disabled=True,
                )
            elif cat == "for_children":
                qs = qs.filter(
                    is_for_children=True,
                )
        cat = form.cleaned_data['calendar']
        if cat:
            facets['selected']['calendar'] = (cat, dict(CALENDAR_CHOICES)[cat])
            today = date.today()
            if cat == "today":
                qs = qs.filter(
                    start__lte=today,
                    end__gte=today,
                )
            if cat == "tomorrow":
                tomorrow = today + timedelta(days=1)
                qs = qs.filter(
                    start__lte=tomorrow,
                    end__gte=tomorrow,
                )
            if cat == "within_7_days":
                selected_start = today
                selected_end = selected_start + timedelta(days=7)
                # Get events which start date is within the selected range
                # -----[--selected range--]----- time ->
                #            [-event-]
                #                   [-event-]
                conditions = models.Q(
                    start__gte=selected_start,
                    start__lte=selected_end,
                )
                # .. which started before and will end after the selected range
                # -----[-selected range-]------- time ->
                #    [------event---------]
                conditions |= models.Q(
                    start__lte=selected_start,
                    end__gte=selected_end,
                )
                # .. or which end date is within the selected range
                # -----[--selected range--]----- time ->
                #          [-event-]
                #   [-event-]
                conditions |= models.Q(
                    end__gte=selected_start,
                    end__lte=selected_end,
                )
                qs = qs.filter(conditions)
            if cat == "within_30_days":
                selected_start = today
                selected_end = selected_start + timedelta(days=30)
                # Get events which start date is within the selected range
                # -----[--selected range--]----- time ->
                #            [-event-]
                #                   [-event-]
                conditions = models.Q(
                    start__gte=selected_start,
                    start__lte=selected_end,
                )
                # .. which started before and will end after the selected range
                # -----[-selected range-]------- time ->
                #    [------event---------]
                conditions |= models.Q(
                    start__lte=selected_start,
                    end__gte=selected_end,
                )
                # .. or which end date is within the selected range
                # -----[--selected range--]----- time ->
                #          [-event-]
                #   [-event-]
                conditions |= models.Q(
                    end__gte=selected_start,
                    end__lte=selected_end,
                )
                qs = qs.filter(conditions)


    if closing_soon:
        qs = qs.order_by("end", "title_%s" % request.LANGUAGE_CODE)
    else:
        qs = qs.order_by("-start", "title_%s" % request.LANGUAGE_CODE)

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
        template_name="exhibitions/exhibition_list_map.html",
        paginate_by=200,
        extra_context=extra_context,
        httpstate_prefix="exhibition_list_map",
        context_processors=(prev_next_processor,),
    )


def exhibition_detail(request, slug):
    if "preview" in request.REQUEST:
        qs = Exhibition.objects.all()
        obj = get_object_or_404(qs, slug=slug)
        if not request.user.has_perm("exhibitions.change_exhibition", obj):
            return access_denied(request)
    else:
        qs = Exhibition.objects.filter(status="published")
    return object_detail(
        request,
        queryset=qs,
        slug=slug,
        slug_field="slug",
        template_name="exhibitions/exhibition_detail.html",
        context_processors=(prev_next_processor,),
    )


def exhibition_detail_ajax(request, slug, template_name="exhibitions/exhibition_detail_ajax.html"):
    if "preview" in request.REQUEST:
        qs = Exhibition.objects.all()
        obj = get_object_or_404(qs, slug=slug)
        if not request.user.has_perm("exhibitions.change_exhibition", obj):
            return access_denied(request)
    else:
        qs = Exhibition.objects.filter(status="published")
    return object_detail(
        request,
        queryset=qs,
        slug=slug,
        slug_field="slug",
        template_name=template_name,
        context_processors=(prev_next_processor,),
    )


def exhibition_detail_slideshow(request, slug):
    if "preview" in request.REQUEST:
        qs = Exhibition.objects.all()
        obj = get_object_or_404(qs, slug=slug)
        if not request.user.has_perm("exhibitions.change_exhibition", obj):
            return access_denied(request)
    else:
        qs = Exhibition.objects.filter(status="published")
    return object_detail(
        request,
        queryset=qs,
        slug=slug,
        slug_field="slug",
        template_name="exhibitions/exhibition_detail_slideshow.html",
        context_processors=(prev_next_processor,),
    )


def exhibition_products(request, slug):
    qs = Exhibition.objects.all()
    obj = get_object_or_404(qs, slug=slug)

    qs = obj.get_related_products()

    extra_context = {
        'object': obj,
    }
    return object_list(
        request,
        queryset=qs,
        template_name="exhibitions/exhibition_products.html",
        paginate_by=24,
        extra_context=extra_context,
        httpstate_prefix="exhibition_%s_products" % obj.pk,
        context_processors=(prev_next_processor,),
    )



def export_json_exhibitions(request):
    #create queryset
    qs = Exhibition.objects.filter(status="published")
    
    exhibitions = []
    for ex in qs:
        start = None
        if ex.start:
            start = ex.start.strftime('%Y-%m-%dT%H:%M:%S')
        end = None
        if ex.end:
            end = ex.end.strftime('%Y-%m-%dT%H:%M:%S')
        data = {
            'museum': ex.museum,
            'title': ex.title,
            'subtitle': ex.subtitle,
            'description': decode_entities(ex.description),
            'website': ex.website,
            'start': start,
            'end': end,
            'newly_opened': ex.newly_opened,
            'featured': ex.featured,
            'image_caption': ex.image_caption,
        }
        exhibitions.append(data)
    json_data = json.dumps(
        exhibitions,
        ensure_ascii=False,
        cls=ExtendedJSONEncoder
    )
    return HttpResponse(json_data, mimetype='text/javascript; charset=utf-8')
    

@never_cache
@login_required
def add_exhibition(request):
    if not request.user.has_perm("exhibitions.add_exhibition"):
        return access_denied(request)
    return show_form_step(request, EXHIBITION_FORM_STEPS, extra_context={});


@never_cache
@login_required
def change_exhibition(request, slug):
    instance = get_object_or_404(Exhibition, slug=slug)
    if not request.user.has_perm("exhibitions.change_exhibition", instance):
        return access_denied(request)
    return show_form_step(request, EXHIBITION_FORM_STEPS, extra_context={'exhibition': instance}, instance=instance);


@never_cache
@login_required
def delete_exhibition(request, slug):
    instance = get_object_or_404(Exhibition, slug=slug)
    if not request.user.has_perm("exhibitions.delete_exhibition", instance):
        return access_denied(request)
    if request.method == "POST" and request.is_ajax():
        instance.status = "trashed"
        instance.save()
        return HttpResponse("OK")
    return redirect(instance.get_url_path())


@never_cache
@login_required
def change_exhibition_status(request, slug):
    instance = get_object_or_404(Exhibition, slug=slug)
    if not request.user.has_perm("exhibitions.change_exhibition", instance):
        return access_denied(request)
    if request.method == "POST" and request.is_ajax():
        instance.status = request.POST['status']
        instance.save()
        return HttpResponse("OK")
    return redirect(instance.get_url_path())
    

### MEDIA FILE MANAGEMENT ###


def update_mediafile_ordering(tokens, exhibition):
    # tokens is in this format:
    # "<mediafile1_token>,<mediafile2_token>,<mediafile3_token>"
    mediafiles = []
    for mediafile_token in tokens.split(u","):
        mediafile = get_object_or_404(
            MediaFile,
            exhibition=exhibition,
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
    instance = get_object_or_404(Exhibition, slug=slug)
    if not request.user.has_perm("exhibitions.change_exhibition", instance):
        return access_denied(request)

    if "ordering" in request.POST and request.is_ajax():
        tokens = request.POST['ordering']
        update_mediafile_ordering(tokens, instance)
        return HttpResponse("OK")

    return render(request, "exhibitions/gallery/overview.html", {'exhibition': instance})


@never_cache
@login_required
def create_update_mediafile(request, slug, mediafile_token="", media_file_type="", **kwargs):
    instance = get_object_or_404(Exhibition, slug=slug)
    if not request.user.has_perm("exhibitions.change_exhibition", instance):
        return access_denied(request)
    
    media_file_type = media_file_type or "image"
    if media_file_type not in ("image",):
        raise Http404
    
    if not "extra_context" in kwargs:
        kwargs["extra_context"] = {}

    rel_dir = "exhibitions/%s/" % instance.slug
    
    filters = {}
    if mediafile_token:
        media_file_obj = get_object_or_404(
            MediaFile,
            exhibition=instance,
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
                    exhibition=instance
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
                    exhibition=instance,
                ).count()
            else:
                # trick not to reorder media files on save
                media_file_obj.sort_order = media_file_obj.sort_order
            media_file_obj.save()
            
            if "hidden_iframe" in request.REQUEST:
                return render(
                    request,
                    "exhibitions/gallery/success.html",
                    {},
                )
            else:
                if cleaned['goto_next']:
                    return redirect(cleaned['goto_next'])
                else:
                    return redirect("exhibition_gallery_overview", slug=instance.slug)
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
        'exhibition': instance,
    }
    
    return render(
        request,
        "exhibitions/gallery/create_update_mediafile.html",
        context_dict,
    )


@never_cache
@login_required
def delete_mediafile(request, slug, mediafile_token="", **kwargs):
    instance = get_object_or_404(Exhibition, slug=slug)
    if not request.user.has_perm("exhibitions.change_exhibition", instance):
        return access_denied(request)
    
    filters = {
        'id': MediaFile.token_to_pk(mediafile_token),
    }
    if instance:
        filters['exhibition'] = instance
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
        'exhibition': instance,
    }
    
    return render(
        request,
        "exhibitions/gallery/delete_mediafile.html",
        context_dict,
    )


### VERNISSAGES
def vernissage_list(request):
    qs = Exhibition.objects.filter(status="published").exclude(vernissage__isnull=True)
    
    #if not request.REQUEST.keys():
    #    return redirect("/%s%s?status=newly_opened" % (request.LANGUAGE_CODE, request.path))
    
    form = ExhibitionFilterForm(data=request.REQUEST)
    
    facets = {
        'selected': {},
        'categories': {
            'categories': get_related_queryset(Exhibition, "categories").order_by("title_%s" % request.LANGUAGE_CODE),
        },
    }

    if form.is_valid():
        cat = form.cleaned_data['category']
        if cat:
            facets['selected']['category'] = cat
            qs = qs.filter(
                categories=cat,
            ).distinct()

    qs = qs.order_by("-start", "title_%s" % request.LANGUAGE_CODE)
        
    extra_context = {}
    extra_context['form'] = form
    extra_context['facets'] = facets

    return object_list(
        request,
        queryset=qs,
        template_name="exhibitions/vernissage_list.html",
        paginate_by=200,
        extra_context=extra_context,
        httpstate_prefix="vernissage_list",
        context_processors=(prev_next_processor,),
    )

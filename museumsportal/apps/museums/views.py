# -*- coding: utf-8 -*-
import os
import shutil
from datetime import datetime, time
import json

from django.db import models
from django.http import HttpResponse
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from django.http import Http404
from django.utils.translation import string_concat
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

MuseumCategory = models.get_model("museums", "MuseumCategory")
Museum = models.get_model("museums", "Museum")
MediaFile = models.get_model("museums", "MediaFile")
AccessibilityOption = models.get_model("museums", "AccessibilityOption")

FRONTEND_LANGUAGES = getattr(settings, "FRONTEND_LANGUAGES", settings.LANGUAGES) 

from forms.museum import MUSEUM_FORM_STEPS
from forms.gallery import ImageFileForm, ImageDeletionForm

from jetson.apps.image_mods.models import FileManager
from filebrowser.models import FileDescription


OPEN_LATE_CHOICES = (
    ('mon_till_20', string_concat(_("Mon"), " / ", _("8pm"))),
    ('mon_till_22', string_concat(_("Mon"), " / ", _("10pm"))),
    ('tue_till_20', string_concat(_("Tue"), " / ", _("8pm"))),
    ('tue_till_22', string_concat(_("Tue"), " / ", _("10pm"))),
    ('wed_till_20', string_concat(_("Wed"), " / ", _("8pm"))),
    ('wed_till_22', string_concat(_("Wed"), " / ", _("10pm"))),
    ('thu_till_20', string_concat(_("Thu"), " / ", _("8pm"))),
    ('thu_till_22', string_concat(_("Thu"), " / ", _("10pm"))),
    ('fri_till_20', string_concat(_("Fri"), " / ", _("8pm"))),
    ('fri_till_22', string_concat(_("Fri"), " / ", _("10pm"))),
    ('sat_till_20', string_concat(_("Sat"), " / ", _("8pm"))),
    ('sat_till_22', string_concat(_("Sat"), " / ", _("10pm"))),
    ('sun_till_20', string_concat(_("Sun"), " / ", _("8pm"))),
    ('sun_till_22', string_concat(_("Sun"), " / ", _("10pm"))),
)


class MuseumFilterForm(dynamicforms.Form):
    category = forms.ModelChoiceField(
        required=False,
        queryset=get_related_queryset(Museum, "categories").filter(parent=None),
        to_field_name="slug",
    )
    subcategory = forms.ModelChoiceField(
        required=False,
        queryset=get_related_queryset(Museum, "categories").exclude(parent=None),
        to_field_name="slug",
    )
    open_on_mondays = forms.BooleanField(
        required=False,
    )
    free_entrance = forms.BooleanField(
        required=False,
    )
    open_late = forms.ChoiceField(
        required=False,
        choices=OPEN_LATE_CHOICES,
    )
    accessibility_option = forms.ModelChoiceField(
        required=False,
        queryset=get_related_queryset(Museum, "accessibility_options"),
        to_field_name="slug",
    )


def museum_list(request):
    from museumsportal.apps.advertising.templatetags.advertising_tags import not_empty_ad_zone
    qs = Museum.objects.filter(status="published")

    form = MuseumFilterForm(data=request.REQUEST)
    
    facets = {
        'selected': {},
        'categories': {
            'categories': MuseumCategory.objects.filter(parent=None).order_by("title_%s" % request.LANGUAGE_CODE),
            'open_on_mondays': _("Open on Mondays"),
            'free_entrance': _("Free entrance"),
            'open_late': OPEN_LATE_CHOICES,
            'accessibility_options': AccessibilityOption.objects.all()
        },
    }
    
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

        cat = form.cleaned_data['accessibility_option']
        if cat:
            facets['selected']['accessibility_option'] = cat
            qs = qs.filter(
                accessibility_options=cat,
            ).distinct()

        cat = form.cleaned_data['open_late']
        if cat:
            facets['selected']['open_late'] = (cat, dict(OPEN_LATE_CHOICES)[cat])
            today = datetime.today().date()
            weekday, _till, hours = cat.split('_')
            qs = qs.filter(**{
                'season__start__lte': today,
                'season__end__gte': today,
                'season__%s_close__gte' % weekday: time(int(hours), 0),
            }).distinct()

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
    
    abc_filter = request.GET.get('abc', None)
    if abc_filter:
        facets['selected']['abc'] = abc_filter
    abc_list = get_abc_list(qs, "title_%s" % request.LANGUAGE_CODE, abc_filter)
    if abc_filter:
        qs = filter_abc(qs, "title_%s" % request.LANGUAGE_CODE, abc_filter)

    request_specific_field_name = 'title_{}'.format(request.LANGUAGE_CODE)
    qs = qs.annotate(title_uni=models.Case(
        models.When(then=models.Value('title_de'), **{request_specific_field_name: ''}),
        default=models.Value(request_specific_field_name),
        output_field=models.CharField(),
    )).order_by("title_uni")

    qs = qs.prefetch_related("season_set", "mediafile_set", "categories", "accessibility_options").defer("tags")
    
    extra_context = {}
    extra_context['form'] = form
    extra_context['abc_list'] = abc_list
    extra_context['facets'] = facets

    first_page_delta = 0
    if not_empty_ad_zone('museums'):
        first_page_delta = 1
        extra_context['show_ad'] = True

    return object_list(
        request,
        queryset=qs,
        template_name="museums/museum_list.html",
        paginate_by=24,
        extra_context=extra_context,
        httpstate_prefix="museum_list",
        context_processors=(prev_next_processor,),
        first_page_delta=first_page_delta,
    )


def museum_list_map(request):
    qs = Museum.objects.filter(status="published")

    form = MuseumFilterForm(data=request.REQUEST)

    facets = {
        'selected': {},
        'categories': {
            'categories': MuseumCategory.objects.filter(parent=None).order_by("title_%s" % request.LANGUAGE_CODE),
            'open_on_mondays': _("Open on Mondays"),
            'free_entrance': _("Free entrance"),
            'open_late': OPEN_LATE_CHOICES,
            'accessibility_options': AccessibilityOption.objects.all()
        },
    }

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

        cat = form.cleaned_data['accessibility_option']
        if cat:
            facets['selected']['accessibility_option'] = cat
            qs = qs.filter(
                accessibility_options=cat,
            ).distinct()

        cat = form.cleaned_data['open_late']
        if cat:
            facets['selected']['open_late'] = (cat, dict(OPEN_LATE_CHOICES)[cat])
            today = datetime.today().date()
            weekday, _till, hours = cat.split('_')
            qs = qs.filter(**{
                'season__start__lte': today,
                'season__end__gte': today,
                'season__%s_close__gte' % weekday: time(int(hours), 0),
            }).distinct()

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
        template_name="museums/museum_list_map.html",
        paginate_by=200,
        extra_context=extra_context,
        httpstate_prefix="museum_list_map",
        context_processors=(prev_next_processor,),
    )


def museum_detail(request, slug):
    if "preview" in request.REQUEST:
        qs = Museum.objects.all()
        obj = get_object_or_404(qs, slug=slug)
        if not request.user.has_perm("museums.change_museum", obj):
            return access_denied(request)
    else:
        qs = Museum.objects.filter(status="published")
    return object_detail(
        request,
        queryset=qs,
        slug=slug,
        slug_field="slug",
        template_name="museums/museum_detail.html",
        context_processors=(prev_next_processor,),
    )


def museum_detail_ajax(request, slug, template_name="museums/museum_detail_ajax.html"):
    if "preview" in request.REQUEST:
        qs = Museum.objects.all()
        obj = get_object_or_404(qs, slug=slug)
        if not request.user.has_perm("museums.change_museum", obj):
            return access_denied(request)
    else:
        qs = Museum.objects.filter(status="published")
    return object_detail(
        request,
        queryset=qs,
        slug=slug,
        slug_field="slug",
        template_name=template_name,
        context_processors=(prev_next_processor,),
    )


def museum_detail_slideshow(request, slug):
    if "preview" in request.REQUEST:
        qs = Museum.objects.all()
        obj = get_object_or_404(qs, slug=slug)
        if not request.user.has_perm("museums.change_museum", obj):
            return access_denied(request)
    else:
        qs = Museum.objects.filter(status="published")
    return object_detail(
        request,
        queryset=qs,
        slug=slug,
        slug_field="slug",
        template_name="museums/museum_detail_slideshow.html",
        context_processors=(prev_next_processor,),
    )


def museum_products(request, slug):
    qs = Museum.objects.all()
    obj = get_object_or_404(qs, slug=slug)

    qs = obj.get_related_products()

    extra_context = {
        'object': obj,
    }
    return object_list(
        request,
        queryset=qs,
        template_name="museums/museum_products.html",
        paginate_by=24,
        extra_context=extra_context,
        httpstate_prefix="museum_%s_products" % obj.pk,
        context_processors=(prev_next_processor,),
    )


def export_json_museums(request):
    #create queryset
    qs = Museum.objects.filter(status="published")
   
    museums = []
    for m in qs:
        phone = ""
        if m.phone_number:
            phone = "+{} ({}) {}".format(m.phone_country, m.phone_area, m.phone_number)
        fax = ""
        if m.fax_number:
            fax = "+{} ({}) {}".format(m.fax_country, m.fax_area, m.fax_number)
        data = {
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
            'phone': phone,
            'fax': fax,
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
    
    json_str = json.dumps(museums, ensure_ascii=False, cls=ExtendedJSONEncoder)
    return HttpResponse(json_str, content_type='text/javascript; charset=utf-8')


@never_cache
@login_required
def add_museum(request):
    if not request.user.has_perm("museums.add_museum"):
        return access_denied(request)
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

    rel_dir = "museums/%s/" % instance.slug
    
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
                    museum=instance
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


@never_cache
def json_museum_attrs(request, museum_id):
    """
    Gets address attributes from a given museum
    """
    json_str = "false"
    try:
        m = Museum.objects.get(pk=museum_id)
    except:
        pass
    else:
        data = {
            'title': m.title,
            'subtitle': m.subtitle,
            'description': decode_entities(m.description),
            'street_address': m.street_address,
            'street_address2': m.street_address2,
            'postal_code': m.postal_code,
            'city': m.city,
            'latitude': m.latitude,
            'longitude': m.longitude,
            'status': m.status,
        }
        json_str = json.dumps(data, ensure_ascii=False, cls=ExtendedJSONEncoder)
    return HttpResponse(json_str, content_type='text/javascript; charset=utf-8')

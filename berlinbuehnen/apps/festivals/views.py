# -*- coding: utf-8 -*-
import os
import shutil
from datetime import datetime

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.views.decorators.cache import never_cache
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

from .models import Festival, Image as FestivalImage

from .forms.festivals import FESTIVAL_FORM_STEPS
from .forms.gallery import ImageFileForm, ImageDeletionForm

from jetson.apps.image_mods.models import FileManager
from filebrowser.models import FileDescription

class FestivalFilterForm(forms.Form):
    pass


def festival_list(request, year=None, month=None, day=None):
    qs = Festival.objects.filter(status="published")

    form = FestivalFilterForm(data=request.REQUEST)
    
    facets = {
        'selected': {},
        'categories': {
        },
    }
    
    if form.is_valid():
        # cats = form.cleaned_data['services']
        # if cats:
        #     facets['selected']['services'] = cats
        #     for cat in cats:
        #         qs = qs.filter(
        #             services=cat,
        #         ).distinct()
        pass

    abc_filter = request.GET.get('abc', None)
    if abc_filter:
        facets['selected']['abc'] = abc_filter
    abc_list = get_abc_list(qs, "title_%s" % request.LANGUAGE_CODE, abc_filter)
    if abc_filter:
        qs = filter_abc(qs, "title_%s" % request.LANGUAGE_CODE, abc_filter)

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
        template_name="festivals/festival_list.html",
        paginate_by=24,
        extra_context=extra_context,
        httpstate_prefix="festival_list",
        context_processors=(prev_next_processor,),
    )


def festival_detail(request, slug):
    if "preview" in request.REQUEST:
        qs = Festival.objects.all()
        obj = get_object_or_404(qs, slug=slug)
        if not request.user.has_perm("festivals.change_festival", obj):
            return access_denied(request)
    else:
        qs = Festival.objects.filter(status="published")
    return object_detail(
        request,
        queryset=qs,
        slug=slug,
        slug_field="slug",
        template_name="festivals/festival_detail.html",
        context_processors=(prev_next_processor,),
    )


@never_cache
@login_required
def add_festival(request):
    if not request.user.has_perm("festivals.add_festival"):
        return access_denied(request)
    return show_form_step(request, FESTIVAL_FORM_STEPS, extra_context={});


@never_cache
@login_required
def change_festival(request, slug):
    instance = get_object_or_404(Festival, slug=slug)
    if not request.user.has_perm("festivals.change_festival", instance):
        return access_denied(request)
    return show_form_step(request, FESTIVAL_FORM_STEPS, extra_context={'festival': instance}, instance=instance);


@never_cache
@login_required
def delete_festival(request, slug):
    instance = get_object_or_404(Festival, slug=slug)
    if not request.user.has_perm("festivals.delete_festival", instance):
        return access_denied(request)
    if request.method == "POST" and request.is_ajax():
        instance.status = "trashed"
        instance.save()
        return HttpResponse("OK")
    return redirect(instance.get_url_path())


@never_cache
@login_required
def change_festival_status(request, slug):
    instance = get_object_or_404(Festival, slug=slug)
    if not request.user.has_perm("festivals.change_festival", instance):
        return access_denied(request)
    if request.method == "POST" and request.is_ajax() and request.POST['status'] in ("draft", "published", "not_listed"):
        instance.status = request.POST['status']
        instance.save()
        return HttpResponse("OK")
    return redirect(instance.get_url_path())


### MEDIA FILE MANAGEMENT ###


def update_mediafile_ordering(tokens, festival):
    # tokens is in this format:
    # "<mediafile1_token>,<mediafile2_token>,<mediafile3_token>"
    mediafiles = []
    for mediafile_token in tokens.split(u","):
        mediafile = get_object_or_404(
            FestivalImage,
            festival=festival,
            pk=FestivalImage.token_to_pk(mediafile_token)
        )
        mediafiles.append(mediafile)
    sort_order = 0
    for mediafile in mediafiles:
        mediafile.sort_order = sort_order
        mediafile.save()
        sort_order += 1


@never_cache
@login_required
def image_overview(request, slug):
    instance = get_object_or_404(Festival, slug=slug)
    if not request.user.has_perm("festivals.change_festival", instance):
        return access_denied(request)

    if "ordering" in request.POST and request.is_ajax():
        tokens = request.POST['ordering']
        update_mediafile_ordering(tokens, instance)
        return HttpResponse("OK")

    return render(request, "festivals/gallery/overview.html", {'festival': instance})


@never_cache
@login_required
def create_update_image(request, slug, mediafile_token="", **kwargs):
    instance = get_object_or_404(Festival, slug=slug)
    if not request.user.has_perm("festivals.change_festival", instance):
        return access_denied(request)

    rel_dir = "festivals/%s/" % instance.slug

    if mediafile_token:
        media_file_obj = get_object_or_404(
            FestivalImage,
            festival=instance,
            pk=FestivalImage.token_to_pk(mediafile_token),
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
                media_file_obj = FestivalImage(
                    festival=instance
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

                os.remove(abs_tmp_path)
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
                media_file_obj.sort_order = FestivalImage.objects.filter(
                    festival=instance,
                ).count()
            else:
                # trick not to reorder media files on save
                media_file_obj.sort_order = media_file_obj.sort_order
            media_file_obj.save()

            if "hidden_iframe" in request.REQUEST:
                return render(
                    request,
                    "festivals/gallery/success.html",
                    {},
                )
            else:
                if cleaned['goto_next']:
                    return redirect(cleaned['goto_next'])
                else:
                    return redirect("festival_gallery_overview", slug=instance.slug)
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
        'form': form,
        'festival': instance,
    }

    return render(
        request,
        "festivals/gallery/create_update_image.html",
        context_dict,
    )


@never_cache
@login_required
def delete_image(request, slug, mediafile_token="", **kwargs):
    instance = get_object_or_404(Festival, slug=slug)
    if not request.user.has_perm("festivals.change_festival", instance):
        return access_denied(request)

    filters = {
        'id': FestivalImage.token_to_pk(mediafile_token),
    }
    if instance:
        filters['festival'] = instance
    try:
        media_file_obj = FestivalImage.objects.get(**filters)
    except:
        raise Http404

    form_class = ImageDeletionForm

    if "POST" == request.method:
        form = form_class(request.POST)
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
        form = form_class()

    form.helper.form_action = request.path

    context_dict = {
        'media_file': media_file_obj,
        'form': form,
        'festival': instance,
    }

    return render(
        request,
        "festivals/gallery/delete_image.html",
        context_dict,
    )


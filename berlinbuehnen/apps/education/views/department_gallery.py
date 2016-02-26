# -*- coding: utf-8 -*-
import os
import shutil
from datetime import datetime, date, timedelta

from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from django.views.decorators.cache import never_cache

from base_libs.views.views import access_denied

from jetson.apps.utils.decorators import login_required

FRONTEND_LANGUAGES = getattr(settings, "FRONTEND_LANGUAGES", settings.LANGUAGES)

from berlinbuehnen.apps.education.forms.gallery import ImageForm, ImageDeletionForm
from berlinbuehnen.apps.education.forms.gallery import PDFForm, PDFDeletionForm

from jetson.apps.image_mods.models import FileManager
from filebrowser.models import FileDescription

from berlinbuehnen.apps.education.models import Department
from berlinbuehnen.apps.education.models import Image, PDF


### MEDIA FILE MANAGEMENT ###

def update_image_ordering(tokens, department):
    # tokens is in this format:
    # "<mediafile1_token>,<mediafile2_token>,<mediafile3_token>"
    mediafiles = []
    for mediafile_token in tokens.split(u","):
        mediafile = get_object_or_404(
            Image,
            department=department,
            pk=Image.token_to_pk(mediafile_token)
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
    instance = get_object_or_404(Department, slug=slug)
    if not instance.is_editable():
        return access_denied(request)

    if "ordering" in request.POST and request.is_ajax():
        tokens = request.POST['ordering']
        update_image_ordering(tokens, instance)
        return HttpResponse("OK")

    return render(request, "education/department_gallery/image_overview.html", {'department': instance})


@never_cache
@login_required
def create_update_image(request, slug, mediafile_token="", **kwargs):
    instance = get_object_or_404(Department, slug=slug)
    if not instance.is_editable():
        return access_denied(request)

    rel_dir = "education/departments/%s/" % instance.slug

    if mediafile_token:
        media_file_obj = get_object_or_404(
            Image,
            department=instance,
            pk=Image.token_to_pk(mediafile_token),
        )
    else:
        media_file_obj = None

    form_class = ImageForm

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
                media_file_obj = Image(
                    department=instance
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
                media_file_obj.sort_order = Image.objects.filter(
                    department=instance,
                ).count()
            else:
                # trick not to reorder media files on save
                media_file_obj.sort_order = media_file_obj.sort_order
            media_file_obj.save()

            if "hidden_iframe" in request.REQUEST:
                return render(
                    request,
                    "education/department_gallery/success.html",
                    {},
                )
            else:
                if cleaned['goto_next']:
                    return redirect(cleaned['goto_next'])
                else:
                    return redirect("department_image_overview", slug=instance.slug)
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
        'department': instance,
    }

    return render(
        request,
        "education/department_gallery/create_update_image.html",
        context_dict,
    )


@never_cache
@login_required
def delete_image(request, slug, mediafile_token="", **kwargs):
    instance = get_object_or_404(Department, slug=slug)
    if not instance.is_editable():
        return access_denied(request)

    filters = {
        'id': Image.token_to_pk(mediafile_token),
    }
    if instance:
        filters['department'] = instance
    try:
        media_file_obj = Image.objects.get(**filters)
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
        'department': instance,
    }

    return render(
        request,
        "education/department_gallery/delete_image.html",
        context_dict,
    )


def update_pdf_ordering(tokens, department):
    # tokens is in this format:
    # "<mediafile1_token>,<mediafile2_token>,<mediafile3_token>"
    mediafiles = []
    for mediafile_token in tokens.split(u","):
        mediafile = get_object_or_404(
            PDF,
            department=department,
            pk=PDF.token_to_pk(mediafile_token)
        )
        mediafiles.append(mediafile)
    sort_order = 0
    for mediafile in mediafiles:
        mediafile.sort_order = sort_order
        mediafile.save()
        sort_order += 1


@never_cache
@login_required
def pdf_overview(request, slug):
    instance = get_object_or_404(Department, slug=slug)
    if not instance.is_editable():
        return access_denied(request)

    if "ordering" in request.POST and request.is_ajax():
        tokens = request.POST['ordering']
        update_pdf_ordering(tokens, instance)
        return HttpResponse("OK")

    return render(request, "education/department_gallery/pdf_overview.html", {'department': instance})


@never_cache
@login_required
def create_update_pdf(request, slug, mediafile_token="", **kwargs):
    instance = get_object_or_404(Department, slug=slug)
    if not instance.is_editable():
        return access_denied(request)

    rel_dir = "education/departments/%s/" % instance.slug

    if mediafile_token:
        media_file_obj = get_object_or_404(
            PDF,
            department=instance,
            pk=PDF.token_to_pk(mediafile_token),
        )
    else:
        media_file_obj = None

    form_class = PDFForm

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
                media_file_obj = PDF(
                    department=instance
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

            file_description.save()

            if not media_file_obj.pk:
                media_file_obj.sort_order = PDF.objects.filter(
                    department=instance,
                ).count()
            else:
                # trick not to reorder media files on save
                media_file_obj.sort_order = media_file_obj.sort_order
            media_file_obj.save()

            if "hidden_iframe" in request.REQUEST:
                return render(
                    request,
                    "education/department_gallery/success.html",
                    {},
                )
            else:
                if cleaned['goto_next']:
                    return redirect(cleaned['goto_next'])
                else:
                    return redirect("department_image_overview", slug=instance.slug)
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
        'department': instance,
    }

    return render(
        request,
        "education/department_gallery/create_update_pdf.html",
        context_dict,
    )


@never_cache
@login_required
def delete_pdf(request, slug, mediafile_token="", **kwargs):
    instance = get_object_or_404(Department, slug=slug)
    if not instance.is_editable():
        return access_denied(request)

    filters = {
        'id': PDF.token_to_pk(mediafile_token),
    }
    if instance:
        filters['department'] = instance
    try:
        media_file_obj = PDF.objects.get(**filters)
    except:
        raise Http404

    form_class = PDFDeletionForm

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
        'department': instance,
    }

    return render(
        request,
        "education/department_gallery/delete_pdf.html",
        context_dict,
    )


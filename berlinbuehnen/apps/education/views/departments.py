# -*- coding: utf-8 -*-
import os
import shutil
from datetime import datetime

from django import forms
from django.db.models.functions import Lower
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

from berlinbuehnen.apps.education.models import Department
from berlinbuehnen.apps.education.forms.departments import DEPARTMENT_FORM_STEPS

FRONTEND_LANGUAGES = getattr(settings, "FRONTEND_LANGUAGES", settings.LANGUAGES)


class EducationFilterForm(forms.Form):
    pass


def department_list(request):
    from berlinbuehnen.apps.advertising.templatetags.advertising_tags import not_empty_ad_zone

    qs = Department.objects.filter(status="published").order_by(Lower("title_%s" % request.LANGUAGE_CODE))

    form = EducationFilterForm(data=request.REQUEST)

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

    extra_context = {}
    extra_context['form'] = form
    extra_context['abc_list'] = abc_list
    extra_context['facets'] = facets

    first_page_delta = 0
    if not_empty_ad_zone('education'):
        first_page_delta = 1
        extra_context['show_ad'] = True

    return object_list(
        request,
        queryset=qs,
        template_name="education/department_list.html",
        paginate_by=24,
        extra_context=extra_context,
        httpstate_prefix="education_list",
        context_processors=(prev_next_processor,),
        first_page_delta=first_page_delta,
    )


def department_detail(request, slug):

    if "preview" in request.REQUEST:
        qs = Department.objects.all()
        obj = get_object_or_404(qs, slug=slug)
        if not obj.is_editable():
            return access_denied(request)
    else:
        qs = Department.objects.filter(status="published")

    return object_detail(
        request,
        queryset=qs,
        slug=slug,
        slug_field="slug",
        template_name="education/department_detail.html",
        context_processors=(prev_next_processor,),
    )

@never_cache
@login_required
def add_department(request):
    if not request.user.has_perm("education.add_department"):
        return access_denied(request)
    return show_form_step(request, DEPARTMENT_FORM_STEPS, extra_context={});


@never_cache
@login_required
def change_department(request, slug):
    instance = get_object_or_404(Department, slug=slug)
    if not instance.is_editable():
        return access_denied(request)
    return show_form_step(request, DEPARTMENT_FORM_STEPS, extra_context={'department': instance}, instance=instance);


@never_cache
@login_required
def delete_department(request, slug):
    instance = get_object_or_404(Department, slug=slug)
    if not instance.is_deletable():
        return access_denied(request)
    if request.method == "POST" and request.is_ajax():
        instance.status = "trashed"
        instance.save()
        return HttpResponse("OK")
    return redirect(instance.get_url_path())


@never_cache
@login_required
def change_department_status(request, slug):
    instance = get_object_or_404(Department, slug=slug)
    if not instance.is_editable():
        return access_denied(request)
    if request.method == "POST" and request.is_ajax() and request.POST['status'] in ("draft", "published", "not_listed"):
        instance.status = request.POST['status']
        instance.save()
        return HttpResponse("OK")
    return redirect(instance.get_url_path())


# @never_cache
# @login_required
# def add_project(request):
#     if not request.user.has_perm("projects.add_project"):
#         return access_denied(request)
#     return show_form_step(request, FESTIVAL_FORM_STEPS, extra_context={});
#
#
# @never_cache
# @login_required
# def change_project(request, slug):
#     instance = get_object_or_404(Project, slug=slug)
#     if not request.user.has_perm("projects.change_project", instance):
#         return access_denied(request)
#     return show_form_step(request, FESTIVAL_FORM_STEPS, extra_context={'project': instance}, instance=instance);
#
#
# @never_cache
# @login_required
# def delete_project(request, slug):
#     instance = get_object_or_404(Project, slug=slug)
#     if not request.user.has_perm("projects.delete_project", instance):
#         return access_denied(request)
#     if request.method == "POST" and request.is_ajax():
#         instance.status = "trashed"
#         instance.save()
#         return HttpResponse("OK")
#     return redirect(instance.get_url_path())
#
#
# @never_cache
# @login_required
# def change_project_status(request, slug):
#     instance = get_object_or_404(Project, slug=slug)
#     if not request.user.has_perm("projects.change_project", instance):
#         return access_denied(request)
#     if request.method == "POST" and request.is_ajax() and request.POST['status'] in ("draft", "published", "not_listed"):
#         instance.status = request.POST['status']
#         instance.save()
#         return HttpResponse("OK")
#     return redirect(instance.get_url_path())
#
#
# ### MEDIA FILE MANAGEMENT ###
#
#
# def update_mediafile_ordering(tokens, project):
#     # tokens is in this format:
#     # "<mediafile1_token>,<mediafile2_token>,<mediafile3_token>"
#     mediafiles = []
#     for mediafile_token in tokens.split(u","):
#         mediafile = get_object_or_404(
#             ProjectImage,
#             project=project,
#             pk=ProjectImage.token_to_pk(mediafile_token)
#         )
#         mediafiles.append(mediafile)
#     sort_order = 0
#     for mediafile in mediafiles:
#         mediafile.sort_order = sort_order
#         mediafile.save()
#         sort_order += 1
#
#
# @never_cache
# @login_required
# def image_overview(request, slug):
#     instance = get_object_or_404(Project, slug=slug)
#     if not request.user.has_perm("projects.change_project", instance):
#         return access_denied(request)
#
#     if "ordering" in request.POST and request.is_ajax():
#         tokens = request.POST['ordering']
#         update_mediafile_ordering(tokens, instance)
#         return HttpResponse("OK")
#
#     return render(request, "education/gallery/overview.html", {'project': instance})
#
#
# @never_cache
# @login_required
# def create_update_image(request, slug, mediafile_token="", **kwargs):
#     instance = get_object_or_404(Project, slug=slug)
#     if not request.user.has_perm("projects.change_project", instance):
#         return access_denied(request)
#
#     rel_dir = "projects/%s/" % instance.slug
#
#     if mediafile_token:
#         media_file_obj = get_object_or_404(
#             ProjectImage,
#             project=instance,
#             pk=ProjectImage.token_to_pk(mediafile_token),
#         )
#     else:
#         media_file_obj = None
#
#     form_class = ImageFileForm
#
#     if request.method == "POST":
#         # just after submitting data
#         form = form_class(media_file_obj, request.POST, request.FILES)
#         if form.is_valid():
#             cleaned = form.cleaned_data
#             path = ""
#             if media_file_obj and media_file_obj.path:
#                 path = media_file_obj.path.path
#             if cleaned.get("media_file_path", None):
#                 if path:
#                     # delete the old file
#                     try:
#                         FileManager.delete_file(path)
#                     except OSError:
#                         pass
#                     path = ""
#
#             if not media_file_obj:
#                 media_file_obj = ProjectImage(
#                     project=instance
#                 )
#             media_file_obj.copyright_restrictions = cleaned['copyright_restrictions']
#
#             media_file_path = ""
#             if cleaned.get("media_file_path", None):
#                 tmp_path = cleaned['media_file_path']
#                 abs_tmp_path = os.path.join(settings.MEDIA_ROOT, tmp_path)
#
#                 fname, fext = os.path.splitext(tmp_path)
#                 filename = datetime.now().strftime("%Y%m%d%H%M%S") + fext
#                 dest_path = "".join((rel_dir, filename))
#                 FileManager.path_exists(os.path.join(settings.MEDIA_ROOT, rel_dir))
#                 abs_dest_path = os.path.join(settings.MEDIA_ROOT, dest_path)
#
#                 shutil.copy2(abs_tmp_path, abs_dest_path)
#
#                 os.remove(abs_tmp_path)
#                 media_file_obj.path = media_file_path = dest_path
#                 media_file_obj.save()
#
#
#             from filebrowser.base import FileObject
#
#             try:
#                 file_description = FileDescription.objects.filter(
#                     file_path=FileObject(media_file_path or path),
#                 ).order_by("pk")[0]
#             except:
#                 file_description = FileDescription(file_path=media_file_path or path)
#
#             for lang_code, lang_name in FRONTEND_LANGUAGES:
#                 setattr(file_description, 'title_%s' % lang_code, cleaned['title_%s' % lang_code])
#                 setattr(file_description, 'description_%s' % lang_code, cleaned['description_%s' % lang_code])
#             setattr(file_description, 'author', cleaned['author'])
#             #setattr(file_description, 'copyright_limitations', cleaned['copyright_limitations'])
#
#             file_description.save()
#
#             if not media_file_obj.pk:
#                 media_file_obj.sort_order = ProjectImage.objects.filter(
#                     project=instance,
#                 ).count()
#             else:
#                 # trick not to reorder media files on save
#                 media_file_obj.sort_order = media_file_obj.sort_order
#             media_file_obj.save()
#
#             if "hidden_iframe" in request.REQUEST:
#                 return render(
#                     request,
#                     "education/gallery/success.html",
#                     {},
#                 )
#             else:
#                 if cleaned['goto_next']:
#                     return redirect(cleaned['goto_next'])
#                 else:
#                     return redirect("project_gallery_overview", slug=instance.slug)
#     else:
#         if media_file_obj:
#             # existing media file
#             try:
#                 file_description = FileDescription.objects.filter(
#                     file_path=media_file_obj.path,
#                 ).order_by("pk")[0]
#             except:
#                 file_description = FileDescription(file_path=media_file_obj.path)
#             initial = {}
#             initial.update(media_file_obj.__dict__)
#             initial.update(file_description.__dict__)
#             form = form_class(media_file_obj, initial=initial)
#         else:
#             # new media file
#             form = form_class(media_file_obj)
#
#     form.helper.form_action = request.path + "?hidden_iframe=1"
#
#     base_template = "base_main.html"
#     if "hidden_iframe" in request.REQUEST:
#         base_template = "base_iframe.html"
#
#     context_dict = {
#         'base_template': base_template,
#         'media_file': media_file_obj,
#         'form': form,
#         'project': instance,
#     }
#
#     return render(
#         request,
#         "education/gallery/create_update_image.html",
#         context_dict,
#     )
#
#
# @never_cache
# @login_required
# def delete_image(request, slug, mediafile_token="", **kwargs):
#     instance = get_object_or_404(Project, slug=slug)
#     if not request.user.has_perm("projects.change_project", instance):
#         return access_denied(request)
#
#     filters = {
#         'id': ProjectImage.token_to_pk(mediafile_token),
#     }
#     if instance:
#         filters['project'] = instance
#     try:
#         media_file_obj = ProjectImage.objects.get(**filters)
#     except:
#         raise Http404
#
#     form_class = ImageDeletionForm
#
#     if "POST" == request.method:
#         form = form_class(request.POST)
#         if media_file_obj:
#             if media_file_obj.path:
#                 try:
#                     FileManager.delete_file(media_file_obj.path.path)
#                 except OSError:
#                     pass
#                 FileDescription.objects.filter(
#                     file_path=media_file_obj.path,
#                 ).delete()
#             media_file_obj.delete()
#
#             return HttpResponse("OK")
#     else:
#         form = form_class()
#
#     form.helper.form_action = request.path
#
#     context_dict = {
#         'media_file': media_file_obj,
#         'form': form,
#         'project': instance,
#     }
#
#     return render(
#         request,
#         "education/gallery/delete_image.html",
#         context_dict,
#     )

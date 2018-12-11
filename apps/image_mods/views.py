# -*- coding: UTF-8 -*-
import os
import math
from PIL import Image
from cStringIO import StringIO

from django.template import loader, RequestContext
from django.views.decorators.cache import never_cache
from django.contrib.admin.views.decorators import staff_member_required
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import Http404
from django.http import HttpResponseBadRequest
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import ugettext_lazy as _, ugettext
from django.core.urlresolvers import reverse
from django.db import models
from django import forms
from django.contrib import messages
from django.conf import settings

from base_libs.views import access_denied

from filebrowser.settings import MEDIA_URL
from filebrowser.decorators import get_path, get_file
from filebrowser.sites import get_settings_var, get_breadcrumbs
from filebrowser.settings import MEDIA_ROOT, DIRECTORY
from filebrowser.templatetags.fb_tags import get_query_string
from filebrowser.base import FileObject

image_mods = models.get_app("image_mods")

CROP_POSITIONS = {
    'top': lambda (bg_w, bg_h), (im_w, im_h): ((bg_w-im_w)/2, 0),
    'right': lambda (bg_w, bg_h), (im_w, im_h): (bg_w-im_w, (bg_h-im_h)/2),
    'bottom': lambda (bg_w, bg_h), (im_w, im_h): ((bg_w-im_w)/2, bg_h-im_h),
    'left': lambda (bg_w, bg_h), (im_w, im_h): (0, (bg_h-im_h)/2),
    'center': lambda (bg_w, bg_h), (im_w, im_h): ((bg_w-im_w)/2, (bg_h-im_h)/2),
    }


class CoordsConverter(object):
    """
    Converts original coordinates to canvas coordinates and vice versa 
    where canvas includes the rescaled version of original image
    """

    def __init__(self, orig_size, rescaled_size, rescaled_pos):
        """
        * orig_size - width and height of the original image
        * rescaled_size - width and height of the rescaled image
        * rescaled_pos - x and y position of rescaled image within the canvas
        """
        self.orig_size = orig_size
        self.rescaled_size = rescaled_size
        self.rescaled_pos = rescaled_pos

    def canvas_to_orig(self, canvas_coords):
        """
        Converts canvas coordinates to original coordinates
        The upper left corner of original image is (0, 0)
        """
        (canvas_x, canvas_y) = canvas_coords
        (orig_w, orig_h) = self.orig_size
        (rescaled_w, rescaled_h) = self.rescaled_size
        (dx, dy) = self.rescaled_pos

        orig_x = int(round((canvas_x - dx) * orig_w / rescaled_w))
        orig_y = int(round((canvas_y - dy) * orig_h / rescaled_h))

        return (orig_x, orig_y)

    def orig_to_canvas(self, orig_coords):
        """
        Converts original coordinates to canvas coordinates
        The upper left corner of canvas is (0, 0)
        """
        (orig_x, orig_y) = orig_coords
        (orig_w, orig_h) = self.orig_size
        (rescaled_w, rescaled_h) = self.rescaled_size
        (dx, dy) = self.rescaled_pos

        canvas_x = max(0, int(round(orig_x * rescaled_w / orig_w + dx)))
        canvas_y = max(0, int(round(orig_y * rescaled_h / orig_h + dy)))

        return (canvas_x, canvas_y)


@never_cache
def get_or_create_modified_path(request):
    retval = ""
    if request.POST:
        file_path = request.POST.get('file_path', "")
        absolute_path = False
        if file_path.startswith(MEDIA_URL):
            absolute_path = True
            file_path = file_path[len(MEDIA_URL):]
        mod_sysname = request.POST.get('mod_sysname', "")
        path, query_params = image_mods.FileManager.modified_path(
            file_path, mod_sysname
        )
        if path and absolute_path:
            retval = "".join((MEDIA_URL, path, query_params))
    response = HttpResponse(retval)
    response['Content-Type'] = "text/javascript"
    response['Pragma'] = "No-Cache"
    return response


def cropping_preview(request, bgcolor=None):
    """
    Return an image for cropping
    
    Required GET params:
    * orig_path - full path of the original image within filebrowser's MEDIA_ROOT
    * sysname - sysname of the modification to make
    
    """
    bgcolor = bgcolor or "092E20"
    rel_orig_path = request.GET.get('orig_path', '')
    sysname = request.GET.get('sysname', '')
    cp_mod = image_mods.ImageModification.objects.get(
        sysname="cropping_preview"
    )
    mod = None
    if sysname:
        mod = image_mods.ImageModification.objects.get(sysname=sysname)

    # ... create/load image here ...
    image = Image.new("RGB", (cp_mod.width, cp_mod.height), "#%s" % bgcolor)

    if rel_orig_path:
        modified_path, query_params = image_mods.FileManager.modified_path(
            rel_orig_path, "cropping_preview"
        )
        orig_path_server = os.path.join(
            settings.UPLOADS_ROOT, *modified_path.split("/")
        )
        im = Image.open(orig_path_server).convert('RGB')

        if mod:
            cropping_pos = CROP_POSITIONS[mod.crop_from or 'center']
        else:
            cropping_pos = CROP_POSITIONS['center']

        image.paste(im, cropping_pos((cp_mod.width, cp_mod.height), im.size))

    buffer = StringIO()
    image.save(buffer, "PNG")
    data = buffer.getvalue()
    buffer.close()
    # serialize to HTTP response
    response = HttpResponse(content_type="image/png")
    response['Content-Disposition'] = 'filename=cropping-preview.png'
    response.write(data)
    return response


def versions(request):
    """
    Show all image modifications for an Image according.
    
    Required GET params:
    * dir - the path to the original image within filebrowser's MEDIA_ROOT
    * filename - the filename of the original image
    
    """

    # QUERY / PATH CHECK
    query = request.GET
    path = u'%s' % os.path.join(DIRECTORY, query.get('dir', ''))
    fileobject = FileObject(os.path.join(path, query.get('filename', '')))
    if path is None or not fileobject:
        if path is None:
            msg = _('The requested Folder does not exist.')
        else:
            msg = _('The requested File does not exist.')
        messages.error(request, msg)
        return HttpResponseRedirect(reverse("fb_browse"))

    return render_to_response(
        'filebrowser/versions.html', {
            'fileobject': fileobject,
            'query': query,
            'title': _(u'Versions for "%s"') % fileobject.filename,
            'settings_var': get_settings_var(),
            'breadcrumbs': get_breadcrumbs(query, path),
            'breadcrumbs_title': _(u'Versions for "%s"') % fileobject.filename
        },
        context_instance=RequestContext(request)
    )


versions = staff_member_required(never_cache(versions))


class CoordsForm(forms.Form):
    x1 = forms.IntegerField(
        min_value=0,
        widget=forms.HiddenInput,
    )
    y1 = forms.IntegerField(
        min_value=0,
        widget=forms.HiddenInput,
    )
    x2 = forms.IntegerField(
        min_value=0,
        widget=forms.HiddenInput,
    )
    y2 = forms.IntegerField(
        min_value=0,
        widget=forms.HiddenInput,
    )
    bgcolor = forms.CharField(
        label=_("Canvas color"),
        min_length=7,
        max_length=7,
        widget=forms.HiddenInput,
    )


def adjust_version(request):
    """
    (Re)crop image version and related versions
    
    Required GET params:
    * dir - the path to the original image within filebrowser's MEDIA_ROOT
    * filename - the filename of the original image
    * sysname - sysname of modification
    
    """
    # QUERY / PATH CHECK
    query = request.GET
    path = u'%s' % os.path.join(DIRECTORY, query.get('dir', ''))
    fileobject = FileObject(os.path.join(path, query.get('filename', '')))
    mod = get_object_or_404(
        image_mods.ImageModification, sysname=query.get('sysname', '')
    )
    cp_mod = get_object_or_404(
        image_mods.ImageModification, sysname="cropping_preview"
    )
    if path is None:
        if path is None:
            msg = _('The requested Folder does not exist.')
        else:
            msg = _('The requested File does not exist.')
        messages.error(request, msg)
        return HttpResponseRedirect(reverse("filebrowser:fb_browse"))
    abs_orig_path = os.path.join(
        settings.UPLOADS_ROOT, *fileobject.path.split("/")
    )

    try:
        cropping = image_mods.ImageCropping.objects.get(
            original=fileobject,
            mods=mod,
        )
    except image_mods.ImageCropping.DoesNotExist:
        cropping = None

    # DEFAULT INITIAL SELECTION
    cropping_pos = None
    if mod:
        cropping_pos = CROP_POSITIONS[mod.crop_from or 'center']
    cp_mod_path, query_params = image_mods.FileManager.modified_path(
        fileobject.path,
        "cropping_preview",
    )
    orig_im = Image.open(abs_orig_path)
    orig_size = orig_im.size
    del orig_im

    abs_cp_mod_path = os.path.join(
        settings.UPLOADS_ROOT, *cp_mod_path.split("/")
    )
    cp_im = Image.open(abs_cp_mod_path)
    (w, h) = rescaled_size = cp_im.size
    del cp_im

    rescaled_pos = cropping_pos((cp_mod.width, cp_mod.height), (w, h))

    if mod.crop and mod.width and mod.height:
        if w < h:
            h = int(w * mod.height / mod.width)
        else:
            w = int(h * mod.width / mod.height)
    x1, y1 = cropping_pos((cp_mod.width, cp_mod.height), (w, h))
    default_initial = {
        'x1': x1,
        'y1': y1,
        'x2': x1 + w,
        'y2': y1 + h,
        'bgcolor': "#ffffff",
    }
    converter = CoordsConverter(
        orig_size=orig_size,
        rescaled_size=rescaled_size,
        rescaled_pos=rescaled_pos
    )
    if request.method == "POST":
        form = CoordsForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            # create, update or delete cropping
            if cropping:
                if (
                    cleaned['x1'] == default_initial['x1'] and
                    cleaned['y1'] == default_initial['y1'] and
                    cleaned['x2'] == default_initial['x2'] and
                    cleaned['y2'] == default_initial['y2'] and
                    cleaned['bgcolor'] == default_initial['bgcolor']
                ):  # if is default, DELETE
                    cropping.delete()
                else:
                    # UPDATE
                    cropping.x1, cropping.y1 = converter.canvas_to_orig(
                        (cleaned['x1'], cleaned['y1']),
                    )
                    cropping.x2, cropping.y2 = converter.canvas_to_orig(
                        (cleaned['x2'], cleaned['y2']),
                    )
                    cropping.bgcolor = cleaned['bgcolor']
                    cropping.save()
                    cropping.mods.clear()
                    cropping.mods.add(mod)
                    for related_mod in mod.related_mods.all():
                        cropping.mods.add(related_mod)
            else:
                if not (
                    cleaned['x1'] == default_initial['x1'] and
                    cleaned['y1'] == default_initial['y1'] and
                    cleaned['x2'] == default_initial['x2'] and
                    cleaned['y2'] == default_initial['y2'] and
                    cleaned['bgcolor'] == default_initial['bgcolor']
                ):  # if is not default, CREATE
                    cropping = image_mods.ImageCropping(
                        original=fileobject,
                        bgcolor=cleaned['bgcolor'],
                    )
                    cropping.x1, cropping.y1 = converter.canvas_to_orig(
                        (cleaned['x1'], cleaned['y1']),
                    )
                    cropping.x2, cropping.y2 = converter.canvas_to_orig(
                        (cleaned['x2'], cleaned['y2']),
                    )
                    cropping.save()
                    cropping.mods.add(mod)
                    for related_mod in mod.related_mods.all():
                        cropping.mods.add(related_mod)
            # create or update modified image(s)
            mod.process_image(abs_orig_path)
            for related_mod in mod.related_mods.all():
                related_mod.process_image(abs_orig_path)
            if request.REQUEST.get("pop", "") == "1":
                # if came from FileBrowseField, redirect back to file detail
                return HttpResponseRedirect(
                    reverse("filebrowser:fb_detail") +
                    get_query_string(query.copy(), remove=["sysname"])
                )
            # else redirect back to versions
            return HttpResponseRedirect(
                reverse("fb_versions") +
                get_query_string(query.copy(), remove=["sysname"])
            )
        else:
            messages.error(request, _("Errors in the coordinates"))
    else:
        if cropping:
            initial = {
                'bgcolor':
                    cropping.bgcolor,
                'x1':
                    converter.orig_to_canvas((cropping.x1, cropping.y1), )[0],
                'y1':
                    converter.orig_to_canvas((cropping.x1, cropping.y1), )[1],
                'x2':
                    converter.orig_to_canvas((cropping.x2, cropping.y2), )[0],
                'y2':
                    converter.orig_to_canvas((cropping.x2, cropping.y2), )[1]
            }
        else:
            initial = default_initial
        form = CoordsForm(initial)

    title = _(u'Adjust the version "%(mod_title)s" for "%(filename)s"') % {
        'mod_title': mod.title,
        'filename': fileobject.filename,
    }

    return render_to_response(
        'filebrowser/adjust_version.html', {
            'default_initial': default_initial,
            'form': form,
            'mod': mod,
            'cp_mod': cp_mod,
            'fileobject': fileobject,
            'query': query,
            'title': title,
            'settings_var': get_settings_var(),
            'breadcrumbs': get_breadcrumbs(query, path),
            'breadcrumbs_title': title,
        },
        context_instance=RequestContext(request)
    )


adjust_version = staff_member_required(never_cache(adjust_version))


def delete_version(request):
    """
    Delete image version
    
    Required GET params:
    * dir - the path to the original image within filebrowser's MEDIA_ROOT
    * filename - the filename of the original image
    * sysname - sysname of modification
    
    """
    # QUERY / PATH CHECK
    query = request.GET
    path = u'%s' % os.path.join(DIRECTORY, query.get('dir', ''))
    fileobject = FileObject(os.path.join(path, query.get('filename', '')))
    mod = get_object_or_404(
        image_mods.ImageModification, sysname=query.get('sysname', '')
    )
    if path is None or not fileobject:
        if path is None:
            msg = _('The requested Folder does not exist.')
        else:
            msg = _('The requested File does not exist.')
        messages.error(request, msg)
        return HttpResponseRedirect(reverse("fb_browse"))
    orig_path = fileobject.path
    modified_path, query_params = image_mods.FileManager.modified_path(
        orig_path, mod.sysname
    )
    if request.method == "POST":
        form = forms.Form(request.POST)  # dummy form
        if form.is_valid():
            for cropping in image_mods.ImageCropping.objects.filter(
                original=fileobject,
                mods=mod,
            ):
                if cropping.mods.count() == 1:
                    cropping.delete()
            image_mods.FileManager.delete_file(modified_path)
        return HttpResponseRedirect(
            reverse("fb_versions") +
            get_query_string(query.copy(), remove=["sysname"])
        )

    title = _(u'Delete the version "%(mod_title)s" for "%(filename)s"') % {
        'mod_title': mod.title,
        'filename': fileobject.filename,
    }

    return render_to_response(
        'filebrowser/delete_version.html', {
            'mod': mod,
            'fileobject': fileobject,
            'query': query,
            'title': title,
            'settings_var': get_settings_var(),
            'breadcrumbs': get_breadcrumbs(query, path),
            'breadcrumbs_title': title,
        },
        context_instance=RequestContext(request)
    )


delete_version = staff_member_required(never_cache(delete_version))


def recrop(request):
    """
    (Re)crop image version and related versions
    
    This view has no information about the object which has the image attached.
    But a per-user unique link to this view will be formed in a template of the
    previous page only if the current user has a permission to edit the object. 
    
    Required GET params:
    * orig_path - full path of the original image within filebrowser's MEDIA_ROOT
    * sysname - sysname of modification
    * token - encrypted string ensuring that current user can modify this file
    
    Optional GET params:
    * goto_next - path where to go after recropping
    
    """

    # QUERY / PATH CHECK
    orig_path = request.GET.get('orig_path', '')
    sysname = request.GET.get('sysname', '')
    token = request.GET.get('token', '')
    goto_next = request.GET.get('goto_next', '/')

    if not orig_path:
        return HttpResponseBadRequest(ugettext("Path is not defined"))

    if not sysname:
        return HttpResponseBadRequest(
            ugettext("Modification sysname is not defined")
        )

    if not token:
        return HttpResponseBadRequest(ugettext("Token is not defined"))

    mod = get_object_or_404(image_mods.ImageModification, sysname=sysname)
    cp_mod = get_object_or_404(
        image_mods.ImageModification, sysname="cropping_preview"
    )

    if image_mods.FileManager.tokenize(
        request.user.username, orig_path
    ) != token:
        return access_denied(request)

    abs_orig_path = os.path.join(MEDIA_ROOT, *orig_path.split("/"))

    try:
        cropping = image_mods.ImageCropping.objects.get(
            original=FileObject(orig_path),
            mods=mod,
        )
    except image_mods.ImageCropping.DoesNotExist:
        cropping = None

    # DEFAULT INITIAL SELECTION
    cropping_pos = None
    if mod:
        cropping_pos = CROP_POSITIONS[mod.crop_from or 'center']

    try:
        orig_im = Image.open(abs_orig_path)
    except:
        return HttpResponseBadRequest(ugettext("Image does not exist"))
    orig_size = orig_im.size
    del orig_im

    cp_mod_path, query_params = image_mods.FileManager.modified_path(
        orig_path,
        "cropping_preview",
    )
    abs_cp_mod_path = os.path.join(MEDIA_ROOT, *cp_mod_path.split("/"))
    cp_im = Image.open(abs_cp_mod_path)
    (w, h) = rescaled_size = cp_im.size
    del cp_im

    rescaled_pos = cropping_pos((cp_mod.width, cp_mod.height), (w, h))

    if mod.crop and mod.width and mod.height:
        if w < h:
            h = int(w * mod.height / mod.width)
        else:
            w = int(h * mod.width / mod.height)
    x1, y1 = cropping_pos((cp_mod.width, cp_mod.height), (w, h))
    default_initial = {
        'x1': x1,
        'y1': y1,
        'x2': x1 + w,
        'y2': y1 + h,
        'bgcolor': "#ffffff",
    }
    converter = CoordsConverter(
        orig_size=orig_size,
        rescaled_size=rescaled_size,
        rescaled_pos=rescaled_pos
    )
    if request.method == "POST":
        form = CoordsForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            # create, update or delete cropping
            if cropping:
                if (
                    cleaned['x1'] == default_initial['x1'] and
                    cleaned['y1'] == default_initial['y1'] and
                    cleaned['x2'] == default_initial['x2'] and
                    cleaned['y2'] == default_initial['y2'] and
                    cleaned['bgcolor'] == default_initial['bgcolor']
                ):  # if is default, DELETE
                    cropping.delete()
                else:
                    # UPDATE
                    cropping.x1, cropping.y1 = converter.canvas_to_orig(
                        (cleaned['x1'], cleaned['y1']),
                    )
                    cropping.x2, cropping.y2 = converter.canvas_to_orig(
                        (cleaned['x2'], cleaned['y2']),
                    )
                    cropping.bgcolor = cleaned['bgcolor']
                    cropping.save()
                    cropping.mods.clear()
                    cropping.mods.add(mod)
                    for related_mod in mod.related_mods.all():
                        cropping.mods.add(related_mod)
            else:
                if not (
                    cleaned['x1'] == default_initial['x1'] and
                    cleaned['y1'] == default_initial['y1'] and
                    cleaned['x2'] == default_initial['x2'] and
                    cleaned['y2'] == default_initial['y2'] and
                    cleaned['bgcolor'] == default_initial['bgcolor']
                ):  # if is not default, CREATE
                    cropping = image_mods.ImageCropping(
                        original=FileObject(orig_path),
                        bgcolor=cleaned['bgcolor'],
                    )
                    cropping.x1, cropping.y1 = converter.canvas_to_orig(
                        (cleaned['x1'], cleaned['y1']),
                    )
                    cropping.x2, cropping.y2 = converter.canvas_to_orig(
                        (cleaned['x2'], cleaned['y2']),
                    )
                    cropping.save()
                    cropping.mods.add(mod)
                    for related_mod in mod.related_mods.all():
                        cropping.mods.add(related_mod)
            # create or update modified image(s)
            mod.process_image(abs_orig_path)
            for related_mod in mod.related_mods.all():
                related_mod.process_image(abs_orig_path)
            return HttpResponseRedirect(goto_next)
    else:
        if cropping:
            initial = {
                'bgcolor':
                    cropping.bgcolor,
                'x1':
                    converter.orig_to_canvas((cropping.x1, cropping.y1), )[0],
                'y1':
                    converter.orig_to_canvas((cropping.x1, cropping.y1), )[1],
                'x2':
                    converter.orig_to_canvas((cropping.x2, cropping.y2), )[0],
                'y2':
                    converter.orig_to_canvas((cropping.x2, cropping.y2), )[1]
            }
        else:
            initial = default_initial
        form = CoordsForm(initial)

    return render_to_response(
        'image_mods/recrop.html', {
            'default_initial': default_initial,
            'form': form,
            'mod': mod,
            'cp_mod': cp_mod,
            'orig_path': orig_path,
        },
        context_instance=RequestContext(request)
    )

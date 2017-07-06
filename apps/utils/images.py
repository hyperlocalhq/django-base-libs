# -*- coding: UTF-8 -*-
### DEPRECATED FILE (just for reference) ###
import os
try:
    import Image
except ImportError:
    from PIL import Image
from django.conf import settings
from django.http import Http404, HttpResponse
from django import forms
from django.utils.translation import ugettext_lazy as _, ugettext
from django.template.defaultfilters import filesizeformat

from filebrowser.settings import MEDIA_ROOT as UPLOADS_ROOT

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

PATH_TMP = getattr(
    settings,
    "PATH_TMP",
    os.path.abspath(os.path.join(settings.MEDIA_ROOT, "tmp")),
    )


def parse_dimensions(dimensions="100x100"):
    width, height = [int(x) for x in dimensions.split('x')]
    return width, height

def mask_image(im, im_mask):
    im = im.convert("RGB")
    im_mask = im_mask.convert("RGB")
    # mask is a greyscale image
    out = im.copy()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            R, G, B = im.getpixel((x,y))
            Rm, Gm, Bm = im_mask.getpixel((x,y))
            out.im.putpixel((x,y), (
                (R+Rm>255) and 255 or (R+Rm),
                (G+Gm>255) and 255 or (G+Gm),
                (B+Bm>255) and 255 or (B+Bm)
                )
            )
    return out
    
def crop_to_square(image, *args, **kwargs):
    # crop the center square
    width, height = image.size
    if width > height:
        left = int((width - height) / 2)
        top = 0
        right = left + height
        bottom = height
    else:
        left = 0
        top = int((height - width) / 2)
        right = width
        bottom = top + width
    image = image.crop((left, top, right, bottom))
    return image
    
def crop_to_rect(image, target_width, target_height, *args, **kwargs):
    # crop the center square
    new_image = image.copy()
    source_width, source_height = new_image.size
    
    w_factor = 1.0 * source_width / target_width
    h_factor = 1.0 * source_height / target_height

    if w_factor < h_factor:
        factor = w_factor
    else:
        factor = h_factor

    new_width = int(source_width / factor)
    new_height = int(source_height / factor)

    new_image = new_image.resize((new_width, new_height), Image.ANTIALIAS)
    
    x_width, x_height = new_image.size
    
    if new_width > target_width:
        left = int((new_width - target_width) / 2)
        top = 0
        right = left + target_width
        bottom = target_height
    else:
        left = 0
        top = int((new_height - target_height) / 2)
        right = target_width
        bottom = top + target_height

    """    
    print 'source_width = ' + str(source_width)
    print 'source_height = ' + str(source_height)
    print 'target_width = ' + str(target_width)
    print 'target_height = ' + str(target_height)
    print 'factor = ' + str(factor)
    print 'new_width = ' + str(new_width)
    print 'new_height = ' + str(new_height)
    
    print 'left = ' + str(left)
    print 'right = ' + str(right)
    print 'top = ' + str(top)
    print 'bottom = ' + str(bottom)
    """
    new_image = new_image.crop((left, top, right, bottom))
    return new_image

def save_png_image(uploaded_image, path_original="", path_normal="", 
                   dimensions_normal="130x130", path_small="", 
                   dimensions_small="50x50", mod_function=crop_to_square):
    tmp_path = ""

    if hasattr(uploaded_image, "im"): # uploaded_image is an image instance
        image = uploaded_image
    elif hasattr(uploaded_image, "filename"): # uploaded_image is a FileField 
        if hasattr(uploaded_image, 'tmp_filename'):
            tmp_path = os.path.join(PATH_TMP, uploaded_image.tmp_filename)
            image = Image.open(tmp_path)
        else:
            image = Image.open(StringIO.StringIO(uploaded_image.data.read()))
    else: # oldforms: uploaded_image is a dictionary
        if "tmp_filename" in uploaded_image:
            tmp_path = os.path.join(PATH_TMP, uploaded_image["tmp_filename"])
            image = Image.open(tmp_path)
        else:
            try:
                image = Image.open(StringIO.StringIO(uploaded_image.get("content")))
            except:
                # uploaded file is just given by "filename"
                image = Image.open(uploaded_image)
    if image.mode != "RGB":
        image = image.convert("RGB")
    if path_original:
        image.save(path_original, "png")

    # make a copy for thumbnail
    small = image.copy()
        
    if path_normal:
        image = mod_function(image, *parse_dimensions(dimensions_normal))
        image.save(path_normal, "png")

    if path_small:
        small = mod_function(small, *parse_dimensions(dimensions_small))
        small.save(path_small, "png")
        
    # remove the temporary file
    if tmp_path:
        os.remove(tmp_path)
    
    return image
    

def save_jpg_image(uploaded_image, path_original="", path_normal="", 
                   dimensions_normal="130x130", path_preview="", 
                   dimensions_preview="130x130", path_small="", 
                   dimensions_small="50x50", mod_function=crop_to_square):
    tmp_path = ""
    if hasattr(uploaded_image, "im"): # uploaded_image is an image instance
        image = uploaded_image
    elif hasattr(uploaded_image, "filename"): # uploaded_image is a FileField 
        if hasattr(uploaded_image, 'tmp_filename'):
            tmp_path = os.path.join(PATH_TMP, uploaded_image.tmp_filename)
            image = Image.open(tmp_path)
        else:
            image = Image.open(StringIO.StringIO(uploaded_image.data.read()))
    else: # oldforms: uploaded_image is a dictionary
        if "tmp_filename" in uploaded_image:
            tmp_path = os.path.join(PATH_TMP, uploaded_image["tmp_filename"])
            image = Image.open(tmp_path)
        else:
            try:
                image = Image.open(StringIO.StringIO(uploaded_image.get("content")))
            except:
                # uploaded file is just given by "filename"
                image = Image.open(uploaded_image)
    if image.mode != "RGB":
        image = image.convert("RGB")
    if path_original:
        image.save(path_original, "jpeg")
        

    # make a copy for thumbnail
    small = image.copy()
    preview = image.copy()
        
    if path_normal:
        #image = mod_function(image, *parse_dimensions(dimensions_normal))
        image.thumbnail(parse_dimensions(dimensions_normal), Image.ANTIALIAS)
        image.save(path_normal, "jpeg")

    if path_preview:
        #preview = mod_function(small, *parse_dimensions(dimensions_preview))
        preview.thumbnail(parse_dimensions(dimensions_preview), Image.ANTIALIAS)
        preview.save(path_preview, "jpeg")

    if path_small:
        small = mod_function(small, *parse_dimensions(dimensions_small))
        small.thumbnail(parse_dimensions(dimensions_small), Image.ANTIALIAS)
        small.save(path_small, "jpeg")
        
    if tmp_path:
        os.remove(tmp_path)
    return image

def image_view(request, width, height, filename="", mod_function=crop_to_square, mod_args=None, mod_kwargs=None):
    if not mod_kwargs:
        mod_kwargs = {}
    if not mod_args:
        mod_args = []
    if filename:
        path = os.path.join(PATH_TMP, filename)
    else:
        path = os.path.join(UPLOADS_ROOT, request.GET.get("path", ""))
    try:
        image = Image.open(path)
    except:
        raise Http404, ugettext("The image doesn't exist")
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = crop_to_rect(image, int(width), int(height))
    if mod_function:
        image = mod_function(image, *mod_args, **mod_kwargs)
    response = HttpResponse(content_type="image/png")
    response['Content-Disposition'] = "inline; filename=tmp.png"
    response['Cache-Control'] = "max-age=0"
    image.save(response, "png") # will call response.write()
    return response
    
def validate_image(
        uploaded_image,
        min_dimensions=(480, 480), # (width, height)
        max_ratio=5,
        allowed_file_types=("gif", "jpg", "jpeg", "png", "tif", "tiff", "bmp"), # lowercase file extensions
        max_file_size=1048576, # 1 MB
        ):
    messages = {
        'too-small-dimensions': _("The media file is too small. The minimal dimensions are %(width)dx%(height)d.") % {
            'width': min_dimensions[0],
            'height': min_dimensions[1],
            },
        'too-large-ratio': _("The ratio of the dimensions is too large. The maximal allowed ratio is %d:1.") % max_ratio,
        'wrong-file-type': _("The file type of the uploaded file is not valid. The allowed file types are these: %s") % ", ".join(allowed_file_types),
        'too-large-file': _("The media file is too large. The maximal allowed file size is %s.") % filesizeformat(max_file_size),
        'interlaced-not-supported': _("The interlaced PNG images are not supported for now. Please resave the image without this option and try again."),
        }
    tmp_path = ""
    if hasattr(uploaded_image, "name"): # uploaded_image is a UploadedFile
        if hasattr(uploaded_image, 'tmp_filename'):
            tmp_path = os.path.join(PATH_TMP, uploaded_image.tmp_filename)
            if tmp_path.split(".")[-1].lower() not in allowed_file_types:
                raise forms.ValidationError(messages['wrong-file-type'])
            if os.stat(tmp_path).st_size > max_file_size:
                raise forms.ValidationError(messages['too-large-file'])
            image = Image.open(tmp_path)
        else:
            if uploaded_image.name.split(".")[-1].lower() not in allowed_file_types:
                raise forms.ValidationError(messages['wrong-file-type'])
            if uploaded_image.size > max_file_size:
                raise forms.ValidationError(messages['too-large-file'])
            uploaded_image.seek(0)
            image = Image.open(StringIO.StringIO(uploaded_image.read()))
            uploaded_image.seek(0)
    else:
        if type(uploaded_image).__name__ in ("str", "unicode"):
            if uploaded_image.split(".")[-1].lower() not in allowed_file_types:
                raise forms.ValidationError(messages['wrong-file-type'])
            if os.stat(uploaded_image).st_size > max_file_size:
                raise forms.ValidationError(messages['too-large-file'])
            image = Image.open(uploaded_image)
        else:
            raise forms.ValidationError("Unknown error")

    if image.info.get("interlace", False):
        raise forms.ValidationError(messages['interlaced-not-supported'])
    width, height = image.size
    if width < min_dimensions[0] or height < min_dimensions[1]:
        raise forms.ValidationError(messages['too-small-dimensions'])
    if 1.0 * max(width, height) / min(width, height) > max_ratio:
        raise forms.ValidationError(messages['too-large-ratio'])

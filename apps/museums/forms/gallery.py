# -*- coding: UTF-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from base_libs.forms import dynamicforms
from base_libs.forms.fields import ImageField

IMAGE_MIN_DIMENSIONS = getattr(settings, "GALLERY_IMAGE_MIN_DIMENSIONS", (100,100))
STR_IMAGE_MIN_DIMENSIONS = "%s x %s" % IMAGE_MIN_DIMENSIONS

class ImageFileForm(forms.Form):
    media_file = ImageField(
        label= _("Image File"),
        help_text= _("You can upload GIF, JPG, PNG, TIFF, and BMP images. The minimal dimensions are %s px.") % STR_IMAGE_MIN_DIMENSIONS,
        required=False,
        min_dimensions=IMAGE_MIN_DIMENSIONS,
        )

    def __init__(self, *args, **kwargs):
        super(ImageFileForm, self).__init__(*args, **kwargs)
        for lang_code, lang_name in settings.FRONTEND_LANGUAGES:
            self.fields['title_%s' % lang_code] = forms.CharField(
                label=_("Title in %s") % lang_name,
                required=False,
                max_length=255,
                )
            self.fields['description_%s' % lang_code] = forms.CharField(
                label= _("Short Description in %s") % lang_name,
                required=False,
                widget=forms.Textarea(),
                )


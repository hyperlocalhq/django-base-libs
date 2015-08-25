# -*- coding: UTF-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from jetson.apps.media_gallery.forms import *

PortfolioSettings = models.get_model("media_gallery", "PortfolioSettings")
Section = models.get_model("media_gallery", "Section")
MediaGallery = models.get_model("media_gallery", "MediaGallery")


class PortfolioSettingsForm(dynamicforms.Form):
    landing_page = forms.ChoiceField(
        label=_("Landing page"),
        required=True,
        choices=PortfolioSettings._meta.get_field("landing_page").get_choices(),
    )
    landing_page_image = ImageField(
        label=_("Image for landing page"),
        help_text=_(
            "You can upload GIF, JPG, PNG, TIFF, and BMP images. The minimal dimensions are %s px.") % STR_IMAGE_MIN_DIMENSIONS,
        required=False,
        min_dimensions=IMAGE_MIN_DIMENSIONS,
    )


class SectionForm(dynamicforms.Form):
    title_en = forms.CharField(
        label=_("Title in English"),
        required=False,
        max_length=255,
    )
    title_de = forms.CharField(
        label=_("Title in German"),
        required=False,
        max_length=255,
    )
    show_title = forms.BooleanField(
        label=_("Show title"),
        required=False,
    )


class MediaGalleryForm(dynamicforms.Form):
    title_en = forms.CharField(
        label=_("Title in English"),
        required=True,
        max_length=255,
    )
    title_de = forms.CharField(
        label=_("Title in German"),
        required=True,
        max_length=255,
    )
    description_en = forms.CharField(
        label=_("Short Description in English"),
        required=False,
        widget=forms.Textarea(),
    )
    description_de = forms.CharField(
        label=_("Short Description in German"),
        required=False,
        widget=forms.Textarea(),
    )
    format = forms.ChoiceField(
        label=_("Presentation format"),
        required=True,
        choices=MediaGallery._meta.get_field("format").get_choices(),
    )
    published = forms.BooleanField(
        label=_("Published"),
        required=False,
    )
    cover_image = ImageField(
        label=_("Cover image"),
        help_text=_(
            "If unspecified, the first image from the album will be used. You can upload GIF, JPG, PNG, TIFF, and BMP images. The minimal dimensions are %s px.") % STR_IMAGE_MIN_DIMENSIONS,
        required=False,
        min_dimensions=IMAGE_MIN_DIMENSIONS,
    )

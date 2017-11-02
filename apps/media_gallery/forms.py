# -*- coding: UTF-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat
from django import forms
from django.conf import settings

from base_libs.forms import dynamicforms
from base_libs.forms.fields import ImageField, VideoField, AudioField
from base_libs.utils.misc import get_related_queryset

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from jetson.apps.utils.forms import ModelMultipleChoiceTreeField, ModelChoiceTreeField

IMAGE_MIN_DIMENSIONS = getattr(settings, "GALLERY_IMAGE_MIN_DIMENSIONS", (850, 400))
STR_IMAGE_MIN_DIMENSIONS = "%s x %s" % IMAGE_MIN_DIMENSIONS

PortfolioSettings = models.get_model("media_gallery", "PortfolioSettings")
Section = models.get_model("media_gallery", "Section")
MediaGallery = models.get_model("media_gallery", "MediaGallery")


class PortfolioFileForm(dynamicforms.Form):
    def __init__(self, *args, **kwargs):
        super(PortfolioFileForm, self).__init__(*args, **kwargs)
        for lang_code, lang_name in settings.LANGUAGES:
            self.fields['title_%s' % lang_code] = forms.CharField(
                label=_("Title in %s") % lang_name,
                required=False,
                max_length=255,
            )
            self.fields['description_%s' % lang_code] = forms.CharField(
                label=_("Short Description in %s") % lang_name,
                required=False,
                widget=forms.Textarea(),
            )


class ImageFileForm(PortfolioFileForm):
    media_file = ImageField(
        label=_("Image File"),
        help_text=_(
            "You can upload GIF, JPG, PNG, TIFF, and BMP images. The minimal dimensions are %s px.") % STR_IMAGE_MIN_DIMENSIONS,
        required=False,
        min_dimensions=IMAGE_MIN_DIMENSIONS,
    )
    external_url = forms.URLField(
        label=_("Image File"),
        help_text=_("You can link to a GIF, JPG, or PNG image."),
        required=False,
    )
    photo_author = forms.CharField(
        label=_("Photo Credits"),
        required=False,
        max_length=100,
    )

    def __init__(self, *args, **kwargs):
        super(ImageFileForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Div (
                layout.Fieldset(
                    _("Upload Image"),
                    layout.HTML("""{% include "media_gallery/includes/media_file_image_preview.html" %}"""),
                    "media_file",
                    layout.HTML("""
                        {% include "media_gallery/includes/upload_and_continue.html" %}
                        {% include "media_gallery/includes/switch_to_external.html" %}
                    """),
                    css_class="upload_media_file",
                ),
                layout.Fieldset(
                    _("Link to External Image"),
                    layout.HTML("""{% include "media_gallery/includes/media_file_image_preview.html" %}"""),
                    layout.Field("external_url", placeholder="http://"),
                    layout.HTML("""
                        {% include "media_gallery/includes/upload_and_continue.html" %}
                        {% include "media_gallery/includes/switch_to_upload.html" %}
                    """),
                    css_class="link_to_media_file",
                ),
                layout.Fieldset(
                    _("Description"),
                    "photo_author",
                    "title_de",
                    "description_de",
                    "title_en",
                    "description_en",
                ),
                bootstrap.FormActions(
                    layout.Submit("submit", _("Save"), css_class = "prepend-cancel"),
                    css_class = "button-group form-buttons"
                ),
                css_class = "media-upload"
            )
        )

    def clean_external_url(self):
        external_url = self.cleaned_data['external_url']
        if external_url:
            if external_url.split(".")[-1].lower() not in ("gif", "jpg", "jpeg", "png"):
                raise forms.ValidationError(
                    _("You can only link to GIF, JPG, and PNG files. This image format is not supported."))
        return external_url


class VideoFileForm(PortfolioFileForm):
    media_file = VideoField(
        label=_("Video File"),
        help_text=_("You can upload only FLV files."),
        required=False,
        valid_file_extensions=("flv",),
    )
    external_url = forms.URLField(
        label=_("Video File"),
        help_text=_(
            "You can link to a FLV file, Youtube video (e.g. http://www.youtube.com/watch?v=rd2izv5JBcE or http://youtu.be/rd2izv5JBcE) or Vimeo video (e.g. http://vimeo.com/17853047)."),
        required=False,
    )
    splash_image_file = ImageField(
        label=_("Illustration File"),
        help_text=_(
            "It will be used for the thumbnail. You can upload GIF, JPG, PNG, TIFF, and BMP images. The minimal dimensions are %s px.") % STR_IMAGE_MIN_DIMENSIONS,
        required=False,
        min_dimensions=IMAGE_MIN_DIMENSIONS,
    )

    def __init__(self, *args, **kwargs):
        super(VideoFileForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Div(
                layout.Fieldset(
                    _("Upload Video"),
                    layout.HTML("""{% include "media_gallery/includes/media_file_image_preview.html" %}"""),
                    "media_file",
                    layout.HTML("""
                        {% include "media_gallery/includes/upload_and_continue.html" %}
                        {% include "media_gallery/includes/switch_to_external.html" %}
                    """),
                    css_class="upload_media_file",
                ),
                layout.Fieldset(
                    _("Link to External Video"),
                    layout.HTML("""{% include "media_gallery/includes/media_file_image_preview.html" %}"""),
                    layout.Field("external_url", placeholder="http://"),
                    layout.HTML("""
                        {% include "media_gallery/includes/upload_and_continue.html" %}
                        {% include "media_gallery/includes/switch_to_upload.html" %}
                    """),
                    css_class="link_to_media_file",
                ),
                layout.Fieldset(
                    _("Upload Illustration"),
                    layout.HTML("""{% include "media_gallery/includes/splash_image_preview.html" %}"""),
                    "splash_image_file",
                    layout.HTML("""{% include "media_gallery/includes/upload_and_continue.html" %}"""),
                ),
                layout.Fieldset(
                    _("Description"),
                    "title_de",
                    "description_de",
                    "title_en",
                    "description_en",
                ),
                bootstrap.FormActions(
                    layout.Submit("submit", _("Save"), css_class = "prepend-cancel"),
                    css_class = "button-group form-buttons"
                ),
                css_class = "media-upload"
            )
        )

    def clean_external_url(self):
        external_url = self.cleaned_data['external_url']
        if external_url:
            if external_url.split(".")[-1].lower() != "flv" and ("youtu" not in external_url.lower()) and (
                    "vimeo" not in external_url.lower()):
                raise forms.ValidationError(
                    _("You can only link to FLV files, Youtube video pages or Vimeo video pages."))
        return external_url


class AudioFileForm(PortfolioFileForm):
    media_file = AudioField(
        label=_("Audio File"),
        help_text=_("You can upload only MP3 files."),
        required=False,
        valid_file_extensions=("mp3",),
    )
    external_url = forms.URLField(
        label=_("Video File"),
        help_text=_("You can link to an MP3 file."),
        required=False,
    )
    splash_image_file = ImageField(
        label=_("Illustration File"),
        help_text=_(
            "It will be used for the thumbnail of the audio file as well as for the splash image in the player. You can upload GIF, JPG, PNG, TIFF, and BMP images. The minimal dimensions are %s px.") % STR_IMAGE_MIN_DIMENSIONS,
        required=False,
        min_dimensions=IMAGE_MIN_DIMENSIONS,
    )

    def __init__(self, *args, **kwargs):
        super(AudioFileForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Div(
                layout.Fieldset(
                    _("Upload Audio"),
                    layout.HTML("""{% include "media_gallery/includes/media_file_image_preview.html" %}"""),
                    "media_file",
                    layout.HTML("""
                        {% include "media_gallery/includes/upload_and_continue.html" %}
                        {% include "media_gallery/includes/switch_to_external.html" %}
                    """),
                    css_class="upload_media_file",
                ),
                layout.Fieldset(
                    _("Link to External Audio"),
                    layout.HTML("""{% include "media_gallery/includes/media_file_image_preview.html" %}"""),
                    layout.Field("external_url", placeholder="http://"),
                    layout.HTML("""
                        {% include "media_gallery/includes/upload_and_continue.html" %}
                        {% include "media_gallery/includes/switch_to_upload.html" %}
                    """),
                    css_class="link_to_media_file",
                ),
                layout.Fieldset(
                    _("Upload Illustration"),
                    layout.HTML("""{% include "media_gallery/includes/splash_image_preview.html" %}"""),
                    "splash_image_file",
                    layout.HTML("""{% include "media_gallery/includes/upload_and_continue.html" %}"""),
                ),
                layout.Fieldset(
                    _("Description"),
                    "title_de",
                    "description_de",
                    "title_en",
                    "description_en",
                ),
                bootstrap.FormActions(
                    layout.Submit("submit", _("Save"), css_class = "prepend-cancel"),
                    css_class = "button-group form-buttons"
                ),
                css_class = "media-upload"
            )
        )

    def clean_external_url(self):
        external_url = self.cleaned_data['external_url']
        if external_url:
            if external_url.split(".")[-1].lower() != "mp3":
                raise forms.ValidationError(_("You can only link to MP3 files. This is not MP3."))
        return external_url


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
    categories = ModelMultipleChoiceTreeField(
        label=_("Categories"),
        required=False,
        queryset=get_related_queryset(MediaGallery, "categories").filter(level=0),
    )
    photo_author = forms.CharField(
        label=_("Photo Credits"),
        required=False,
        max_length=100,
    )

    def __init__(self, gallery, *args, **kwargs):
        super(MediaGalleryForm, self).__init__(*args, **kwargs)
        self.gallery = gallery

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Change Album") if gallery.pk else _("Create Album"),
                layout.HTML("""{% load image_modifications %}
                    {% if gallery.cover_image %}
                        <dt>""" + (_("Cover Image") + "") + """</dt><dd><img class="avatar" src="{{ MEDIA_URL}}{{ gallery.cover_image|modified_path:"article" }}" alt="{{ gallery.get_title|escape }}"/></dd>
                    {% else %}
                        <dt>""" + (_("Cover Image") + "") + """</dt><dd><img class="avatar" src="{{ STATIC_URL }}site/img/placeholder/gallery_square.png" alt="{{ object.get_title|escape }}"/></dd>
                    {% endif %}
                """),
                "cover_image",
                "photo_author",
                "title_de",
                "description_de",
                "title_en",
                "description_en",
                "published",
                layout.HTML(string_concat('<dt>', _("Categories"), '</dt>')),
                layout.Field(
                    "categories",
                    template="ccb_form/custom_widgets/checkboxselectmultipletree.html",
                ),
            ),
            bootstrap.FormActions(
                layout.Submit("submit", _("Save")),
            )
        )


class MediaGallerySearchForm(forms.Form):
    category = ModelChoiceTreeField(
        empty_label=_("All"),
        label=_("Category"),
        required=False,
        queryset=get_related_queryset(MediaGallery, "categories").filter(level=0),
    )

    def __init__(self, *args, **kwargs):
        super(MediaGallerySearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "GET"
        self.helper.form_id = "filter_form"
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Filter"),
                layout.Field("category", template="ccb_form/custom_widgets/filter_field.html"),
                template="ccb_form/custom_widgets/filter.html"
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Search')),
            )
        )

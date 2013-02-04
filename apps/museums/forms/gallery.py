# -*- coding: UTF-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from base_libs.forms import dynamicforms
from base_libs.forms.fields import ImageField

IMAGE_MIN_DIMENSIONS = getattr(settings, "GALLERY_IMAGE_MIN_DIMENSIONS", (100,100))
STR_IMAGE_MIN_DIMENSIONS = "%s x %s" % IMAGE_MIN_DIMENSIONS

FRONTEND_LANGUAGES = getattr(settings, "FRONTEND_LANGUAGES", settings.LANGUAGES) 

class ImageFileForm(forms.Form):
    goto_next = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
        )
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
                label=_('Title <span class="lang">%s</span>') % lang_code.upper(),
                required=False,
                max_length=255,
                )
            self.fields['description_%s' % lang_code] = forms.CharField(
                label= _('Description <span class="lang">%s</span>') % lang_code.upper(),
                required=False,
                widget=forms.Textarea(),
                )

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        layout_blocks = []

        layout_blocks.append(layout.Fieldset(
            _("Photo"),
            layout.HTML("""{% load image_modifications %}
                {% if media_file.path %}
                    <img src="{{ MEDIA_URL }}{{ media_file.path|modified_path:"gl" }}" alt="" />
                {% endif %}
            """),
            "media_file",
            "goto_next",
            layout.Row(
                css_class="div-title",
                *('title_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),
            layout.Row(
                css_class="div-description",
                *('description_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

                css_class="fieldset-media-file",
                ))

        layout_blocks.append(bootstrap.FormActions(
            layout.Submit('submit', _('Save file')),
            layout.Button('cancel', _('Cancel')),
            ))
        self.helper.layout = layout.Layout(
            *layout_blocks
            )

class ImageDeletionForm(forms.Form):
    goto_next = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
        )
    def __init__(self, *args, **kwargs):
        super(ImageDeletionForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        layout_blocks = []

        layout_blocks.append(layout.Fieldset(
            _("Delete Photo?"),
            layout.HTML("""{% load image_modifications %}
                {% if media_file.path %}
                    <img src="{{ MEDIA_URL }}{{ media_file.path|modified_path:"gl" }}" alt="" />
                    <p>Are you sure you want to delete this photo?</p>
                {% endif %}
            """),
            "goto_next",

            css_class="fieldset-media-file",
            ))

        layout_blocks.append(bootstrap.FormActions(
            layout.Submit('submit', _('Delete')),
            layout.Button('cancel', _('Cancel')),
            ))
        self.helper.layout = layout.Layout(
            *layout_blocks
            )


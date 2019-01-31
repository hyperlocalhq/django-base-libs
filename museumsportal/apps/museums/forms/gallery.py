# -*- coding: UTF-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from base_libs.forms import dynamicforms
from base_libs.forms.fields import ImageField

from museumsportal.utils.forms import PrimarySubmit
from museumsportal.utils.forms import SecondarySubmit
from museumsportal.utils.forms import SecondaryButton

from ..models import COPYRIGHT_RESTRICTION_CHOICES

COPYRIGHT_RESTRICTION_CHOICES = (('', '---------'),) + COPYRIGHT_RESTRICTION_CHOICES

IMAGE_MIN_DIMENSIONS = getattr(settings, "GALLERY_IMAGE_MIN_DIMENSIONS", (100,100))
STR_IMAGE_MIN_DIMENSIONS = "%s x %s" % IMAGE_MIN_DIMENSIONS

FRONTEND_LANGUAGES = getattr(settings, "FRONTEND_LANGUAGES", settings.LANGUAGES) 

# translatable strings to collect
_("Please enable JavaScript to use file uploader.")
_("Add Image")
_("Edit Image")
_("Crop image")
_("Delete")
_("Do you really want to delete this image?")
_("Yes, Please")
_("No, Thanks")
_("Are you sure you want to delete this photo?")
_(u"Available formats are JPG, GIF, PNG, TIFF, and BMP. Minimal size is 100 × 100 px. Optimal size is 1000 × 350 px (min).")


class ImageFileForm(forms.Form):
    goto_next = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
    )
    #media_file = ImageField(
    #    label= _("Image File"),
    #    help_text= _("You can upload GIF, JPG, PNG, TIFF, and BMP images. The minimal dimensions are %s px.") % STR_IMAGE_MIN_DIMENSIONS,
    #    required=False,
    #    min_dimensions=IMAGE_MIN_DIMENSIONS,
    #)
    media_file_path = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
    )
    author = forms.CharField(
        label=_('Copyright / Photographer'),
        required=False,
        max_length=255,
    )
    copyright_limitations = forms.CharField(
        label=_('Details of any restrictions on use (time limit) for the disclosure to third parties (Cinemarketing, Berlin online, etc.)'),
        help_text=_('If this field does not contain precise restrictions or if no restrictions are set, the rights of use are granted non-exclusively, and unrestricted in terms of time, place and content.'),
        required=False,
        max_length=255,
    )
    copyright_restrictions = forms.ChoiceField(
        label=_("Copyright restrictions"),
        choices=COPYRIGHT_RESTRICTION_CHOICES,
        required=False,
    )

    def __init__(self, media_file_obj=None, *args, **kwargs):
        self.media_file_obj = media_file_obj
        super(ImageFileForm, self).__init__(*args, **kwargs)
        for lang_code, lang_name in settings.FRONTEND_LANGUAGES:
            self.fields['title_%s' % lang_code] = forms.CharField(
                label=_('Caption <span class="lang">%s</span>') % lang_code.upper(),
                required=False,
                max_length=255,
            )
            self.fields['description_%s' % lang_code] = forms.CharField(
                label= _('Description (will be used as alt attribute) <span class="lang">%s</span>') % lang_code.upper(),
                required=False,
                widget=forms.Textarea(),
            )

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        layout_blocks = []

        fieldset_content = []  # collect multilingual divs into one list...

        fieldset_content.append(
            "media_file_path"
        )
        fieldset_content.append(
            "goto_next",
        )
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('title_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('description_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(
            "author"
        )
        fieldset_content.append(
            "copyright_limitations"
        )
        fieldset_content.append(
            "copyright_restrictions"
        )

        layout_blocks.append(layout.Fieldset(
            """{% load i18n %}
            {% if media_file %}
                {% trans "Edit Image" %}
            {% else %}
                {% trans "Add Image" %}
            {% endif %}
            """,
            layout.HTML(u"""{% load i18n base_tags image_modifications %}
            <div class="row row-md">
                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">
                    <div id="image_preview">
                        {% if media_file.path %}
                            <img class="img-responsive" src="{{ MEDIA_URL }}{{ media_file.path|modified_path:"medium" }}?now={% now "YmdHis" %}" alt="" />
                        {% endif %}
                    </div>

                    {% if not media_file.path %}
                        <div id="image_uploader">
                            <noscript>
                                <p>{% trans "Please enable JavaScript to use file uploader." %}</p>
                            </noscript>
                        </div>
                        <p id="image_help_text" class="help-block">{% trans "Available formats are JPG, GIF, PNG, TIFF, and BMP. Minimal size is 100 × 100 px. Optimal size is 1000 × 350 px (min)." %}</p>
                    {% endif %}
                </div>
                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">
                    {% if media_file.path %}
                        {% parse "{{ museum.get_url_path }}change/" as goto_next %}
                        <input type="button" id="button-id-crop-photo" class="crop btn btn-primary" data-href="{% cropping_url media_file.path "medium" request goto_next %}" value="{% trans "Crop image" %}" />&zwnj;
                    {% endif %}
                </div>
            </div>
            """),
            css_class="fieldset-media-file",
            *fieldset_content
        ))

        layout_blocks.append(bootstrap.FormActions(
            PrimarySubmit('submit', _('Save file')),
            SecondaryButton('cancel', _('Cancel')),
            layout.HTML(u"""{% load i18n base_tags image_modifications %}
                {% if media_file %}
                    {% parse "{{ museum.get_url_path }}change/" as goto_next %}
                    <input type="button" id="button-id-delete-photo" class="delete_photo btn btn btn-lg btn-info" data-href="{{ museum.get_url_path }}gallery/file_{{ media_file.get_token }}/delete/" value="{% trans "Delete" %}" />&zwnj;
                    <!-- Modal -->
                    <div id="deleteConfirmation" class="modal hide" tabindex="-1" role="dialog" aria-labelledby="deleteConfirmationLabel" aria-hidden="true">
                        <div class="modal-centered">
                            <div class="cell">
                                <div class="inner">
                                    <div class="modal-body">
                                        <p>{% trans "Do you really want to delete this image?" %}</p>
                                    </div>
                                    <div class="modal-footer">
                                        <button id="button-id-confirm-deletion" class="btn btn-primary">{% trans "Yes, Please" %}</button>
                                        <button name="cancel" class="btn" data-dismiss="modal" aria-hidden="true">{% trans "No, Thanks" %}</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>    
                {% endif %}
            """),
        ))
        self.helper.layout = layout.Layout(
            *layout_blocks
        )
        
    def clean_media_file_path(self):
        data = self.cleaned_data['media_file_path']
        if ".." in data:
            raise forms.ValidationError(_("Double dots are not allowed in the file name."))
        return data

    def clean(self):
        cleaned = self.cleaned_data
        if not cleaned.get("media_file_path") and not self.media_file_obj:
            raise forms.ValidationError(_("You need to upload a valid file."))
        return cleaned


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
            layout.HTML("""{% load i18n image_modifications %}
                {% if media_file.path %}
                    <img src="{{ MEDIA_URL }}{{ media_file.path|modified_path:"small" }}?now={% now "YmdHis" %}" alt="" />
                    <p>{% trans "Are you sure you want to delete this photo?" %}</p>
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

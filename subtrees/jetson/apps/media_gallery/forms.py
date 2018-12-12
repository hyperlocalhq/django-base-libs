# -*- coding: UTF-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils.translation import string_concat

from base_libs.forms import dynamicforms
from base_libs.forms.fields import ImageField, VideoField, AudioField
      
from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

IMAGE_MIN_DIMENSIONS = getattr(settings, "GALLERY_IMAGE_MIN_DIMENSIONS", (100,100))
STR_IMAGE_MIN_DIMENSIONS = "%s x %s" % IMAGE_MIN_DIMENSIONS


class PortfolioFileForm(dynamicforms.Form):
    def __init__(self, *args, **kwargs):
        super(PortfolioFileForm, self).__init__(*args, **kwargs)
        for lang_code, lang_name in settings.FRONTEND_LANGUAGES:
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
    # media_file = ImageField(
    #     label=_("Image File"),
    #     help_text=_("You can upload GIF, JPG, and PNG images. The minimal dimensions are %s px.") % STR_IMAGE_MIN_DIMENSIONS,
    #     required=False,
    #     min_dimensions=IMAGE_MIN_DIMENSIONS,
    # )
    media_file_path = forms.CharField(
        max_length=255,
        widget=forms.HiddenInput(),
        required=False,
        )
    external_url = forms.URLField(
        label=_("Image File"),
        help_text=_("You can link to a GIF, JPG, or PNG image."),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(ImageFileForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.form_id = "image_file_form"

        layout_bits = [
            layout.Div(
                layout.HTML("""
                    {% load i18n %}
                    <ul class="nav nav-tabs">
                        <li class="active"><a id="upload_tab" href="#upload" data-toggle="tab">{% trans "Upload" %}</a></li>
                        <li><a id="link_tab" href="#link" data-toggle="tab">{% trans "Link" %}</a></li>
                    </ul>
                """),
                layout.Div(
                    layout.Div(
                        layout.Fieldset(
                            _("Upload Image"),
                            layout.HTML(string_concat("""
                                {% load i18n image_modifications %}
                                <div id="media_file_preview">
                                {% if not media_file.external_url and media_file.get_preview_representation %}
                                    {{ media_file.get_preview_representation }}
                                {% endif %}
                                </div>
                                <div id="media_file_uploader" data-media_file_type="image">
                                    <noscript>
                                        <p>{% trans "Please enable JavaScript to use file uploader." %}</p>
                                    </noscript>
                                </div>
                                <p id="image_help_text" class="help-block">""",
                                (_("You can upload GIF, JPG, and PNG images. The minimal dimensions are %s px.") % STR_IMAGE_MIN_DIMENSIONS),
                                """</p>"""
                            )),
                            layout.Field("media_file_path"),
                        ),
                        css_id="upload", css_class="tab-pane active",
                    ),
                    layout.Div(
                        layout.Fieldset(
                            _("Link to External Image"),
                            layout.HTML("""
                                <div id="external_media_file_preview">
                                {% if media_file.external_url and media_file.get_preview_representation %}
                                    {{ media_file.get_preview_representation }}
                                {% endif %}
                                </div>
                            """),
                            layout.Field("external_url", css_class="input-block-level"),
                        ),
                        css_id="link", css_class="tab-pane",
                    ),
                    css_class="tab-content"
                ),
                css_class="tabbable",
            )
        ]
        for lang_code, lang_name in settings.FRONTEND_LANGUAGES:
            layout_bits += [layout.Fieldset(
                _("Description"),
                layout.Field('title_%s' % lang_code, css_class="input-block-level"),
                layout.Field('description_%s' % lang_code, css_class="input-block-level"),
            )]
        layout_bits += [
            bootstrap.FormActions(
                layout.Submit('submit', _('Save')),
                layout.Submit('save_add', _('Save and add another')),
                layout.HTML("""
                    {% load i18n %}
                    {% if media_file.pk %}
                        <button id="delete_media_file" class="btn btn-danger">{% trans "Delete" %}</button>&zwnj;
                    {% endif %}
                    <a href="{{ object.get_url_path }}{{ URL_ID_PORTFOLIO }}/" class="btn">{% trans "Cancel" %}</a>&zwnj;
                """),
            ),
        ]
        self.helper.layout = layout.Layout(*layout_bits)

    def clean_external_url(self):
        external_url = self.cleaned_data['external_url']
        if external_url:
            if external_url.split(".")[-1].lower() not in ("gif", "jpg", "jpeg", "png"):
                raise forms.ValidationError(_("You can only link to GIF, JPG, and PNG files. This image format is not supported."))
        return external_url


class VideoFileForm(PortfolioFileForm):
    # media_file = VideoField(
    #     label=_("Video File"),
    #     help_text=_("You can upload only FLV files."),
    #     required=False,
    #     valid_file_extensions=("flv",),
    # )
    media_file_path = forms.CharField(
        max_length=255,
        widget=forms.HiddenInput(),
        required=False,
        )
    external_url = forms.URLField(
        label=_("Video File"),
        help_text=_("You can link to a FLV file, Youtube video (e.g. http://www.youtube.com/watch?v=rd2izv5JBcE or http://youtu.be/rd2izv5JBcE) or Vimeo video (e.g. http://vimeo.com/17853047)."),
        required=False,
    )
    # splash_image_file = ImageField(
    #     label=_("Illustration File"),
    #     help_text=_("It will be used for the thumbnail. You can upload GIF, JPG, and PNG images. The minimal dimensions are %s px.") % STR_IMAGE_MIN_DIMENSIONS,
    #     required=False,
    #     min_dimensions=IMAGE_MIN_DIMENSIONS,
    # )
    splash_image_file_path = forms.CharField(
        max_length=255,
        widget=forms.HiddenInput(),
        required=False,
        )

    def __init__(self, *args, **kwargs):
        super(VideoFileForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.form_id = "video_file_form"

        layout_bits = [
            layout.Div(
                layout.HTML("""
                    {% load i18n %}
                    <ul class="nav nav-tabs">
                        <li class="active"><a id="upload_tab" href="#upload" data-toggle="tab">{% trans "Upload" %}</a></li>
                        <li><a id="link_tab" href="#link" data-toggle="tab">{% trans "Link" %}</a></li>
                    </ul>
                """),
                layout.Div(
                    layout.Div(
                        layout.Fieldset(
                            _("Upload Video"),
                            layout.HTML(string_concat("""
                                {% load i18n image_modifications %}
                                <div id="media_file_preview">
                                {% if not media_file.external_url and media_file.get_preview_representation %}
                                    {{ media_file.get_preview_representation }}
                                {% endif %}
                                </div>
                                <div id="media_file_uploader" data-media_file_type="video">
                                    <noscript>
                                        <p>{% trans "Please enable JavaScript to use file uploader." %}</p>
                                    </noscript>
                                </div>
                                <p id="image_help_text" class="help-block">""",
                                _("You can upload only FLV files."),
                                """</p>"""
                            )),
                            layout.Field("media_file_path"),
                        ),
                        css_id="upload", css_class="tab-pane active",
                    ),
                    layout.Div(
                        layout.Fieldset(
                            _("Link to External Video"),
                            layout.HTML("""
                                <div id="external_media_file_preview">
                                {% if media_file.external_url and media_file.get_preview_representation %}
                                    {{ media_file.get_preview_representation }}
                                {% endif %}
                                </div>
                            """),
                            layout.Field("external_url", css_class="input-block-level"),
                        ),
                        css_id="link", css_class="tab-pane",
                    ),
                    css_class="tab-content"
                ),
                css_class="tabbable",
            )
        ]
        layout_bits += [
            layout.Fieldset(
                _("Upload Splash Image"),
                layout.HTML(string_concat("""
                    {% load i18n image_modifications %}
                    <div id="splash_image_preview">
                        {% if media_file.splash_image_path %}
                            <img src="{{ UPLOADS_URL }}{{ media_file.splash_image_path|modified_path:"gt" }}" alt="{{ object.get_title|escape }}" />
                        {% endif %}
                    </div>
                    <div id="splash_image_uploader">
                        <noscript>
                            <p>{% trans "Please enable JavaScript to use file uploader." %}</p>
                        </noscript>
                    </div>
                    <p id="splash_image_help_text" class="help-block">""",
                    (_("You can upload GIF, JPG, and PNG images. The minimal dimensions are %s px.") % STR_IMAGE_MIN_DIMENSIONS),
                    """</p>"""
                )),
                layout.Field("splash_image_file_path"),
            ),
        ]
        for lang_code, lang_name in settings.FRONTEND_LANGUAGES:
            layout_bits += [layout.Fieldset(
                _("Description"),
                layout.Field('title_%s' % lang_code, css_class="input-block-level"),
                layout.Field('description_%s' % lang_code, css_class="input-block-level"),
            )]
        layout_bits += [
            bootstrap.FormActions(
                layout.Submit('submit', _('Save')),
                layout.Submit('save_add', _('Save and add another')),
                layout.HTML("""
                    {% load i18n %}
                    {% if media_file.pk %}
                        <button id="delete_media_file" class="btn btn-danger">{% trans "Delete" %}</button>&zwnj;
                    {% endif %}
                    <a href="{{ object.get_url_path }}{{ URL_ID_PORTFOLIO }}/" class="btn">{% trans "Cancel" %}</a>&zwnj;
                """),
            ),
        ]
        self.helper.layout = layout.Layout(*layout_bits)

    def clean_external_url(self):
        external_url = self.cleaned_data['external_url']
        if external_url:
            if external_url.split(".")[-1].lower() != "flv" and ("youtu" not in external_url.lower()) and ("vimeo" not in external_url.lower()):
                raise forms.ValidationError(_("You can only link to FLV files, Youtube video pages or Vimeo video pages."))
        return external_url


class AudioFileForm(PortfolioFileForm):
    media_file_path = forms.CharField(
        max_length=255,
        widget=forms.HiddenInput(),
        required=False,
        )
    # media_file = AudioField(
    #     label=_("Audio File"),
    #     help_text=_("You can upload only MP3 files."),
    #     required=False,
    #     valid_file_extensions=("mp3",),
    # )
    external_url = forms.URLField(
        label=_("Video File"),
        help_text=_("You can link to an MP3 file."),
        required=False,
    )
    # splash_image_file = ImageField(
    #     label=_("Illustration File"),
    #     help_text=_("It will be used for the thumbnail of the audio file as well as for the splash image in the player. You can upload GIF, JPG, and PNG images. The minimal dimensions are %s px.") % STR_IMAGE_MIN_DIMENSIONS,
    #     required=False,
    #     min_dimensions=IMAGE_MIN_DIMENSIONS,
    # )
    splash_image_file_path = forms.CharField(
        max_length=255,
        widget=forms.HiddenInput(),
        required=False,
        )

    def __init__(self, *args, **kwargs):
        super(AudioFileForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.form_id = "video_file_form"

        layout_bits = [
            layout.Div(
                layout.HTML("""
                    {% load i18n %}
                    <ul class="nav nav-tabs">
                        <li class="active"><a id="upload_tab" href="#upload" data-toggle="tab">{% trans "Upload" %}</a></li>
                        <li><a id="link_tab" href="#link" data-toggle="tab">{% trans "Link" %}</a></li>
                    </ul>
                """),
                layout.Div(
                    layout.Div(
                        layout.Fieldset(
                            _("Upload Audio"),
                            layout.HTML(string_concat("""
                                {% load i18n image_modifications %}
                                <div id="media_file_preview">
                                {% if not media_file.external_url and media_file.get_preview_representation %}
                                    {{ media_file.get_preview_representation }}
                                {% endif %}
                                </div>
                                <div id="media_file_uploader" data-media_file_type="audio">
                                    <noscript>
                                        <p>{% trans "Please enable JavaScript to use file uploader." %}</p>
                                    </noscript>
                                </div>
                                <p id="image_help_text" class="help-block">""",
                                _("You can upload only MP3 files."),
                                """</p>"""
                            )),
                            layout.Field("media_file_path"),
                        ),
                        css_id="upload", css_class="tab-pane active",
                    ),
                    layout.Div(
                        layout.Fieldset(
                            _("Link to External Audio"),
                            layout.HTML("""
                                <div id="external_media_file_preview">
                                {% if media_file.external_url and media_file.get_preview_representation %}
                                    {{ media_file.get_preview_representation }}
                                {% endif %}
                                </div>
                            """),
                            layout.Field("external_url", css_class="input-block-level"),
                        ),
                        css_id="link", css_class="tab-pane",
                    ),
                    css_class="tab-content"
                ),
                css_class="tabbable",
            )
        ]
        layout_bits += [
            layout.Fieldset(
                _("Upload Splash Image"),
                layout.HTML(string_concat("""
                    {% load i18n image_modifications %}
                    <div id="splash_image_preview">
                        {% if media_file.splash_image_path %}
                            <img src="{{ UPLOADS_URL }}{{ media_file.splash_image_path|modified_path:"gt" }}" alt="{{ object.get_title|escape }}" />
                        {% endif %}
                    </div>
                    <div id="splash_image_uploader">
                        <noscript>
                            <p>{% trans "Please enable JavaScript to use file uploader." %}</p>
                        </noscript>
                    </div>
                    <p id="splash_image_help_text" class="help-block">""",
                    (_("You can upload GIF, JPG, and PNG images. The minimal dimensions are %s px.") % STR_IMAGE_MIN_DIMENSIONS),
                    """</p>"""
                )),
                layout.Field("splash_image_file_path"),
            ),
        ]
        for lang_code, lang_name in settings.FRONTEND_LANGUAGES:
            layout_bits += [layout.Fieldset(
                _("Description"),
                layout.Field('title_%s' % lang_code, css_class="input-block-level"),
                layout.Field('description_%s' % lang_code, css_class="input-block-level"),
            )]
        layout_bits += [
            bootstrap.FormActions(
                layout.Submit('submit', _('Save')),
                layout.Submit('save_add', _('Save and add another')),
                layout.HTML("""
                    {% load i18n %}
                    {% if media_file.pk %}
                        <button id="delete_media_file" class="btn btn-danger">{% trans "Delete" %}</button>&zwnj;
                    {% endif %}
                    <a href="{{ object.get_url_path }}{{ URL_ID_PORTFOLIO }}/" class="btn">{% trans "Cancel" %}</a>&zwnj;
                """),
            ),
        ]
        self.helper.layout = layout.Layout(*layout_bits)

    def clean_external_url(self):
        external_url = self.cleaned_data['external_url']
        if external_url:
            if external_url.split(".")[-1].lower() != "mp3":
                raise forms.ValidationError(_("You can only link to MP3 files. This is not MP3."))
        return external_url

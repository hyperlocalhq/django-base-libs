# -*- coding: UTF-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from base_libs.forms import dynamicforms
from base_libs.forms.fields import ImageField

from ruhrbuehnen.utils.forms import PrimarySubmit
from ruhrbuehnen.utils.forms import SecondarySubmit
from ruhrbuehnen.utils.forms import SecondaryButton

IMAGE_MIN_DIMENSIONS = getattr(
    settings, "GALLERY_IMAGE_MIN_DIMENSIONS", (100, 100)
)
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
_(u"Available formats are JPG, GIF, and PNG.")
_(u"Minimal size is 148 × 148 px.")
_(u"Optimal size is 680 × 375 px (min).")
_(u"Size of a video should be 640 × 360 px.")

from ruhrbuehnen.apps.locations.models import COPYRIGHT_RESTRICTION_CHOICES

COPYRIGHT_RESTRICTION_CHOICES = (('', '---------'),
                                ) + COPYRIGHT_RESTRICTION_CHOICES

# TODO: use https://css-tricks.com/NetMag/FluidWidthVideo/Article-FluidWidthVideo.php for responsive video


class VideoForm(forms.Form):
    goto_next = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
    )
    link_or_embed = forms.CharField(
        # label=_("Link or embed code"),
        label=_("Embed code"),
        widget=forms.Textarea(),
        required=True,
    )

    def __init__(self, media_file_obj=None, *args, **kwargs):
        self.media_file_obj = media_file_obj
        super(VideoForm, self).__init__(*args, **kwargs)
        for lang_code, lang_name in settings.FRONTEND_LANGUAGES:
            self.fields['title_%s' % lang_code] = forms.CharField(
                label=_('Title <span class="lang">%s</span>') %
                lang_code.upper(),
                required=False,
                max_length=255,
            )
        self.fields['title_%s' % settings.LANGUAGE_CODE].required = True

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        layout_blocks = []

        fieldset_content = [
            "goto_next",
            layout.Row(
                css_class="row-md",
                *[
                    layout.Div(
                        layout.Field('title_%s' % lang_code),
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ) for lang_code, lang_name in FRONTEND_LANGUAGES
                ]
            ),
            layout.Row(
                layout.Div(
                    layout.Field('link_or_embed'),
                    css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12",
                ),
                layout.HTML(
                    u"""{% load i18n %}
            <div class="col-xs-12" style="margin-top:-10px;"><small>{% trans "Size of a video should be 640 × 360 px." %}</small></div>
            """
                ),
                css_class="row-md"
            )
        ]  # collect multilingual divs into one list...

        layout_blocks.append(
            layout.Fieldset(
                """{% load i18n %}
            {% if media_file %}
                {% trans "Edit Video/Audio" %}
            {% else %}
                {% trans "Add Video/Audio" %}
            {% endif %}
            """,
                layout.HTML(
                    u"""{% load i18n base_tags image_modifications %}
            <div class="row row-md">
                <div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">
                    <div id="video_preview">
                        {% if media_file.get_embed %}
                            {{ media_file.get_embed|safe }}
                        {% endif %}
                    </div>
                </div>
            </div>
            """
                ),
                css_class="fieldset-media-file",
                *fieldset_content
            )
        )

        layout_blocks.append(
            bootstrap.FormActions(
                PrimarySubmit('submit', _('Save file')),
                SecondarySubmit('cancel', _('Cancel')),
                layout.HTML(
                    u"""{% load i18n base_tags image_modifications %}
                {% if media_file %}
                    {% if event %}
                        <input type="button" id="button-id-delete-video" class="delete_photo btn btn-lg btn-info" data-href="{% url "event_delete_video" slug=production.slug event_id=event.pk mediafile_token=media_file.get_token %}" value="{% trans "Delete" %}" />&zwnj;
                    {% else %}
                        <input type="button" id="button-id-delete-video" class="delete_photo btn btn-lg btn-info" data-href="{% url "production_delete_video" slug=production.slug mediafile_token=media_file.get_token %}" value="{% trans "Delete" %}" />&zwnj;
                    {% endif %}
                    <!-- Modal -->
                    <div id="deleteConfirmation" class="modal hide" tabindex="-1" role="dialog" aria-labelledby="deleteConfirmationLabel" aria-hidden="true">
                        <div class="modal-centered">
                            <div class="cell">
                                <div class="inner">
                                    <div class="modal-body">
                                        <p>{% trans "Do you really want to delete this video/audio?" %}</p>
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
            """
                ),
            )
        )
        self.helper.layout = layout.Layout(*layout_blocks)

    def get_embed(self):
        from pyoembed import oEmbed, PyOembedException
        link_or_embed = self.cleaned_data['link_or_embed']
        if link_or_embed.startswith("http"):
            try:
                # maxwidth and maxheight are optional.
                data = oEmbed(link_or_embed, maxwidth=640, maxheight=480)
            except PyOembedException, e:
                pass
            except:  # catch any other exception, for example in BeatifulSoup
                pass
            else:
                if data['type'] in ('video', 'audio'):
                    return data['html']
        return link_or_embed


class VideoDeletionForm(forms.Form):
    goto_next = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(VideoDeletionForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        layout_blocks = [
            layout.Fieldset(
                _("Delete Video/Audio?"),
                layout.HTML(
                    """{% load image_modifications %}
                {% if media_file.link_or_embed %}
                    <p>Are you sure you want to delete this video?</p>
                {% endif %}
            """
                ),
                "goto_next",
                css_class="fieldset-media-file",
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Delete')),
                layout.Button('cancel', _('Cancel')),
            )
        ]

        self.helper.layout = layout.Layout(*layout_blocks)


class StreamingForm(forms.Form):
    goto_next = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
    )
    link_or_embed = forms.CharField(
        label=_("Link or embed code"),
        widget=forms.Textarea(),
        required=True,
    )

    def __init__(self, media_file_obj=None, *args, **kwargs):
        self.media_file_obj = media_file_obj
        super(StreamingForm, self).__init__(*args, **kwargs)
        for lang_code, lang_name in settings.FRONTEND_LANGUAGES:
            self.fields['title_%s' % lang_code] = forms.CharField(
                label=_('Title <span class="lang">%s</span>') %
                lang_code.upper(),
                required=False,
                max_length=255,
            )

        self.fields['title_%s' % settings.LANGUAGE_CODE].required = True

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        layout_blocks = []

        fieldset_content = [
            "goto_next",
            layout.Row(
                css_class="row-md",
                *[
                    layout.Div(
                        layout.Field('title_%s' % lang_code),
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ) for lang_code, lang_name in FRONTEND_LANGUAGES
                ]
            ),
            layout.Row(
                layout.Div(
                    layout.Field('link_or_embed'),
                    css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12",
                ),
                css_class="row-md"
            )
        ]  # collect multilingual divs into one list...

        layout_blocks.append(
            layout.Fieldset(
                """{% load i18n %}
            {% if media_file %}
                {% trans "Edit Live Stream" %}
            {% else %}
                {% trans "Add Live Stream" %}
            {% endif %}
            """,
                layout.HTML(
                    u"""{% load i18n base_tags image_modifications %}
            <div class="row row-md">
                <div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">
                    <div id="video_preview">
                        {% if media_file.get_embed %}
                            {{ media_file.get_embed|safe }}
                        {% endif %}
                    </div>
                </div>
            </div>
            """
                ),
                css_class="fieldset-media-file",
                *fieldset_content
            )
        )

        layout_blocks.append(
            bootstrap.FormActions(
                PrimarySubmit('submit', _('Save file')),
                SecondarySubmit('cancel', _('Cancel')),
                layout.HTML(
                    u"""{% load i18n base_tags image_modifications %}
                {% if media_file %}
                    {% if event %}
                        <input type="button" id="button-id-delete-streaming" class="delete_photo btn btn-lg btn-info" data-href="{% url "event_delete_streaming" slug=production.slug event_id=event.pk mediafile_token=media_file.get_token %}" value="{% trans "Delete" %}" />&zwnj;
                    {% else %}
                        <input type="button" id="button-id-delete-streaming" class="delete_photo btn btn-lg btn-info" data-href="{% url "production_delete_streaming" slug=production.slug mediafile_token=media_file.get_token %}" value="{% trans "Delete" %}" />&zwnj;
                    {% endif %}
                    <!-- Modal -->
                    <div id="deleteConfirmation" class="modal hide" tabindex="-1" role="dialog" aria-labelledby="deleteConfirmationLabel" aria-hidden="true">
                        <div class="modal-centered">
                            <div class="cell">
                                <div class="inner">
                                    <div class="modal-body">
                                        <p>{% trans "Do you really want to delete this live stream?" %}</p>
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
            """
                ),
            )
        )
        self.helper.layout = layout.Layout(*layout_blocks)

    def get_embed(self):
        from pyoembed import oEmbed, PyOembedException
        link_or_embed = self.cleaned_data['link_or_embed']
        if link_or_embed.startswith("http"):
            try:
                # maxwidth and maxheight are optional.
                data = oEmbed(link_or_embed, maxwidth=640, maxheight=480)
            except PyOembedException, e:
                pass
            except:  # catch any other exception, for example in BeatifulSoup
                pass
            else:
                if data['type'] == 'video':
                    return data['html']
        return link_or_embed


class StreamingDeletionForm(forms.Form):
    goto_next = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(StreamingDeletionForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        layout_blocks = [
            layout.Fieldset(
                _("Delete Live Streaming?"),
                layout.HTML(
                    """{% load image_modifications %}
                {% if media_file.link_or_embed %}
                    <p>Are you sure you want to delete this live streaming?</p>
                {% endif %}
            """
                ),
                "goto_next",
                css_class="fieldset-media-file",
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Delete')),
                layout.Button('cancel', _('Cancel')),
            )
        ]

        self.helper.layout = layout.Layout(*layout_blocks)


class ImageForm(forms.Form):
    goto_next = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
    )
    media_file_path = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
    )
    author = forms.CharField(
        label=_('Copyright / Photographer'),
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
        super(ImageForm, self).__init__(*args, **kwargs)
        for lang_code, lang_name in settings.FRONTEND_LANGUAGES:
            self.fields['title_%s' % lang_code] = forms.CharField(
                label=_('Caption <span class="lang">%s</span>') %
                lang_code.upper(),
                required=False,
                max_length=255,
            )
            self.fields['description_%s' % lang_code] = forms.CharField(
                label=_(
                    'Description (will be used as alt attribute) <span class="lang">%s</span>'
                ) % lang_code.upper(),
                required=False,
                widget=forms.Textarea(),
            )

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        layout_blocks = []

        fieldset_content = [
            "media_file_path", "goto_next",
            layout.Row(
                css_class="row-md",
                *[
                    layout.Div(
                        layout.Field('title_%s' % lang_code),
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ) for lang_code, lang_name in FRONTEND_LANGUAGES
                ]
            ),
            layout.Row(
                css_class="row-md",
                *[
                    layout.Div(
                        layout.Field('description_%s' % lang_code),
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ) for lang_code, lang_name in FRONTEND_LANGUAGES
                ]
            ), "author", "copyright_restrictions"
        ]  # collect multilingual divs into one list...

        layout_blocks.append(
            layout.Fieldset(
                """{% load i18n %}
            {% if media_file %}
                {% trans "Edit Image" %}
            {% else %}
                {% trans "Add Image" %}
            {% endif %}
            """,
                layout.HTML(
                    u"""{% load i18n base_tags image_modifications %}
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
                        <p id="image_help_text" class="help-block">{% trans "Available formats are JPG, GIF, and PNG." %}<br/>{% trans "Minimal size is 148 × 148 px." %} {% trans "Optimal size is 680 × 375 px (min)." %}</p>
                    {% endif %}
                </div>
                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">
                    {% if media_file.path %}
                        {% if event %}
                            {% parse "{{ event.get_url_path }}change/gallery/" as goto_next %}
                        {% else %}
                            {% parse "{{ production.get_url_path }}gallery/" as goto_next %}
                        {% endif %}
                        <!--<input type="button" id="button-id-crop-photo" class="crop btn btn-primary" data-href="{% cropping_url media_file.path "medium" request goto_next %}" value="{% trans "Crop image" %}" />&zwnj;-->
                    {% endif %}
                </div>
            </div>
            """
                ),
                css_class="fieldset-media-file",
                *fieldset_content
            )
        )

        layout_blocks.append(
            bootstrap.FormActions(
                PrimarySubmit('submit', _('Save file')),
                SecondarySubmit('cancel', _('Cancel')),
                layout.HTML(
                    u"""{% load i18n base_tags image_modifications %}
                {% if media_file %}
                    {% if event %}
                        <input type="button" id="button-id-delete-photo" class="delete_photo btn btn-lg btn-info" data-href="{% url "event_delete_image" slug=production.slug event_id=event.pk mediafile_token=media_file.get_token %}" value="{% trans "Delete" %}" />&zwnj;
                    {% else %}
                        <input type="button" id="button-id-delete-photo" class="delete_photo btn btn-lg btn-info" data-href="{% url "production_delete_image" slug=production.slug mediafile_token=media_file.get_token %}" value="{% trans "Delete" %}" />&zwnj;
                    {% endif %}
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
            """
                ),
            )
        )
        self.helper.layout = layout.Layout(*layout_blocks)

    def clean_media_file_path(self):
        data = self.cleaned_data['media_file_path']
        if ".." in data:
            raise forms.ValidationError(
                _("Double dots are not allowed in the file name.")
            )
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
        layout_blocks = [
            layout.Fieldset(
                _("Delete Photo?"),
                layout.HTML(
                    """{% load image_modifications %}
                {% if media_file.path %}
                    <img src="{{ MEDIA_URL }}{{ media_file.path|modified_path:"small" }}?now={% now "YmdHis" %}" alt="" />
                    <p>Are you sure you want to delete this photo?</p>
                {% endif %}
            """
                ),
                "goto_next",
                css_class="fieldset-media-file",
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Delete')),
                layout.Button('cancel', _('Cancel')),
            )
        ]

        self.helper.layout = layout.Layout(*layout_blocks)


class PDFForm(forms.Form):
    goto_next = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
    )
    media_file_path = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
    )

    def __init__(self, media_file_obj=None, *args, **kwargs):
        self.media_file_obj = media_file_obj
        super(PDFForm, self).__init__(*args, **kwargs)
        for lang_code, lang_name in settings.FRONTEND_LANGUAGES:
            self.fields['title_%s' % lang_code] = forms.CharField(
                label=_('Title <span class="lang">%s</span>') %
                lang_code.upper(),
                required=False,
                max_length=255,
            )

        self.fields['title_%s' % settings.LANGUAGE_CODE].required = True

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        layout_blocks = []

        fieldset_content = [
            "media_file_path", "goto_next",
            layout.Row(
                css_class="row-md",
                *[
                    layout.Div(
                        layout.Field('title_%s' % lang_code),
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ) for lang_code, lang_name in FRONTEND_LANGUAGES
                ]
            )
        ]  # collect multilingual divs into one list...

        layout_blocks.append(
            layout.Fieldset(
                """{% load i18n %}
            {% if media_file %}
                {% trans "Edit PDF Document" %}
            {% else %}
                {% trans "Add PDF Document" %}
            {% endif %}
            """,
                layout.HTML(
                    u"""{% load i18n base_tags image_modifications %}
            <div class="row row-md">
                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">
                    <div id="pdf_preview">
                        {% if media_file.path %}
                            <a href="{{ MEDIA_URL }}{{ media_file.path.path }}" target="_blank">
                                <img class="img-responsive" src="{{ STATIC_URL }}site/img/pdf.png" alt="" />
                            </a>
                        {% endif %}
                    </div>
                    {% if not media_file.path %}
                        <div id="pdf_uploader">
                            <noscript>
                                <p>{% trans "Please enable JavaScript to use file uploader." %}</p>
                            </noscript>
                        </div>
                        <p id="image_help_text" class="help-block">{% trans "Available format is PDF." %}</p>
                    {% endif %}
                </div>
            </div>
            """
                ),
                css_class="fieldset-media-file",
                *fieldset_content
            )
        )

        layout_blocks.append(
            bootstrap.FormActions(
                PrimarySubmit('submit', _('Save file')),
                SecondarySubmit('cancel', _('Cancel')),
                layout.HTML(
                    u"""{% load i18n base_tags image_modifications %}
                {% if media_file %}
                    {% if event %}
                        <input type="button" id="button-id-delete-pdf" class="delete_photo btn btn-lg btn-info" data-href="{% url "event_delete_pdf" slug=production.slug event_id=event.pk mediafile_token=media_file.get_token %}" value="{% trans "Delete" %}" />&zwnj;
                    {% else %}
                        <input type="button" id="button-id-delete-pdf" class="delete_photo btn btn-lg btn-info" data-href="{% url "production_delete_pdf" slug=production.slug mediafile_token=media_file.get_token %}" value="{% trans "Delete" %}" />&zwnj;
                    {% endif %}
                    <!-- Modal -->
                    <div id="deleteConfirmation" class="modal hide" tabindex="-1" role="dialog" aria-labelledby="deleteConfirmationLabel" aria-hidden="true">
                        <div class="modal-centered">
                            <div class="cell">
                                <div class="inner">
                                    <div class="modal-body">
                                        <p>{% trans "Do you really want to delete this document?" %}</p>
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
            """
                ),
            )
        )
        self.helper.layout = layout.Layout(*layout_blocks)

    def clean_media_file_path(self):
        data = self.cleaned_data['media_file_path']
        if ".." in data:
            raise forms.ValidationError(
                _("Double dots are not allowed in the file name.")
            )
        return data

    def clean(self):
        cleaned = self.cleaned_data
        if not cleaned.get("media_file_path") and not self.media_file_obj:
            raise forms.ValidationError(_("You need to upload a valid file."))
        return cleaned


class PDFDeletionForm(forms.Form):
    goto_next = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(PDFDeletionForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        layout_blocks = [
            layout.Fieldset(
                _("Delete PDF Document?"),
                layout.HTML(
                    """{% load image_modifications %}
                {% if media_file.path %}
                    <a href="{{ MEDIA_URL }}{{ media_file.path.path }}" target="_blank">
                        <img class="img-responsive" src="{{ STATIC_URL }}site/img/pdf.png" alt="" />
                    </a>
                    <p>Are you sure you want to delete this PDF document?</p>
                {% endif %}
            """
                ),
                "goto_next",
                css_class="fieldset-media-file",
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Delete')),
                layout.Button('cancel', _('Cancel')),
            )
        ]

        self.helper.layout = layout.Layout(*layout_blocks)

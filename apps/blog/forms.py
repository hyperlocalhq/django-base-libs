# -*- coding: UTF-8 -*-
from crispy_forms import layout, bootstrap
from crispy_forms.helper import FormHelper
from django import forms
from django.conf import settings
from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from base_libs.forms import dynamicforms
from base_libs.forms.fields import ImageField
from tagging.forms import TagField
from tagging_autocomplete.widgets import TagAutocomplete

from ckeditor_uploader.widgets import CKEditorUploadingWidget

Post = apps.get_model("blog", "Post")

MIN_LOGO_SIZE = getattr(settings, "LOGO_SIZE", (850, 400))
STR_MIN_LOGO_SIZE = "%sx%s" % MIN_LOGO_SIZE


class BlogPostForm(dynamicforms.Form):
    title = forms.CharField(
        label=_("Title"),
        required=True,
        max_length=100,
    )
    image = ImageField(
        label=_("Main Photo"),
        help_text=_(
            "You can upload GIF, JPG, and PNG images. The minimal dimensions are %s px.") % STR_MIN_LOGO_SIZE,
        required=False,
        min_dimensions=MIN_LOGO_SIZE,
    )
    tmp_image_filename = forms.CharField(
        required=False,
        max_length=255,
        widget=forms.HiddenInput(),
    )
    image_author = forms.CharField(
        label=_("Photo Credits"),
        required=False,
        max_length=100,
    )
    tags = TagField(
        label=_("Tags"),
        required=False,
        max_length=200,
        help_text=_(
            "Use commas to separate your tags. Tags can have multiple words. For example: 'one, two, three apples' would define three tags."),
        widget=TagAutocomplete,
    )
    body = forms.CharField(
        label=_("Body"),
        required=True,
        widget=CKEditorUploadingWidget(
            config_name="basic",
            external_plugin_resources=getattr(settings, 'CKEDITOR_EXTERNAL_PLUGIN_SOURCES', [])
        ),
    )
    status = forms.ChoiceField(
        label=_("Status"),
        required=True,
        choices=Post._meta.get_field("status").get_choices(),
    )

    published_from = forms.DateTimeField(
        label=_("publishing date"),
        help_text=_(
            "Please use the format 'yyyy-mm-dd hh:mi:ss'. If not provided and the status is set to 'published', the post will be published immediately."),
        required=False,
    )

    published_till = forms.DateTimeField(
        label=_("expire date"),
        help_text=_(
            "Please use the format 'yyyy-mm-dd hh:mi:ss'. If not provided and the status is set to 'published', the post will be published forever."),
        required=False,
    )

    # enable_comment_form = forms.BooleanField(
    #     label=_("Enable comment form"),
    #     required=False,
    #     )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.action = ''
        self.helper.method = 'POST'
        self.helper.form_tag = False
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                '''{% load i18n %}
                    {% if form_handler_action == "new" %}
                        {% trans "Post To the Blog" %}
                    {% else %}
                        {% if form_handler_action == "edit" %}
                            {% trans "Edit Post" %}
                        {% endif %}
                    {% endif %}
                ''',
                "title",
                "image",
                layout.HTML("""{% load image_modifications %}
                    {% if form.tmp_image_filename.data %}
                        <dt>&nbsp;</dt>
                        <dd>
                            <img src="/{{ LANGUAGE_CODE }}/helper/tmpimage/{{ form.tmp_image_filename.data }}/800x600/" alt="" />
                        </dd>
                    {% elif current_post.image %}
                        <dt>&nbsp;</dt>
                        <dd>
                            <img src="{{ UPLOADS_URL }}{{ current_post.image|modified_path:'article' }}" alt="" />
                        </dd>
                    {% else %}
                        <dt>&nbsp;</dt>
                        <dd>
                            <img src="{{ STATIC_URL }}site/img/placeholder/event.png" alt="" />
                        </dd>
                    {% endif %}
                """),
                "tmp_image_filename",
                "image_author",
                layout.Field("body", css_class="tiny_mce_responsive"),
                "tags",
                "status",
                # "enable_comment_form",
            ),
            layout.HTML('''
                <input
                    type="hidden"
                    name="{{ hash_field }}"
                    value="{{ hash_value }}"
                />
                <input
                    type="hidden"
                    name="goto_next"
                    value="{% if goto_next %}{{ goto_next }}{% else %}/blog/{% endif %}"
                />
            '''),
            bootstrap.FormActions(
                layout.Submit('submit_preview', _('Preview')),
                layout.Submit('submit_cancel', _('Cancel'), css_class="btn-default"),
                css_class="button-group form-buttons"
            ),
        )

        super(BlogPostForm, self).__init__(*args, **kwargs)

    def clean_tmp_image_filename(self):
        value = self.cleaned_data['tmp_image_filename']
        if "/" in value:
            # quick security check ensuring that there are no relative paths instead of just a filename
            raise forms.ValidationError(_("Temporary image filename is invalid"))
        return value

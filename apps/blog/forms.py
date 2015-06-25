# -*- coding: UTF-8 -*-
import datetime

from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from base_libs.forms import dynamicforms

from tagging.forms import TagField
from tagging_autocomplete.widgets import TagAutocomplete

Post = models.get_model("blog", "Post")

class BlogPostForm(dynamicforms.Form):
    title = forms.CharField(
        label=_("Title"),
        required=True,
        max_length=100,
        )
    tags = TagField(
        label=_("Tags"),
        required=False,
        max_length=200,
        help_text=_("Use commas to separate your tags. Tags can have multiple words. For example: 'one, two, three apples' would define three tags."),
        widget=TagAutocomplete,
        )
    body = forms.CharField(
        label= _("Body"),
        required=True,
        widget=forms.Textarea(),
        )
    status = forms.ChoiceField(
        label=_("Status"),
        required=True,
        choices=Post._meta.get_field("status").get_choices(),
        )
  
    published_from = forms.DateTimeField(
        label=_("publishing date"),
        help_text=_("Please use the format 'yyyy-mm-dd hh:mi:ss'. If not provided and the status is set to 'published', the post will be published immediately."),
        required=False,
        )

    published_till = forms.DateTimeField(
        label=_("expire date"),
                help_text=_("Please use the format 'yyyy-mm-dd hh:mi:ss'. If not provided and the status is set to 'published', the post will be published forever."),
        required=False,
        )
    enable_comment_form = forms.BooleanField(
        label=_("Enable comment form"),
        required=False,
        )
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = layout.Layout(
            layout.HTML(
                """
                {% load i18n %}
                <fieldset>
                    <legend>
                        {% if form_handler_action == "new" %}
                            {% trans "Post To the Blog" %}
                        {% else %}
                            {% if form_handler_action == "edit" %}
                                {% trans "Edit Post" %}
                            {% endif %}
                        {% endif %}
                    </legend>
                """,
                ),
            layout.Div(
                "title",
                "body",
                "tags",
                "enable_comment_form",
                "status",
                "published_from",
                "published_till",
                ),
            layout.HTML("</fieldset>"),
            bootstrap.FormActions(
                layout.HTML("""
                    {% load i18n %}
                    <input id="id_preview" class="btn btn-primary" type="submit" name="{{ preview_stage_field }}" value="{% filter upper %}{% trans 'Preview' %}{% endfilter %}" />&zwnj;
                    <input id="id_cancel" type="submit" class="btn btn-warning" name="{{ cancel_stage_field }}" value="{% filter upper %}{% trans 'Cancel' %}{% endfilter %}" />&zwnj;
                    <input type="hidden" name="{{ hash_field }}" value="{{ hash_value }}" />
                    <input type="hidden" name="goto_next" value="{% if goto_next %}{{ goto_next }}{% else %}/blog/{% endif %}" />
                    """),
                )
            )
        
        super(BlogPostForm, self).__init__(*args, **kwargs)

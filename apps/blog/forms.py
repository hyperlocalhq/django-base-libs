import datetime
from django import forms
from django.utils.translation import ugettext_lazy as _

from base_libs.forms import dynamicforms

from tagging.forms import TagField
from tagging_autocomplete.widgets import TagAutocomplete

from jetson.apps.blog.models import Post

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
    

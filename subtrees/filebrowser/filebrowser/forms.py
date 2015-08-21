# coding: utf-8

# PYTHON IMPORTS
import os
import re

# DJANGO IMPORTS
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

# CRISPY FORMS IMPORTS
from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

# FILEBROWSER IMPORTS
from filebrowser.settings import FOLDER_REGEX
from filebrowser.utils import convert_filename

ALNUM_NAME_RE = re.compile(FOLDER_REGEX, re.U)

FileDescription = models.get_model("filebrowser", "FileDescription")

# CHOICES
TRANSPOSE_CHOICES = (
    ("", u"-----"),
    ("0", _(u"Flip horizontal")),
    ("1", _(u"Flip vertical")),
    ("2", _(u"Rotate 90° CW")),
    ("4", _(u"Rotate 90° CCW")),
    ("3", _(u"Rotate 180°")),
)


class CreateDirForm(forms.Form):
    """
    Form for creating a folder.
    """

    name = forms.CharField(widget=forms.TextInput(attrs=dict({'class': 'vTextField'}, max_length=50, min_length=3)), label=_(u'Name'), help_text=_(u'Only letters, numbers, underscores, spaces and hyphens are allowed.'), required=True)

    def __init__(self, path, *args, **kwargs):
        self.path = path
        self.site = kwargs.pop("filebrowser_site", None)
        super(CreateDirForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        "validate name"
        if self.cleaned_data['name']:
            # only letters, numbers, underscores, spaces and hyphens are allowed.
            if not ALNUM_NAME_RE.search(self.cleaned_data['name']):
                raise forms.ValidationError(_(u'Only letters, numbers, underscores, spaces and hyphens are allowed.'))
            # Folder must not already exist.
            if self.site.storage.isdir(os.path.join(self.path, convert_filename(self.cleaned_data['name']))):
                raise forms.ValidationError(_(u'The Folder already exists.'))
        return convert_filename(self.cleaned_data['name'])


class ChangeForm(forms.ModelForm):
    """
    Form for renaming a file/folder.
    """

    custom_action = forms.ChoiceField(label=_(u'Actions'), required=False)
    name = forms.CharField(widget=forms.TextInput(attrs=dict({ 'class': 'vTextField' }, max_length=50, min_length=3)), label=_(u'Name'), help_text=_(u'Only letters, numbers, underscores, spaces and hyphens are allowed.'), required=True)

    class Meta:
        model = FileDescription
        exclude = ['file_path']

    def __init__(self, *args, **kwargs):
        self.path = kwargs.pop("path", None)
        self.fileobject = kwargs.pop("fileobject", None)
        self.site = kwargs.pop("filebrowser_site", None)
        super(ChangeForm, self).__init__(*args, **kwargs)

        # Initialize choices of custom action
        choices = [("", u"-----")]
        for name, action in self.site.applicable_actions(self.fileobject):
            choices.append((name, action.short_description))
        self.fields['custom_action'].choices = choices

        if self.fileobject.filetype != "Image":
            self.fields['custom_action'].widget = forms.HiddenInput()
        
        self.helper = FormHelper()
        self.helper.form_tag = False

        layout_blocks = [layout.Fieldset(
            '',
            layout.Field("name", template="filebrowser/widgets/admin_field.html", css_class="vTextField"),
            css_class="grp-module",
        ), layout.Fieldset(
            '',
            layout.HTML('{% load i18n %}<h2 class="grp-collapse-handler">{% trans "Author" %}</h2>'),
            layout.Field("author", template="filebrowser/widgets/admin_field.html", css_class="vTextField"),
            layout.Field("copyright_limitations", template="filebrowser/widgets/admin_field.html",
                         css_class="vTextField"),
            css_class="grp-module grp-collapse grp-open",
        )]

        for lang_code, lang_name in settings.LANGUAGES:
            layout_blocks.append(layout.Fieldset(
                '',
                layout.HTML('{% load i18n %}<h2 class="grp-collapse-handler">{% trans "Description" %} (' + lang_name + ')</h2>'),
                layout.Field("title_%s" % lang_code, template="filebrowser/widgets/admin_field.html", css_class="vTextField"),
                layout.Field("description_%s" % lang_code, template="filebrowser/widgets/admin_field.html"),
                css_class="grp-module grp-collapse grp-open multilingual multilingual-set-0 multilingual-language-%s" % lang_code,
            ))

        if self.fileobject.filetype == "Image":
            layout_blocks.append(layout.Fieldset(
                '',
                layout.HTML('{% load i18n %}<h2 class="grp-collapse-handler">{% trans "Edit" %}</h2>'),
                layout.Field("custom_action", template="filebrowser/widgets/admin_field.html"),
                css_class="grp-module grp-collapse grp-open",
            ))

        self.helper.layout = layout.Layout(
            *layout_blocks
        )

    def clean_name(self):
        "validate name"
        if self.cleaned_data['name']:
            # only letters, numbers, underscores, spaces and hyphens are allowed.
            if not ALNUM_NAME_RE.search(self.cleaned_data['name']):
                raise forms.ValidationError(_(u'Only letters, numbers, underscores, spaces and hyphens are allowed.'))
            #  folder/file must not already exist.
            if self.site.storage.isdir(os.path.join(self.path, convert_filename(self.cleaned_data['name']))) and os.path.join(self.path, convert_filename(self.cleaned_data['name'])) != self.fileobject.path.lower():
                raise forms.ValidationError(_(u'The Folder already exists.'))
            elif self.site.storage.isfile(os.path.join(self.path, convert_filename(self.cleaned_data['name']))) and os.path.join(self.path, convert_filename(self.cleaned_data['name'])) != self.fileobject.path:
                raise forms.ValidationError(_(u'The File already exists.'))
        return convert_filename(self.cleaned_data['name'])

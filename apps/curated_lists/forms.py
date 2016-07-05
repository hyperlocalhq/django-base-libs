# -*- coding: UTF-8 -*-
from django.conf import settings
from django.utils.translation import ugettext_lazy as _, ugettext
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap


class CuratedListForm(forms.Form):
    title = forms.CharField(
        label=_("Title"),
        required=True,
    )
    description = forms.CharField(
        label=_("Description"),
        required=True,
    )

    def __init__(self, instance, *args, **kwargs):
        super(CuratedListForm, self).__init__(*args, **kwargs)

        self.instance = instance

        if not self.initial:
            self.initial = {
                'title': getattr(instance, "title_{}".format(settings.LANGUAGE_CODE), ""),
                'description': getattr(instance, "description_{}".format(settings.LANGUAGE_CODE), ""),
            }

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Edit Curated List Description"),
                "title",
                layout.Field("description", rows=5),
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Save')),
            )
        )

    def save(self, commit=True):
        cleaned = self.cleaned_data
        for lang_code, lang_name in settings.LANGUAGES:
            setattr(self.instance, "title_{}".format(lang_code), cleaned['title'])
            setattr(self.instance, "description_{}".format(lang_code), cleaned['description'])
            if not getattr(self.instance, "description_{}_markup_type".format(lang_code)):
                setattr(self.instance, "description_{}_markup_type".format(lang_code), "pt")
        if commit:
            self.instance.save()
        return self.instance

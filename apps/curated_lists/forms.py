# -*- coding: UTF-8 -*-
import operator

from django.conf import settings
from django.utils.translation import ugettext_lazy as _, ugettext
from django.db import models
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from ccb.apps.curated_lists.models import ListOwner
from ccb.apps.site_specific.models import ContextItem
from jetson.apps.structure.models import Category


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


class CuratedListFilterForm(forms.Form):
    category = forms.ModelChoiceField(
        empty_label=_("All"),
        queryset=Category.objects.filter(level=0),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(CuratedListFilterForm, self).__init__(*args, **kwargs)

        # Get all unique Person and Institution instances
        # that apply for owners of published and featured curated lists
        unique_owners = ListOwner.objects.filter(
            curated_list__privacy="public",
            curated_list__is_featured=True,
        ).values(
            "owner_content_type", "owner_object_id"
        ).order_by("owner_content_type", "owner_object_id").distinct()

        # Create an owner ModelChoiceField with ContextItem instances matching unique owners
        context_item_qs = ContextItem.objects.filter(
            reduce(operator.ior, [
                models.Q(content_type__id=owner['owner_content_type']) &
                models.Q(object_id=owner['owner_object_id'])
                for owner in unique_owners
            ])
        ).order_by("title")

        self.fields['owner'] = forms.ModelChoiceField(
            empty_label=_("All"),
            queryset=context_item_qs,
            required=False,
        )

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "GET"
        self.helper.form_id = "filter_form"
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Filter"),
                layout.Field("owner", template="ccb_form/custom_widgets/filter_field.html"),
                layout.Field("category", template="ccb_form/custom_widgets/category_filter_field.html"),
                template="ccb_form/custom_widgets/filter.html"
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Search')),
            )
        )

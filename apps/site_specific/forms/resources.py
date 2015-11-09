# -*- coding: UTF-8 -*-
from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from base_libs.forms import dynamicforms
from base_libs.forms.fields import ImageField
from base_libs.utils.misc import get_related_queryset

image_mods = models.get_app("image_mods")

from ccb.apps.resources.models import Document
from ccb.apps.site_specific.models import ContextItem


# prexixes of fields to guarantee uniqueness
PREFIX_CI = 'CI_'  # Creative Sector aka Creative Industry
PREFIX_BC = 'BC_'  # Context Category aka Business Category
PREFIX_OT = 'OT_'  # Object Type
PREFIX_LT = 'LT_'  # Location Type
PREFIX_JS = 'JS_'  # Job Sector


LOGO_SIZE = getattr(settings, "LOGO_SIZE", (100, 100))
MIN_LOGO_SIZE = getattr(settings, "MIN_LOGO_SIZE", (100, 100))
STR_LOGO_SIZE = "%sx%s" % LOGO_SIZE
STR_MIN_LOGO_SIZE = "%sx%s" % MIN_LOGO_SIZE


# noinspection PyClassHasNoInit
class DescriptionForm(dynamicforms.Form):
    description_en = forms.CharField(
        label=_("Description (English)"),
        required=False,
        widget=forms.Textarea(),
    )
    description_de = forms.CharField(
        label=_("Description (German)"),
        required=False,
        widget=forms.Textarea(),
    )

    def __init__(self, document, index, *args, **kwargs):
        super(DescriptionForm, self).__init__(*args, **kwargs)
        self.document = document
        self.index = index
        if not args and not kwargs:  # if nothing is posted
            self.fields['description_en'].initial = document.description_en
            self.fields['description_de'].initial = document.description_de

    def save(self):
        document = self.document
        document.description_en = self.cleaned_data['description_en']
        document.description_de = self.cleaned_data['description_de']
        document.save()
        return document

    def get_extra_context(self):
        return {}

class AvatarForm(dynamicforms.Form):
    media_file = ImageField(
        label=_("Photo"),
        help_text=_(
            "You can upload GIF, JPG, PNG, TIFF, and BMP images. The minimal dimensions are %s px.") % STR_MIN_LOGO_SIZE,
        required=False,
        min_dimensions=MIN_LOGO_SIZE,
    )

    def __init__(self, document, index, *args, **kwargs):
        super(AvatarForm, self).__init__(*args, **kwargs)
        self.document = document
        self.index = index

    def save(self):
        document = self.document
        if "media_file" in self.files:
            media_file = self.files['media_file']
            image_mods.FileManager.save_file_for_object(
                document,
                media_file.name,
                media_file,
                subpath="avatar/"
            )
        return document

    def get_extra_context(self):
        return {}

class DetailsForm(dynamicforms.Form):
    document_type = forms.ModelChoiceField(
        label=_("Document Type"),
        queryset=get_related_queryset(Document, "document_type"),
        required=False,
    )
    url_link = forms.URLField(
        label=_("URL"),
        required=False,
    )
    medium = forms.ModelChoiceField(
        label=_("Medium"),
        queryset=get_related_queryset(Document, "medium"),
        required=False,
    )

    def __init__(self, document, index, *args, **kwargs):
        super(DetailsForm, self).__init__(*args, **kwargs)
        self.document = document
        self.index = index
        if not args and not kwargs:  # if nothing is posted
            self.fields['document_type'].initial = self.document.document_type
            self.fields['medium'].initial = self.document.medium
            self.fields['url_link'].initial = self.document.url_link

    def save(self):
        document = self.document
        document.url_link = self.cleaned_data['url_link']
        document.document_type = self.cleaned_data['document_type']
        document.medium = self.cleaned_data['medium']
        document.save()
        return document

    def get_extra_context(self):
        return {}

class CategoriesForm(dynamicforms.Form):
    choose_creative_sectors = forms.BooleanField(
        initial=True,
        widget=forms.HiddenInput(
            attrs={
                "class": "form_hidden",
            }
        ),
        required=False,
    )

    def clean_choose_creative_sectors(self):
        data = self.data
        el_count = 0
        for el in self.creative_sectors.values():
            if el['field_name'] in data:
                el_count += 1
        if not el_count:
            raise forms.ValidationError(_("Please choose at least one creative sector."))
        return True

    choose_context_categories = forms.BooleanField(
        initial=True,
        widget=forms.HiddenInput(
            attrs={
                "class": "form_hidden",
            }
        ),
        required=False,
    )

    def clean_choose_context_categories(self):
        data = self.data
        el_count = 0
        for el in self.context_categories.values():
            if el['field_name'] in data:
                el_count += 1
        if not el_count:
            raise forms.ValidationError(_("Please choose at least one context category."))
        return True

    def __init__(self, document, index, *args, **kwargs):
        super(CategoriesForm, self).__init__(*args, **kwargs)
        self.document = document
        self.creative_sectors = {}
        for item in get_related_queryset(Document, "creative_sectors"):
            self.creative_sectors[item.sysname] = {
                'id': item.id,
                'field_name': PREFIX_CI + str(item.id),
            }
        self.context_categories = {}
        for item in get_related_queryset(Document, "context_categories"):
            self.context_categories[item.sysname] = {
                'id': item.id,
                'field_name': PREFIX_BC + str(item.id),
            }
        for s in self.creative_sectors.values():
            self.fields[s['field_name']] = forms.BooleanField(
                required=False
            )
        for el in document.get_creative_sectors():
            for ancestor in el.get_ancestors(include_self=True):
                self.fields[PREFIX_CI + str(ancestor.id)].initial = True
        for c in self.context_categories.values():
            self.fields[c['field_name']] = forms.BooleanField(
                required=False
            )
        for el in document.get_context_categories():
            for ancestor in el.get_ancestors(include_self=True):
                self.fields[PREFIX_BC + str(ancestor.id)].initial = True

    def save(self, *args, **kwargs):
        document = self.document
        cleaned = self.cleaned_data
        selected_cs = {}
        for item in get_related_queryset(Document, "creative_sectors"):
            if cleaned.get(PREFIX_CI + str(item.id), False):
                # remove all the parents
                for ancestor in item.get_ancestors():
                    if ancestor.id in selected_cs:
                        del (selected_cs[ancestor.id])
                # add current
                selected_cs[item.id] = item
        document.creative_sectors.clear()
        document.creative_sectors.add(*selected_cs.values())

        selected_cc = {}
        for item in get_related_queryset(Document, "context_categories"):
            if cleaned.get(PREFIX_BC + str(item.id), False):
                # remove all the parents
                for ancestor in item.get_ancestors():
                    if ancestor.id in selected_cc:
                        del (selected_cc[ancestor.id])
                # add current
                selected_cc[item.id] = item
        document.context_categories.clear()
        document.context_categories.add(*selected_cc.values())
        ContextItem.objects.update_for(document)

        return document

    def get_extra_context(self):
        return {}

profile_forms = {
    'description': DescriptionForm,
    'avatar': AvatarForm,
    'details': DetailsForm,
    'categories': CategoriesForm,
}

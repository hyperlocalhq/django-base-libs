# -*- coding: UTF-8 -*-
from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _, ugettext

from base_libs.utils.misc import get_related_queryset
from base_libs.forms import dynamicforms
from base_libs.forms.fields import HierarchicalModelChoiceField

from mptt.forms import TreeNodeChoiceField

Document = models.get_model("resources", "Document")

class DocumentSearchForm(dynamicforms.Form):
    creative_sector = TreeNodeChoiceField(
        empty_label=_("All"),
        label=_("Creative Sector"),
        required=False,
        queryset=get_related_queryset(Document, "creative_sectors"),
        )
    context_category = TreeNodeChoiceField(
        empty_label=_("All"),
        label=_("Business Category"),
        required=False,
        queryset=get_related_queryset(Document, "context_categories"),
        )
    document_type = TreeNodeChoiceField(
        empty_label=_("All"),
        label=_("Type"),
        required=False,
        queryset=get_related_queryset(Document, "document_type"),
        )
    
    def get_query(self):
        from django.template.defaultfilters import urlencode
        cleaned = self.cleaned_data
        return "&".join([
            ("%s=%s" % (k, urlencode(isinstance(v, models.Model) and v.pk or v)))
            for (k, v) in cleaned.items()
            if v
            ])
        


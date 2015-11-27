# -*- coding: UTF-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.forms import TreeNodeChoiceField

from base_libs.forms import dynamicforms
from base_libs.utils.misc import get_related_queryset

from jetson.apps.location.models import LocalityType

Person = models.get_model("people", "Person")
Term = models.get_model("structure", "Term")


class PersonSearchForm(dynamicforms.Form):
    creative_sector = TreeNodeChoiceField(
        empty_label=_("All"),
        label=_("Creative Sector"),
        required=False,
        queryset=get_related_queryset(Person, "creative_sectors"),
    )
    context_category = TreeNodeChoiceField(
        empty_label=_("All"),
        label=_("Business Category"),
        required=False,
        queryset=get_related_queryset(Person, "context_categories"),
    )
    individual_type = TreeNodeChoiceField(
        empty_label=_("All"),
        label=_("Type"),
        required=False,
        queryset=get_related_queryset(Person, "individual_type"),
    )
    locality_type = TreeNodeChoiceField(
        empty_label=_("All"),
        label=_("Location Type"),
        required=False,
        queryset=LocalityType.objects.order_by("tree_id", "lft"),
    )

    def get_query(self):
        from django.template.defaultfilters import urlencode
        if self.is_valid():
            cleaned = self.cleaned_data
            return "&".join([
                ("%s=%s" % (k, urlencode(isinstance(v, models.Model) and v.pk or v)))
                for (k, v) in cleaned.items()
                if v
            ])
        return ""
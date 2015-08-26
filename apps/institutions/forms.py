# -*- coding: UTF-8 -*-

from django.utils.translation import ugettext_lazy as _
from mptt.forms import TreeNodeChoiceField

from jetson.apps.institutions.forms import *
from base_libs.forms import dynamicforms
from jetson.apps.structure.models import Term


class InstitutionSearchForm(dynamicforms.Form):
    creative_sector = TreeNodeChoiceField(
        empty_label=_("All"),
        label=_("Creative Sector"),
        required=False,
        queryset=get_related_queryset(Institution, "creative_sectors"),
    )
    context_category = TreeNodeChoiceField(
        empty_label=_("All"),
        label=_("Business Category"),
        required=False,
        queryset=get_related_queryset(Institution, "context_categories"),
    )
    institution_type = TreeNodeChoiceField(
        empty_label=_("All"),
        label=_("Type"),
        required=False,
        queryset=get_related_queryset(Institution, "institution_types"),
    )
    location_type = TreeNodeChoiceField(
        empty_label=_("All"),
        label=_("Location Type"),
        required=False,
        queryset=Term.objects.filter(
            vocabulary__sysname='basics_locality',
        ).order_by("tree_id", "lft"),
    )

    def get_query(self):
        from django.template.defaultfilters import urlencode

        cleaned = self.cleaned_data
        return "&".join([
                            ("%s=%s" % (k, urlencode(isinstance(v, models.Model) and v.pk or v)))
                            for (k, v) in cleaned.items()
                            if v
                            ])

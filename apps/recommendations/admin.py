# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django import forms

from .models import Recommendation


class RecommendationForm(forms.ModelForm):
    widget_template = forms.ChoiceField(
        label=_("Widget Template"),
        choices=Recommendation.WIDGET_TEMPLATE_CHOICES,
        required=True,
    )

    class Meta:
        model = Recommendation
        fields = "__all__"


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    form = RecommendationForm
    save_on_top = True
    list_display = ["sysname", "get_widget_template_display", "creation_date", "modified_date", "status"]
    search_fields = ["sysname"]
    list_filter = ["creation_date", "modified_date", "widget_template", "status"]
    fieldsets = [
        (_("Content"), {'fields': ["sysname", "widget_template", "status"]}),
    ]

    def get_widget_template_display(self, obj):
        return dict(Recommendation.WIDGET_TEMPLATE_CHOICES).get(obj.widget_template)
    get_widget_template_display.short_description = _("Widget Template")


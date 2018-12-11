# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase

from base_libs.admin.options import MarkupTypeOptions

from .models import PageTeaser



class PageTeaserPlugin(MarkupTypeOptions, CMSPluginBase):
    model = PageTeaser
    name = _("Page Teaser")
    render_template = "cms/plugins/page_teaser.html"
    change_form_template = "cms/plugins/richtext_plugin_change_form.html"

    def render(self, context, instance, placeholder):
        context.update({
            'object': instance,
            'placeholder':placeholder,
        })
        return context

plugin_pool.register_plugin(PageTeaserPlugin)

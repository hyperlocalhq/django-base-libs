# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase

from base_libs.admin.options import MarkupTypeOptions

from .models import RichText


class RichTextPlugin(MarkupTypeOptions, CMSPluginBase):
    model = RichText
    name = _("Rich Text")
    render_template = "cms/plugins/richtext.html"
    change_form_template = "cms/plugins/richtext_plugin_change_form.html"

    def render(self, context, instance, placeholder):
        context.update({
            'object': instance,
            'placeholder': placeholder,
        })
        return context


plugin_pool.register_plugin(RichTextPlugin)

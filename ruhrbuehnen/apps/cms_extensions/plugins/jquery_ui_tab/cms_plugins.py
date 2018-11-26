# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase

from base_libs.admin.options import MarkupTypeOptions

from .models import JQueryUITab


class JQueryUITabPlugin(MarkupTypeOptions, CMSPluginBase):
    model = JQueryUITab
    name = _("Tab")
    render_template = "cms/plugins/jquery_ui_tab.html"
    change_form_template = "cms/plugins/jquery_ui_tab_plugin_change_form.html"

    def render(self, context, instance, placeholder):
        context.update({
            'object': instance,
            'placeholder': placeholder,
        })
        return context


plugin_pool.register_plugin(JQueryUITabPlugin)

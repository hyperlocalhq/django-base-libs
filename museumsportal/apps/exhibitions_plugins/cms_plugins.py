# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from base_libs.admin.options import MarkupTypeOptions

from .models import NewlyOpenedExhibitionExt


class NewlyOpenedExhibitionExtPlugin(MarkupTypeOptions, CMSPluginBase):
    model = NewlyOpenedExhibitionExt
    name = _("Newly Opened Exhibition w/ Teaser")
    render_template = "cms/plugins/newly_opened_exhibition_ext.html"
    change_form_template = "cms/plugins/newly_opened_exhibition_ext_change_form.html"

    def render(self, context, instance, placeholder):
        context.update({
            'object':instance,
            'placeholder':placeholder
            })
        return context

plugin_pool.register_plugin(NewlyOpenedExhibitionExtPlugin)

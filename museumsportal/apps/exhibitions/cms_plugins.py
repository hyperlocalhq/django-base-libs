# -*- coding: utf-8 -*-

from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from models import NewlyOpenedExhibition

class NewlyOpenedExhibitionPlugin(CMSPluginBase):
    model = NewlyOpenedExhibition
    name = _("Newly Opened Exhibition")
    render_template = "cms/plugins/newly_opened_exhibition.html"

    def render(self, context, instance, placeholder):
        context.update({
            'object':instance,
            'placeholder':placeholder
            })
        return context

plugin_pool.register_plugin(NewlyOpenedExhibitionPlugin)

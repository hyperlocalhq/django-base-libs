# -*- coding: utf-8 -*-

from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from models import Headline

class HeadlinePlugin(CMSPluginBase):
    model = Headline
    name = _("Headline")
    render_template = "cms/plugins/headline.html"
    
    def render(self, context, instance, placeholder):
        context.update({
            'object':instance,
            'placeholder':placeholder
            })
        return context

plugin_pool.register_plugin(HeadlinePlugin)

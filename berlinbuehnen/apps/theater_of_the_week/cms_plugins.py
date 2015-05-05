# -*- coding: utf-8 -*-

from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from models import ArticleSelection

class TheaterOfTheWeekSelectionPlugin(CMSPluginBase):
    model = ArticleSelection
    name = _("Theater of the week selection")
    render_template = "cms/plugins/theater_of_the_week_selection.html"
    
    def render(self, context, instance, placeholder):
        context.update({
            'object':instance,
            'placeholder':placeholder
            })
        return context

plugin_pool.register_plugin(TheaterOfTheWeekSelectionPlugin)

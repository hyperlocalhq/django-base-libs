# -*- coding: utf-8 -*-

from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from models import CMSAdZone


class AdZonePlugin(CMSPluginBase):
    model = CMSAdZone
    name = _("Ad Zone")
    render_template = "cms/plugins/adzone.html"
    
    def render(self, context, instance, placeholder):
        context.update({
            'object': instance,
            'placeholder': placeholder
        })
        return context

plugin_pool.register_plugin(AdZonePlugin)

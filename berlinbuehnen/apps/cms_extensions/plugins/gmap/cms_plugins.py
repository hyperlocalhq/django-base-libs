# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import Media
from django.conf import settings

from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase

from .models import GMap

class GMapPlugin(CMSPluginBase):
    # TODO: Do we still need this plugin? If YES, get_plugin_media should be replaced with sekizai. If NOT, it should be uninstalled and removed
    model = GMap
    name = _("Google Map V3")
    render_template = "cms/plugins/gmap.html"
    
    def render(self, context, instance, placeholder):
        context.update({
            'object':instance, 
            'placeholder':placeholder, 
        })
        return context
    
    def get_plugin_media(self, request, context, plugin):
        return Media(
            js=('//maps.google.com/maps/api/js?key={}'.format(getattr(settings, "GOOGLE_API_KEY", "")),)
        )
 
plugin_pool.register_plugin(GMapPlugin)
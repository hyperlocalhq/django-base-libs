# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase

from models import FilebrowserImage

class FilebrowserImagePlugin(CMSPluginBase):
    model = FilebrowserImage
    name = _("Image")
    
    render_template = "cms/plugins/filebrowser_image.html"
    
    def render(self, context, instance, placeholder):
        context.update({
            'object': instance,
            'placeholder':placeholder,
        })
        return context
    
plugin_pool.register_plugin(FilebrowserImagePlugin)
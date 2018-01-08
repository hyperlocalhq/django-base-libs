# -*- coding: utf-8 -*-
import re
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase

from models import RichText

class RichTextPlugin(CMSPluginBase):
    model = RichText
    name = _("Rich Text")
    render_template = "cms/plugins/richtext.html"
    change_form_template = "cms/plugins/richtext_plugin_change_form.html"

    def formfield_for_dbfield(self, db_field, **kwargs):
        # add .markupType to body_markup_type
        field = super(RichTextPlugin, self).formfield_for_dbfield(db_field, **kwargs)
        if re.search('markup_type$', db_field.name):
            field.widget.attrs['class'] = "markupType"
        return field

    def render(self, context, instance, placeholder):
        context.update({
            'object': instance,
            'placeholder':placeholder,
        })
        return context

plugin_pool.register_plugin(RichTextPlugin)

# -*- coding: utf-8 -*-

import re

from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from models import NewlyOpenedExhibitionExt

class NewlyOpenedExhibitionExtPlugin(CMSPluginBase):
    model = NewlyOpenedExhibitionExt
    name = _("Newly Opened Exhibition w/ Teaser")
    render_template = "cms/plugins/newly_opened_exhibition_ext.html"
    change_form_template = "cms/plugins/newly_opened_exhibition_ext_change_form.html"

    def formfield_for_dbfield(self, db_field, **kwargs):
        # add .markupType to body_markup_type
        field = super(NewlyOpenedExhibitionExtPlugin, self).formfield_for_dbfield(db_field, **kwargs)
        if re.search('markup_type$', db_field.name):
            field.widget.attrs['class'] = "markupType"
        return field
    
    def render(self, context, instance, placeholder):
        context.update({
            'object':instance,
            'placeholder':placeholder
            })
        return context

plugin_pool.register_plugin(NewlyOpenedExhibitionExtPlugin)

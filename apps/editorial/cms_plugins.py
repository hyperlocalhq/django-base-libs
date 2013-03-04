# -*- coding: utf-8 -*-

import re

from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from models import Intro
from models import EditorialContent
from models import TeaserBlock
from models import Footnote

class EditorialContentPlugin(CMSPluginBase):
    model = EditorialContent
    name = _("Editorial Content")
    render_template = "cms/plugins/editorial_content.html"
    change_form_template = "cms/plugins/editorial_content_plugin_change_form.html"

    def formfield_for_dbfield(self, db_field, **kwargs):
        # add .markupType to body_markup_type
        field = super(EditorialContentPlugin, self).formfield_for_dbfield(db_field, **kwargs)
        if re.search('markup_type$', db_field.name):
            field.widget.attrs['class'] = "markupType"
        return field
    
    def render(self, context, instance, placeholder):
        context.update({
            'object':instance,
            'placeholder':placeholder
            })
        return context

plugin_pool.register_plugin(EditorialContentPlugin)

class TeaserBlockPlugin(CMSPluginBase):
    model = TeaserBlock
    name = _("Teaser")
    render_template = "cms/plugins/teaser.html"
    change_form_template = "cms/plugins/teaser_plugin_change_form.html"

    def formfield_for_dbfield(self, db_field, **kwargs):
        # add .markupType to body_markup_type
        field = super(TeaserBlockPlugin, self).formfield_for_dbfield(db_field, **kwargs)
        if re.search('markup_type$', db_field.name):
            field.widget.attrs['class'] = "markupType"
        return field
    
    def render(self, context, instance, placeholder):
        context.update({
            'object':instance,
            'placeholder':placeholder
            })
        return context

plugin_pool.register_plugin(TeaserBlockPlugin)

class FootnotePlugin(CMSPluginBase):
    model = Footnote
    name = _("Footnote")
    render_template = "cms/plugins/footnote.html"
    change_form_template = "cms/plugins/footnote_plugin_change_form.html"

    def formfield_for_dbfield(self, db_field, **kwargs):
        # add .markupType to body_markup_type
        field = super(FootnotePlugin, self).formfield_for_dbfield(db_field, **kwargs)
        if re.search('markup_type$', db_field.name):
            field.widget.attrs['class'] = "markupType"
        return field
    
    def render(self, context, instance, placeholder):
        context.update({
            'object':instance,
            'placeholder':placeholder
            })
        return context

plugin_pool.register_plugin(FootnotePlugin)

class IntroPlugin(CMSPluginBase):
    model = Intro
    name = _("Intro")
    render_template = "cms/plugins/intro.html"
    change_form_template = "cms/plugins/intro_plugin_change_form.html"

    def formfield_for_dbfield(self, db_field, **kwargs):
        # add .markupType to body_markup_type
        field = super(IntroPlugin, self).formfield_for_dbfield(db_field, **kwargs)
        if re.search('markup_type$', db_field.name):
            field.widget.attrs['class'] = "markupType"
        return field
    
    def render(self, context, instance, placeholder):
        context.update({
            'object':instance,
            'placeholder':placeholder
            })
        return context

plugin_pool.register_plugin(IntroPlugin)
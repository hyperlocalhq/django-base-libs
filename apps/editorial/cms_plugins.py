# -*- coding: utf-8 -*-

import re

from django.utils.translation import ugettext as _
from django.template.loader import select_template

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from models import Intro
from models import EditorialContent
from models import TeaserBlock
from models import Footnote
from models import FrontpageTeaser

from base_libs.admin import ExtendedModelAdmin


class EditorialContentPlugin(CMSPluginBase, ExtendedModelAdmin):
    model = EditorialContent
    name = _("Editorial Content")
    render_template = "cms/plugins/editorial_content.html"

    change_form_template = "cms/plugins/editorial_content_plugin_change_form.html"

    fieldsets = (
        (_("Main Content"), {'fields': ('title', 'subtitle', 'description', 'website'), 'classes': ['collapse open']}),
        (_("Image"), {'fields': ('image', 'image_caption'), 'classes': ['collapse open']}),
        (_("Presentation"), {'fields': ('col_xs_width', 'col_sm_width', 'col_md_width', 'col_lg_width', 'css_class'), 'classes': ['collapse closed']}),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        # add .markupType to body_markup_type
        field = super(EditorialContentPlugin, self).formfield_for_dbfield(db_field, **kwargs)
        if re.search('markup_type$', db_field.name):
            field.widget.attrs['class'] = "markupType"
        return field
    
    def render(self, context, instance, placeholder):
        # choose the first available template from the list:
        #   "editorial_content_for_<placeholder>_in_<page_id>.html"
        #   "editorial_content_for_<placeholder>.html"
        #   "editorial_content.html"
        template_name_list = [
            # "cms/plugins/editorial_content_for_%s.html" % placeholder,
            "cms/plugins/editorial_content.html",
        ]
        # if context['request'].current_page.reverse_id:
        #     template_name_list.insert(0, "cms/plugins/editorial_content_for_%s_in_%s.html" % (placeholder, context['request'].current_page.reverse_id))
        self.render_template = select_template(template_name_list)
        context.update({
            'object': instance,
            'placeholder': placeholder,
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


class FrontpageTeaserPlugin(CMSPluginBase):
    model = FrontpageTeaser
    name = _("Frontpage Teaser")
    render_template = "cms/plugins/frontpage_teaser.html"
    change_form_template = "cms/plugins/frontpage_teaser_plugin_change_form.html"

    def formfield_for_dbfield(self, db_field, **kwargs):
        # add .markupType to body_markup_type
        field = super(FrontpageTeaserPlugin, self).formfield_for_dbfield(db_field, **kwargs)
        if re.search('markup_type$', db_field.name):
            field.widget.attrs['class'] = "markupType"
        return field
    
    def render(self, context, instance, placeholder):
        context.update({
            'object':instance,
            'placeholder':placeholder
            })
        return context

plugin_pool.register_plugin(FrontpageTeaserPlugin)

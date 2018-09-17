# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django.template.loader import select_template

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from base_libs.admin.options import MarkupTypeOptions, ExtendedModelAdmin

from .models import Intro
from .models import EditorialContent
from .models import TeaserBlock
from .models import Footnote
from .models import FrontpageTeaser


class EditorialContentPlugin(MarkupTypeOptions, CMSPluginBase):
    model = EditorialContent
    name = _("Editorial Content")
    render_template = "cms/plugins/editorial_content.html"

    change_form_template = "cms/plugins/editorial_content_plugin_change_form.html"

    fieldsets = (
        (_("Main Content"), {'fields': ('title', 'subtitle', 'description_markup_type', 'description', 'website'), 'classes': ['collapse open']}),
        (_("Image"), {'fields': ('image', 'image_caption_markup_type', 'image_caption'), 'classes': ['collapse open']}),
        (_("Presentation"), {'fields': ('col_xs_width', 'col_sm_width', 'col_md_width', 'col_lg_width', 'css_class'), 'classes': ['collapse closed']}),
    )

    def render(self, context, instance, placeholder):
        template_name_list = [
            "cms/plugins/editorial_content.html",
        ]
        self.render_template = select_template(template_name_list)
        context.update({
            'object': instance,
            'placeholder': placeholder,
        })
        return context

plugin_pool.register_plugin(EditorialContentPlugin)


class TeaserBlockPlugin(MarkupTypeOptions, CMSPluginBase):
    model = TeaserBlock
    name = _("Teaser")
    render_template = "cms/plugins/teaser.html"
    change_form_template = "cms/plugins/teaser_plugin_change_form.html"

    def render(self, context, instance, placeholder):
        context.update({
            'object':instance,
            'placeholder':placeholder
            })
        return context

plugin_pool.register_plugin(TeaserBlockPlugin)


class FootnotePlugin(MarkupTypeOptions, CMSPluginBase):
    model = Footnote
    name = _("Footnote")
    render_template = "cms/plugins/footnote.html"
    change_form_template = "cms/plugins/footnote_plugin_change_form.html"

    def render(self, context, instance, placeholder):
        context.update({
            'object':instance,
            'placeholder':placeholder
            })
        return context

plugin_pool.register_plugin(FootnotePlugin)


class IntroPlugin(MarkupTypeOptions, CMSPluginBase):
    model = Intro
    name = _("Intro")
    render_template = "cms/plugins/intro.html"
    change_form_template = "cms/plugins/intro_plugin_change_form.html"

    def render(self, context, instance, placeholder):
        context.update({
            'object':instance,
            'placeholder':placeholder
            })
        return context

plugin_pool.register_plugin(IntroPlugin)


class FrontpageTeaserPlugin(MarkupTypeOptions, CMSPluginBase):
    model = FrontpageTeaser
    name = _("Frontpage Teaser")
    render_template = "cms/plugins/frontpage_teaser.html"
    change_form_template = "cms/plugins/frontpage_teaser_plugin_change_form.html"

    def render(self, context, instance, placeholder):
        context.update({
            'object':instance,
            'placeholder':placeholder
            })
        return context

plugin_pool.register_plugin(FrontpageTeaserPlugin)

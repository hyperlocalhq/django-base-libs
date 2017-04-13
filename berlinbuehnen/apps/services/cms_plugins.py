# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import re

from django.utils.translation import ugettext_lazy as _
from django.cotrib import admin

from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase

from .models import IndexItem, TitleAndText, ImageAndText, LinkCategory, Link


class PluginBase(CMSPluginBase):
    module = _("Service Plugins")

    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance,
            'placeholder': placeholder,
        })
        return context


class IndexItemPlugin(PluginBase):
    model = IndexItem
    name = _("Index Item")
    render_template = "cms/plugins/index_item.html"

plugin_pool.register_plugin(IndexItemPlugin)


class TitleAndTextPlugin(PluginBase):
    model = TitleAndText
    name = _("Title and text")
    render_template = "cms/plugins/title_and_text.html"

    def formfield_for_dbfield(self, db_field, **kwargs):
        # add .markupType to body_markup_type
        field = super(TitleAndTextPlugin, self).formfield_for_dbfield(db_field, **kwargs)
        if re.search('markup_type$', db_field.name):
            field.widget.attrs['class'] = "markupType"
        return field

plugin_pool.register_plugin(TitleAndTextPlugin)


class ImageAndTextPlugin(PluginBase):
    model = ImageAndText
    name = _("Image and text")
    render_template = "cms/plugins/image_and_text.html"

    def formfield_for_dbfield(self, db_field, **kwargs):
        # add .markupType to body_markup_type
        field = super(ImageAndTextPlugin, self).formfield_for_dbfield(db_field, **kwargs)
        if re.search('markup_type$', db_field.name):
            field.widget.attrs['class'] = "markupType"
        return field

plugin_pool.register_plugin(ImageAndTextPlugin)


class LinkInline(admin.StackedInline):
    model = Link
    extra = 0


class LinkCategoryPlugin(PluginBase):
    model = LinkCategory
    name = _("Link Category")
    render_template = "cms/plugins/link_category.html"
    inlines = [LinkInline]

plugin_pool.register_plugin(LinkCategoryPlugin)

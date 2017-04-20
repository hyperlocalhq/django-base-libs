# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import re

from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase

from .models import IndexItem, ServicePageBanner, ServiceGridItem, ServiceListItem, LinkCategory, Link, TitleAndText, ImageAndText


class PluginBase(CMSPluginBase):
    module = _("Service Plugins")
    change_form_template = "services/plugins/richtext_plugin_change_form.html"

    def formfield_for_dbfield(self, db_field, **kwargs):
        # add .markupType to body_markup_type
        field = super(PluginBase, self).formfield_for_dbfield(db_field, **kwargs)
        if re.search('markup_type$', db_field.name):
            field.widget.attrs['class'] = "markupType"
        return field

    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance,
            'placeholder': placeholder,
        })
        return context


### BANNERS ###

class IndexItemPlugin(PluginBase):
    model = IndexItem
    name = _("Index Page Item")
    render_template = "services/plugins/index_item.html"

plugin_pool.register_plugin(IndexItemPlugin)


class ServicePageBannerPlugin(PluginBase):
    model = ServicePageBanner
    name = _("Service Page Banner")
    render_template = "services/plugins/service_page_banner.html"

plugin_pool.register_plugin(ServicePageBannerPlugin)

### SERVICE LISTS ###

class ServiceGridItemPlugin(PluginBase):
    model = ServiceGridItem
    name = _("Service Grid Item")
    render_template = "services/plugins/service_grid_item.html"
    fields = ("title", "subtitle", "short_description", "short_description_markup_type", "image", "internal_link", "external_link")

plugin_pool.register_plugin(ServiceGridItemPlugin)

class ServiceListItemPlugin(PluginBase):
    model = ServiceListItem
    name = _("Service List Item")
    render_template = "services/plugins/service_list_item.html"
    fields = ("title", "subtitle", "location", "short_description", "short_description_markup_type", "image", "external_link")

plugin_pool.register_plugin(ServiceListItemPlugin)


### LINKS ###

class LinkInline(admin.StackedInline):
    classes = ('grp-collapse grp-open',)
    model = Link
    extra = 0


class LinkCategoryPlugin(PluginBase):
    model = LinkCategory
    name = _("Link Category")
    render_template = "services/plugins/link_category.html"
    inlines = [LinkInline]
    sortable_field_name = "sort_order"

plugin_pool.register_plugin(LinkCategoryPlugin)


### ARTICLES ###

class TitleAndTextPlugin(PluginBase):
    model = TitleAndText
    name = _("Title and text")
    render_template = "services/plugins/title_and_text.html"

plugin_pool.register_plugin(TitleAndTextPlugin)


class ImageAndTextPlugin(PluginBase):
    model = ImageAndText
    name = _("Image and text")
    render_template = "services/plugins/image_and_text.html"

plugin_pool.register_plugin(ImageAndTextPlugin)

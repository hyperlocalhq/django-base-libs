# -*- coding: UTF-8 -*-

from django.utils.translation import ugettext_lazy as _

from jetson.apps.media_gallery.admin import *
from base_libs.models.admin import PublishingMixinAdminOptions

PortfolioSettings = models.get_model("media_gallery", "PortfolioSettings")
Section = models.get_model("media_gallery", "Section")


class CCBMediaGalleryOptions(MediaGalleryOptions):
    list_filter = ['creation_date', 'content_type', 'status', 'is_featured']
    list_display = (
        'id', '__unicode__', 'content_type', 'get_content_object_display', 'creation_date', 'file_count', 'views',
        'status',
        'is_featured')

    fieldsets = ObjectRelationMixinAdminOptions().fieldsets
    fieldsets += get_admin_lang_section(None, ['title', 'description'])
    fieldsets += [
        (_("Cover"), {'fields': ("cover_image",), 'classes': ["collapse closed"]}),
    ]
    fieldsets += [
        (_("Details"), {'fields': ("section", "is_featured", "sort_order"), 'classes': ["collapse closed"]}),
    ]
    fieldsets += [
        (_("Categories"), {
            'fields': ('categories',),
        }),
    ]
    fieldsets += PublishingMixinAdminOptions.fieldsets


class PortfolioSettingsAdminForm(ObjectRelationMixinAdminForm()):
    pass


class PortfolioSettingsOptions(ObjectRelationMixinAdminOptions(admin_order_field="content_object_repr")):
    form = PortfolioSettingsAdminForm
    save_on_top = True
    list_display = ('id', '__unicode__', 'content_type', 'get_content_object_display', 'creation_date', 'landing_page')
    list_display_links = ('id', '__unicode__',)
    list_filter = ['creation_date', 'content_type', 'landing_page']
    search_fields = ["content_object_repr"]
    date_hierarchy = 'creation_date'
    fieldsets = ObjectRelationMixinAdminOptions().fieldsets
    fieldsets += [
        (_("Details"), {'fields': ("landing_page", "landing_page_image"), 'classes': ["collapse closed"]}),
    ]


class SectionAdminForm(ObjectRelationMixinAdminForm()):
    pass


class SectionOptions(ObjectRelationMixinAdminOptions(admin_order_field="content_object_repr")):
    form = SectionAdminForm
    save_on_top = True
    list_display = ('id', '__unicode__', 'content_type', 'get_content_object_display', 'creation_date')
    list_display_links = ('id', '__unicode__',)
    list_filter = ['creation_date', 'content_type', 'show_title']
    search_fields = ["title", "content_object_repr"]
    date_hierarchy = 'creation_date'
    fieldsets = ObjectRelationMixinAdminOptions().fieldsets
    fieldsets += get_admin_lang_section(None, ['title'])
    fieldsets += [
        (_("Details"), {'fields': ("show_title", "sort_order"), 'classes': ["collapse closed"]}),
    ]


admin.site.register(PortfolioSettings, PortfolioSettingsOptions)
admin.site.register(Section, SectionOptions)

admin.site.unregister(MediaGallery)
admin.site.register(MediaGallery, CCBMediaGalleryOptions)

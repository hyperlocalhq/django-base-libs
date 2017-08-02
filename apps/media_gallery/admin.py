# -*- coding: UTF-8 -*-

from django.utils.translation import ugettext_lazy as _

from jetson.apps.media_gallery.admin import *
from base_libs.models.admin import PublishingMixinAdminOptions

from .models import PortfolioSettings, Section


class CCBMediaGalleryOptions(MediaGalleryOptions):
    list_filter = ['creation_date', 'content_type', 'status', 'is_featured']
    list_display = (
        'id', '__unicode__', 'content_type', 'get_content_object_display', 'creation_date', 'file_count', 'views',
        'status',
        'is_featured'
    )
    fieldsets = [
        (_("Related Object"), {'fields': ("content_type", "object_id")}),
    ]
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

    raw_id_fields = ("section", 'author',)
    related_lookup_fields = deepcopy(MediaGalleryOptions.related_lookup_fields)
    related_lookup_fields.setdefault('fk', [])
    related_lookup_fields['fk'] += ["section", "author"]


class PortfolioSettingsOptions(ObjectRelationAdminMixin):
    save_on_top = True
    list_display = ('id', '__unicode__', 'content_type', 'get_content_object_display', 'creation_date', 'landing_page')
    list_display_links = ('id', '__unicode__',)
    list_filter = ['creation_date', 'content_type', 'landing_page']
    search_fields = ["content_object_repr"]
    date_hierarchy = 'creation_date'
    fieldsets = deepcopy(ObjectRelationAdminMixin.fieldsets)
    fieldsets += [
        (_("Details"), {'fields': ("landing_page", "landing_page_image"), 'classes': ["collapse closed"]}),
    ]


class SectionOptions(ObjectRelationAdminMixin):
    save_on_top = True
    list_display = ('id', '__unicode__', 'content_type', 'get_content_object_display', 'creation_date')
    list_display_links = ('id', '__unicode__',)
    list_filter = ['creation_date', 'content_type', 'show_title']
    search_fields = ["title", "content_object_repr"]
    date_hierarchy = 'creation_date'
    fieldsets = deepcopy(ObjectRelationAdminMixin.fieldsets)
    fieldsets += get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [
        (_("Details"), {'fields': ("show_title", "sort_order"), 'classes': ["collapse closed"]}),
    ]


admin.site.register(PortfolioSettings, PortfolioSettingsOptions)
admin.site.register(Section, SectionOptions)

admin.site.unregister(MediaGallery)
admin.site.register(MediaGallery, CCBMediaGalleryOptions)

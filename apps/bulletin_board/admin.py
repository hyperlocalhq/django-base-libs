# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from base_libs.admin.options import ExtendedModelAdmin
from base_libs.admin.options import ExtendedStackedInline
from base_libs.models.admin import get_admin_lang_section

BulletinCategory = models.get_model("bulletin_board", "BulletinCategory")
Bulletin = models.get_model("bulletin_board", "Bulletin")


class BulletinCategoryAdmin(ExtendedModelAdmin):
    list_display = ['title', 'sort_order']
    search_fields = ['title']
    fieldsets = get_admin_lang_section(_("Title"), ['title',])
    fieldsets += [
        (None, {'fields': ['slug',]}),
        #(None, {'fields': ['slug', 'sort_order']}),
    ]


class BulletinAdmin(ExtendedModelAdmin):
    list_display = ["title", "bulletin_type", "bulletin_category", "creator", "creation_date", "published_from", "published_till", "status"]
    list_filter = ["bulletin_type", "bulletin_category", "categories", "status"]
    search_fields = ["title", "description", "contact_person", "creator__username"]
    list_editable = ["status"]
    
    fieldsets = [ 
        (_("Main data"), {'fields': ('title', 'description'), 'classes': ("grp-collapse", "grp-open")}),
        (_("Categories"), {'fields': ('bulletin_type', 'bulletin_category', 'categories',), 'classes': ("grp-collapse", "grp-open")}),
        (_("Image"), {'fields': ('image', 'image_description'), 'classes': ("grp-collapse", "grp-open")}),
        (_("Region"), {'fields': ('locality_type',), 'classes': ("grp-collapse", "grp-open")}),
        (_("Contact"), {'fields': ('institution', 'institution_title', 'institution_url', 'contact_person', 'phone', 'email'), 'classes': ("grp-collapse", "grp-open")}),
        (_("Publishing"), {'fields': ('published_from', 'published_till', 'source_url', 'status'), 'classes': ("grp-collapse", "grp-closed")}),
    ]
    
    filter_horizontal = ('categories',)

admin.site.register(BulletinCategory, BulletinCategoryAdmin)
admin.site.register(Bulletin, BulletinAdmin) 


# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from base_libs.admin.options import ExtendedStackedInline
from base_libs.models.admin import get_admin_lang_section
from base_libs.admin import ExtendedModelAdmin

from .models import PartnerCategory
from .models import Partner


class Partner_Inline(ExtendedStackedInline):
    model = Partner
    sortable = True
    sortable_field_name = "sort_order"
    allow_add = True
    extra = 0
        
    save_on_top = True
    list_display = ['title', 'category']
    list_filter = ['category']
    
    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(_("Images"), {'fields': ('image',)}),]
    fieldsets += [(_("Details"), {'fields': ('website_url', 'sort_order')}),]
    fieldsets += [(_("Status"), {'fields': ('status',)}),]
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)
    ordering = ("sort_order",)


class PartnerCategoryAdmin(ExtendedModelAdmin):
    save_on_top = True
    list_display = ['title', 'sysname', 'status', 'get_partners']
    list_filter = ['status',]
    
    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('sysname', 'status', 'sort_order', )}),]
    
    inlines = [Partner_Inline]
    
    def get_partners(self, obj):
        partners = []
        for p in obj.partner_set.order_by("sort_order"):
            if p.status == "published":
                partners.append(p.title)
            else:
                partners.append("%s (%s)" % (p.title, _("draft")))
        return '<br />'.join(partners)
    get_partners.short_description = _("Partners")
    get_partners.allow_tags = True
    
class PartnerAdmin(ExtendedModelAdmin):
    save_on_top = True
    list_display = ['title', ]
    list_filter = ['category',]
    search_fields = ['title']
    
    fieldsets = [(None, {'fields': ('category',)}),]
    fieldsets += get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(_("Images"), {'fields': ('image', )}),]
    fieldsets += [(_("Details"), {'fields': ('website_url', 'sort_order')}),]
    fieldsets += [(_("Status"), {'fields': ('status',)}),]
    
    ordering = ['title']
    
admin.site.register(PartnerCategory, PartnerCategoryAdmin)
admin.site.register(Partner, PartnerAdmin)


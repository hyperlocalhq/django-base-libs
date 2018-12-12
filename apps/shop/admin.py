# -*- coding: UTF-8 -*-

from django import forms
from django.forms import TextInput
from django.forms.models import modelform_factory
from django.contrib import admin
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _, ugettext

from filebrowser.settings import URL_FILEBROWSER_MEDIA

from base_libs.admin import ExtendedModelAdmin
from base_libs.admin import ExtendedStackedInline
from base_libs.models.admin import get_admin_lang_section
from base_libs.admin.tree_editor import TreeEditor
from base_libs.forms.fields import AutocompleteModelChoiceField


ShopProductCategory = models.get_model("shop", "ShopProductCategory")
ShopProductType = models.get_model("shop", "ShopProductType")
ShopProduct = models.get_model("shop", "ShopProduct")


class ShopProductCategoryAdmin(ExtendedModelAdmin):

    save_on_top = True
    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug',)}),]

admin.site.register(ShopProductCategory, ShopProductCategoryAdmin)


class ShopProductTypeAdmin(TreeEditor, ExtendedModelAdmin):

    save_on_top = True
    list_display = ['actions_column', 'indented_short_title', ]
    
    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug', 'parent')}),]
    
    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}

admin.site.register(ShopProductType, ShopProductTypeAdmin)


class ShopProductAdmin(ExtendedModelAdmin):

    ShopProductAdminForm = modelform_factory(ShopProduct)
    form = modelform_factory(ShopProduct, form=ShopProductAdminForm, widgets={"price": TextInput(attrs={'size':'10'})})

    class Media:
        js = (
            "%sjs/AddFileBrowser.js" % URL_FILEBROWSER_MEDIA,
        )
        
    save_on_top = True
    list_display = ('id', 'title', 'subtitle', 'get_categories_display', 'get_types_display', 'price', 'is_featured', 'is_for_children', 'is_new', 'status')
    list_editable = ('is_featured', 'is_for_children', 'is_new', 'status')
    list_display_links = ('title', )
    list_filter = ('product_categories', 'product_types', 'is_featured', 'is_for_children', 'is_new', 'languages', 'creation_date', 'status')
    search_fields = ('title', 'subtitle', 'slug')
    
    fieldsets = get_admin_lang_section(_("Title"), ['title', 'subtitle', 'description',])
    fieldsets += [(None, {'fields': ('slug', )}),]
    fieldsets += [(None, {'fields': ('image', 'price', 'link', 'languages')}),]
    fieldsets += [('Categories', {'fields': ('product_categories', 'product_types')}),]
    fieldsets += [('Relations', {'fields': ('museums', 'exhibitions', 'events', 'workshops')}),]
    fieldsets += [(None, {'fields': ('is_featured', 'is_for_children', 'is_new')})]
    fieldsets += [(_("Status"), {'fields': ('status',)}),]

    filter_horizontal = ('museums', 'exhibitions', 'events', 'workshops', 'product_categories', 'product_types', 'languages')
    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}
    
    
    def get_categories_display(self, obj):
        text = u''
        if obj.product_categories:
            first = True
            for category in obj.product_categories.all():
                if first:
                    first = False
                else:
                    text += u", "
                text += category.title
        return text
    get_categories_display.short_description = _("Categories")
    
    
    def get_types_display(self, obj):
        text = u''
        if obj.product_types:
            first = True
            for category in obj.product_types.all():
                if first:
                    first = False
                else:
                    text += u", "
                text += category.title
        return text
    get_types_display.short_description = _("Types")

admin.site.register(ShopProduct, ShopProductAdmin)
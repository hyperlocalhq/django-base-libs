# -*- coding: UTF-8 -*-

from django.contrib import admin
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _, ugettext
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.conf.urls import patterns, include, url
from django import forms

from filebrowser.settings import URL_FILEBROWSER_MEDIA

from base_libs.admin import ExtendedModelAdmin
from base_libs.admin import ExtendedStackedInline
from base_libs.models.admin import get_admin_lang_section
from base_libs.admin.tree_editor import TreeEditor

from .models import Location, Season


class SeasonInline(ExtendedStackedInline):
    model = Season
    extra = 0
    allow_add = True
    template = "admin/museums/museum/season_inline.html"


class LocationAdmin(ExtendedModelAdmin):
    class Media:
        js = (
            "%sjs/AddFileBrowser.js" % URL_FILEBROWSER_MEDIA,
            )
    save_on_top = True
    list_display = ('id', 'title', 'subtitle', 'creation_date', 'status', 'is_geoposition_set')
    list_editable = ('status', )
    list_display_links = ('title', )
    list_filter = ('creation_date', 'status', )
    search_fields = ('title', 'subtitle', 'slug')
    
    fieldsets = get_admin_lang_section(_("Title"), ['title', 'subtitle', 'description', 'link_url'])
    fieldsets += [(None, {'fields': ('slug', 'cover_image')}),]
    fieldsets += [(_("Address"), {'fields': ('street_address','street_address2','postal_code','city', 'country','latitude','longitude')}),]
    fieldsets += [(_("Status"), {'fields': ('status',)}),]
    
    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}

    inlines = [SeasonInline]

    def is_geoposition_set(self, obj):
        return bool(obj.latitude)
    is_geoposition_set.boolean = True
    is_geoposition_set.short_description = _("Geoposition?")


admin.site.register(Location, LocationAdmin)

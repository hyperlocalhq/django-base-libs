# -*- coding: UTF-8 -*-

from django.contrib import admin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _, ugettext

from base_libs.admin import ExtendedModelAdmin
from base_libs.admin import ExtendedStackedInline
from base_libs.models.admin import get_admin_lang_section

from filebrowser.settings import URL_FILEBROWSER_MEDIA

from models import Service
from models import AccessibilityOption
from models import Location
from models import Stage
from models import Image
from models import SocialMediaChannel

class ServiceAdmin(ExtendedModelAdmin):

    save_on_top = True
    list_display = ['title', 'icon']

    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug', 'image', 'sort_order', )}),]

    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}

    def icon(self, obj):
        return """<img alt="" src="%s%s" />""" % (settings.MEDIA_URL, obj.image.path)
    icon.allow_tags = True

admin.site.register(Service, ServiceAdmin)


class AccessibilityOptionAdmin(ExtendedModelAdmin):

    save_on_top = True
    list_display = ['title', 'icon']

    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug', 'image', 'sort_order', )}),]

    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}

    def icon(self, obj):
        return """<img alt="" src="%s%s" />""" % (settings.MEDIA_URL, obj.image.path)
    icon.allow_tags = True

admin.site.register(AccessibilityOption, AccessibilityOptionAdmin)


class StageInline(ExtendedStackedInline):
    model = Stage
    extra = 0
    fieldsets = get_admin_lang_section(_("Title"), ['title', 'description',])
    fieldsets += [(None, {'fields': ('slug', )}),]
    fieldsets += [(_("Address"), {'fields': ('street_address', 'street_address2', 'postal_code', 'city', 'latitude', 'longitude')}),]
    # classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)


class ImageInline(ExtendedStackedInline):
    model = Image
    extra = 0
    # classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)


class SocialMediaChannelInline(ExtendedStackedInline):
    model = SocialMediaChannel
    extra = 0
    # classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)


class LocationAdmin(ExtendedModelAdmin):
    class Media:
        js = (
            "%sjs/AddFileBrowser.js" % URL_FILEBROWSER_MEDIA,
        )

    fieldsets = get_admin_lang_section(_("Title"), ['title', 'subtitle', 'description',])
    fieldsets += [(None, {'fields': ('slug', )}),]
    fieldsets += [(_("Address"), {'fields': ('street_address', 'street_address2', 'postal_code', 'city', 'latitude', 'longitude')}),]
    fieldsets += [(_("Contacts"), {'fields': ((_("Phone"), {'fields': ('phone_country', 'phone_area', 'phone_number')}), (_("Fax"), {'fields': ('fax_country', 'fax_area', 'fax_number')}),'email','website', )}),]
    fieldsets += [(_("Tickets"), {'fields': ('tickets_street_address', 'tickets_street_address2', 'tickets_postal_code', 'tickets_city', 'tickets_email', 'tickets_website')}),]
    fieldsets += [(_("Services"), {'fields': ('services',)}),]
    fieldsets += [(_("Accessibility"), {'fields': ('accessibility_options',)}),]
    fieldsets += [(_("Status"), {'fields': ('status',)}),]

    inlines = [StageInline, ImageInline, SocialMediaChannelInline]

    filter_horizontal = ['services', 'accessibility_options']

    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}

admin.site.register(Location, LocationAdmin)
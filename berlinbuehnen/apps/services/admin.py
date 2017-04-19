# -*- coding: UTF-8 -*-

from django.contrib import admin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _, ugettext
from django.core.urlresolvers import reverse
from django.utils.text import force_unicode

from cms.admin.placeholderadmin import PlaceholderAdmin

from base_libs.admin import ExtendedModelAdmin
from base_libs.admin import ExtendedStackedInline
from base_libs.models.admin import get_admin_lang_section

from .models import (
    ServicesOverviewPage,
    ServicesCategory,
    Service,
    LinksPage,
    ArticlesPage,
)


class ServicesCategoryInline(ExtendedStackedInline):
    model = ServicesCategory
    extra = 0
    fieldsets = get_admin_lang_section(_("Title"), ["title", "subtitle", "short_description"])
    fieldsets += [
        (_("Details"), {'fields': ("slug", "image", "sort_order", "get_edit_link")}),
    ]
    readonly_fields = ["get_edit_link"]

    def get_edit_link(self, obj=None):
        if obj.pk:  # if object has already been saved and has a primary key, show link to it
            url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.module_name), args=[force_unicode(obj.pk)])
            return """<a href="{url}">{text}</a>""".format(
                url=url,
                text=ugettext("Edit this category separately to add services"),
            )
        return ugettext("(save and continue editing to create a link)")
    get_edit_link.short_description = _("Edit link")
    get_edit_link.allow_tags = True

class ServicesOverviewPageAdmin(ExtendedModelAdmin):
    save_on_top = True
    list_display = ["title", "creation_date", "modified_date", "header_bg_color", "status"]
    list_filter = ["status", "creation_date", "modified_date"]

    fieldsets = get_admin_lang_section(_("Title"), ["title", "short_description"])
    fieldsets += [
        (_("Details"), {'fields': ("slug", "header_bg_color", "header_icon")}),
        (_("Publishing status"), {'fields': ("status",)}),
    ]
    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}
    inlines = [ServicesCategoryInline]

admin.site.register(ServicesOverviewPage, ServicesOverviewPageAdmin)


class ServiceInline(ExtendedStackedInline):
    model = Service
    extra = 0
    fieldsets = get_admin_lang_section(_("Title"), ["title", "subtitle", "short_description", "external_link"])
    fieldsets += [
        (_("Details"), {'fields': ("location", "image", "sort_order")}),
    ]


class ServicesCategoryAdmin(ExtendedModelAdmin):
    list_display = ("title", "page")
    list_filter = ("page", "creation_date", "modified_date")

    fieldsets = [
        (_("Page"), {'fields': ("page",)}),
    ]
    fieldsets += get_admin_lang_section(_("Title"), ["title", "subtitle", "short_description"])
    fieldsets += [
        (_("Details"), {'fields': ("slug", "page", "image", "sort_order")}),
    ]
    inlines = [ServiceInline]

admin.site.register(ServicesCategory, ServicesCategoryAdmin)


class LinksPageAdmin(ExtendedModelAdmin, PlaceholderAdmin):
    change_form_template = 'admin/change_form_with_placeholder.html'
    save_on_top = True
    list_display = ["title", "creation_date", "modified_date", "header_bg_color", "status"]
    list_filter = ["status", "creation_date", "modified_date"]

    fieldsets = get_admin_lang_section(_("Title"), ["title", "short_description"])
    fieldsets += [
        (_("Details"), {'fields': ("slug", "header_bg_color", "header_icon")}),
        (_("Content"), {'fields': ("content",)}),
        (_("Publishing status"), {'fields': ("status",)}),
    ]

    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}

admin.site.register(LinksPage, LinksPageAdmin)


class ArticlesPageAdmin(ExtendedModelAdmin, PlaceholderAdmin):
    change_form_template = 'admin/change_form_with_placeholder.html'
    save_on_top = True
    list_display = ["title", "creation_date", "modified_date", "header_bg_color", "status"]
    list_filter = ["status", "creation_date", "modified_date"]

    fieldsets = get_admin_lang_section(_("Title"), ["title", "short_description"])
    fieldsets += [
        (_("Details"), {'fields': ("slug", "header_bg_color", "header_icon")}),
        (_("Content"), {'fields': ("content",)}),
        (_("Publishing status"), {'fields': ("status",)}),
    ]

    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}

admin.site.register(ArticlesPage, ArticlesPageAdmin)



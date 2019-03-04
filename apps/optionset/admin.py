from django.contrib import admin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from base_libs.models.admin import get_admin_lang_section

from jetson.apps.optionset.models import Prefix, Salutation, IndividualLocationType, InstitutionalLocationType, PhoneType, EmailType, URLType, IMType


class IMTypeOptions(admin.ModelAdmin):
    save_on_top = True
    list_display = ['title', 'sort_order']

    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [
        (None, {
            'fields': ('slug', 'sort_order')
        }),
    ]
    prepopulated_fields = {
        "slug": ("title_%s" % settings.LANGUAGE_CODE, ),
    }


class URLTypeOptions(admin.ModelAdmin):
    save_on_top = True
    list_display = ['title', 'sort_order']

    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [
        (None, {
            'fields': ('slug', 'sort_order')
        }),
    ]
    prepopulated_fields = {
        "slug": ("title_%s" % settings.LANGUAGE_CODE, ),
    }


class InstitutionalLocationTypeOptions(admin.ModelAdmin):
    save_on_top = True
    list_display = ['title', 'sort_order']

    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [
        (None, {
            'fields': ('slug', 'sort_order')
        }),
    ]
    prepopulated_fields = {
        "slug": ("title_%s" % settings.LANGUAGE_CODE, ),
    }


class IndividualLocationTypeOptions(admin.ModelAdmin):
    save_on_top = True
    list_display = ['title', 'sort_order']

    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [
        (None, {
            'fields': ('slug', 'sort_order')
        }),
    ]
    prepopulated_fields = {
        "slug": ("title_%s" % settings.LANGUAGE_CODE, ),
    }


class PrefixOptions(admin.ModelAdmin):
    save_on_top = True
    list_display = ['title', 'sort_order']

    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [
        (None, {
            'fields': ('slug', 'sort_order', 'gender')
        }),
    ]
    radio_fields = {'gender': admin.HORIZONTAL}
    prepopulated_fields = {
        "slug": ("title_%s" % settings.LANGUAGE_CODE, ),
    }


class PhoneTypeOptions(admin.ModelAdmin):
    save_on_top = True
    list_display = ['title', 'sort_order', 'vcard_name']

    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [
        (None, {
            'fields': ('slug', 'sort_order', 'vcard_name')
        }),
    ]
    prepopulated_fields = {
        "slug": ("title_%s" % settings.LANGUAGE_CODE, ),
    }


class EmailTypeOptions(admin.ModelAdmin):
    save_on_top = True
    list_display = ['title', 'sort_order']

    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [
        (None, {
            'fields': ('slug', 'sort_order')
        }),
    ]
    prepopulated_fields = {
        "slug": ("title_%s" % settings.LANGUAGE_CODE, ),
    }


class SalutationOptions(admin.ModelAdmin):
    save_on_top = True
    list_display = ['title', 'sort_order']

    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [
        (None, {
            'fields': ('slug', 'sort_order')
        }),
    ]
    fieldsets += get_admin_lang_section(_("Template"), ['template'])
    prepopulated_fields = {
        "slug": ("title_%s" % settings.LANGUAGE_CODE, ),
    }


admin.site.register(IMType, IMTypeOptions)
admin.site.register(URLType, URLTypeOptions)
admin.site.register(InstitutionalLocationType, InstitutionalLocationTypeOptions)
admin.site.register(IndividualLocationType, IndividualLocationTypeOptions)
admin.site.register(Prefix, PrefixOptions)
admin.site.register(PhoneType, PhoneTypeOptions)
admin.site.register(EmailType, EmailTypeOptions)
admin.site.register(Salutation, SalutationOptions)

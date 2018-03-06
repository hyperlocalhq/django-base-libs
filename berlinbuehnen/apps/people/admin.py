# -*- coding: UTF-8 -*-

from django.contrib import admin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _, ugettext

from base_libs.admin import ExtendedModelAdmin
from base_libs.admin import ExtendedStackedInline
from base_libs.models.admin import get_admin_lang_section

from models import Prefix
from models import InvolvementType
from models import AuthorshipType
from models import Person


class PrefixAdmin(ExtendedModelAdmin):
    save_on_top = True
    list_display = ['title', 'sort_order']

    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug', 'gender', 'sort_order', )}),]

    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}

admin.site.register(Prefix, PrefixAdmin)


class InvolvementTypeAdmin(ExtendedModelAdmin):
    save_on_top = True
    list_display = ['title', 'sort_order']

    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug', 'sort_order', )}),]

    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}

admin.site.register(InvolvementType, InvolvementTypeAdmin)


class AuthorshipTypeAdmin(ExtendedModelAdmin):
    save_on_top = True
    list_display = ['title', 'sort_order']

    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug', 'sort_order', )}),]

    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}

admin.site.register(AuthorshipType, AuthorshipTypeAdmin)


class PersonAdmin(ExtendedModelAdmin):
    list_display = ('last_name', 'first_name', 'prefix')
    search_fields = ('first_name', 'last_name')

    fieldsets = [(None, {'fields': ('prefix', 'first_name', 'last_name', 'slug')}),]
    fieldsets += [(_("Status"), {'fields': ('status',)}),]

    prepopulated_fields = {"slug": ("first_name", "last_name"),}

admin.site.register(Person, PersonAdmin)
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from base_libs.models.admin import get_admin_lang_section
from base_libs.admin import ExtendedModelAdmin
from base_libs.models.admin import PublishingMixinAdminOptions

from .models import LoginAction, WelcomeMessage


@admin.register(LoginAction)
class LoginActionAdmin(ExtendedModelAdmin):
    save_on_top = True
    list_display = ["login_date", "user", "user_agent"]
    list_filter = ["login_date"]
    search_fields = ["user__username", "user__email", "user__first_name", "user__last_name"]
    fields = ["login_date", "user", "user_agent"]
    readonly_fields = ["login_date", "user", "user_agent"]

    def has_add_permission(self, request):
        return False


@admin.register(WelcomeMessage)
class WelcomeMessageAdmin(ExtendedModelAdmin):
    save_on_top = True
    list_display = ["title", "get_rendered_content", "condition", "creation_date", "modified_date", "is_published"]
    list_filter = ["condition", "creation_date", "modified_date"]
    search_fields = ["title_de", "title_en", "content_de", "content_en"]

    fieldsets = [
        (None, {'fields': ("condition",)}),
    ]
    fieldsets += get_admin_lang_section(_("Contents"), ["title", "content"])
    fieldsets += PublishingMixinAdminOptions.fieldsets

    raw_id_fields = ('author',)
    autocomplete_lookup_fields = {
        'fk': ["author"],
    }

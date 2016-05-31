# -*- coding: UTF-8 -*-
from django.contrib import admin
from .models import PrivacySettings


class PrivacySettingsAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ("user", "display_to_public", "display_username")
    list_filter = ("display_to_public", "display_username")
    search_fields = ("user__username", "user__first_name", "user__last_name", "user__email")


admin.site.register(PrivacySettings, PrivacySettingsAdmin)
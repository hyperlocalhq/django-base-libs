# -*- coding: UTF-8 -*-

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.admin import User, Group


class UserAdminExtended(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff',
        'date_joined', 'last_login'
    )
    list_filter = (
        'is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login'
    )
    ordering = ('last_name', 'first_name', 'username')
    save_on_top = True


class GroupAdminExtended(GroupAdmin):
    list_display = ("__str__", "display_users")


admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, UserAdminExtended)
admin.site.register(Group, GroupAdminExtended)

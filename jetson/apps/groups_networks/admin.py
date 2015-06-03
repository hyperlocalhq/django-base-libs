# -*- coding: UTF-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from filebrowser.settings import URL_FILEBROWSER_MEDIA

from jetson.apps.groups_networks.models import PersonGroup, GroupMembership

class GroupMembershipOptions(admin.ModelAdmin):
    save_on_top = True
    list_display = ('user', 'person_group', 'role', 'title', 'activation')
    list_filter = ('person_group', 'role')
    fieldsets = (
      (None, {'classes': ('collapse open', 'float-checkbox'), 'fields': ( 'user', 'person_group', 'role', 'title_en', 'title_de','inviter',
      ('is_accepted','is_blocked','is_contact_person'),'confirmer'
        )}),
    )

class PersonGroupOptions(admin.ModelAdmin):
    class Media:
        js = (
            "%sjs/AddFileBrowser.js" % URL_FILEBROWSER_MEDIA,
            )
    save_on_top = True
    list_display = ('title', 'title2', 'group_type', 'access_type', 'preferred_language', 'status')
    list_filter = ('creation_date', 'group_type', 'status', 'preferred_language')

admin.site.register(GroupMembership, GroupMembershipOptions)
admin.site.register(PersonGroup, PersonGroupOptions)


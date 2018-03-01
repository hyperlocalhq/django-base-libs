# -*- coding: UTF-8 -*-
import os

from django.conf import settings
from django.contrib import admin

from filebrowser.settings import URL_FILEBROWSER_MEDIA

from cms.admin.pageadmin import PageAdmin
from cms.admin.permissionadmin import PagePermissionInlineAdmin
from cms.models import Page, GlobalPagePermission
from cms.utils.conf import get_cms_setting

from .models import CMSPageOpenGraph

# def has_recover_permission(self, request):
#     if "reversion" not in settings.INSTALLED_APPS:
#         return False
#     user = request.user
#     if user.is_superuser:
#         return True
#     try:
#         perm = GlobalPagePermission.objects.get(user=user)
#         if perm.can_recover:
#             return True
#     except:
#         pass
#     return False
#
# PageAdmin.has_recover_permission = has_recover_permission
# # PageAdmin.fieldsets[0][1]['classes'] = ("grp-collapse", "grp-closed",)
# # if len(PageAdmin.fieldsets) > 4:
# #     PageAdmin.fieldsets[4][1]['classes'] = ("grp-collapse", "grp-closed",)
#
# PageAdmin.media.js = [
#     'cms/js/plugins/admincompat.js',
#     'cms/js/libs/jquery.query.js',
#     'cms/js/libs/jquery.ui.core.js',
#     'cms/js/libs/jquery.ui.dialog.js',
#     '{}js/AddFileBrowser.js'.format(URL_FILEBROWSER_MEDIA),
# ]
#
# # PageAdmin.fieldsets[3][1]['classes'] = ("grp-collapse", "grp-closed")
# #
# # if get_cms_setting('SEO_FIELDS'):
# #     PageAdmin.fieldsets[4][1]['classes'] = ("grp-collapse", "grp-closed")
#
# PagePermissionInlineAdmin.classes = ['grp-collapse', 'grp-closed']


class CMSPageOpenGraphInline(admin.StackedInline):
    model = CMSPageOpenGraph
    classes = ['grp-collapse', 'grp-closed']
    extra = 0

PageAdmin.inlines.append(CMSPageOpenGraphInline)


admin.site.unregister(Page)
admin.site.register(Page, PageAdmin)

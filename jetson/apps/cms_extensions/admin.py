# -*- coding: UTF-8 -*-
import os

from django.conf import settings

from cms.admin.pageadmin import PageAdmin
from cms.admin.permissionadmin import PagePermissionInlineAdmin
from cms.forms.widgets import PluginEditor
from cms.models import GlobalPagePermission

def has_recover_permission(self, request):
    if "reversion" not in settings.INSTALLED_APPS:
        return False
    user = request.user
    if user.is_superuser:
        return True
    try:
        perm = GlobalPagePermission.objects.get(user=user)
        if perm.can_recover:
            return True
    except:
        pass
    return False
    
PageAdmin.has_recover_permission = has_recover_permission
PageAdmin.fieldsets[3][1]['classes'] = ("collapse", "closed",)
if len(PageAdmin.fieldsets) > 4:
    PageAdmin.fieldsets[4][1]['classes'] = ("collapse", "closed",)
    
PageAdmin.Media.js = [os.path.join(settings.CMS_MEDIA_URL, path) for path in (
    #'js/lib/jquery.js',
    'js/lib/jquery.query.js',
    #'js/lib/ui.core.js',
    #'js/lib/ui.dialog.js',
    )]

PagePermissionInlineAdmin.classes = ['collapse', 'closed']

PluginEditor.Media.js = [os.path.join(settings.CMS_MEDIA_URL, path) for path in (
    #'js/lib/ui.core.js',
    #'js/lib/ui.sortable.js',
    'js/plugin_editor.js',
    )]

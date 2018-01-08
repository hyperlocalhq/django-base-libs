# -*- coding: UTF-8 -*-
import os

from django.conf import settings

from cms.admin.pageadmin import PageAdmin
from cms.admin.permissionadmin import PagePermissionInlineAdmin
from cms.forms.widgets import PluginEditor
from cms.models import GlobalPagePermission
from cms.utils import cms_static_url
from cms.utils.conf import get_cms_setting

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
PageAdmin.fieldsets[3][1]['classes'] = ("grp-collapse", "grp-closed",)
if len(PageAdmin.fieldsets) > 4:
    PageAdmin.fieldsets[4][1]['classes'] = ("grp-collapse", "grp-closed",)

PageAdmin.Media.js = [cms_static_url(path) for path in [
    'js/plugins/admincompat.js',
    'js/libs/jquery.query.js',
    'js/libs/jquery.ui.core.js',
    'js/libs/jquery.ui.dialog.js',
    ]]

PageAdmin.fieldsets[3][1]['classes'] = ("grp-collapse", "grp-closed")

if get_cms_setting('SEO_FIELDS'):
    PageAdmin.fieldsets[4][1]['classes'] = ("grp-collapse", "grp-closed")

PagePermissionInlineAdmin.classes = ['grp-collapse', 'grp-closed']

'''
PluginEditor.Media.js = [os.path.join(settings.CMS_MEDIA_URL, path) for path in (
    #'js/lib/ui.core.js',
    #'js/lib/ui.sortable.js',
    'js/plugin_editor.js',
    )]
'''

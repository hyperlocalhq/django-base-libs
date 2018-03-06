# -*- coding: UTF-8 -*-
import os

from django.conf import settings
from django.contrib import admin

from cms.admin.pageadmin import PageAdmin
from cms.admin.permissionadmin import PagePermissionInlineAdmin
from cms.models import Page, GlobalPagePermission
from cms.utils.conf import get_cms_setting

from .models import CMSPageOpenGraph

class CMSPageOpenGraphInline(admin.StackedInline):
    model = CMSPageOpenGraph
    classes = ['grp-collapse', 'grp-closed']
    extra = 0

PageAdmin.inlines.append(CMSPageOpenGraphInline)


admin.site.unregister(Page)
admin.site.register(Page, PageAdmin)

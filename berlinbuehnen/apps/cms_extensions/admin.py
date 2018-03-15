# -*- coding: UTF-8 -*-
from django.contrib import admin

from cms.admin.pageadmin import PageAdmin
from cms.models import Page

from .models import CMSPageOpenGraph

class CMSPageOpenGraphInline(admin.StackedInline):
    model = CMSPageOpenGraph
    classes = ['grp-collapse', 'grp-closed']
    extra = 0

PageAdmin.inlines.append(CMSPageOpenGraphInline)

admin.site.unregister(Page)
admin.site.register(Page, PageAdmin)

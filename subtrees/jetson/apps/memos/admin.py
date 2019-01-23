# -*- coding: UTF-8 -*-
from django.contrib import admin

from base_libs.models.admin import ObjectRelationMixinAdminOptions

from jetson.apps.memos.models import MemoCollection, Memo


class Memo_Inline(
    ObjectRelationMixinAdminOptions(extending=admin.StackedInline)
):
    model = Memo
    extra = 0


class MemoCollectionOptions(admin.ModelAdmin):
    save_on_top = True
    list_display = ('token', 'creation_date', 'expiration', 'memo_count')
    inlines = [Memo_Inline]


admin.site.register(MemoCollection, MemoCollectionOptions)

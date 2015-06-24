# -*- coding: UTF-8 -*-
from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.forms.models import inlineformset_factory

from base_libs.models.admin import ObjectRelationMixinAdminForm, ObjectRelationMixinAdminOptions

from jetson.apps.memos.models import MemoCollection, Memo

class MemoAdminForm(ObjectRelationMixinAdminForm()):
    pass

class Memo_Inline(ObjectRelationMixinAdminOptions(extending=admin.StackedInline)):
    form = MemoAdminForm
    model = Memo
    extra = 0

class MemoCollectionOptions(admin.ModelAdmin):
    save_on_top = True
    list_display = ('token', 'creation_date', 'expiration', 'memo_count')
    inlines = [Memo_Inline]

admin.site.register(MemoCollection, MemoCollectionOptions)


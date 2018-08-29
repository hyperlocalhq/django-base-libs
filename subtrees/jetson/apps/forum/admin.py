# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from base_libs.admin import ExtendedModelAdmin
from base_libs.admin import ExtendedStackedInline
from base_libs.models import MultiSiteContainerMixinAdminOptions
from base_libs.models import MultiSiteContainerMixinAdminForm
from base_libs.models.admin import get_admin_lang_section
from base_libs.admin.tree_editor import TreeEditor

from jetson.apps.forum.models import ForumContainer, Forum, ForumThread, ForumReply

class ForumContainerAdminForm(MultiSiteContainerMixinAdminForm):
    class Meta:
        model = ForumContainer

class ForumContainerOptions(MultiSiteContainerMixinAdminOptions):
    save_on_top = True
    search_fields = ('title',)
    list_display = ('title', 'get_sites', 'get_content_object_display', 'sysname')
    list_filter =  ("creation_date", "modified_date",)

    fieldsets = get_admin_lang_section(_('Title'), ['title'])
    fieldsets += MultiSiteContainerMixinAdminOptions.fieldsets
    fieldsets += [
        (_('Administration'), {'fields': ('allow_bumping', 'max_level'), 'classes': ("grp-collapse grp-closed",),}),
    ]
    form = ForumContainerAdminForm

class ForumThread_Inline(ExtendedStackedInline):
    model = ForumThread
    extra = 0
    
    fieldsets = [
        (None, {'fields': ('is_sticky', )}),
    ]
    fieldsets += [
        (_('Contents'), {'fields': ('subject', 'message'),}),
    ]
    fieldsets += [
        (_('Administration'), {'fields': ('status',),}),
    ]

class ForumOptions(TreeEditor):
    save_on_top = True
    # dragndrop should not be allowed for forums!!!!!
    dragdrop_allowed = True
    
    inlines = [ForumThread_Inline]
    search_fields = ('title',)    
    list_display = ('actions_column', 'indented_short_title', 'container', 'creator', 'get_nof_threads', 'get_nof_replies', 'status') 
    list_filter = ('container', 'creation_date', 'creator', 'modified_date', 'modifier', 'status')
 
    fieldsets = [(None, {'fields': ('container', 'parent', 'slug')}),]
    fieldsets += [
        (_('Contents'), {'fields': ('title', 'short_title', 'description'),}),
    ]
    prepopulated_fields = {'slug': ('title',),}
    

class ForumReply_Inline(ExtendedStackedInline):
    model = ForumReply
    extra = 0
    fieldsets = [
        (None, {'fields': ('parent', )}),
    ]
    fieldsets += [
        (_('Contents'), {'fields': ('message', ),}),
    ]

class ForumThreadOptions(ExtendedModelAdmin):
    save_on_top = True
    inlines = [ForumReply_Inline]
    search_fields = ('subject',)
    list_display = ('__unicode__', 'forum', 'creator', 'get_nof_replies', 'is_sticky', 'views')
    list_filter = ('forum', 'creation_date', 'creator', 'modified_date', 'modifier')
 
    fieldsets = [(None, {'fields': ('forum', 'is_sticky')}),]

    fieldsets += [
        (_('Contents'), {'fields': ('subject', 'message'),}),
    ]
    
class ForumReplyOptions(TreeEditor):
    save_on_top = True
    # drag & drop should not be allowed for forums!!!!!
    dragdrop_allowed = False
    search_fields = ('message',)
    list_display = ('actions_column', 'indented_short_title', 'thread', 'creator')
    list_filter = ('thread', 'creation_date', 'creator', 'modified_date', 'modifier')
 
    fieldsets = [(None, {'fields': ('thread', 'parent', )}),]

    fieldsets += [
        (_('Contents'), {'fields': ('message', ),}),
    ]

admin.site.register(ForumContainer, ForumContainerOptions)
admin.site.register(Forum, ForumOptions)
admin.site.register(ForumThread, ForumThreadOptions)
admin.site.register(ForumReply, ForumReplyOptions)


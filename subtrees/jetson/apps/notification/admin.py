# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from base_libs.models.admin import ObjectRelationMixinAdminOptions
from base_libs.models.admin import get_admin_lang_section

from jetson.apps.notification.models import NoticeTypeCategory
from jetson.apps.notification.models import NoticeType
from jetson.apps.notification.models import NoticeSetting
from jetson.apps.notification.models import NoticeEmailTemplate
from jetson.apps.notification.models import Notice
from jetson.apps.notification.models import ObservedItem
from jetson.apps.notification.models import Digest
from jetson.apps.notification.models import DigestNotice


class NoticeTypeCategoryAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('title', 'is_public')
    list_filter = ('is_public', )
    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [
        (None, {
            'fields': ('is_public', )
        }),
    ]


class NoticeTypeAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = (
        'sysname', 'display', 'description', 'category', 'sort_order',
        'default', 'is_public'
    )
    list_filter = ('category', 'is_public', 'default')
    list_editable = ('sort_order', )
    fieldsets = [
        (None, {
            'fields': (
                'category',
                'sysname',
            )
        }),
    ]
    fieldsets += get_admin_lang_section(
        _("Contents"), ['display', 'description', 'message_template']
    )
    fieldsets += [
        (
            _('Additional'), {
                'fields': ('default', 'is_public'),
                'classes': ("grp-collapse grp-closed", ),
            }
        ),
    ]


class NoticeEmailTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'subject', 'get_site']
    search_fields = (
        'name',
        'subject',
        'subject_de',
        'body',
        'body_de',
        'body_html',
        'body_html_de',
    )
    save_on_top = True
    filter_horizontal = ('allowed_placeholders', )


class NoticeSettingAdmin(admin.ModelAdmin):
    save_on_top = True
    list_filter = ('notice_type', 'medium', 'frequency')
    list_display = ('id', 'user', 'notice_type', 'medium', 'frequency')


class NoticeAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = (
        'message', 'user', 'notice_type', 'added', 'unseen', 'archived'
    )


class DigestNotice_Inline(admin.StackedInline):
    model = DigestNotice
    extra = 0


class DigestAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ("user", "frequency", "creation_date", "is_sent")
    list_filter = ("frequency", "is_sent")
    inlines = (DigestNotice_Inline, )


class ObservedItemOptions(ObjectRelationMixinAdminOptions()):
    save_on_top = True
    list_display = ('__unicode__', 'get_content_object_display')
    fieldsets = []


admin.site.register(NoticeTypeCategory, NoticeTypeCategoryAdmin)
admin.site.register(NoticeType, NoticeTypeAdmin)
admin.site.register(NoticeEmailTemplate, NoticeEmailTemplateAdmin)
admin.site.register(NoticeSetting, NoticeSettingAdmin)
admin.site.register(Notice, NoticeAdmin)
admin.site.register(Digest, DigestAdmin)
admin.site.register(ObservedItem, ObservedItemOptions)
admin.site.register(DigestNotice)

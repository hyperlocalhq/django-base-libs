# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from base_libs.models.admin import ObjectRelationMixinAdminOptions
from base_libs.models.admin import get_admin_lang_section
from base_libs.admin import ExtendedModelAdmin

from jetson.apps.comments.models import Comment, ModeratorDeletionReason, ModeratorDeletion


class CommentOptions(ObjectRelationMixinAdminOptions()):
    save_on_top = True
    fieldsets = (
        ('Related', {'fields': ('content_type', 'object_id', 'site')}),
        ('Author', {'fields': ('user', 'name', 'email', 'url_link')}),
        ('Content', {'fields': ('headline', 'comment')}),
        ('Ratings', {'fields': ('rating1', 'rating2', 'rating3', 'rating4', 'rating5', 'rating6', 'rating7', 'rating8', 'valid_rating')}),
        ('Meta', {'fields': ('is_public', 'is_removed', 'is_spam', 'ip_address')}),
    )
    list_display = ('name', 'submit_date', 'content_type', 'get_content_object_display')
    list_filter = ('submit_date',)
    date_hierarchy = 'submit_date'
    search_fieldsets = ('comment',)
    raw_id_fields = ["user"]

class ModeratorDeletionReasonOptions(ExtendedModelAdmin):
    save_on_top = True
    list_display = ('title',)
    
    fieldsets = get_admin_lang_section(_('Reason'), ['title', 'reason'])
    search_fieldsets = ('title',)

class ModeratorDeletionOptions(admin.ModelAdmin):
    save_on_top = True
    list_display = ('user', 'comment', 'deletion_reason', 'deletion_date')
    search_fieldsets = ('user', 'deletion_reason')

admin.site.register(Comment, CommentOptions)
admin.site.register(ModeratorDeletionReason, ModeratorDeletionReasonOptions)
admin.site.register(ModeratorDeletion, ModeratorDeletionOptions)


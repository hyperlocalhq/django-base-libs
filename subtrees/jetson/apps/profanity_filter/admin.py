# -*- coding: UTF-8 -*-
from django.contrib import admin

from base_libs.models.admin import ObjectRelationMixinAdminOptions

from jetson.apps.profanity_filter.models import SwearWord
from jetson.apps.profanity_filter.models import SwearingCase


class SwearWordOptions(admin.ModelAdmin):
    save_on_top = True

    list_display = ('word', )
    search_fields = ('word', )


class SwearingCaseOptions(ObjectRelationMixinAdminOptions()):

    save_on_top = True

    list_display = (
        'creation_date', 'modified_date', 'user', 'get_content_object_display',
        'used_words'
    )
    list_filter = ('creation_date', 'modified_date')
    search_fields = ('used_words', )

    fieldsets = (
        (
            None, {
                'fields': (
                    'user',
                    'content_type',
                    'object_id',
                    'used_words',
                )
            }
        ),
    )


admin.site.register(SwearWord, SwearWordOptions)
admin.site.register(SwearingCase, SwearingCaseOptions)

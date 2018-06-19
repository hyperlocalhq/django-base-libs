# -*- coding: UTF-8 -*-

from django.utils.translation import ugettext_lazy as _

from jetson.apps.external_services.admin import *

ArticleImportSource = models.get_model("external_services", "ArticleImportSource")


class ArticleImportSourceOptions(ExtendedModelAdmin):
    save_on_top = True

    list_filter = ('content_provider',)

    list_display = ('title', 'url', 'sysname', 'content_provider', 'are_excerpts')

    search_fields = ('title', 'url', 'sysname')

    fieldsets = (
        (None, {
            'fields': ('title', 'url', 'sysname', 'content_provider', 'are_excerpts')
        }),
        (_("Defaults"), {
            'fields': ('default_sites', 'default_creative_sectors', 'default_categories', 'default_status')
        }),
        # (_("Authentication"), {
        #    'fields':  ('api_key', 'user', 'password', )
        #    }),
    )


admin.site.register(ArticleImportSource, ArticleImportSourceOptions)

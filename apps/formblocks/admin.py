from django.contrib import admin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from base_libs.models.admin import get_admin_lang_section
from base_libs.admin import ExtendedModelAdmin
from base_libs.models.admin import PublishingMixinAdminOptions

from ccb.apps.formblocks.models import FormBlock


class FormBlockOptions(ExtendedModelAdmin):
    save_on_top = True
    list_display = [
        "sysname", "_get_stripped_content"
    ]
    search_fields = [
        "sysname", "content_de", "content_en"
    ]
    ordering = [
        "sysname",
    ]

    fieldsets = []
    fieldsets += get_admin_lang_section(_("Contents"), ["content",])
    fieldsets += [
        (None, {
            'fields': ("sysname", )
        }),
    ]


admin.site.register(FormBlock, FormBlockOptions)

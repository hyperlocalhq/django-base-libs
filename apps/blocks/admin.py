from django.contrib import admin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from base_libs.models.admin import get_admin_lang_section
from base_libs.admin import ExtendedModelAdmin
from base_libs.models.admin import PublishingMixinAdminOptions

from jetson.apps.blocks.models import InfoBlock

class InfoBlockOptions(ExtendedModelAdmin):
    save_on_top = True
    list_display = ["sysname", "title", "_get_stripped_content", "get_site", 'is_published']
    search_fields = ["sysname", "title_de", "title_en", "content_de", "content_en"]
    ordering = ["sysname",]
    
    fieldsets = [
        (None, {'fields': ("site",)}),
    ]
    fieldsets += get_admin_lang_section(_("Contents"), ["title", "content"])
    fieldsets += [
        (None, {'fields': ("sysname",)}),
    ]
    fieldsets += PublishingMixinAdminOptions.fieldsets
    
    prepopulated_fields = {"sysname": ("title_%s" % settings.LANGUAGE_CODE,),}

    raw_id_fields = ("author",)
    autocomplete_lookup_fields = {
        'fk': ["author"],
    }

admin.site.register(InfoBlock, InfoBlockOptions)


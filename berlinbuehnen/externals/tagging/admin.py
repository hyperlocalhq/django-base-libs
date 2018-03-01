from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from tagging.models import Tag, TaggedItem
from tagging.forms import TagAdminForm
from base_libs.models.admin import get_admin_lang_section

def get_translated_name(lang_code, lang_name):
    def get_name(self, obj):
        return getattr(obj, "name_%s" % lang_code)
    get_name.short_description = _("Name (%s)") % lang_name
    get_name.admin_order_field = "name_%s" % lang_code
    return get_name

class TagAdmin(admin.ModelAdmin):
    form = TagAdminForm
    
    fieldsets = get_admin_lang_section(_("Name"), ["name", "slug"])
    
    search_fields = []
    prepopulated_fields = {}
    for lang_code, lang_name in settings.LANGUAGES:
        prepopulated_fields['slug_%s' % lang_code] = ("name_%s" % lang_code,)
        search_fields += ['name_%s' % lang_code]

    def __init__(self, *args, **kwargs):
        super(TagAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = []

        for lang_code, lang_name in settings.LANGUAGES:
            function = get_translated_name(lang_code, lang_name)
            setattr(self, "get_name_%s" % lang_code, function.__get__(self, TagAdmin))

    def get_list_display(self, request):
        list_display = []
        for lang_code, lang_name in settings.LANGUAGES:
            list_display += ['get_name_%s' % lang_code]
        return list_display

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = []
        for lang_code, lang_name in settings.LANGUAGES:
            readonly_fields += ['get_name_%s' % lang_code]
        return readonly_fields


admin.site.register(TaggedItem)
admin.site.register(Tag, TagAdmin)





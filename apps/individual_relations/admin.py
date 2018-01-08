from django.contrib import admin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from base_libs.models.admin import get_admin_lang_section
from base_libs.admin.tree_editor import TreeEditor

from jetson.apps.individual_relations.models import IndividualRelationType, IndividualRelation

class IndividualRelationOptions(admin.ModelAdmin):
    fieldsets = (
        (   None,
            {'fields': ('user', 'relation_types', 'to_user', 'status')}
        ),
        (   _("Permissions granted to user #2 by user #1"),
            {'classes': ('grp-collapse grp-open','float-checkbox'),'fields': (
                ('display_birthday', 'display_address', 'display_phone'), 
                ('display_fax', 'display_mobile', 'display_im'), )}
        ),
        (   _("Additional"),
            {'fields': ('message',)}
        ),
    )
    list_display = ('__unicode__', 'status')
    list_filter = ('status',)
    save_on_top = True
    raw_id_fields = ('user','to_user',)
    autocomplete_lookup_fields = {
        'fk': ['user','to_user',],
        }

class IndividualRelationTypeOptions(TreeEditor):
    save_on_top = True
    list_display = ['actions_column', 'indented_short_title', 'backwards']
    
    fieldsets = [(None, {'fields': ('parent',)}),]
    fieldsets += get_admin_lang_section(_('Title'), ['title'])
    fieldsets += [(None, {'fields': ('slug', 'backwards')}),]

    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}

admin.site.register(IndividualRelation, IndividualRelationOptions)
admin.site.register(IndividualRelationType, IndividualRelationTypeOptions)


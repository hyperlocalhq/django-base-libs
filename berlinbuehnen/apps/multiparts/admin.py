# -*- coding: UTF-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from base_libs.admin import ExtendedModelAdmin
from base_libs.admin import ExtendedStackedInline

from models import Parent, Part


class PartInline(ExtendedStackedInline):
    model = Part
    extra = 0
    raw_id_fields = ['production']
    inline_classes = ('grp-collapse grp-open',)
    classes = ("grp-collapse grp-open",)


class ParentAdmin(ExtendedModelAdmin):
    list_display = ('production', 'creation_date', 'modified_date', 'get_children')
    search_fields = ('production__title',)

    raw_id_fields = ['production']
    inlines = [PartInline]

    def get_children(self, obj):
        return u'<br />'.join([u'» <a target="_blank" href="/admin/productions/production/%s/">%s</a>' % (part.production.pk, part.production.title) for part in obj.part_set.all()])
    get_children.short_description = _("Contains")
    get_children.allow_tags = True

admin.site.register(Parent, ParentAdmin)
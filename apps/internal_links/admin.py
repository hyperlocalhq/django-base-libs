# -*- coding: UTF-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _, ugettext
from django.utils.translation import string_concat
from base_libs.admin import ExtendedModelAdmin

from models import LinkGroup


class LinkGroupAdmin(ExtendedModelAdmin):
    list_display = ['__unicode__', 'creation_date', 'get_links_str', 'get_placement_str']
    list_filter = ['creation_date', 'language']
    search_fields = ['group_title', 'link_1_text', 'link_2_text', 'link_3_text']
    filter_horizontal = ['museums', 'exhibitions', 'events', 'workshops']

    fieldsets = (
        (_("Main data"), {'fields': ['group_title', 'language']}),
        (_("Links"), {'fields': [
            ('link_1_url', 'link_1_text'),
            ('link_2_url', 'link_2_text'),
            ('link_3_url', 'link_3_text'),
        ]}),
        (_("Placement"), {'fields': ['museums', 'exhibitions', 'events', 'workshops']}),
    )

    def get_links_str(self, obj):
        return u"<br />".join(['<a href="%(url)s" target="_blank">%(text)s</a>' % link for link in obj.get_links()])
    get_links_str.short_description = _('Links')
    get_links_str.allow_tags = True

    def get_placement_str(self, obj):
        placement_list = []
        if obj.museums.count():
            placement_list.append("<strong>" + ugettext("Museums") + "</strong>")
            for item in obj.museums.all():
                placement_list.append('<a href="%s" target="_blank">%s</a>' % (item.get_url_path(), item.title))
        if obj.exhibitions.count():
            placement_list.append("<strong>" + ugettext("Exhibitions") + "</strong>")
            for item in obj.exhibitions.all():
                placement_list.append('<a href="%s" target="_blank">%s</a>' % (item.get_url_path(), item.title))
        if obj.events.count():
            placement_list.append("<strong>" + ugettext("Events") + "</strong>")
            for item in obj.events.all():
                placement_list.append('<a href="%s" target="_blank">%s</a>' % (item.get_url_path(), item.title))
        if obj.workshops.count():
            placement_list.append("<strong>" + ugettext("Workshops") + "</strong>")
            for item in obj.workshops.all():
                placement_list.append('<a href="%s" target="_blank">%s</a>' % (item.get_url_path(), item.title))
        return u"<br />".join(placement_list)
    get_placement_str.short_description = _("Placement")
    get_placement_str.allow_tags = True


admin.site.register(LinkGroup, LinkGroupAdmin)
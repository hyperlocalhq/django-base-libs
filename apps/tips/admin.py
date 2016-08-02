# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from django.utils.translation import ugettext_lazy as _, ugettext

from filebrowser.settings import URL_FILEBROWSER_MEDIA

from base_libs.admin import ExtendedModelAdmin
from base_libs.models.admin import get_admin_lang_section
from base_libs.models.admin import ObjectRelationMixinAdminOptions

from .models import TipOfTheDay


class TipOfTheDayAdmin(ObjectRelationMixinAdminOptions()):
    class Media:
        js = (
            "%sjs/AddFileBrowser.js" % URL_FILEBROWSER_MEDIA,
        )

    save_on_top = True
    list_display = ('day', 'content_type', 'get_content_object_display', 'title', 'subtitle', )
    list_filter = ('event_type', 'content_type')
    date_hierarchy = 'day'
    search_fields = ('title', 'subtitle', 'location_title', 'event_type')

    fieldsets = [(_("Day"), {'fields': ('day',)}), ]
    fieldsets += [(_("Related Object"), {'fields': ('content_type', 'object_id')}), ]
    fieldsets += get_admin_lang_section(_("Details"), ['title', 'subtitle', 'location_title', 'event_type'])
    fieldsets += [(None, {'fields': ('image', 'starting_time')}), ]

    ordering = ['-day']

    related_lookup_fields = {
        'generic': [['content_type', 'object_id'],],
    }

    def related_object_details_json(self, request, content_type_id, object_id):
        """ Returns details about the chosen exhibition, event or workshop in JSON format """
        import json
        from django.utils.translation import activate, get_language

        ct = get_object_or_404(ContentType, pk=content_type_id)
        if ct.model.lower() not in ('exhibition', 'event', 'workshop'):
            raise Http404("This content type is not available")

        content_object = None
        try:
            content_object = ct.get_all_objects_for_this_type(pk=object_id)[0]
        except IndexError:
            raise Http404("This content object does not exist")

        data = {}

        data['image'] = ""
        if content_object.cover_image:
            data['image'] = content_object.cover_image.path

        data['starting_time'] = ""
        if ct.model.lower() == "event":
            t = content_object.get_closest_event_time()
            if t and t.start is not None:
                data['starting_time'] = t.start.strftime("%H:%M")
        elif ct.model.lower() == "workshop":
            t = content_object.get_closest_workshop_time()
            if t and t.start is not None:
                data['starting_time'] = t.start.strftime("%H:%M")

        current_language = get_language()
        for lang_code, lang_name in settings.LANGUAGES:
            activate(lang_code)
            field_name = 'title_{}'.format(lang_code)
            data[field_name] = getattr(content_object, field_name) or getattr(content_object, 'title_{}'.format(settings.LANGUAGE_CODE))
            field_name = 'subtitle_{}'.format(lang_code)
            data[field_name] = getattr(content_object, field_name) or getattr(content_object, 'subtitle_{}'.format(settings.LANGUAGE_CODE))
            data['location_title_{}'.format(lang_code)] = getattr(content_object.museum, 'title_{}'.format(lang_code), '') or getattr(content_object, 'location_title', '')
            if ct.model.lower() == "event":
                data['event_type_{}'.format(lang_code)] = ", ".join([
                    getattr(cat, 'title_{}'.format(lang_code), '') or getattr(cat, 'title_{}'.format(settings.LANGUAGE_CODE), '')
                    for cat in content_object.categories.all()
                ])
            else:
                data['event_type_{}'.format(lang_code)] = unicode(content_object._meta.verbose_name)
        activate(current_language)

        return HttpResponse(json.dumps(data))

    def get_urls(self):
        from django.conf.urls import patterns, url, include
        urls = super(TipOfTheDayAdmin, self).get_urls()
        urls = patterns('',
            url('^details-json/(?P<content_type_id>\d+)/(?P<object_id>\d+)/$', self.related_object_details_json),
        ) + urls
        return urls


admin.site.register(TipOfTheDay, TipOfTheDayAdmin)
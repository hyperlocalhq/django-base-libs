# -*- coding: UTF-8 -*-

from jetson.apps.articles.admin import *
from django.utils.translation import ugettext_lazy as _

from .models import TheaterOfTheWeek, TheaterOfTheWeekProduction


class TheaterOfTheWeekProductionInline(admin.StackedInline):
    extra = 0
    model = TheaterOfTheWeekProduction
    inline_classes = ('grp-collapse grp-open',)
    raw_id_fields = ('production',)
    autocomplete_lookup_fields = {
        'fk': ['production'],
    }
    ordering = ("sort_order",)
    sortable = True
    sortable_field_name = "sort_order"


@admin.register(TheaterOfTheWeek)
class TheaterOfTheWeekAdmin(ExtendedModelAdmin):
    save_on_top = True
    
    list_display = ['id', 'title', 'theater', 'author', 'status', 'published_from', 'published_till', 'views', 'language']
    list_display_links = ['title']
    list_filter = ('theater', 'published_from', 'published_till', 'status', 'language')
    search_fields = ('title', 'description', 'content', 'author__username', 'theater')
    
    fieldsets = []
    fieldsets += [(_("Theater of the week"), {'fields': ('title', 'subtitle', 'short_title', 'content', 'description', 'theater', 'language')})]
    fieldsets += [(None, {'fields': ('slug',)}),]
    fieldsets += [(_('Additional Content'), {
        'classes': ("collapse open",),
        'fields': ['image', (_("Description"), {'fields':['image_title', 'image_description']})]
    }),]
    fieldsets += [(_('Publish Status'), {
        'fields': ('author', 'status', 'published_from', 'published_till',),
        'classes': ("collapse open",),
        }),
    ]

    prepopulated_fields = {"slug": ("title",),}
    inlines = [TheaterOfTheWeekProductionInline]

# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from base_libs.admin.options import ExtendedStackedInline
from base_libs.models.admin import get_admin_lang_section
from base_libs.admin import ExtendedModelAdmin

from .models import Slideshow, Slide


class SlideInline(ExtendedStackedInline):
    model = Slide
    inline_classes = ("grp-collapse grp-closed",)
    sortable = True
    sortable_field_name = "sort_order"
    allow_add = True
    extra = 0
    fieldsets = get_admin_lang_section(None, ['title', 'subtitle', 'credits', 'alt'])
    fieldsets += [
        (None, {'fields': ["path", "link", "highlight"] }),
    ]
    fieldsets += [(None, {'fields': ["published_from", "published_till"]} ),]
    fieldsets += [(None, {'fields': ("sort_order", )}),]


class SlideshowOptions(ExtendedModelAdmin):
    save_on_top = True
    inlines = [SlideInline]
    list_display = ('id', '__unicode__', 'slides_shown_now')
    list_display_links = ('id', '__unicode__',)

    def slides_shown_now(self, obj):
        now = timezone.now()
        return _("%(num)s out of %(total)s") % {
            'num': obj.slide_set.filter(
                models.Q(published_from__lte=now) | models.Q(published_from__isnull=True),
                models.Q(published_till__gt=now) | models.Q(published_till__isnull=True)
            ).count(),
            'total': obj.slide_set.count(),
        }
        pass

    slides_shown_now.short_description = _("Slides published now")

admin.site.register(Slideshow, SlideshowOptions)

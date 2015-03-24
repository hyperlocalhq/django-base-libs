# -*- coding: UTF-8 -*-

from django.contrib import admin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from base_libs.admin import ExtendedModelAdmin
from base_libs.admin import ExtendedStackedInline
from base_libs.models.admin import get_admin_lang_section
from base_libs.admin.tree_editor import TreeEditor

from models import LanguageAndSubtitles
from models import ProductionCategory
from models import ProductionCharacteristics
from models import Production
from models import ProductionSocialMediaChannel
from models import ProductionVideo
from models import ProductionLiveStream
from models import ProductionImage
from models import ProductionPDF
from models import ProductionLeadership
from models import ProductionAuthorship
from models import ProductionInvolvement
from models import EventCharacteristics
from models import Event
from models import EventSocialMediaChannel
from models import EventVideo
from models import EventLiveStream
from models import EventImage
from models import EventPDF
from models import EventLeadership
from models import EventAuthorship
from models import EventInvolvement


class LanguageAndSubtitlesAdmin(ExtendedModelAdmin):
    save_on_top = True
    list_display = ['title', 'sort_order']

    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug', 'sort_order')}),]

    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}

admin.site.register(LanguageAndSubtitles, LanguageAndSubtitlesAdmin)


class ProductionCategoryAdmin(TreeEditor, ExtendedModelAdmin):
    save_on_top = True
    list_display = ['actions_column', 'indented_short_title', ]

    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug', 'parent')}),]

    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}

admin.site.register(ProductionCategory, ProductionCategoryAdmin)


class ProductionCharacteristicsAdmin(ExtendedModelAdmin):
    save_on_top = True
    list_display = ['title', 'sort_order']

    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug', 'sort_order')}),]

    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}

admin.site.register(ProductionCharacteristics, ProductionCharacteristicsAdmin)


class ProductionSocialMediaChannelInline(ExtendedStackedInline):
    model = ProductionSocialMediaChannel
    extra = 0
    inline_classes = ('grp-collapse grp-open',)


class ProductionVideoInline(ExtendedStackedInline):
    model = ProductionVideo
    extra = 0
    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('link_or_embed', 'sort_order')}),]
    inline_classes = ('grp-collapse grp-open',)


class ProductionLiveStreamInline(ExtendedStackedInline):
    model = ProductionLiveStream
    extra = 0
    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('link_or_embed', 'sort_order')}),]
    inline_classes = ('grp-collapse grp-open',)


class ProductionImageInline(ExtendedStackedInline):
    model = ProductionImage
    extra = 0
    inline_classes = ('grp-collapse grp-open',)


class ProductionPDFInline(ExtendedStackedInline):
    model = ProductionPDF
    extra = 0
    inline_classes = ('grp-collapse grp-open',)


class ProductionLeadershipInline(ExtendedStackedInline):
    model = ProductionLeadership
    extra = 0
    fieldsets = [(None, {'fields': ('person', 'sort_order', )}),]
    fieldsets += get_admin_lang_section(_("Function"), ['function',])
    raw_id_fields = ['person']
    inline_classes = ('grp-collapse grp-open',)


class ProductionAuthorshipInline(ExtendedStackedInline):
    model = ProductionAuthorship
    extra = 0
    raw_id_fields = ['person']
    inline_classes = ('grp-collapse grp-open',)


class ProductionInvolvementInline(ExtendedStackedInline):
    model = ProductionInvolvement
    extra = 0
    fieldsets = [(None, {'fields': ('person', 'involvement_type', 'sort_order')}),]
    fieldsets += get_admin_lang_section(_("Role / Instrument"), ['involvement_role', 'involvement_instrument'])
    raw_id_fields = ['person']
    inline_classes = ('grp-collapse grp-open',)


class ProductionAdmin(ExtendedModelAdmin):
    search_fields = ['title']
    fieldsets = get_admin_lang_section(_("Title"), ['title', 'prefix', 'subtitle', 'original', 'website'])
    fieldsets += [(None, {'fields': ('slug', )}),]
    fieldsets += [(_("Location"), {'fields': ['in_program_of', 'ensembles', 'play_locations', 'play_stages', 'organizers', 'in_cooperation_with']}),]
    fieldsets += [(_("Free Location"), {'fields': ['location_title', 'street_address', 'street_address2', 'postal_code', 'city', 'latitude', 'longitude']}),]
    fieldsets += [(_("Relations"), {'fields': ['categories', 'festivals', 'language_and_subtitles', 'related_productions']}),]
    fieldsets += get_admin_lang_section(_("Description"), ['description', 'teaser', 'work_info', 'contents', 'press_text', 'credits'])
    fieldsets += get_admin_lang_section(_("Imported"), ['concert_programm', 'supporting_programm', 'remarks', 'duration_text', 'subtitles_text', 'age_text'])
    fieldsets += [(_("Prices"), {'fields': ['price_from', 'price_till', 'free_entrance', 'tickets_website', get_admin_lang_section(_("Price information"), ['price_information'])]}),]
    fieldsets += [(_("Additional details"), {'fields': ['characteristics', 'age_from', 'age_till', 'edu_offer_website']}),]
    fieldsets += [(_("Sponsors"), {'fields': ['sponsors',]}),]
    fieldsets += [(_("Status"), {'fields': ['status',]}),]

    filter_horizontal = ['in_program_of', 'play_locations', 'play_stages', 'categories', 'festivals', 'related_productions', 'characteristics', 'sponsors']
    inlines = [
        ProductionSocialMediaChannelInline,
        ProductionVideoInline, ProductionLiveStreamInline, ProductionImageInline, ProductionPDFInline,
        ProductionLeadershipInline, ProductionAuthorshipInline, ProductionInvolvementInline,
    ]

admin.site.register(Production, ProductionAdmin)


class EventCharacteristicsAdmin(ExtendedModelAdmin):
    save_on_top = True
    list_display = ['title', 'sort_order']

    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug', 'sort_order')}),]

    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}

admin.site.register(EventCharacteristics, EventCharacteristicsAdmin)


class EventSocialMediaChannelInline(ExtendedStackedInline):
    model = EventSocialMediaChannel
    extra = 0
    inline_classes = ('grp-collapse grp-open',)


class EventVideoInline(ExtendedStackedInline):
    model = EventVideo
    extra = 0
    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('link_or_embed', 'sort_order')}),]
    inline_classes = ('grp-collapse grp-open',)


class EventLiveStreamInline(ExtendedStackedInline):
    model = EventLiveStream
    extra = 0
    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('link_or_embed', 'sort_order')}),]
    inline_classes = ('grp-collapse grp-open',)


class EventImageInline(ExtendedStackedInline):
    model = EventImage
    extra = 0
    inline_classes = ('grp-collapse grp-open',)


class EventPDFInline(ExtendedStackedInline):
    model = EventPDF
    extra = 0
    inline_classes = ('grp-collapse grp-open',)


class EventLeadershipInline(ExtendedStackedInline):
    model = EventLeadership
    extra = 0
    fieldsets = [(None, {'fields': ('person', 'sort_order', )}),]
    fieldsets += get_admin_lang_section(_("Function"), ['function',])
    raw_id_fields = ['person']
    inline_classes = ('grp-collapse grp-open',)


class EventAuthorshipInline(ExtendedStackedInline):
    model = EventAuthorship
    extra = 0
    raw_id_fields = ['person']
    inline_classes = ('grp-collapse grp-open',)


class EventInvolvementInline(ExtendedStackedInline):
    model = EventInvolvement
    extra = 0
    fieldsets = [(None, {'fields': ('person', 'involvement_type', 'sort_order')}),]
    fieldsets += get_admin_lang_section(_("Role / Instrument"), ['involvement_role', 'involvement_instrument'])
    raw_id_fields = ['person']
    inline_classes = ('grp-collapse grp-open',)


class EventAdmin(ExtendedModelAdmin):
    list_display = ['title', 'start_date', 'start_time']
    search_fields = ['production__title']
    fieldsets = [(_("Main Data"), {'fields': ('production', 'start_date', 'start_time', 'end_date', 'end_time', 'duration', 'pauses')}),]
    fieldsets += [(_("Location"), {'fields': ['play_locations', 'play_stages', 'organizers']}),]
    fieldsets += [(_("Free Location"), {'fields': ['location_title', 'street_address', 'street_address2', 'postal_code', 'city', 'latitude', 'longitude']}),]
    fieldsets += get_admin_lang_section(_("Description"), ['description', 'teaser', 'work_info', 'contents', 'press_text', 'credits'])
    fieldsets += get_admin_lang_section(_("Imported"), ['concert_programm', 'supporting_programm', 'remarks', 'duration_text', 'subtitles_text', 'age_text'])
    fieldsets += [(_("Prices"), {'fields': ['price_from', 'price_till', 'free_entrance', 'tickets_website', get_admin_lang_section(_("Price information"), ['price_information'])]}),]
    fieldsets += [(_("Sponsors"), {'fields': ['sponsors',]}),]
    fieldsets += [(_("Additional details"), {'fields': ['event_status', 'ticket_status', 'characteristics', get_admin_lang_section(_("Other characteristics"), ['other_characteristics',])]}),]
    raw_id_fields = ['production']
    filter_horizontal = ['play_locations', 'play_stages', 'characteristics', 'sponsors']
    inlines = [
        EventSocialMediaChannelInline,
        EventVideoInline, EventLiveStreamInline, EventImageInline, EventPDFInline,
        EventLeadershipInline, EventAuthorshipInline, EventInvolvementInline,
    ]

    def title(self, obj):
        return unicode(obj.production)
    title.short_description = _("Title")

admin.site.register(Event, EventAdmin)
# -*- coding: UTF-8 -*-

from django.contrib import admin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _, ugettext
from django.db import models
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.conf.urls import patterns, include, url
from django import forms

from base_libs.admin import ExtendedModelAdmin
from base_libs.admin import ExtendedStackedInline
from base_libs.models.admin import get_admin_lang_section
from base_libs.admin.tree_editor import TreeEditor

from .models import LanguageAndSubtitles
from .models import ProductionCategory
from .models import ProductionCharacteristics
from .models import Production
from .models import ProductionSocialMediaChannel
from .models import ProductionVideo
from .models import ProductionLiveStream
from .models import ProductionImage
from .models import ProductionPDF
from .models import ProductionLeadership
from .models import ProductionAuthorship
from .models import ProductionInvolvement
from .models import ProductionSponsor
from .models import EventCharacteristics
from .models import Event
from .models import EventSocialMediaChannel
from .models import EventVideo
from .models import EventLiveStream
from .models import EventImage
from .models import EventPDF
from .models import EventLeadership
from .models import EventAuthorship
from .models import EventInvolvement
from .models import EventSponsor


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
    fieldsets = [(None, {'fields': ('person', 'sort_order', 'imported_sort_order')}),]
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
    fieldsets = [(None, {'fields': ('person', 'involvement_type', get_admin_lang_section(_("Another type"), ['another_type',]), 'sort_order', 'imported_sort_order')}),]
    fieldsets += get_admin_lang_section(_("Role / Instrument"), ['involvement_role', 'involvement_instrument'])
    raw_id_fields = ['person']
    inline_classes = ('grp-collapse grp-open',)


class ProductionSponsorInline(ExtendedStackedInline):
    model = ProductionSponsor
    extra = 0
    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('website', 'image')}),]
    inline_classes = ('grp-collapse grp-open',)


class OwnersForm(forms.Form):
    users = forms.ModelMultipleChoiceField(
        label=_("Users"),
        queryset=User.objects.filter(is_active=True),
        required=False,
    )


class ProductionAdmin(ExtendedModelAdmin):
    list_display = ('title_de', 'get_locations', 'get_import_source', 'get_external_id', 'get_owners_list', 'get_editors_list', 'creation_date', 'modified_date', 'show_among_others', 'no_overwriting', 'classiccard', 'newsletter', 'status')
    list_editable = ('show_among_others', 'no_overwriting', 'newsletter', 'classiccard', 'status')
    search_fields = ('title_de', 'title_en')
    list_filter = ['show_among_others', 'no_overwriting', 'classiccard', "creation_date", "modified_date", 'import_source', 'newsletter', 'status']
    date_hierarchy = "modified_date"

    fieldsets = get_admin_lang_section(_("Title"), ['title', 'prefix', 'subtitle', 'original', 'website'])
    fieldsets += [(None, {'fields': ('slug', 'classiccard', )}),]
    fieldsets += [(_("Location"), {'fields': ['in_program_of', 'ensembles', 'play_locations', 'play_stages', 'organizers', 'in_cooperation_with']}),]
    fieldsets += [(_("Free Location"), {'fields': ['location_title', 'street_address', 'street_address2', 'postal_code', 'city', 'latitude', 'longitude']}),]
    fieldsets += [(_("Relations"), {'fields': ['categories', 'festivals', 'related_productions']}),]
    fieldsets += get_admin_lang_section(_("Description"), ['description', 'teaser', 'work_info', 'contents', 'press_text', 'credits'])
    fieldsets += get_admin_lang_section(_("Imported"), ['concert_program', 'supporting_program', 'remarks', 'duration_text', 'subtitles_text', 'age_text'])
    fieldsets += [(_("Prices"), {'fields': ['price_from', 'price_till', 'free_entrance', 'tickets_website', get_admin_lang_section(_("Price information"), ['price_information'])]}),]
    fieldsets += [(_("Additional details"), {'fields': ['language_and_subtitles', 'characteristics', get_admin_lang_section(_("Other characteristics"), ['other_characteristics',]), 'age_from', 'age_till', 'edu_offer_website']}),]
    fieldsets += [(_("Status"), {'fields': ['show_among_others', 'no_overwriting', 'newsletter', 'status',]}),]

    filter_horizontal = ['in_program_of', 'play_locations', 'play_stages', 'categories', 'festivals', 'related_productions', 'characteristics']
    inlines = [
        ProductionSocialMediaChannelInline,
        ProductionVideoInline, ProductionLiveStreamInline, ProductionImageInline, ProductionPDFInline,
        ProductionLeadershipInline, ProductionAuthorshipInline, ProductionInvolvementInline,
        ProductionSponsorInline,
    ]

    def get_locations(self, obj):
        html = []
        if obj.in_program_of.count():
            html.append(ugettext('In program of') + ': ' + ', '.join(('<a href="' + loc.get_url_path() + '" tagret="_blank">' + unicode(loc) + '</a>' for loc in obj.in_program_of.all())))
        if obj.play_locations.count():
            html.append(ugettext('Theaters') + ': ' + ', '.join(('<a href="' + loc.get_url_path() + '" tagret="_blank">' + unicode(loc) + '</a>' for loc in obj.play_locations.all())))
        if obj.play_stages.count():
            html.append(ugettext('Stages') + ': ' + ', '.join(('<a href="' + stage.location.get_url_path() + '" tagret="_blank">' + unicode(stage) + '</a>' for stage in obj.play_stages.all())))
        if obj.location_title:
            html.append(ugettext('Free text venue') + ': ' + obj.location_title)
        return '<br />'.join(html)
    get_locations.short_description = _("Locations")
    get_locations.allow_tags = True

    def get_external_id(self, obj):
        ObjectMapper = models.get_model("external_services", "ObjectMapper")
        ContentType = models.get_model("contenttypes", "ContentType")
        mappers = ObjectMapper.objects.filter(
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.pk,
        )
        if mappers:
            return mappers[0].external_id
        return ""
    get_external_id.short_description = _("External ID")

    def get_owners_list(self, obj):
        owners_list = set()
        manage_owners_link = '<a href="%s/owners/"><span>%s</span></a>' % (obj.pk, ugettext('Manage owners'))
        for o in obj.get_owners():
            owners_list.add('<a href="/admin/auth/user/%s/">%s</a>' % (o.pk, o.username))
        if owners_list:
            return '<br />'.join(owners_list) + '<br />' + manage_owners_link
        return manage_owners_link
    get_owners_list.allow_tags = True
    get_owners_list.short_description = _("Owners")

    def get_editors_list(self, obj):
        owners_list = set()
        for o in obj.get_owners():
            owners_list.add('<a href="/admin/auth/user/%s/">%s</a>' % (o.pk, o.username))
        for location in obj.in_program_of.all():
            for o in location.get_owners():
                owners_list.add('<a href="/admin/auth/user/%s/">%s</a>' % (o.pk, o.username))
        for location in obj.play_locations.all():
            for o in location.get_owners():
                owners_list.add('<a href="/admin/auth/user/%s/">%s</a>' % (o.pk, o.username))
        if owners_list:
            return '<br />'.join(owners_list)
        return ''
    get_editors_list.allow_tags = True
    get_editors_list.short_description = _("Editors")

    def owners_view(self, request, production_id):
        from base_libs.views.views import access_denied
        production = get_object_or_404(Production, pk=production_id)

        if not production.is_editable():
            return access_denied(request)

        if request.method == "POST":
            form = OwnersForm(request.POST)
            if form.is_valid():
                existing_owners = set(production.get_owners())
                changed_owners = set(form.cleaned_data['users'])

                removed_owners = existing_owners - changed_owners
                new_owners = changed_owners - existing_owners

                for u in removed_owners:
                    production.remove_owner(u)

                for u in new_owners:
                    production.set_owner(u)
                return redirect('../../?id__exact=%d' % production.pk)
        else:
            form = OwnersForm(initial={
                'users': production.get_owners()
            })

        return render(request, 'admin/owners.html', {
            'production': production,
            'original': production,
            'app_label': Production._meta.app_label,
            'opts': Production._meta,
            'form': form,
            'title': ugettext('The owners of %(production)s') % {'production': production},
        })

    def get_urls(self):
        urls = super(ProductionAdmin, self).get_urls()
        return patterns('', url(r'^(?P<production_id>\d+)/owners/$', self.owners_view)) + urls


admin.site.register(Production, ProductionAdmin)


class EventCharacteristicsAdmin(ExtendedModelAdmin):
    save_on_top = True
    list_display = ['title', 'sort_order', 'show_as_main_category']

    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug', 'sort_order', 'show_as_main_category')}),]

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
    fieldsets = [(None, {'fields': ('person', 'sort_order', 'imported_sort_order')}),]
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
    fieldsets = [(None, {'fields': ('person', 'involvement_type', get_admin_lang_section(_("Another type"), ['another_type',]), 'sort_order', 'imported_sort_order')}),]
    fieldsets += get_admin_lang_section(_("Role / Instrument"), ['involvement_role', 'involvement_instrument'])
    raw_id_fields = ['person']
    inline_classes = ('grp-collapse grp-open',)


class EventSponsorInline(ExtendedStackedInline):
    model = EventSponsor
    extra = 0
    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('website', 'image')}),]
    inline_classes = ('grp-collapse grp-open',)


class EventAdmin(ExtendedModelAdmin):
    list_display = ['title', 'start_date', 'start_time', 'creation_date', 'modified_date', 'classiccard']
    list_filter = ['classiccard', 'creation_date', 'modified_date']
    list_editable = ['classiccard']
    search_fields = ['production__title']
    date_hierarchy = 'start_date'
    ordering = ('-creation_date', )

    fieldsets = [(_("Main Data"), {'fields': ('production', 'start_date', 'start_time', 'end_date', 'end_time', 'duration', 'pauses', 'classiccard')}),]
    fieldsets += [(_("Location"), {'fields': ['play_locations', 'play_stages', 'organizers']}),]
    fieldsets += [(_("Free Location"), {'fields': ['location_title', 'street_address', 'street_address2', 'postal_code', 'city', 'latitude', 'longitude']}),]
    fieldsets += get_admin_lang_section(_("Description"), ['description', 'teaser', 'work_info', 'contents', 'press_text', 'credits'])
    fieldsets += get_admin_lang_section(_("Imported"), ['concert_program', 'supporting_program', 'remarks', 'duration_text', 'subtitles_text', 'age_text'])
    fieldsets += [(_("Prices"), {'fields': ['price_from', 'price_till', 'free_entrance', 'tickets_website', get_admin_lang_section(_("Price information"), ['price_information'])]}),]
    fieldsets += [(_("Additional details"), {'fields': ['event_status', 'ticket_status', 'language_and_subtitles', 'characteristics', get_admin_lang_section(_("Other characteristics"), ['other_characteristics',])]}),]
    raw_id_fields = ['production']
    filter_horizontal = ['play_locations', 'play_stages', 'characteristics']
    inlines = [
        EventSocialMediaChannelInline,
        EventVideoInline, EventLiveStreamInline, EventImageInline, EventPDFInline,
        EventLeadershipInline, EventAuthorshipInline, EventInvolvementInline,
        EventSponsorInline,
    ]

    def title(self, obj):
        return unicode(obj.production)
    title.short_description = _("Title")

admin.site.register(Event, EventAdmin)
# -*- coding: UTF-8 -*-

from django.contrib import admin
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _, ugettext
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.conf.urls import patterns, include, url
from django import forms

from base_libs.admin import ExtendedModelAdmin
from base_libs.admin import ExtendedStackedInline
from base_libs.models.admin import get_admin_lang_section
from base_libs.admin.tree_editor import TreeEditor

MuseumCategory = models.get_model("museums", "MuseumCategory")
AccessibilityOption = models.get_model("museums", "AccessibilityOption")
Museum = models.get_model("museums", "Museum")
Season = models.get_model("museums", "Season")
SpecialOpeningTime = models.get_model("museums", "SpecialOpeningTime")
MediaFile = models.get_model("museums", "MediaFile")
SocialMediaChannel = models.get_model("museums", "SocialMediaChannel")


class MuseumCategoryAdmin(TreeEditor, ExtendedModelAdmin):

    save_on_top = True
    list_display = ['actions_column', 'indented_short_title', ]

    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug', 'parent')}),]

    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}


admin.site.register(MuseumCategory, MuseumCategoryAdmin)


class AccessibilityOptionAdmin(ExtendedModelAdmin):

    save_on_top = True
    list_display = ['title', 'icon']

    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug', 'image', 'sort_order', )}),]

    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}

    def icon(self, obj):
        return """<img alt="" src="%s%s" />""" % (settings.MEDIA_URL, obj.image.path)
    icon.allow_tags = True

admin.site.register(AccessibilityOption, AccessibilityOptionAdmin)


class SeasonInline(ExtendedStackedInline):
    model = Season
    extra = 0
    allow_add = True
    template = "admin/museums/museum/season_inline.html"


class SpecialOpeningTimeInline(ExtendedStackedInline):
    model = SpecialOpeningTime
    allow_add = True
    extra = 0
    fieldsets = get_admin_lang_section(_("Title"), ['day_label'])
    fieldsets += [(_("Date"), {'fields': ('yyyy', 'mm', 'dd'), })]
    fieldsets += [(_("Opening hours"), {'fields': ('is_closed', 'is_regular', 'opening', 'break_close', 'break_open', 'closing', get_admin_lang_section(_("Exceptions"), ['exceptions']))})]


class SocialMediaChannelInline(admin.TabularInline):
    model = SocialMediaChannel
    allow_add = True
    extra = 0


class MediaFileInline(ExtendedStackedInline):
    model = MediaFile
    allow_add = True
    extra = 0
    sortable = True
    sortable_field_name = "sort_order"


class OwnersForm(forms.Form):
    users = forms.ModelMultipleChoiceField(
        label=_("Users"),
        queryset=User.objects.filter(is_active=True),
        required=False,
    )


class MuseumAdmin(ExtendedModelAdmin):
    save_on_top = True
    list_display = ('id', 'title', 'subtitle', 'get_owners_list', 'creation_date', 'status', 'participates_in_langenacht', 'participates_in_berlinartweek', 'participates_in_emop', 'is_geoposition_set', 'favorites_count')
    list_editable = ('status', 'participates_in_langenacht', 'participates_in_berlinartweek', 'participates_in_emop')
    list_display_links = ('title', )
    list_filter = ('creation_date', 'status', 'categories', 'open_on_mondays', 'free_entrance', 'linkgroup')
    search_fields = ('title', 'subtitle', 'slug')

    fieldsets = get_admin_lang_section(_("Title"), ['title', 'subtitle', 'description',])
    fieldsets += [(None, {'fields': ('slug', )}),]
    fieldsets += [(_("Categories"), {'fields': ('categories', 'tags', 'open_on_mondays', 'is_for_children')}),]
    fieldsets += [(_("Prices"), {'fields': ('free_entrance', 'member_of_museumspass',
        'admission_price', get_admin_lang_section(_("Price info"), ['admission_price_info']),
        'reduced_price', get_admin_lang_section(_("Price info"), ['reduced_price_info']),
        'show_group_ticket', get_admin_lang_section(_("Price info"), ['group_ticket']),
        'show_family_ticket',
        'show_yearly_ticket',
        )}),]
    fieldsets += [(_("Location"), {'fields': ('parent', 'street_address','street_address2','postal_code','city', 'country','latitude','longitude')}),]
    fieldsets += [(_("Contacts"), {'fields': ((_("Phone"), {'fields': ('phone_country', 'phone_area', 'phone_number')}), (_("Fax"), {'fields': ('fax_country', 'fax_area', 'fax_number')}),'email','website', (_("Group bookings phone"), {'fields': ('group_bookings_phone_country', 'group_bookings_phone_area', 'group_bookings_phone_number')}), (_("Service phone"), {'fields': ('service_phone_country', 'service_phone_area', 'service_phone_number')}),)}),]
    fieldsets += [(_("Mediation offer"), {'fields': ('has_audioguide', (_("Audioguide languages"), {'fields': ('has_audioguide_de', 'has_audioguide_en', 'has_audioguide_fr', 'has_audioguide_it', 'has_audioguide_sp', 'has_audioguide_pl', 'has_audioguide_tr', 'audioguide_other_languages')}), 'has_audioguide_for_children', 'has_audioguide_for_learning_difficulties')}),]
    fieldsets += [(_("Accessibility"), {'fields': ['accessibility_options', get_admin_lang_section(_("Explanation"), ['accessibility', 'mobidat'])]})]
    fieldsets += [(_("Services"), {'fields': [
        'service_shop',
        'service_restaurant',
        'service_cafe',
        'service_library',
        'service_archive',
        'service_diaper_changing_table',
    ]})]
    fieldsets += get_admin_lang_section(_("Search"), ['search_keywords',])
    fieldsets += [(_("Status"), {'fields': ('participates_in_langenacht', 'participates_in_berlinartweek', 'participates_in_emop', 'status',)}),]

    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}
    filter_horizontal = ("categories", "accessibility_options")

    inlines = [SeasonInline, SpecialOpeningTimeInline, SocialMediaChannelInline, MediaFileInline]

    def is_geoposition_set(self, obj):
        return bool(obj.latitude)
    is_geoposition_set.boolean = True
    is_geoposition_set.short_description = _("Geoposition?")


    def get_owners_list(self, obj):
        owners_list = []
        manage_owners_link = '<br /><a href="%s/owners/"><span>%s</span></a>' % (obj.pk, ugettext('Manage owners'))
        for o in obj.get_owners():
            owners_list.append('<a href="/admin/auth/user/%s/">%s</a>' % (o.pk, o.username))
        if owners_list:
            return '<br />'.join(owners_list) + manage_owners_link
        return '<a href="/claiming-invitation/?museum_id=%s">%s</a>%s' % (obj.pk, ugettext("Invite owners"), manage_owners_link)
    get_owners_list.allow_tags = True
    get_owners_list.short_description = _("Owners")

    def owners_view(self, request, museum_id):
        from base_libs.views.views import access_denied
        museum = get_object_or_404(Museum, pk=museum_id)

        if not request.user.has_perm('museums.change_museum', museum):
            return access_denied(request)

        if request.method == "POST":
            form = OwnersForm(request.POST)
            if form.is_valid():
                existing_owners = set(museum.get_owners())
                changed_owners = set(form.cleaned_data['users'])

                removed_owners = existing_owners - changed_owners
                new_owners = changed_owners - existing_owners

                for u in removed_owners:
                    museum.remove_owner(u)
                    for e in museum.event_set.all():
                        e.remove_owner(u)
                    for e in museum.exhibition_set.all():
                        e.remove_owner(u)

                for u in new_owners:
                    museum.set_owner(u)
                    for e in museum.event_set.all():
                        e.set_owner(u)
                    for e in museum.exhibition_set.all():
                        e.set_owner(u)
                return redirect('../../?id__exact=%d' % museum.pk)
        else:
            form = OwnersForm(initial={
                'users': museum.get_owners()
            })

        return render(request, 'admin/owners.html', {
            'museum': museum,
            'original': museum,
            'app_label': Museum._meta.app_label,
            'opts': Museum._meta,
            'form': form,
            'title': ugettext('The owners of %(museum)s') % {'museum': museum},
        })

    def get_urls(self):
        urls = super(MuseumAdmin, self).get_urls()
        return patterns('', url(r'^(?P<museum_id>\d+)/owners/$', self.owners_view)) + urls

admin.site.register(Museum, MuseumAdmin)

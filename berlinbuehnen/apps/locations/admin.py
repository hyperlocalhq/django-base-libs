# -*- coding: UTF-8 -*-

from django.contrib import admin
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

from filebrowser.settings import URL_FILEBROWSER_MEDIA

from .models import District
from .models import Service
from .models import AccessibilityOption
from .models import Location
from .models import Stage
from .models import Image
from .models import SocialMediaChannel
from .models import LocationCategory


class LocationCategoryAdmin(TreeEditor, ExtendedModelAdmin):
    save_on_top = True
    list_display = ['actions_column', 'indented_short_title', ]

    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug', 'parent')}),]

    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}

admin.site.register(LocationCategory, LocationCategoryAdmin)

class DistrictAdmin(ExtendedModelAdmin):

    save_on_top = True
    list_display = ['title',]

    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug', 'sort_order', )}),]

    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}

admin.site.register(District, DistrictAdmin)

class ServiceAdmin(ExtendedModelAdmin):

    save_on_top = True
    list_display = ['title', 'icon']

    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug', 'image', 'sort_order', )}),]

    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}

    def icon(self, obj):
        if not obj.image:
            return u""
        return u"""<img alt="" src="%s%s" />""" % (settings.MEDIA_URL, obj.image.path)
    icon.allow_tags = True

admin.site.register(Service, ServiceAdmin)


class AccessibilityOptionAdmin(ExtendedModelAdmin):

    save_on_top = True
    list_display = ['title', 'icon']

    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug', 'image', 'sort_order', )}),]

    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}

    def icon(self, obj):
        if not obj.image:
            return u""
        return u"""<img alt="" src="%s%s" />""" % (settings.MEDIA_URL, obj.image.path)
    icon.allow_tags = True

admin.site.register(AccessibilityOption, AccessibilityOptionAdmin)


class StageInline(ExtendedStackedInline):
    model = Stage
    extra = 0
    fieldsets = get_admin_lang_section(_("Title"), ['title', 'description',])
    fieldsets += [(None, {'fields': ('slug', 'sort_order', )}),]
    fieldsets += [(_("Address"), {'fields': ('street_address', 'street_address2', 'postal_code', 'city', 'district', 'latitude', 'longitude')}),]
    # classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)


class ImageInline(ExtendedStackedInline):
    model = Image
    extra = 0
    # classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)


class SocialMediaChannelInline(ExtendedStackedInline):
    model = SocialMediaChannel
    extra = 0
    # classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)


class OwnersForm(forms.Form):
    users = forms.ModelMultipleChoiceField(
        label=_("Users"),
        queryset=User.objects.filter(is_active=True),
        required=False,
    )


class LocationAdmin(ExtendedModelAdmin):
    class Media:
        js = (
            "%sjs/AddFileBrowser.js" % URL_FILEBROWSER_MEDIA,
        )

    list_display = ('title', 'creation_date', 'modified_date', 'get_owners_list', 'newsletter', 'status')
    list_editable = ('newsletter', 'status', )
    list_filter = ('newsletter', 'status', )

    fieldsets = get_admin_lang_section(_("Title"), ['title', 'subtitle', 'description', 'teaser',])
    fieldsets += [(None, {'fields': ('slug', 'logo')}),]
    fieldsets += [(_("Address"), {'fields': ('street_address', 'street_address2', 'postal_code', 'city', 'latitude', 'longitude')}),]
    fieldsets += [(_("District"), {'fields': ('districts',)}),]
    fieldsets += [(_("Contacts"), {'fields': ((_("Phone"), {'fields': ('phone_country', 'phone_area', 'phone_number')}), (_("Fax"), {'fields': ('fax_country', 'fax_area', 'fax_number')}),'email','website', )}),]
    fieldsets += [(_("Tickets"), {'fields': ('tickets_street_address', 'tickets_street_address2', 'tickets_postal_code', 'tickets_city', 'tickets_email', 'tickets_website', (_("Phone"), {'fields': ('tickets_phone_country', 'tickets_phone_area', 'tickets_phone_number')}), (_("Fax"), {'fields': ('tickets_fax_country', 'tickets_fax_area', 'tickets_fax_number')}), get_admin_lang_section(_("Additional information"), ['tickets_calling_prices', 'tickets_additional_info',]))}),]
    fieldsets += [(_("Tickets Opening Hours"), {'fields': ('is_appointment_based',
       ('mon_open', 'mon_break_close', 'mon_break_open', 'mon_close'),
       ('tue_open', 'tue_break_close', 'tue_break_open', 'tue_close'),
       ('wed_open', 'wed_break_close', 'wed_break_open', 'wed_close'),
       ('thu_open', 'thu_break_close', 'thu_break_open', 'thu_close'),
       ('fri_open', 'fri_break_close', 'fri_break_open', 'fri_close'),
       ('sat_open', 'sat_break_close', 'sat_break_open', 'sat_close'),
       ('sun_open', 'sun_break_close', 'sun_break_open', 'sun_close'),
       get_admin_lang_section(_("Exceptions"), ['exceptions',]),
    )}),]
    fieldsets += [(_("Press Contact"), {'fields': ('press_contact_name', 'press_email', 'press_website', (_("Phone"), {'fields': ('press_phone_country', 'press_phone_area', 'press_phone_number')}), (_("Fax"), {'fields': ('press_fax_country', 'press_fax_area', 'press_fax_number')}))}),]
    fieldsets += [(_("Categories"), {'fields': ('categories',)}),]
    fieldsets += [(_("Service"), {'fields': ('services',)}),]
    fieldsets += [(_("Accessibility"), {'fields': ('accessibility_options',)}),]
    fieldsets += [(_("Status"), {'fields': ('newsletter', 'status',)}),]

    inlines = [StageInline, ImageInline, SocialMediaChannelInline]

    filter_horizontal = ['services', 'accessibility_options', 'categories', 'districts']

    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}

    def get_owners_list(self, obj):
        owners_list = []
        manage_owners_link = '<br /><a href="%s/owners/"><span>%s</span></a>' % (obj.pk, ugettext('Manage owners'))
        for o in obj.get_owners():
            owners_list.append('<a href="/admin/auth/user/%s/">%s</a>' % (o.pk, o.username))
        if owners_list:
            return '<br />'.join(owners_list) + manage_owners_link
        return '<a href="/claiming-invitation/?location_id=%s">%s</a>%s' % (obj.pk, ugettext("Invite owners"), manage_owners_link)
    get_owners_list.allow_tags = True
    get_owners_list.short_description = _("Owners")

    def owners_view(self, request, location_id):
        from base_libs.views.views import access_denied
        location = get_object_or_404(Location, pk=location_id)

        if not location.is_editable():
            return access_denied(request)

        if request.method == "POST":
            form = OwnersForm(request.POST)
            if form.is_valid():
                existing_owners = set(location.get_owners())
                changed_owners = set(form.cleaned_data['users'])

                removed_owners = existing_owners - changed_owners
                new_owners = changed_owners - existing_owners

                for u in removed_owners:
                    location.remove_owner(u)
                    for p in location.program_productions.all():
                        p.remove_owner(u)
                    for p in location.located_productions.all():
                        p.remove_owner(u)

                for u in new_owners:
                    location.set_owner(u)
                    for p in location.program_productions.all():
                        p.set_owner(u)
                    for p in location.located_productions.all():
                        p.set_owner(u)
                return redirect('../../?id__exact=%d' % location.pk)
        else:
            form = OwnersForm(initial={
                'users': location.get_owners()
            })

        return render(request, 'admin/owners.html', {
            'location': location,
            'original': location,
            'app_label': Location._meta.app_label,
            'opts': Location._meta,
            'form': form,
            'title': ugettext('The owners of %(location)s') % {'location': location},
        })

    def get_urls(self):
        urls = super(LocationAdmin, self).get_urls()
        return patterns('', url(r'^(?P<location_id>\d+)/owners/$', self.owners_view)) + urls

admin.site.register(Location, LocationAdmin)
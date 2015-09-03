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

from filebrowser.settings import URL_FILEBROWSER_MEDIA

from berlinbuehnen.apps.locations.models import Location
from berlinbuehnen.apps.locations.models import Stage
from berlinbuehnen.apps.locations.models import Image
from berlinbuehnen.apps.locations.models import SocialMediaChannel
from .models import Department
from .models import DepartmentMember
from .models import Project
from .models import ProjectTime
from .models import ProjectMember
from .models import ProjectImage
from .models import ProjectSocialMediaChannel
from .models import ProjectTargetGroup
from .models import ProjectFormat


class OwnersForm(forms.Form):
    users = forms.ModelMultipleChoiceField(
        label=_("Users"),
        queryset=User.objects.filter(is_active=True),
        required=False,
    )


class ProjectTargetGroupAdmin(ExtendedModelAdmin):
    save_on_top = True
    list_display = ['title',]

    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug', 'sort_order', )}),]

    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}

admin.site.register(ProjectTargetGroup, ProjectTargetGroupAdmin)


class ProjectFormatAdmin(ExtendedModelAdmin):
    save_on_top = True
    list_display = ['title',]

    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug', 'sort_order', )}),]

    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}

admin.site.register(ProjectFormat, ProjectFormatAdmin)


class StageInline(ExtendedStackedInline):
    model = Stage
    extra = 0
    fieldsets = get_admin_lang_section(_("Title"), ['title', 'description',])
    fieldsets += [(None, {'fields': ('slug', 'sort_order', )}),]
    fieldsets += [(_("Address"), {'fields': ('street_address', 'street_address2', 'postal_code', 'city', 'district', 'latitude', 'longitude')}),]
    # classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)


class LocationImageInline(ExtendedStackedInline):
    model = Image
    extra = 0
    # classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)


class LocationSocialMediaChannelInline(ExtendedStackedInline):
    model = SocialMediaChannel
    extra = 0
    # classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)


class DepartmentMemberInline(ExtendedStackedInline):
    model = DepartmentMember
    extra = 0
    fieldsets = [(None, {'fields': ('person', 'sort_order')}),]
    fieldsets += get_admin_lang_section(_("Function"), ['function',])
    fieldsets += [(_("Contacts"), {'fields': ((_("Phone"), {'fields': ('phone_country', 'phone_area', 'phone_number')}), 'email', )}),]
    raw_id_fields = ['person']
    inline_classes = ('grp-collapse grp-open',)


class DepartmentAdmin(ExtendedModelAdmin):
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

    inlines = [StageInline, DepartmentMemberInline, LocationImageInline, LocationSocialMediaChannelInline]

    filter_horizontal = ['services', 'accessibility_options', 'categories', 'districts']

    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}

    def get_owners_list(self, obj):
        owners_list = []
        manage_owners_link = '<a href="%s/owners/"><span>%s</span></a>' % (obj.pk, ugettext('Manage owners'))
        for o in obj.get_owners():
            owners_list.append('<a href="/admin/auth/user/%s/">%s</a>' % (o.pk, o.username))
        if owners_list:
            return '<br />'.join(owners_list) + '<br />' +  manage_owners_link
        return manage_owners_link
    get_owners_list.allow_tags = True
    get_owners_list.short_description = _("Owners")

    def owners_view(self, request, department_id):
        from base_libs.views.views import access_denied
        location = get_object_or_404(Location, department__pk=department_id)

        if not request.user.has_perm('locations.change_location', location):
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

        return render(request, 'admin/locations/location/owners.html', {
            'location': location,
            'original': location,
            'app_label': Department._meta.app_label,
            'opts': Department._meta,
            'form': form,
            'title': ugettext('The owners of %(location)s') % {'location': location},
        })

    def get_urls(self):
        urls = super(DepartmentAdmin, self).get_urls()
        return patterns('', url(r'^(?P<department_id>\d+)/owners/$', self.owners_view)) + urls

admin.site.register(Department, DepartmentAdmin)


class ProjectTimeInline(ExtendedStackedInline):
    model = ProjectTime
    extra = 0
    # classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)


class ProjectMemberInline(ExtendedStackedInline):
    model = ProjectMember
    extra = 0
    fieldsets = [(None, {'fields': ('person', 'sort_order')}),]
    fieldsets += get_admin_lang_section(_("Function"), ['function',])
    fieldsets += [(_("Contacts"), {'fields': ((_("Phone"), {'fields': ('phone_country', 'phone_area', 'phone_number')}), 'email', )}),]
    raw_id_fields = ['person']
    inline_classes = ('grp-collapse grp-open',)


class ProjectImageInline(ExtendedStackedInline):
    model = ProjectImage
    extra = 0
    # classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)


class ProjectSocialMediaChannelInline(ExtendedStackedInline):
    model = ProjectSocialMediaChannel
    extra = 0
    # classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)


class ProjectAdmin(ExtendedModelAdmin):
    list_display = ('title_de', 'get_locations', 'get_owners_list', 'creation_date', 'modified_date', 'status')
    list_editable = ('status',)
    search_fields = ('title_de', 'title_en')
    list_filter = ["creation_date", "modified_date", 'status']
    date_hierarchy = "modified_date"

    fieldsets = get_admin_lang_section(_("Title"), ['title', 'subtitle',])
    fieldsets += [(None, {'fields': ('slug', 'logo')}),]
    fieldsets += [(_("Location"), {'fields': ['departments',]}),]
    fieldsets += [(_("Free Location"), {'fields': ['location_title', 'street_address', 'street_address2', 'postal_code', 'city', 'latitude', 'longitude']}),]
    fieldsets += [(_("Contacts"), {'fields': ((_("Phone"), {'fields': ('phone_country', 'phone_area', 'phone_number')}), (_("Fax"), {'fields': ('fax_country', 'fax_area', 'fax_number')}),'email','website', )}),]
    fieldsets += get_admin_lang_section(_("Description"), ['description', 'special_conditions', 'remarks', 'cooperation', 'supporters', 'participant_count'])
    fieldsets += [(_("Prices"), {'fields': ['free_entrance', get_admin_lang_section(_("Price information"), ['prices'])]}),]
    fieldsets += [(_("Additional details"), {'fields': ['age_from', 'age_till', 'needs_teachers', 'target_group', 'format']})]
    fieldsets += [(_("Sponsors"), {'fields': ['sponsors',]}),]
    fieldsets += [(_("Status"), {'fields': ['status',]}),]

    filter_horizontal = ['departments', 'sponsors']
    inlines = [
        ProjectTimeInline,
        ProjectMemberInline,
        ProjectSocialMediaChannelInline,
        ProjectImageInline,
    ]

    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}

    def get_locations(self, obj):
        html = []
        if obj.departments.count():
            html.append(ugettext('Departments') + ': ' + ', '.join(('<a href="' + loc.get_url_path() + '" tagret="_blank">' + unicode(loc) + '</a>' for loc in obj.departments.all())))
        return '<br />'.join(html)
    get_locations.short_description = _("Locations")
    get_locations.allow_tags = True

    def get_owners_list(self, obj):
        owners_list = []
        manage_owners_link = '<a href="%s/owners/"><span>%s</span></a>' % (obj.pk, ugettext('Manage owners'))
        for o in obj.get_owners():
            owners_list.append('<a href="/admin/auth/user/%s/">%s</a>' % (o.pk, o.username))
        if owners_list:
            return '<br />'.join(owners_list) + '<br />' + manage_owners_link
        return manage_owners_link
    get_owners_list.allow_tags = True
    get_owners_list.short_description = _("Owners")

    def owners_view(self, request, project_id):
        from base_libs.views.views import access_denied
        production = get_object_or_404(Project, pk=project_id)

        if not request.user.has_perm('productions.change_production', production):
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

        return render(request, 'admin/productions/production/owners.html', {
            'production': production,
            'original': production,
            'app_label': Project._meta.app_label,
            'opts': Project._meta,
            'form': form,
            'title': ugettext('The owners of %(production)s') % {'production': production},
        })

    def get_urls(self):
        urls = super(ProjectAdmin, self).get_urls()
        return patterns('', url(r'^(?P<project_id>\d+)/owners/$', self.owners_view)) + urls


admin.site.register(Project, ProjectAdmin)

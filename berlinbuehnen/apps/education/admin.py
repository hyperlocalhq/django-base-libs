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
from .models import Image
from .models import SocialMediaChannel
from .models import PDF
from .models import Department
from .models import DepartmentMember
from .models import Project
from .models import ProjectTime
from .models import ProjectMember
from .models import ProjectImage
from .models import ProjectSocialMediaChannel
from .models import ProjectPDF
from .models import ProjectVideo
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



class DepartmentImageInline(ExtendedStackedInline):
    model = Image
    extra = 0
    # classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)


class DepartmentSocialMediaChannelInline(ExtendedStackedInline):
    model = SocialMediaChannel
    extra = 0
    # classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)


class DepartmentPDFInline(ExtendedStackedInline):
    model = PDF
    extra = 0
    inline_classes = ('grp-collapse grp-open',)


class DepartmentMemberInline(ExtendedStackedInline):
    model = DepartmentMember
    extra = 0
    fieldsets = [(None, {'fields': ('person', 'sort_order')}),]
    fieldsets += get_admin_lang_section(_("Function"), ['function',])
    fieldsets += [(None, {'fields': ((_("Phone"), {'fields': ('phone_country', 'phone_area', 'phone_number')}), 'email', )}),]
    raw_id_fields = ['person']
    inline_classes = ('grp-collapse grp-open',)


class DepartmentAdmin(ExtendedModelAdmin):
    class Media:
        js = (
            "%sjs/AddFileBrowser.js" % URL_FILEBROWSER_MEDIA,
        )

    list_display = ('title', 'creation_date', 'modified_date', 'status')
    list_editable = ('status', )
    list_filter = ('status', )

    fieldsets = get_admin_lang_section(_("Title"), ['title', 'description', 'teaser',])
    fieldsets += [(None, {'fields': ('slug',)}),]
    fieldsets += [(_("Location"), {'fields': ('location',)})]
    fieldsets += [(_("Address"), {'fields': ('street_address', 'street_address2', 'postal_code', 'city', 'latitude', 'longitude')}),]
    fieldsets += [(_("District"), {'fields': ('districts',)}),]
    fieldsets += [(_("Contacts"), {'fields': ('contact_name',(_("Phone"), {'fields': ('phone_country', 'phone_area', 'phone_number')}), (_("Fax"), {'fields': ('fax_country', 'fax_area', 'fax_number')}),'email','website', )}),]
    fieldsets += [(_("Status"), {'fields': ('status',)}),]

    inlines = [DepartmentMemberInline, DepartmentSocialMediaChannelInline, DepartmentImageInline, DepartmentPDFInline,]

    filter_horizontal = ['districts']

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
        department = get_object_or_404(Department, pk=department_id)

        if not department.is_editable():
            return access_denied(request)

        if request.method == "POST":
            form = OwnersForm(request.POST)
            if form.is_valid():
                existing_owners = set(department.get_owners())
                changed_owners = set(form.cleaned_data['users'])

                removed_owners = existing_owners - changed_owners
                new_owners = changed_owners - existing_owners

                for u in removed_owners:
                    department.remove_owner(u)

                for u in new_owners:
                    department.set_owner(u)
                    
                return redirect('../../?id__exact=%d' % department.pk)
        else:
            form = OwnersForm(initial={
                'users': department.get_owners()
            })

        return render(request, 'admin/owners.html', {
            'department': department,
            'original': department,
            'app_label': Department._meta.app_label,
            'opts': Department._meta,
            'form': form,
            'title': ugettext('The owners of %(department)s') % {'department': department},
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


class ProjectPDFInline(ExtendedStackedInline):
    model = ProjectPDF
    extra = 0
    inline_classes = ('grp-collapse grp-open',)


class ProjectVideoInline(ExtendedStackedInline):
    model = ProjectVideo
    extra = 0
    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('link_or_embed', 'sort_order')}),]
    inline_classes = ('grp-collapse grp-open',)


class ProjectAdmin(ExtendedModelAdmin):
    list_display = ('title_de', 'get_locations', 'creation_date', 'modified_date', 'status')
    list_editable = ('status',)
    search_fields = ('title_de', 'title_en')
    list_filter = ["creation_date", "modified_date", 'status']
    date_hierarchy = "modified_date"

    fieldsets = get_admin_lang_section(_("Title"), ['title', 'subtitle',])
    fieldsets += [(None, {'fields': ('slug',)}),]
    fieldsets += [(_("Location"), {'fields': ['departments',]}),]
    fieldsets += [(_("Free Location"), {'fields': ['location_title', 'street_address', 'street_address2', 'postal_code', 'city', 'latitude', 'longitude']}),]
    fieldsets += [(_("Contact"), {'fields': ('contact_department', 'contact_name', (_("Phone"), {'fields': ('phone_country', 'phone_area', 'phone_number')}), (_("Fax"), {'fields': ('fax_country', 'fax_area', 'fax_number')}),'email','website', )}),]
    fieldsets += get_admin_lang_section(_("Description"), ['description', 'special_conditions', 'remarks', 'cooperation', 'supporters', 'participant_count'])
    fieldsets += [(_("Prices"), {'fields': ['free_entrance', 'tickets_website', get_admin_lang_section(_("Price information"), ['prices'])]}),]
    fieldsets += [(_("Additional details"), {'fields': ['age_from', 'age_till', 'needs_teachers', 'target_groups', 'formats']})]
    fieldsets += [(_("Sponsors"), {'fields': ['sponsors',]}),]
    fieldsets += [(_("Status"), {'fields': ['status',]}),]

    filter_horizontal = ['departments', 'sponsors', 'target_groups', 'formats']
    inlines = [
        ProjectTimeInline,
        ProjectMemberInline,
        ProjectSocialMediaChannelInline,
        ProjectImageInline,
        ProjectPDFInline,
        ProjectVideoInline,
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
        project = get_object_or_404(Project, pk=project_id)

        if not project.is_editable():
            return access_denied(request)

        if request.method == "POST":
            form = OwnersForm(request.POST)
            if form.is_valid():
                existing_owners = set(project.get_owners())
                changed_owners = set(form.cleaned_data['users'])

                removed_owners = existing_owners - changed_owners
                new_owners = changed_owners - existing_owners

                for u in removed_owners:
                    project.remove_owner(u)

                for u in new_owners:
                    project.set_owner(u)
                return redirect('../../?id__exact=%d' % project.pk)
        else:
            form = OwnersForm(initial={
                'users': project.get_owners()
            })

        return render(request, 'admin/owners.html', {
            'project': project,
            'original': project,
            'app_label': Project._meta.app_label,
            'opts': Project._meta,
            'form': form,
            'title': ugettext('The owners of %(project)s') % {'project': project},
        })

    def get_urls(self):
        urls = super(ProjectAdmin, self).get_urls()
        return patterns('', url(r'^(?P<project_id>\d+)/owners/$', self.owners_view)) + urls


admin.site.register(Project, ProjectAdmin)

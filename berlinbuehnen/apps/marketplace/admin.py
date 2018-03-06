# -*- coding: UTF-8 -*-

from django.contrib import admin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _, ugettext
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.conf.urls import patterns, include, url
from django import forms
from django.utils.html import mark_safe
from django.template.loader import render_to_string

from base_libs.admin import ExtendedModelAdmin
from base_libs.admin import ExtendedStackedInline
from base_libs.models.admin import get_admin_lang_section
from base_libs.admin.tree_editor import TreeEditor

from .models import JobCategory
from .models import JobType
from .models import JobOffer


class JobCategoryAdmin(TreeEditor, ExtendedModelAdmin):
    save_on_top = True
    list_display = ['actions_column', 'indented_short_title', ]

    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug', 'parent')}), ]

    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,), }


admin.site.register(JobCategory, JobCategoryAdmin)


class JobTypeAdmin(ExtendedModelAdmin):
    save_on_top = True
    list_display = ['title', ]

    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug', 'sort_order',)}), ]

    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,), }


admin.site.register(JobType, JobTypeAdmin)


class OwnersForm(forms.Form):
    users = forms.ModelMultipleChoiceField(
        label=_("Users"),
        queryset=User.objects.filter(is_active=True),
        required=False,
    )


class JobOfferAdmin(ExtendedModelAdmin):
    list_display = ('position', 'creation_date', 'modified_date', 'deadline', 'start_contract_on', 'get_owners_list', 'status')
    list_editable = ('status',)
    list_filter = ('status',)

    fieldsets = get_admin_lang_section(
        _("Position"),
        [
            #'title',
            #'subtitle',
            'position',
            'description',
            'remarks',
        ]
    )
    fieldsets += [
        (
            _("Dates"),
            {
                'fields': (
                    'deadline',
                    'start_contract_on'
                )
            }
        ),
    ]
    fieldsets += [
        (
            _("Address"),
            {
                'fields': (
                    'company',
                    'street_address',
                    'street_address2',
                    'postal_code',
                    'city',
                    'latitude',
                    'longitude',
                    'get_map'
                ),
            }
        ),
    ]
    fieldsets += [
        (
            _("Contacts"),
            {
                'fields': (
                    'name',
                    (
                        _("Phone"), {
                            'fields': (
                                'phone_country',
                                'phone_area',
                                'phone_number'
                            )
                        }
                    ),
                    (_("Fax"), {'fields': ('fax_country', 'fax_area', 'fax_number')}),
                    'email',
                    'website',
                )
            }
        ),
    ]
    fieldsets += [
        (
            _("Categories"),
            {
                'fields': (
                    'job_type',
                    'categories',
                )
            }
        ),
    ]
    fieldsets += [
        (
            _("Status"),
            {
                'fields': (
                    'status',
                )
            }
        ),
    ]

    filter_horizontal = ['categories']
    readonly_fields = ["get_map"]

    def get_map(self, instance):
        return mark_safe(render_to_string("admin/map.html", {'STATIC_URL': settings.STATIC_URL}))

    get_map.short_description = _("Map")
    get_map.allow_tags = True

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

    def owners_view(self, request, job_offer_id):
        from base_libs.views.views import access_denied
        job_offer = get_object_or_404(JobOffer, pk=job_offer_id)

        if not job_offer.is_editable():
            return access_denied(request)

        if request.method == "POST":
            form = OwnersForm(request.POST)
            if form.is_valid():
                existing_owners = set(job_offer.get_owners())
                changed_owners = set(form.cleaned_data['users'])

                removed_owners = existing_owners - changed_owners
                new_owners = changed_owners - existing_owners

                for u in removed_owners:
                    job_offer.remove_owner(u)
                    for p in job_offer.program_productions.all():
                        p.remove_owner(u)
                    for p in job_offer.located_productions.all():
                        p.remove_owner(u)

                for u in new_owners:
                    job_offer.set_owner(u)
                    for p in job_offer.program_productions.all():
                        p.set_owner(u)
                    for p in job_offer.located_productions.all():
                        p.set_owner(u)
                return redirect('../../?id__exact=%d' % job_offer.pk)
        else:
            form = OwnersForm(initial={
                'users': job_offer.get_owners()
            })

        return render(request, 'admin/owners.html', {
            'job_offer': job_offer,
            'original': job_offer,
            'app_label': JobOffer._meta.app_label,
            'opts': JobOffer._meta,
            'form': form,
            'title': ugettext('The owners of %(job_offer)s') % {'job_offer': job_offer},
        })

    def get_urls(self):
        urls = super(JobOfferAdmin, self).get_urls()
        return patterns('', url(r'^(?P<job_offer_id>\d+)/owners/$', self.owners_view)) + urls


admin.site.register(JobOffer, JobOfferAdmin)

# -*- coding: UTF-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _, ugettext
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.conf.urls import patterns, include, url
from django import forms

from base_libs.admin import ExtendedModelAdmin
from base_libs.admin import ExtendedStackedInline

from .models import Parent, Part


class PartInline(ExtendedStackedInline):
    model = Part
    extra = 0
    raw_id_fields = ['production']
    inline_classes = ('grp-collapse grp-open', )
    classes = ("grp-collapse grp-open", )


class OwnersForm(forms.Form):
    users = forms.ModelMultipleChoiceField(
        label=_("Users"),
        queryset=User.objects.filter(is_active=True),
        required=False,
    )


class ParentAdmin(ExtendedModelAdmin):
    list_display = (
        'production', 'creation_date', 'modified_date', 'get_children'
    )
    search_fields = ('production__title', )

    raw_id_fields = ['production']
    inlines = [PartInline]

    def get_children(self, obj):
        return u'<br />'.join(
            [
                u'» <a target="_blank" href="/admin/productions/production/%s/">%s</a>'
                % (part.production.pk, part.production.title)
                for part in obj.part_set.all()
            ]
        )

    get_children.short_description = _("Contains")
    get_children.allow_tags = True

    def get_owners_list(self, obj):
        owners_list = []
        manage_owners_link = '<a href="%s/owners/"><span>%s</span></a>' % (
            obj.pk, ugettext('Manage owners')
        )
        for o in obj.get_owners():
            owners_list.append(
                '<a href="/admin/auth/user/%s/">%s</a>' % (o.pk, o.username)
            )
        if owners_list:
            return '<br />'.join(owners_list) + '<br />' + manage_owners_link
        return manage_owners_link

    get_owners_list.allow_tags = True
    get_owners_list.short_description = _("Owners")

    def owners_view(self, request, multipart_id):
        from base_libs.views.views import access_denied
        multipart = get_object_or_404(Parent, pk=multipart_id)

        if not multipart.is_editable():
            return access_denied(request)

        if request.method == "POST":
            form = OwnersForm(request.POST)
            if form.is_valid():
                existing_owners = set(multipart.get_owners())
                changed_owners = set(form.cleaned_data['users'])

                removed_owners = existing_owners - changed_owners
                new_owners = changed_owners - existing_owners

                for u in removed_owners:
                    multipart.remove_owner(u)

                for u in new_owners:
                    multipart.set_owner(u)
                return redirect('../../?id__exact=%d' % multipart.pk)
        else:
            form = OwnersForm(initial={'users': multipart.get_owners()})

        return render(
            request, 'admin/owners.html', {
                'multipart':
                    multipart,
                'original':
                    multipart,
                'app_label':
                    Parent._meta.app_label,
                'opts':
                    Parent._meta,
                'form':
                    form,
                'title':
                    ugettext('The owners of %(multipart)s') % {
                        'multipart': multipart
                    },
            }
        )

    def get_urls(self):
        urls = super(ParentAdmin, self).get_urls()
        return [
            url(
                r'^(?P<multipart_id>\d+)/owners/$',
                self.admin_site.admin_view(self.owners_view)
            )
        ] + urls


admin.site.register(Parent, ParentAdmin)

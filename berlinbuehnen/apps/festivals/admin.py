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

from filebrowser.settings import URL_FILEBROWSER_MEDIA

from .models import Festival
from .models import Image
from .models import SocialMediaChannel
from .models import FestivalPDF


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


class FestivalPDFInline(ExtendedStackedInline):
    model = FestivalPDF
    extra = 0
    inline_classes = ('grp-collapse grp-open',)


class OwnersForm(forms.Form):
    users = forms.ModelMultipleChoiceField(
        label=_("Users"),
        queryset=User.objects.filter(is_active=True),
        required=False,
    )


class FestivalAdmin(ExtendedModelAdmin):
    class Media:
        js = (
            "%sjs/AddFileBrowser.js" % URL_FILEBROWSER_MEDIA,
        )
    list_display = ('id', 'title', 'start', 'end', 'get_organizers', 'get_owners_list', 'creation_date', 'modified_date', 'featured', 'slideshow', 'newsletter', 'status')
    list_display_links = ('id', 'title')
    list_editable = ('featured', 'slideshow', 'newsletter', 'status', )
    list_filter = ('start', 'creation_date', 'modified_date', 'featured', 'slideshow', 'newsletter', 'status')
    date_hierarchy = 'start'
    search_fields = ('title_de', 'title_en')

    fieldsets = get_admin_lang_section(_("Title"), ['title', 'subtitle', 'description',])
    fieldsets += [(None, {'fields': ('slug', "organizers")}),]
    fieldsets += [(_("Duration"), {'fields': ('start', 'end', )}),]
    fieldsets += [(_("Festival Office Address"), {'fields': ('street_address', 'street_address2', 'postal_code', 'city', 'latitude', 'longitude')}),]
    fieldsets += [(_("Contacts"), {'fields': ((_("Phone"), {'fields': ('phone_country', 'phone_area', 'phone_number')}), (_("Fax"), {'fields': ('fax_country', 'fax_area', 'fax_number')}),'email','website', )}),]
    fieldsets += [(_("Tickets"), {'fields': ('tickets_street_address', 'tickets_street_address2', 'tickets_postal_code', 'tickets_city', 'tickets_email', 'tickets_website', (_("Phone"), {'fields': ('tickets_phone_country', 'tickets_phone_area', 'tickets_phone_number')}), (_("Fax"), {'fields': ('tickets_fax_country', 'tickets_fax_area', 'tickets_fax_number')}), get_admin_lang_section(_("Calling prices"), ['tickets_calling_prices',]))}),]
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
    fieldsets += [(_("Press Contact"), {'fields': ('press_contact_name', 'press_email', 'press_website', (_("Phone"), {'fields': ('press_phone_country', 'press_phone_area', 'press_phone_number')}), (_("Mobile"), {'fields': ('press_mobile_country', 'press_mobile_area', 'press_mobile_number')}), (_("Fax"), {'fields': ('press_fax_country', 'press_fax_area', 'press_fax_number')}))}),]
    fieldsets += [(_("Status"), {'fields': ('newsletter', 'status',)}),]

    inlines = [ImageInline, SocialMediaChannelInline, FestivalPDFInline]

    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}
    filter_horizontal = ('organizers', )

    def get_organizers(self, obj):
        html = []
        if obj.organizers.count():
            html.append(', '.join(('<a href="' + loc.get_url_path() + '" tagret="_blank">' + unicode(loc) + '</a>' for loc in obj.organizers.all())))
        return '<br />'.join(html)
    get_organizers.short_description = _("Organizers")
    get_organizers.allow_tags = True

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

    def owners_view(self, request, festival_id):
        from base_libs.views.views import access_denied
        festival = get_object_or_404(Festival, pk=festival_id)

        if not festival.is_editable():
            return access_denied(request)

        if request.method == "POST":
            form = OwnersForm(request.POST)
            if form.is_valid():
                existing_owners = set(festival.get_owners())
                changed_owners = set(form.cleaned_data['users'])

                removed_owners = existing_owners - changed_owners
                new_owners = changed_owners - existing_owners

                for u in removed_owners:
                    festival.remove_owner(u)

                for u in new_owners:
                    festival.set_owner(u)
                return redirect('../../?id__exact=%d' % festival.pk)
        else:
            form = OwnersForm(initial={
                'users': festival.get_owners()
            })

        return render(request, 'admin/owners.html', {
            'festival': festival,
            'original': festival,
            'app_label': Festival._meta.app_label,
            'opts': Festival._meta,
            'form': form,
            'title': ugettext('The owners of %(festival)s') % {'festival': festival},
        })

    def get_urls(self):
        urls = super(FestivalAdmin, self).get_urls()
        return patterns('', url(r'^(?P<festival_id>\d+)/owners/$', self.owners_view)) + urls


admin.site.register(Festival, FestivalAdmin)
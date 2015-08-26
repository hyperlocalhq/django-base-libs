# -*- coding: UTF-8 -*-

from django import forms
from django.db import models
from django import template
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.admin import helpers
from django.contrib.admin.util import model_ngettext
from django.utils.encoding import force_unicode

from base_libs.admin import ExtendedModelAdmin
from base_libs.models.admin import get_admin_lang_section
from base_libs.admin.tree_editor import TreeEditor

LegalForm = models.get_model("institutions", "LegalForm")
Institution = models.get_model("institutions", "Institution")
InstitutionType = models.get_model("institutions", "InstitutionType")
MList = models.get_model("mailchimp", "MList")
Subscription = models.get_model("mailchimp", "Subscription")


class InstitutionTypeOptions(TreeEditor):
    save_on_top = True
    list_display = ['actions_column', 'indented_short_title']

    fieldsets = [(None, {'fields': ('parent',)}), ]
    fieldsets += get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug',)}), ]

    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,), }


class MListForm(forms.Form):
    mailinglist = forms.ModelChoiceField(
        queryset=MList.objects.all(),
        label=_("Mailing List"),
        required=True,
    )
    email_type = forms.ChoiceField(
        choices=(
            ('', "---------"),
            ('contact', _("Contact Email")),
            ('owner', _("Owner Email")),
        ),
        label=_("Email type"),
        required=True,
    )


def mailchimp_subscribe(modeladmin, request, queryset):
    """
    An action which subscribes institutions to mailchimp lists
    
    This action at first displays a list of mailing lists to subscribe to.
    
    Next it subscribes the selected people to the mailing list.
    """
    opts = modeladmin.model._meta
    app_label = opts.app_label

    if request.POST.get('mailchimp_subscribe'):
        form = MListForm(request.POST)
        if form.is_valid():
            mailing_list = form.cleaned_data['mailinglist']
            email_type = form.cleaned_data['email_type']
            n = queryset.count()
            if n:
                for obj in queryset:
                    if email_type == "contact":
                        email = obj.get_primary_contact()['email0_address']
                        if email:
                            sub, created = Subscription.objects.get_or_create(
                                mailinglist=mailing_list,
                                email=email,
                                defaults={
                                    'first_name': "",
                                    'last_name': "",
                                    'subscriber': None,
                                    'ip': "",
                                    'status': "subscribed",
                                }
                            )

                    elif email_type == "owner":
                        for p in obj.get_owners():
                            user = p.user
                            sub, created = Subscription.objects.get_or_create(
                                mailinglist=mailing_list,
                                email=user.email,
                                defaults={
                                    'first_name': user.first_name,
                                    'last_name': user.last_name,
                                    'subscriber': user,
                                    'ip': "",
                                    'status': "subscribed",
                                }
                            )

                modeladmin.message_user(request, _("Successfully subscribed %(count)d %(items)s.") % {
                    "count": n, "items": model_ngettext(modeladmin.opts, n)
                })
            # Return None to display the change list page again.
            return None
    else:
        form = MListForm()

    if len(queryset) == 1:
        objects_name = force_unicode(opts.verbose_name)
    else:
        objects_name = force_unicode(opts.verbose_name_plural)

    title = _("Subscribe to a mailing list")

    context = {
        "title": title,
        "objects_name": objects_name,
        'queryset': queryset,
        "opts": opts,
        "root_path": modeladmin.admin_site.root_path,
        "app_label": app_label,
        'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
        'form': form,
    }
    # Display the confirmation page
    return render_to_response(
        "admin/%s/%s/mailchimp_subscribe_selected.html" % (app_label, opts.object_name.lower()),
        context,
        context_instance=template.RequestContext(request)
    )


mailchimp_subscribe.short_description = _("Subscribe to mailing list")


class LegalFormOptions(ExtendedModelAdmin):
    save_on_top = True
    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug', 'sort_order')}), ]
    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,), }


class InstitutionOptions(ExtendedModelAdmin):
    save_on_top = True
    list_display = ('title', 'get_admin_links_to_owners', 'slug', 'creation_date', 'status')
    list_filter = ('creation_date', 'status',)
    search_fields = ('title', 'title2', 'slug')
    ordering = ('-creation_date',)
    actions = ["publish", "publish_commercial", mailchimp_subscribe]

    def publish(self, request, queryset):
        for inst in queryset:
            inst.status = "published"
            inst.save()

    publish.short_description = _("Publish selected institutions as non-commercial")

    def publish_commercial(self, request, queryset):
        for inst in queryset:
            inst.status = "published_commercial"
            inst.save()

    publish_commercial.short_description = _("Publish selected institutions as commercial")


admin.site.register(Institution, InstitutionOptions)
admin.site.register(InstitutionType, InstitutionTypeOptions)
admin.site.register(LegalForm, LegalFormOptions)

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
from django.contrib.admin.util import NestedObjects, quote
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db import router
from django.template.defaultfilters import date
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.text import capfirst

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


def get_deleted_objects(objs, opts, user, admin_site, using):
    """
    Find all objects related to ``objs`` that should also be deleted. ``objs``
    must be a homogenous iterable of objects (e.g. a QuerySet).

    Returns a nested list of strings suitable for display in the
    template with the ``unordered_list`` filter.

    """
    FIELDS_AND_DISPLAYS = (
        ("title", lambda obj: obj.title),
        ("email", lambda obj: obj.email),
        ("phone_number", lambda obj: obj.phone_number),
        ("cell_phone_number", lambda obj: obj.cell_phone_number),
        ("street_address", lambda obj: obj.street_address),
        ("postal_code", lambda obj: obj.postal_code),
        ("city", lambda obj: obj.city),
        ("district", lambda obj: obj.district),
        ("website", lambda obj: obj.website),
        ("short_description", lambda obj: obj.short_description),
        ("categories", lambda obj: ", ".join((unicode(el) for el in obj.categories.all()))),
        ("reference_url_1", lambda obj: obj.reference_url_1),
        ("reference_url_2", lambda obj: obj.reference_url_2),
        ("reference_url_3", lambda obj: obj.reference_url_3),
    )

    collector = NestedObjects(using=using)
    collector.collect(objs)
    perms_needed = set()

    def format_callback(obj):
        has_admin = obj.__class__ in admin_site._registry
        opts = obj._meta

        if has_admin:
            admin_url = reverse('%s:%s_%s_change'
                                % (admin_site.name,
                                   opts.app_label,
                                   opts.object_name.lower()),
                                None, (quote(obj._get_pk_val()),))
            p = '%s.%s' % (opts.app_label,
                           opts.get_delete_permission())
            if not user.has_perm(p):
                perms_needed.add(opts.verbose_name)
            # Display a link to the admin page.
            obj_str = ""
            if isinstance(obj, Institution) and type(obj) == Institution:
                obj_str += u'<input type="radio" name="main_institution" value="%s" /> ' % obj.pk
            obj_str += u'%s: <a href="%s">%s</a>.' % (
                escape(capfirst(opts.verbose_name)),
                admin_url,
                escape(obj))
            if isinstance(obj, Institution) and type(obj) == Institution:
                obj_str += " %s." % obj.get_address()
                if obj.creation_date:
                    obj_str += " Erstellungsdatum: %s." % date(obj.creation_date, "j. E Y H:i:s")
                for field_name, display_function in FIELDS_AND_DISPLAYS:
                    obj_str += u'<div class="row cells-1"><div><div class="column span-4">%s</div><div class="column span-flexible">%s&nbsp;</div></div></div>' % (
                        Institution._meta.get_field(field_name).verbose_name,
                        display_function(obj) or "-",
                    )
                try:
                    obj.artisticinstitution
                except Institution.DoesNotExist:
                    pass
                else:
                    obj_str += u'<div class="row cells-1"><div><div class="column span-4">%s</div><div class="column span-flexible">%s&nbsp;</div></div></div>' % (
                        obj.artisticinstitution._meta.get_field("legal_form").verbose_name,
                        obj.artisticinstitution.legal_form or "-",
                    )
                    obj_str += u'<div class="row cells-1"><div><div class="column span-4">%s</div><div class="column span-flexible">%s&nbsp;</div></div></div>' % (
                        obj.artisticinstitution._meta.get_field("other_legal_form").verbose_name,
                        obj.artisticinstitution.other_legal_form or "-",
                    )
                try:
                    obj.educationalinstitution
                except Institution.DoesNotExist:
                    pass
                else:
                    obj_str += u'<div class="row cells-1"><div><div class="column span-4">%s</div><div class="column span-flexible">%s&nbsp;</div></div></div>' % (
                        obj.educationalinstitution._meta.get_field("organization_forms").verbose_name,
                        ", ".join((unicode(el) for el in obj.educationalinstitution.organization_forms.all())) or "-",
                    )
                    obj_str += u'<div class="row cells-1"><div><div class="column span-4">%s</div><div class="column span-flexible">%s&nbsp;</div></div></div>' % (
                        obj.educationalinstitution._meta.get_field("bsn").verbose_name,
                        obj.educationalinstitution.bsn or "-",
                    )
                    obj_str += u'<div class="row cells-1"><div><div class="column span-4">%s</div><div class="column span-flexible">%s&nbsp;</div></div></div>' % (
                        obj.educationalinstitution._meta.get_field("school_branch").verbose_name,
                        obj.educationalinstitution.school_branch or "-",
                    )
                try:
                    obj.youthinstitution
                except Institution.DoesNotExist:
                    pass
                else:
                    obj_str += u'<div class="row cells-1"><div><div class="column span-4">%s</div><div class="column span-flexible">%s&nbsp;</div></div></div>' % (
                        obj.youthinstitution._meta.get_field("legal_form").verbose_name,
                        obj.youthinstitution.legal_form or "-",
                    )
                    obj_str += u'<div class="row cells-1"><div><div class="column span-4">%s</div><div class="column span-flexible">%s&nbsp;</div></div></div>' % (
                        obj.youthinstitution._meta.get_field("other_legal_form").verbose_name,
                        obj.youthinstitution.other_legal_form or "-",
                    )

            return mark_safe(obj_str)
        else:
            # Don't display link to edit, because it either has no
            # admin or is edited inline.
            return u'%s: %s' % (capfirst(opts.verbose_name),
                                force_unicode(obj))

    to_delete = collector.nested(format_callback)

    protected = [format_callback(obj) for obj in collector.protected]

    return to_delete, perms_needed, protected


def merge_selected(modeladmin, request, queryset):
    MANAGERS_AND_FIELDS = (
        ("artapplicant_set", "institution"),
        ("cooperationpartner_set", "institution"),
        ("eduapplicant_set", "institution"),
        ("membership_set", "institution"),
    )

    opts = modeladmin.model._meta
    app_label = opts.app_label

    # Check that the user has delete permission for the actual model
    if not modeladmin.has_delete_permission(request):
        raise PermissionDenied

    using = router.db_for_write(modeladmin.model)

    # Populate deletable_objects, a data structure of all related objects that
    # will also be deleted.
    queryset.model = Institution
    deletable_objects, perms_needed, protected = get_deleted_objects(
        queryset, opts, request.user, modeladmin.admin_site, using)

    # The user has already confirmed the merging.
    # Do the merging and return a None to display the change list view again.
    if request.POST.get('post') and 'main_institution' in request.POST:
        if perms_needed:
            raise PermissionDenied
        main_person = queryset.get(pk=request.POST['main_institution'])
        queryset = queryset.exclude(pk=request.POST['main_institution'])
        n = queryset.count()
        if n:
            for obj in queryset:
                for manager_name, field_name in MANAGERS_AND_FIELDS:
                    for related in getattr(obj, manager_name).all():
                        setattr(related, field_name, main_person)
                        related.save()
                obj.delete()
            modeladmin.message_user(request, _("Successfully merged %(count)d institutions to %(name)s.") % {
                "count": n + 1,
                "name": unicode(main_person),
            })
        # Return None to display the change list page again.
        return None

    if len(queryset) == 1:
        objects_name = force_unicode(opts.verbose_name)
    else:
        objects_name = force_unicode(opts.verbose_name_plural)

    if perms_needed or protected:
        title = _("Cannot merge %(name)s") % {"name": objects_name}
    else:
        title = _("Are you sure?")

    context = {
        "title": title,
        "objects_name": objects_name,
        "deletable_objects": [deletable_objects],
        'queryset': queryset,
        "perms_lacking": perms_needed,
        "protected": protected,
        "opts": opts,
        "root_path": modeladmin.admin_site.root_path,
        "app_label": app_label,
        'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
    }

    # Display the confirmation page
    return render_to_response("admin/institutions/institution/merge_selected.html", context,
                              context_instance=template.RequestContext(request))


merge_selected.short_description = "Merge selected institutions"


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
    actions = ["publish", "publish_commercial", mailchimp_subscribe, merge_selected]

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

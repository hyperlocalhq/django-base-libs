# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django import forms
from django.conf.urls import patterns, url
from django.apps import apps
from django import template
from django.contrib import admin, messages
from django.utils.translation import ugettext_lazy as _, ugettext
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404, redirect, render
from django.contrib.admin import helpers
from django.utils.text import force_text
from django.utils.encoding import force_unicode
from django.contrib.admin.util import NestedObjects, quote
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db import router
from django.template.defaultfilters import date
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.db.models.functions import Lower

from base_libs.admin import ExtendedModelAdmin
from base_libs.models.admin import get_admin_lang_section
from base_libs.admin.tree_editor import TreeEditor


Person = apps.get_model("people", "Person")
LegalForm = apps.get_model("institutions", "LegalForm")
Institution = apps.get_model("institutions", "Institution")
InstitutionType = apps.get_model("institutions", "InstitutionType")


class InstitutionTypeOptions(TreeEditor):
    save_on_top = True
    list_display = ['actions_column', 'indented_short_title']

    fieldsets = [(None, {'fields': ('parent',)}), ]
    fieldsets += get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug',)}), ]

    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,), }


def get_deleted_objects(objs, opts, user, admin_site, using):
    """
    Find all objects related to ``objs`` that should also be deleted. ``objs``
    must be a homogenous iterable of objects (e.g. a QuerySet).

    Returns a nested list of strings suitable for display in the
    template with the ``unordered_list`` filter.

    """
    FIELDS_AND_DISPLAYS = (
        ("title", lambda obj: obj.title),
        ("title2", lambda obj: obj.title2),
        ("slug", lambda obj: obj.slug),
        ("parent", lambda obj: obj.parent),
        ("description", lambda obj: obj.description),
        ("image", lambda obj: obj.image),
        # ("institution_types", lambda obj: obj.institution_types),
        ("status", lambda obj: obj.status),
        ("legal_form", lambda obj: obj.legal_form),
        # ("context_categories", lambda obj: obj.context_categories),
        ("access", lambda obj: obj.access),
        ("is_parking_avail", lambda obj: obj.is_parking_avail),
        ("is_wlan_avail", lambda obj: obj.is_wlan_avail),
        ("is_non_profit", lambda obj: obj.is_non_profit),
        ("tax_id_number", lambda obj: obj.tax_id_number),
        ("vat_id_number", lambda obj: obj.vat_id_number),
        ("is_card_visa_ok", lambda obj: obj.is_card_visa_ok),
        ("is_card_mastercard_ok", lambda obj: obj.is_card_mastercard_ok),
        ("is_card_americanexpress_ok", lambda obj: obj.is_card_americanexpress_ok),
        ("is_paypal_ok", lambda obj: obj.is_paypal_ok),
        ("is_cash_ok", lambda obj: obj.is_cash_ok),
        ("is_transaction_ok", lambda obj: obj.is_transaction_ok),
        ("is_prepayment_ok", lambda obj: obj.is_prepayment_ok),
        ("is_on_delivery_ok", lambda obj: obj.is_on_delivery_ok),
        ("is_invoice_ok", lambda obj: obj.is_invoice_ok),
        ("is_ec_maestro_ok", lambda obj: obj.is_ec_maestro_ok),
        ("is_giropay_ok", lambda obj: obj.is_giropay_ok),
        ("establishment_yyyy", lambda obj: obj.establishment_yyyy),
        ("establishment_mm", lambda obj: obj.establishment_mm),
        ("nof_employees", lambda obj: obj.nof_employees),
        # ("creative_sectors", lambda obj: obj.creative_sectors),
        ("creation_date", lambda obj: obj.creation_date),
        ("modified_date", lambda obj: obj.modified_date),
        ("is_appointment_based", lambda obj: obj.is_appointment_based),
        ("mon_open", lambda obj: obj.mon_open),
        ("mon_break_close", lambda obj: obj.mon_break_close),
        ("mon_break_open", lambda obj: obj.mon_break_open),
        ("mon_close", lambda obj: obj.mon_close),
        ("tue_open", lambda obj: obj.tue_open),
        ("tue_break_close", lambda obj: obj.tue_break_close),
        ("tue_break_open", lambda obj: obj.tue_break_open),
        ("tue_close", lambda obj: obj.tue_close),
        ("wed_open", lambda obj: obj.wed_open),
        ("wed_break_close", lambda obj: obj.wed_break_close),
        ("wed_break_open", lambda obj: obj.wed_break_open),
        ("wed_close", lambda obj: obj.wed_close),
        ("thu_open", lambda obj: obj.thu_open),
        ("thu_break_close", lambda obj: obj.thu_break_close),
        ("thu_break_open", lambda obj: obj.thu_break_open),
        ("thu_close", lambda obj: obj.thu_close),
        ("fri_open", lambda obj: obj.fri_open),
        ("fri_break_close", lambda obj: obj.fri_break_close),
        ("fri_break_open", lambda obj: obj.fri_break_open),
        ("fri_close", lambda obj: obj.fri_close),
        ("sat_open", lambda obj: obj.sat_open),
        ("sat_break_close", lambda obj: obj.sat_break_close),
        ("sat_break_open", lambda obj: obj.sat_break_open),
        ("sat_close", lambda obj: obj.sat_close),
        ("sun_open", lambda obj: obj.sun_open),
        ("sun_break_close", lambda obj: obj.sun_break_close),
        ("sun_break_open", lambda obj: obj.sun_break_open),
        ("sun_close", lambda obj: obj.sun_close),
        ("exceptions", lambda obj: obj.exceptions),
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
            obj_str = '<h3>'
            if isinstance(obj, Institution) and type(obj) == Institution:
                obj_str += u'<input type="radio" name="main_institution" value="%s" /> ' % obj.pk
            obj_str += u'%s: <a href="%s">%s</a></h3>' % (
                escape(capfirst(opts.verbose_name)),
                admin_url,
                escape(obj))
            if isinstance(obj, Institution) and type(obj) == Institution:
                row_template = u'''
                <div class="grp-row grp-cells-1">
                    <div class="l-2c-fluid l-d-4">
                        <div class="c-1">{0}</div>
                        <div class="c-2">{1}&nbsp;</div>
                    </div>
                </div>'''
                if obj.creation_date:
                    obj_str += row_template.format('Erstellungsdatum', date(obj.creation_date, "j. E Y H:i:s"))
                for field_name, display_function in FIELDS_AND_DISPLAYS:
                    obj_str += row_template.format(
                        Institution._meta.get_field(field_name).verbose_name,
                        display_function(obj) or "-",
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
        ("events_happened", "venue"),
        ("event_set", "organizing_institution"),
        ("institution_set", "parent"),
        ("document_set", "publisher"),
        # ("institutionalcontact_set", "institution"),
        ("individualcontact_set", "institution"),
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
        main_institution = queryset.get(pk=request.POST['main_institution'])
        queryset = queryset.exclude(pk=request.POST['main_institution'])
        n = queryset.count()
        if n:
            address_ids = set()
            for obj in queryset:
                for manager_name, field_name in MANAGERS_AND_FIELDS:
                    for related in getattr(obj, manager_name).all():
                        setattr(related, field_name, main_institution)
                        related.save()
                for related in obj.institutionalcontact_set.all():
                    if related.postal_address_id not in address_ids:
                        related.institution = main_institution
                        related.save()
                        address_ids.add(related.postal_address_id)
                    else:
                        related.delete()
                obj.delete()
            modeladmin.message_user(request, _("Successfully merged %(count)d institutions to %(name)s.") % {
                "count": n + 1,
                "name": unicode(main_institution),
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
        # "root_path": modeladmin.admin_site.root_path,
        "app_label": app_label,
        'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
    }

    # Display the confirmation page
    return render_to_response("admin/institutions/institution/merge_selected.html", context,
                              context_instance=template.RequestContext(request))


merge_selected.short_description = _("Merge selected institutions")


class LegalFormOptions(ExtendedModelAdmin):
    save_on_top = True
    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug', 'sort_order')}), ]
    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,), }


class ModelMultiRawInput(forms.TextInput):
    def render(self, name, value, attrs=None):
        if value:
            value = ','.join([force_text(v) for v in value])
        else:
            value = ''
        return super(ModelMultiRawInput, self).render(name, value, attrs)

    def value_from_datadict(self, data, files, name):
        value = data.get(name)
        if value:
            return value.split(',')


class OwnersForm(forms.Form):
    people = forms.ModelMultipleChoiceField(
        label=_("Users"),
        queryset=Person.objects.filter(user__is_active=True).order_by(Lower('user__username')),
        required=False,
        widget=ModelMultiRawInput(),
    )


class InstitutionOptions(ExtendedModelAdmin):
    save_on_top = True
    list_display = ('title', 'get_owners_list', 'slug', 'creation_date', 'status')
    list_filter = ('creation_date', 'status', 'context_categories')
    search_fields = ('title', 'title2', 'slug')
    ordering = ('-creation_date',)
    actions = ["publish", "publish_commercial", merge_selected]

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

    def get_owners_list(self, obj):
        lines = []
        for o in obj.get_owners():
            lines.append('<a href="/admin/people/person/%s/">%s</a>' % (o.pk, o))
        lines.append('<a href="%s/owners/"><span>%s</span></a>' % (obj.pk, ugettext('Manage owners')))
        return '<br />'.join(lines)

    get_owners_list.allow_tags = True
    get_owners_list.short_description = _("Owners")

    def owners_view(self, request, institution_id):
        from base_libs.views.views import access_denied
        institution = get_object_or_404(Institution, pk=institution_id)

        if not (request.user.is_staff and institution.is_editable()):
            return access_denied(request)

        if request.method == "POST":
            form = OwnersForm(request.POST)
            if form.is_valid():
                existing_owners = set(institution.get_owners())
                changed_owners = set(form.cleaned_data['people'])

                removed_owners = existing_owners - changed_owners
                new_owners = changed_owners - existing_owners

                for p in removed_owners:
                    institution.remove_owner(p)
                    messages.success(
                        request,
                        _("User {} was removed from institution owners").format(p)
                    )

                for p in new_owners:
                    institution.set_owner(p)
                    messages.success(
                        request,
                        _("User {} was added to institution owners").format(p)
                    )

                return redirect('../../?id__exact=%d' % institution.pk)
        else:
            form = OwnersForm(initial={
                'people': institution.get_owners()
            })

        return render(request, 'admin/owners.html', {
            'location': institution,
            'original': institution,
            'app_label': Institution._meta.app_label,
            'opts': Institution._meta,
            'form': form,
            'title': ugettext('The owners of %(institution)s') % {'institution': institution},
        })

    def get_urls(self):
        urls = super(InstitutionOptions, self).get_urls()
        return patterns('', url(r'^(?P<institution_id>\d+)/owners/$', self.owners_view)) + urls


admin.site.register(Institution, InstitutionOptions)
admin.site.register(InstitutionType, InstitutionTypeOptions)
admin.site.register(LegalForm, LegalFormOptions)

# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib import admin
from django.contrib.admin.options import *
from django.forms.models import modelform_factory
from django import forms
from django.views.decorators.cache import never_cache
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404, render_to_response
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.utils.encoding import force_text

from base_libs.models.admin import get_admin_lang_section
from base_libs.admin import ExtendedStackedInline
from base_libs.admin import ExtendedModelAdmin
from base_libs.forms.fields import AutocompleteModelChoiceField

import filebrowser.settings as filebrowser_settings
URL_FILEBROWSER_MEDIA = getattr(
    filebrowser_settings, "FILEBROWSER_DIRECTORY", 'uploads/'
)
Address = models.get_model("location", "Address")
Locality = models.get_model("location", "Locality")
Geoposition = models.get_model("location", "Geoposition")

JobType = models.get_model("marketplace", "JobType")
JobQualification = models.get_model("marketplace", "JobQualification")
JobSector = models.get_model("marketplace", "JobSector")
JobOffer = models.get_model("marketplace", "JobOffer")


def add_form_fields(form, modelform):
    for field_name, field in modelform.base_fields.items():
        setattr(form, field_name, field)
        form.fields[field_name] = field


class JobTypeAdmin(admin.ModelAdmin):
    save_on_top = True
    list_filter = ('is_internship', )
    list_display = ['title', 'is_internship', 'sort_order']

    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [
        (None, {
            'fields': ('slug', 'is_internship', 'sort_order')
        }),
    ]
    prepopulated_fields = {
        "slug": ("title_%s" % settings.LANGUAGE_CODE, ),
    }


class JobSectorAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['title', 'sort_order']

    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [
        (None, {
            'fields': ('slug', 'sort_order')
        }),
    ]
    prepopulated_fields = {
        "slug": ("title_%s" % settings.LANGUAGE_CODE, ),
    }


class JobQualificationAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['title', 'sort_order']

    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [
        (None, {
            'fields': ('slug', 'sort_order')
        }),
    ]
    prepopulated_fields = {
        "slug": ("title_%s" % settings.LANGUAGE_CODE, ),
    }


AddressForm = modelform_factory(
    Address,
    exclude=["id"],
    #formfield_callback=formfield_for_dbfield,
)
LocalityForm = modelform_factory(
    Locality,
    exclude=["id", "address"],
    #formfield_callback=formfield_for_dbfield,
)
GeopositionForm = modelform_factory(
    Geoposition,
    exclude=["id", "address"],
    #formfield_callback=formfield_for_dbfield,
)


class JobOfferForm(forms.ModelForm):
    """
    Job offer form for administration combines
    * all fields from JobOffer model
    * fields from Address model
    * fields from Locality model
    * fields from Geoposition model
    """

    try:
        JobOffer._meta.get_field("offering_institution")
    except models.FieldDoesNotExist:
        pass
    else:
        offering_institution = AutocompleteModelChoiceField(
            required=False,
            label=_("Offering institution"),
            help_text=_(
                "Please enter a letter to display a list of available institutions"
            ),
            app="marketplace",
            qs_function="get_institutions",
            display_attr="title",
            add_display_attr="get_address_string",
            options={
                "minChars": 1,
                "max": 20,
                "mustMatch": 1,
                "highlight": False,
            },
        )

    try:
        JobOffer._meta.get_field("contact_person")
    except models.FieldDoesNotExist:
        pass
    else:
        contact_person = AutocompleteModelChoiceField(
            required=False,
            label=_("Contact Person"),
            help_text=_(
                "Please enter a letter to display a list of available people"
            ),
            app="marketplace",
            qs_function="get_people",
            display_attr="get_username",
            add_display_attr="get_name_and_email",
            options={
                "minChars": 1,
                "max": 20,
                "mustMatch": 1,
                "highlight": False,
            },
        )

    try:
        JobOffer._meta.get_field("author")
    except models.FieldDoesNotExist:
        pass
    else:
        author = AutocompleteModelChoiceField(
            required=False,
            label=_("Author"),
            help_text=_(
                "Please enter a letter to display a list of available authors"
            ),
            app="marketplace",
            qs_function="get_users",
            display_attr="username",
            add_display_attr="get_profile",
            options={
                "minChars": 1,
                "max": 20,
                "mustMatch": 1,
                "highlight": False,
            },
        )

    class Meta:
        model = JobOffer
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(JobOfferForm, self).__init__(*args, **kwargs)
        add_form_fields(self, AddressForm)
        add_form_fields(self, LocalityForm)
        add_form_fields(self, GeopositionForm)

        self.country = self.fields['country'] = AutocompleteModelChoiceField(
            required=False,
            label=_("Country"),
            help_text=_(
                "Please enter a letter to display a list of available countries"
            ),
            app="i18n",
            qs_function="get_countries",
            display_attr="get_name",
            options={
                "minChars": 1,
                "max": 20,
                "mustMatch": 1,
                "highlight": False,
            }
        )

        # initial fields from the Address, Locality, and Geoposition models
        # should also be added (only those which are necessary)
        if self.instance.id and self.instance.postal_address:
            address_form = AddressForm(instance=self.instance.postal_address, )
            locality_form = LocalityForm(
                instance=self.instance.postal_address.get_locality(),
            )
            geoposition_form = GeopositionForm(
                instance=self.instance.postal_address.get_geoposition(),
            )
        else:
            address_form = AddressForm()
            locality_form = LocalityForm()
            geoposition_form = GeopositionForm()

        self.initial.update(address_form.initial)
        self.initial.update(locality_form.initial)
        self.initial.update(geoposition_form.initial)
        '''
        self.fields['venue'].widget.attrs.setdefault("class", "")
        self.fields['venue'].widget.attrs['class'] = (
            self.fields['venue'].widget.attrs['class']
            + " autocomplete"
            ).strip()
        self.fields['organizing_institution'].widget.attrs.setdefault("class", "")
        self.fields['organizing_institution'].widget.attrs['class'] = (
            self.fields['organizing_institution'].widget.attrs['class']
            + " autocomplete"
            ).strip()
        '''


class JobOfferAdmin(ExtendedModelAdmin):
    form = JobOfferForm
    change_form_template = "extendedadmin/job_offer_change.html"
    save_on_top = True
    list_display = ['position', 'job_type', 'status', 'creation_date']
    list_filter = ('creation_date', 'job_type', 'status')
    search_fields = ['position']
    ordering = ('-creation_date', )

    #never_cache doesn't work for class methods with django r11611
    @transaction.atomic
    def add_view(self, request, form_url='', extra_context=None):
        """The 'add' admin view for this model."""
        model = self.model
        opts = model._meta

        if not self.has_add_permission(request):
            raise PermissionDenied

        ModelForm = self.get_form(request)
        formsets = []
        inline_instances = self.get_inline_instances(request)
        if request.method == 'POST':
            form = ModelForm(request.POST, request.FILES)
            if form.is_valid():
                form_validated = True
                new_object = self.save_form(request, form, change=False)
            else:
                form_validated = False
                new_object = self.model()
            prefixes = {}
            for FormSet in self.get_formsets(request):
                prefix = FormSet.get_default_prefix()
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])
                formset = FormSet(
                    data=request.POST,
                    files=request.FILES,
                    instance=new_object,
                    save_as_new=request.POST.has_key("_saveasnew"),
                    prefix=prefix
                )
                formsets.append(formset)
            if all_valid(formsets) and form_validated:
                self.save_model(request, new_object, form, change=False)
                form.save_m2m()
                for formset in formsets:
                    self.save_formset(request, form, formset, change=False)

                self.log_addition(request, new_object)
                return self.response_add(request, new_object)
        else:
            # Prepare the dict of initial data from the request.
            # We have to special-case M2Ms as a list of comma-separated PKs.
            initial = dict(request.GET.items())
            for k in initial:
                try:
                    f = opts.get_field(k)
                except models.FieldDoesNotExist:
                    continue
                if isinstance(f, models.ManyToManyField):
                    initial[k] = initial[k].split(",")
            form = ModelForm(initial=initial)
            prefixes = {}
            for FormSet in self.get_formsets(request):
                prefix = FormSet.get_default_prefix()
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])
                formset = FormSet(instance=self.model(), prefix=prefix)
                formsets.append(formset)

        adminForm = helpers.AdminForm(
            form, list(self.get_fieldsets(request)), self.prepopulated_fields
        )
        media = self.media + adminForm.media

        inline_admin_formsets = []
        for inline, formset in zip(inline_instances, formsets):
            fieldsets = list(inline.get_fieldsets(request))
            inline_admin_formset = helpers.InlineAdminFormSet(
                inline, formset, fieldsets
            )
            inline_admin_formsets.append(inline_admin_formset)
            media = media + inline_admin_formset.media

        context = {
            'title': _('Add %s') % force_text(opts.verbose_name),
            'adminform': adminForm,
            'form': form,  # form added
            'is_popup': request.REQUEST.has_key('_popup'),
            'show_delete': False,
            'media': mark_safe(media),
            'inline_admin_formsets': inline_admin_formsets,
            'errors': helpers.AdminErrorList(form, formsets),
            'app_label': opts.app_label,
        }
        context.update(extra_context or {})
        return self.render_change_form(
            request, context, form_url=form_url, add=True
        )

    #never_cache doesn't work for class methods with django r11611
    @transaction.atomic
    def change_view(self, request, object_id, extra_context=None):
        """Displays the job offer add/change form and handles job offer saving."""
        "The 'change' admin view for this model."
        model = self.model
        opts = model._meta

        try:
            obj = self.get_queryset(request).get(pk=unquote(object_id))
        except model.DoesNotExist:
            # Don't raise Http404 just yet, because we haven't checked
            # permissions yet. We don't want an unauthenticated user to be able
            # to determine whether a given object exists.
            obj = None

        if not self.has_change_permission(request, obj):
            raise PermissionDenied

        if obj is None:
            raise Http404(
                _('%(name)s object with primary key %(key)r does not exist.') %
                {
                    'name': force_text(opts.verbose_name),
                    'key': escape(object_id)
                }
            )

        if request.method == 'POST' and request.POST.has_key("_saveasnew"):
            return self.add_view(request, form_url='../add/')

        ModelForm = self.get_form(request, obj)
        formsets = []
        inline_instances = self.get_inline_instances(request)
        if request.method == 'POST':
            form = ModelForm(request.POST, request.FILES, instance=obj)
            if form.is_valid():
                form_validated = True
                new_object = self.save_form(request, form, change=True)
            else:
                form_validated = False
                new_object = obj
            prefixes = {}
            for FormSet in self.get_formsets(request, new_object):
                prefix = FormSet.get_default_prefix()
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])
                formset = FormSet(
                    request.POST,
                    request.FILES,
                    instance=new_object,
                    prefix=prefix
                )
                formsets.append(formset)

            if all_valid(formsets) and form_validated:
                self.save_model(request, new_object, form, change=True)
                form.save_m2m()
                for formset in formsets:
                    self.save_formset(request, form, formset, change=True)

                change_message = self.construct_change_message(
                    request, form, formsets
                )
                self.log_change(request, new_object, change_message)
                return self.response_change(request, new_object)

        else:
            form = ModelForm(instance=obj)
            prefixes = {}
            for FormSet in self.get_formsets(request, obj):
                prefix = FormSet.get_default_prefix()
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])
                formset = FormSet(instance=obj, prefix=prefix)
                formsets.append(formset)

        adminForm = helpers.AdminForm(
            form, self.get_fieldsets(request, obj), self.prepopulated_fields
        )
        media = self.media + adminForm.media

        inline_admin_formsets = []
        for inline, formset in zip(inline_instances, formsets):
            fieldsets = list(inline.get_fieldsets(request, obj))
            inline_admin_formset = helpers.InlineAdminFormSet(
                inline, formset, fieldsets
            )
            inline_admin_formsets.append(inline_admin_formset)
            media = media + inline_admin_formset.media

        context = {
            'title': _('Change %s') % force_text(opts.verbose_name),
            'adminform': adminForm,
            'form': form,  # form added
            'object_id': object_id,
            'original': obj,
            'is_popup': request.REQUEST.has_key('_popup'),
            'media': mark_safe(media),
            'inline_admin_formsets': inline_admin_formsets,
            'errors': helpers.AdminErrorList(form, formsets),
            'app_label': opts.app_label,
        }
        context.update(extra_context or {})
        return self.render_change_form(request, context, change=True, obj=obj)

    def save_form(self, request, form, change):
        """
        Given a ModelForm return an unsaved instance. ``change`` is True if
        the object is being changed, and False if it's being added.
        """
        job_offer = super(JobOfferAdmin, self).save_form(request, form, change)
        job_offer.save()  # to ensure that creation date is saved
        Address.objects.set_for(
            job_offer,
            "postal_address",
            country=form.cleaned_data["country"],
            state=form.cleaned_data["state"],
            city=form.cleaned_data["city"],
            street_address=form.cleaned_data["street_address"],
            street_address2=form.cleaned_data["street_address2"],
            street_address3=form.cleaned_data["street_address3"],
            postal_code=form.cleaned_data["postal_code"],
            district=form.cleaned_data["district"],
            neighborhood=form.cleaned_data["neighborhood"],
            latitude=form.cleaned_data["latitude"],
            longitude=form.cleaned_data["longitude"],
            altitude=form.cleaned_data["altitude"],
        )
        return job_offer


admin.site.register(JobType, JobTypeAdmin)
admin.site.register(JobQualification, JobQualificationAdmin)
admin.site.register(JobSector, JobSectorAdmin)
admin.site.register(JobOffer, JobOfferAdmin)

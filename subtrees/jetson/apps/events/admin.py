# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib import admin
from django.contrib.admin.options import *
from django.forms.models import modelform_factory
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404, render_to_response
from django.core.exceptions import PermissionDenied
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.utils.encoding import force_text

from base_libs.admin import ExtendedStackedInline
from base_libs.admin import ExtendedModelAdmin
from base_libs.forms.fields import AutocompleteModelChoiceField
from base_libs.forms.fields import AutocompleteModelMultipleChoiceField
from base_libs.middleware import get_current_user
from base_libs.utils.misc import get_related_queryset
from base_libs.models.admin import get_admin_lang_section
from base_libs.admin.tree_editor import TreeEditor

import filebrowser.settings as filebrowser_settings
URL_FILEBROWSER_MEDIA = getattr(
    filebrowser_settings, "FILEBROWSER_DIRECTORY", 'uploads/'
)
from jetson.apps.location.models import Address
from jetson.apps.location.models import Locality
from jetson.apps.location.models import Geoposition

Event = models.get_model("events", "Event")
EventType = models.get_model("events", "EventType")
EventTimeLabel = models.get_model("events", "EventTimeLabel")
EventTime = models.get_model("events", "EventTime")


class EventTypeOptions(TreeEditor):

    save_on_top = True
    list_display = ['actions_column', 'indented_short_title']

    fieldsets = [
        (None, {
            'fields': ('parent', )
        }),
    ]
    fieldsets += get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [
        (None, {
            'fields': ('slug', )
        }),
    ]

    prepopulated_fields = {
        "slug": ("title_%s" % settings.LANGUAGE_CODE, ),
    }


def add_form_fields(form, modelform):
    for field_name, field in modelform.base_fields.items():
        setattr(form, field_name, field)
        form.fields[field_name] = field


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


class EventTimeLabelOptions(ExtendedModelAdmin):
    save_on_top = True
    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [
        (None, {
            'fields': ('slug', 'sort_order')
        }),
    ]
    prepopulated_fields = {
        "slug": ("title_%s" % settings.LANGUAGE_CODE, ),
    }


class EventForm(forms.ModelForm):
    """
    Event form for administration combines
    * all fields from Event model
    """

    try:
        Event._meta.get_field("venue")
    except models.FieldDoesNotExist:
        pass
    else:
        venue = AutocompleteModelChoiceField(
            required=False,
            label=_("Venue"),
            help_text=_(
                "Please enter a letter to display a list of available venues"
            ),
            app="events",
            qs_function="get_venues",
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
        Event._meta.get_field("organizing_institution")
    except models.FieldDoesNotExist:
        pass
    else:
        organizing_institution = AutocompleteModelChoiceField(
            required=False,
            label=_("Organizing institution"),
            help_text=_(
                "Please enter a letter to display a list of available institutions"
            ),
            app="events",
            qs_function="get_organizing_institutions",
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
        Event._meta.get_field("organizing_person")
    except:
        pass
    else:
        organizing_person = AutocompleteModelChoiceField(
            required=False,
            label=_("Organizing person"),
            help_text=_(
                "Please enter a letter to display a list of available people"
            ),
            app="events",
            qs_function="get_organizing_people",
            display_attr="get_username",
            add_display_attr="get_name_and_email",
            options={
                "minChars": 1,
                "max": 20,
                "mustMatch": 1,
                "highlight": False,
            }
        )

    try:
        Event._meta.get_field("related_events")
    except:
        pass
    else:
        related_events = AutocompleteModelMultipleChoiceField(
            required=False,
            label=_("Related events"),
            help_text=_(
                "Please enter a letter to display a list of available events"
            ),
            app="events",
            qs_function="get_all_events",
            display_attr="get_title",
            options={
                "minChars": 1,
                "max": 20,
                "mustMatch": 1,
                "highlight": False,
            }
        )

    class Meta:
        model = Event

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
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


class EventTime_Inline(ExtendedStackedInline):
    model = EventTime
    extra = 0
    verbose_name = _("Time")
    verbose_name_plural = _("Times")


class EventOptions(ExtendedModelAdmin):
    form = EventForm
    inlines = [EventTime_Inline]
    change_form_template = "extendedadmin/event_change.html"
    save_on_top = True
    list_display = [
        'title', 'get_venue_display', 'get_start_date_string',
        'get_end_date_string', 'event_type', 'status', 'creation_date'
    ]
    list_filter = ('creation_date', 'event_type', 'status')
    search_fields = ['title', 'venue__title', 'venue_title']
    ordering = ('-creation_date', )
    actions = ["publish"]

    def publish(self, request, queryset):
        for ev in queryset:
            ev.status = "published"
            ev.save()

    publish.short_description = _("Publish selected events")

    def get_venue_display(self, obj):
        """this method is just used for display in the admin"""
        user = get_current_user()
        if obj.venue:
            if user.has_perm("institutions.change_institution", obj.venue):
                return u"""<a href="/admin/institutions/institution/%s/" class="content_object">%s</a>""" % (
                    obj.venue._get_pk_val(),
                    obj.venue,
                )
            else:
                return unicode(obj.venue)
        else:
            return obj.venue_title

    get_venue_display.allow_tags = True
    get_venue_display.short_description = _("Venue")

    #@never_cache # doesn't work for class methods with django r11611
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
            'root_path': self.admin_site.root_path,
            'app_label': opts.app_label,
        }
        context.update(extra_context or {})
        return self.render_change_form(
            request, context, form_url=form_url, add=True
        )

    #@never_cache # doesn't work for class methods with django r11611
    @transaction.atomic
    def change_view(self, request, object_id, extra_context=None):
        """Displays the event add/change form and handles event saving."""
        "The 'change' admin view for this model."
        model = self.model
        opts = model._meta

        try:
            obj = self.queryset(request).get(pk=unquote(object_id))
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
            'root_path': self.admin_site.root_path,
            'app_label': opts.app_label,
        }
        context.update(extra_context or {})
        return self.render_change_form(request, context, change=True, obj=obj)

    def save_form(self, request, form, change):
        """
        Given a ModelForm return an unsaved instance. ``change`` is True if
        the object is being changed, and False if it's being added.
        """
        event = super(EventOptions, self).save_form(request, form, change)
        event.save()  # to ensure that creation date is saved
        Address.objects.set_for(
            event,
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
        return event


admin.site.register(EventType, EventTypeOptions)
admin.site.register(EventTimeLabel, EventTimeLabelOptions)
admin.site.register(Event, EventOptions)

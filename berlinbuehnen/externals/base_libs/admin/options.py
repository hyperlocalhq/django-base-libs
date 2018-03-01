# -*- coding: UTF-8 -*-
import re
from django import forms
from django.db import models, transaction
from django.contrib import admin
from django.contrib.admin import helpers
from django.contrib.admin import util
from django.contrib.admin import options
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.forms.formsets import all_valid
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db.models.fields import FieldDoesNotExist

try:
    from django.utils.encoding import force_text
except:
    from django.utils.encoding import force_unicode as force_text

from base_libs.models.base_libs_settings import MARKUP_PLAIN_TEXT
from base_libs.models.base_libs_settings import MARKUP_HTML_WYSIWYG
from base_libs.models.base_libs_settings import MARKUP_RAW_HTML
from base_libs.models.fields import ExtendedTextField

### Guerilla patches for nested fieldsets


def flatten_fieldsets(fieldsets):
    """Returns a list of field names from an admin fieldsets structure."""
    field_names = []
    for name, opts in fieldsets:
        for field in opts['fields']:
            if isinstance(field, (tuple, list)):
                if len(field)==2 and isinstance(field[1], dict):
                    # it's a nested fieldset
                    field_names.extend(flatten_fieldsets((field,)))
                else:
                    # it's a tuple of field names
                    field_names.extend(field)
            else:
                # it's a field name
                field_names.append(field)
    return field_names

options.flatten_fieldsets = util.flatten_fieldsets = flatten_fieldsets



class Fieldset(object):
    is_fieldset = True
    def __init__(self, form, name=None, readonly_fields=(), fields=(), classes=(), description=None, model_admin=None, level=0):
        self.form = form
        self.name, self.fields = name, fields
        self.classes = u' '.join(classes)
        self.description = description
        self.model_admin = model_admin
        self.readonly_fields = readonly_fields
        self.level = level

    def _media(self):
        if 'collapse' in self.classes:
            js = []
            return forms.Media(js=['%s%s' % (settings.ADMIN_MEDIA_PREFIX, url) for url in js])
            #return forms.Media(js=['%sjs/admin/CollapsedFieldsets.js' % settings.ADMIN_MEDIA_PREFIX])
        return forms.Media()
    media = property(_media)

    def __iter__(self):
        for field in self.fields:
            if len(field)==2 and isinstance(field[1], dict):
                # nested fieldset
                yield Fieldset(self.form,
                    name=field[0],
                    fields=field[1].get("fields", ()),
                    classes=field[1].get("classes", ()),
                    description=field[1].get("description", ()),
                    readonly_fields=self.readonly_fields,
                    model_admin=self.model_admin,
                    level=self.level + 1,
                    )
            else:
                # field name or a tuple of field names
                yield helpers.Fieldline(self.form, field, self.readonly_fields, model_admin=self.model_admin)
                
helpers.Fieldset = Fieldset


class InlineFieldset(Fieldset):
    def __init__(self, formset, *args, **kwargs):
        self.formset = formset
        super(InlineFieldset, self).__init__(*args, **kwargs)
        
    def __iter__(self):
        fk = getattr(self.formset, "fk", None)
        for field in self.fields:
            if fk and fk.name == field:
                continue
            if len(field)==2 and isinstance(field[1], dict):
                # nested fieldset
                yield Fieldset(self.form,
                    name=field[0],
                    fields=field[1].get("fields", ()),
                    classes=field[1].get("classes", ()),
                    description=field[1].get("description", ()),
                    readonly_fields=self.readonly_fields,
                    model_admin=self.model_admin,
                    level=self.level + 1,
                    )
            else:
                # field name or a tuple of field names
                yield helpers.Fieldline(self.form, field, self.readonly_fields,
                model_admin=self.model_admin)

helpers.InlineFieldset = InlineFieldset


def _declared_fieldsets(self):
    """ overriden to handle additional <<whatever>>_markup_type field!!! """
    def attach_markup_type(model, fieldsets):
        """ Goes through all fields and adds *_markup_type fields """
        
        def traverse_fieldsets(fieldsets):
            new_fieldsets = []
            for name, opts in fieldsets:
                opts['fields'] = traverse_fields(opts['fields'])
                new_fieldsets.append((name, opts))
            return new_fieldsets
            
        def traverse_fields(fields):
            new_fields = []
            for field in fields:
                if isinstance(field, (tuple, list)):
                    if len(field)==2 and isinstance(field[1], dict):
                        # it's a nested fieldset
                        new_fields.extend(traverse_fieldsets((field,)))
                    else:
                        # it's a tuple of field names
                        new_fields.extend(traverse_fields(field))
                else:
                    # it's a field name
                    try:
                        f = model._meta.get_field(field)
                    except FieldDoesNotExist: # allow readonly methods instead of fields
                        pass
                    else:
                        if isinstance(f, ExtendedTextField):
                            if "%s_markup_type" % field not in fields:
                                new_fields.append("%s_markup_type" % field)
                    new_fields.append(field)
            return new_fields
            
        return traverse_fieldsets(fieldsets)
        
    if self.fieldsets:
        return attach_markup_type(self.model, self.fieldsets)
        
    elif self.fields:
        return [(None, {'fields': self.fields})]
    return None


class MarkupTypeOptions(object):
    # default allowed markup types for TextFields in the Admin ...
    allowed_markup_admin = [
        MARKUP_PLAIN_TEXT,
        MARKUP_RAW_HTML,
        MARKUP_HTML_WYSIWYG,
        #MARKUP_MARKDOWN
    ]

    def formfield_for_choice_field(self, db_field, request=None, **kwargs):
        # catch markup type fields
        if re.search('markup_type$', db_field.name):
            new_choices = ()
            for choice in db_field.choices:
                if choice[0] in self.allowed_markup_admin:
                    new_choices += (choice,)
            kwargs['choices'] = new_choices
            if len(new_choices) > 0:
                kwargs['default'] = new_choices[-1][0]
        return super(MarkupTypeOptions, self).formfield_for_choice_field(db_field, request, **kwargs)

    def formfield_for_dbfield(self, db_field, **kwargs):
        # catch markup type fields here and modify the widget to assign
        # a special css class. we need that for javascript stuff alter....
        field = super(MarkupTypeOptions, self).formfield_for_dbfield(db_field, **kwargs)
        if re.search('markup_type$', db_field.name):
            field.widget.attrs['class'] = "markupType"
        return field


class ExtendedStackedInline(MarkupTypeOptions, admin.StackedInline):
    classes = ("grp-collapse grp-closed",)
    declared_fieldsets = property(_declared_fieldsets)


class ExtendedTabularInline(MarkupTypeOptions, admin.TabularInline):
    classes = ("grp-collapse grp-closed",)
    declared_fieldsets = property(_declared_fieldsets)


class ExtendedModelAdmin(MarkupTypeOptions, admin.ModelAdmin):
    """
    overwritten to handle custom buttons for the admin 
    add and change view and other stuff
    """
    # additional save buttons
    additional_buttons = []
    
    @classmethod
    def get_modified_fieldsets(cls, additional_fields, prefixed=True):
        """ 
        returns the fieldsets with some added fields provided by
        "additional_fields" as a tuple. 
        """
        fields = cls.fieldsets[0][1]['fields']
        if prefixed:
            new_fields = additional_fields + fields
        else:
            new_fields = fields + additional_fields
    
        return [(cls.fieldsets[0][0],
                 {'fields': new_fields,
                  'classes': cls.fieldsets[0][1]['classes']
                 }),]
    
    """
    this is a callback to be overwritten. 
    It gets the additional buttons to be displayed.
    The action for the buttons is handled by the
    handle_buttons_action_callback method (see below).
     
    The additional_buttons parameter is a list of tuples
    like this:
    
    [(<<button_name>>, <<button_text>>), ...]
    
    """
    def add_get_additional_buttons_callback(self):
        return []
    
    def add_handle_button_action_callback(self, action, obj):
        pass

    def change_get_additional_buttons_callback(self):
        return []
    
    def change_handle_button_action_callback(self, action, obj):
        pass
    
    # overwritten
    def __init__(self, model, admin_site):
        super(ExtendedModelAdmin, self).__init__(model, admin_site)
        self.add_additional_buttons = self.add_get_additional_buttons_callback()
        self.change_additional_buttons = self.change_get_additional_buttons_callback()
    
    # overwritten
    @options.csrf_protect_m
    @transaction.atomic
    def add_view(self, request, form_url='', extra_context=None):
        """
        The 'add' admin view for this model.
        unfortunately, we have to add the whole django
        code from contrib.admin.options.add_view. If that
        method changes in the django code, it should be 
        updated here!!!

        overwritten add_view. The default behaviour is extended by
        simple additional button actions.
        """
        if not extra_context:
            extra_context = {}
        extra_context['additional_buttons'] = self.add_additional_buttons
                
        # HERE THE PART TAKEN FROM DJANGO STARTS
        model = self.model
        opts = model._meta

        if not self.has_add_permission(request):
            raise PermissionDenied

        ModelForm = self.get_form(request)
        formsets = []
        inline_instances = self.get_inline_instances(request, None)
        if request.method == 'POST':
            form = ModelForm(request.POST, request.FILES)
            if form.is_valid():
                new_object = self.save_form(request, form, change=False)
                form_validated = True
            else:
                new_object = self.model()
                form_validated = False
            prefixes = {}
            for FormSet, inline in zip(self.get_formsets(request), inline_instances):
                prefix = FormSet.get_default_prefix()
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1 or not prefix:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])
                formset = FormSet(data=request.POST, files=request.FILES,
                                  instance=new_object,
                                  save_as_new="_saveasnew" in request.POST,
                                  prefix=prefix, queryset=inline.get_queryset(request))
                formsets.append(formset)
            if all_valid(formsets) and form_validated:
                self.save_model(request, new_object, form, False)
                self.save_related(request, form, formsets, False)
                self.log_addition(request, new_object)
                """ HERE THE CUSTOM CODE BEGINS"""
                # action handling has to be done after the usual form processing!!!
                if self.add_additional_buttons:
                    action = None
                    for key, value in self.add_additional_buttons:
                        if request.POST.has_key(key):
                            action = key
                            break
                    if action:
                        if new_object:  
                            self.add_handle_button_action_callback(action, new_object)
                """ HERE THE CUSTOM CODE ENDS"""
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
            for FormSet, inline in zip(self.get_formsets(request), inline_instances):
                prefix = FormSet.get_default_prefix()
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1 or not prefix:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])
                formset = FormSet(instance=self.model(), prefix=prefix,
                                  queryset=inline.get_queryset(request))
                formsets.append(formset)

        adminForm = helpers.AdminForm(form, list(self.get_fieldsets(request)),
            self.get_prepopulated_fields(request),
            self.get_readonly_fields(request),
            model_admin=self)
        media = self.media + adminForm.media

        inline_admin_formsets = []
        for inline, formset in zip(inline_instances, formsets):
            fieldsets = list(inline.get_fieldsets(request))
            readonly = list(inline.get_readonly_fields(request))
            prepopulated = dict(inline.get_prepopulated_fields(request))
            inline_admin_formset = helpers.InlineAdminFormSet(inline, formset,
                fieldsets, prepopulated, readonly, model_admin=self)
            inline_admin_formsets.append(inline_admin_formset)
            media = media + inline_admin_formset.media

        context = {
            'title': _('Add %s') % force_text(opts.verbose_name),
            'adminform': adminForm,
            'is_popup': "_popup" in request.REQUEST,
            'media': mark_safe(media),
            'inline_admin_formsets': inline_admin_formsets,
            'errors': helpers.AdminErrorList(form, formsets),
            'app_label': opts.app_label,
        }
        context.update(extra_context or {})
        return self.render_change_form(request, context, form_url=form_url, add=True)
    
    # overwritten    
    @options.csrf_protect_m
    @transaction.atomic
    def change_view(self, request, object_id, form_url='', extra_context=None):
        """
        overwritten change_view. The default behaviour is extended by
        simple additional button actions.
        """
        # add the additional buttons ...
        if not extra_context:
            extra_context = {}
        extra_context['additional_buttons'] = self.change_additional_buttons
        result = super(ExtendedModelAdmin, self).change_view(request, object_id, form_url, extra_context)

        # action ahandling has to be done after the usual form processing!!!
        if request.POST:
            if self.change_additional_buttons:
                action = None
                for key, value in self.change_additional_buttons:
                    if request.POST.has_key(key):
                        action = key
                        break
                if action:
                    obj = self.model._default_manager.get(pk=object_id)
                    if obj:  
                        response = self.change_handle_button_action_callback(action, obj)
                        if response:
                            result = response
        return result

    declared_fieldsets = property(_declared_fieldsets)

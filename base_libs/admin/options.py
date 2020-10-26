# -*- coding: UTF-8 -*-
import re
from copy import deepcopy

from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.admin import helpers
from django.contrib.admin import options

try:
    from django.contrib.admin import utils
except:
    from django.contrib.admin import util as utils

from django.core.exceptions import PermissionDenied
from django.db import models, transaction
from django.db.models.fields import FieldDoesNotExist
from django.forms.formsets import all_valid
from django.forms.models import BaseModelForm
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

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
        for field in opts["fields"]:
            if isinstance(field, (tuple, list)):
                if len(field) == 2 and isinstance(field[1], dict):
                    # it's a nested fieldset
                    field_names.extend(flatten_fieldsets((field,)))
                else:
                    # it's a tuple of field names
                    field_names.extend(field)
            else:
                # it's a field name
                field_names.append(field)
    return field_names


options.flatten_fieldsets = utils.flatten_fieldsets = flatten_fieldsets


def patch_validation():
    from django.core.exceptions import ImproperlyConfigured
    from django.contrib.admin.options import HORIZONTAL, VERTICAL
    from django.contrib.admin import validation
    from django.contrib.admin.validation import check_isseq, get_field, check_isdict

    def validate_base(cls, model):
        opts = model._meta

        # raw_id_fields
        if hasattr(cls, "raw_id_fields"):
            check_isseq(cls, "raw_id_fields", cls.raw_id_fields)
            for idx, field in enumerate(cls.raw_id_fields):
                f = get_field(cls, model, opts, "raw_id_fields", field)
                if not isinstance(f, (models.ForeignKey, models.ManyToManyField)):
                    raise ImproperlyConfigured(
                        "'%s.raw_id_fields[%d]', '%s' must "
                        "be either a ForeignKey or ManyToManyField."
                        % (cls.__name__, idx, field)
                    )

        # fields
        if cls.fields:  # default value is None
            check_isseq(cls, "fields", cls.fields)
            for field in cls.fields:
                if field in cls.readonly_fields:
                    # Stuff can be put in fields that isn't actually a model field
                    # if it's in readonly_fields, readonly_fields will handle the
                    # validation of such things.
                    continue
                check_formfield(cls, model, opts, "fields", field)
                try:
                    f = opts.get_field(field)
                except models.FieldDoesNotExist:
                    # If we can't find a field on the model that matches,
                    # it could be an extra field on the form.
                    continue
                if (
                    isinstance(f, models.ManyToManyField)
                    and not f.rel.through._meta.auto_created
                ):
                    raise ImproperlyConfigured(
                        "'%s.fields' can't include the ManyToManyField "
                        "field '%s' because '%s' manually specifies "
                        "a 'through' model." % (cls.__name__, field, field)
                    )
            if cls.fieldsets:
                raise ImproperlyConfigured(
                    "Both fieldsets and fields are specified in %s." % cls.__name__
                )
            if len(cls.fields) > len(set(cls.fields)):
                raise ImproperlyConfigured(
                    "There are duplicate field(s) in %s.fields" % cls.__name__
                )
        """
        # fieldsets
        if cls.fieldsets: # default value is None
            check_isseq(cls, 'fieldsets', cls.fieldsets)
            for idx, fieldset in enumerate(cls.fieldsets):
                check_isseq(cls, 'fieldsets[%d]' % idx, fieldset)
                if len(fieldset) != 2:
                    raise ImproperlyConfigured("'%s.fieldsets[%d]' does not "
                            "have exactly two elements." % (cls.__name__, idx))
                check_isdict(cls, 'fieldsets[%d][1]' % idx, fieldset[1])
                if 'fields' not in fieldset[1]:
                    raise ImproperlyConfigured("'fields' key is required in "
                            "%s.fieldsets[%d][1] field options dict."
                            % (cls.__name__, idx))
                for fields in fieldset[1]['fields']:
                    # The entry in fields might be a tuple. If it is a standalone
                    # field, make it into a tuple to make processing easier.
                    if type(fields) != tuple:
                        fields = (fields,)
                    for field in fields:
                        if field in cls.readonly_fields:
                            # Stuff can be put in fields that isn't actually a
                            # model field if it's in readonly_fields,
                            # readonly_fields will handle the validation of such
                            # things.
                            continue
                        check_formfield(cls, model, opts, "fieldsets[%d][1]['fields']" % idx, field)
                        try:
                            f = opts.get_field(field)
                            if isinstance(f, models.ManyToManyField) and not f.rel.through._meta.auto_created:
                                raise ImproperlyConfigured("'%s.fieldsets[%d][1]['fields']' "
                                    "can't include the ManyToManyField field '%s' because "
                                    "'%s' manually specifies a 'through' model." % (
                                        cls.__name__, idx, field, field))
                        except models.FieldDoesNotExist:
                            # If we can't find a field on the model that matches,
                            # it could be an extra field on the form.
                            pass
            flattened_fieldsets = flatten_fieldsets(cls.fieldsets)
            if len(flattened_fieldsets) > len(set(flattened_fieldsets)):
                raise ImproperlyConfigured('There are duplicate field(s) in %s.fieldsets' % cls.__name__)
        """
        # exclude
        if cls.exclude:  # default value is None
            check_isseq(cls, "exclude", cls.exclude)
            for field in cls.exclude:
                check_formfield(cls, model, opts, "exclude", field)
                try:
                    f = opts.get_field(field)
                except models.FieldDoesNotExist:
                    # If we can't find a field on the model that matches,
                    # it could be an extra field on the form.
                    continue
            if len(cls.exclude) > len(set(cls.exclude)):
                raise ImproperlyConfigured(
                    "There are duplicate field(s) in %s.exclude" % cls.__name__
                )

        # form
        if hasattr(cls, "form") and not issubclass(cls.form, BaseModelForm):
            raise ImproperlyConfigured(
                "%s.form does not inherit from " "BaseModelForm." % cls.__name__
            )

        # filter_vertical
        if hasattr(cls, "filter_vertical"):
            check_isseq(cls, "filter_vertical", cls.filter_vertical)
            for idx, field in enumerate(cls.filter_vertical):
                f = get_field(cls, model, opts, "filter_vertical", field)
                if not isinstance(f, models.ManyToManyField):
                    raise ImproperlyConfigured(
                        "'%s.filter_vertical[%d]' must be "
                        "a ManyToManyField." % (cls.__name__, idx)
                    )

        # filter_horizontal
        if hasattr(cls, "filter_horizontal"):
            check_isseq(cls, "filter_horizontal", cls.filter_horizontal)
            for idx, field in enumerate(cls.filter_horizontal):
                f = get_field(cls, model, opts, "filter_horizontal", field)
                if not isinstance(f, models.ManyToManyField):
                    raise ImproperlyConfigured(
                        "'%s.filter_horizontal[%d]' must be "
                        "a ManyToManyField." % (cls.__name__, idx)
                    )

        # radio_fields
        if hasattr(cls, "radio_fields"):
            check_isdict(cls, "radio_fields", cls.radio_fields)
            for field, val in cls.radio_fields.items():
                f = get_field(cls, model, opts, "radio_fields", field)
                if not (isinstance(f, models.ForeignKey) or f.choices):
                    raise ImproperlyConfigured(
                        "'%s.radio_fields['%s']' "
                        "is neither an instance of ForeignKey nor does "
                        "have choices set." % (cls.__name__, field)
                    )
                if not val in (HORIZONTAL, VERTICAL):
                    raise ImproperlyConfigured(
                        "'%s.radio_fields['%s']' "
                        "is neither admin.HORIZONTAL nor admin.VERTICAL."
                        % (cls.__name__, field)
                    )

        # prepopulated_fields
        if hasattr(cls, "prepopulated_fields"):
            check_isdict(cls, "prepopulated_fields", cls.prepopulated_fields)
            for field, val in cls.prepopulated_fields.items():
                f = get_field(cls, model, opts, "prepopulated_fields", field)
                if isinstance(
                    f, (models.DateTimeField, models.ForeignKey, models.ManyToManyField)
                ):
                    raise ImproperlyConfigured(
                        "'%s.prepopulated_fields['%s']' "
                        "is either a DateTimeField, ForeignKey or "
                        "ManyToManyField. This isn't allowed." % (cls.__name__, field)
                    )
                check_isseq(cls, "prepopulated_fields['%s']" % field, val)
                for idx, f in enumerate(val):
                    get_field(
                        cls,
                        model,
                        opts,
                        "prepopulated_fields['%s'][%d]" % (field, idx),
                        f,
                    )

    validation.validate_base = validate_base


def patch_checks():
    from django.contrib.admin import checks

    def _check_fieldsets(self, obj):
        return []

    checks.BaseModelAdminChecks._check_fieldsets = _check_fieldsets


try:
    from django.contrib.admin import validation
except:
    patch_checks()
else:
    patch_validation()


class Fieldset(object):
    is_fieldset = True

    def __init__(
        self,
        form,
        name=None,
        readonly_fields=(),
        fields=(),
        classes=(),
        description=None,
        model_admin=None,
        level=0,
    ):
        self.form = form
        self.name, self.fields = name, fields
        self.classes = u" ".join(classes)
        self.description = description
        self.model_admin = model_admin
        self.readonly_fields = readonly_fields
        self.level = level

    def _media(self):
        if "collapse" in self.classes:
            js = []
            return forms.Media(
                js=["%s%s" % (settings.ADMIN_MEDIA_PREFIX, url) for url in js]
            )
            # return forms.Media(js=['%sjs/admin/CollapsedFieldsets.js' % settings.ADMIN_MEDIA_PREFIX])
        return forms.Media()

    media = property(_media)

    def __iter__(self):
        for field in self.fields:
            if len(field) == 2 and isinstance(field[1], dict):
                # nested fieldset
                yield Fieldset(
                    self.form,
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
                yield helpers.Fieldline(
                    self.form, field, self.readonly_fields, model_admin=self.model_admin
                )


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
            if len(field) == 2 and isinstance(field[1], dict):
                # nested fieldset
                yield Fieldset(
                    self.form,
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
                yield helpers.Fieldline(
                    self.form, field, self.readonly_fields, model_admin=self.model_admin
                )


helpers.InlineFieldset = InlineFieldset


def nested_fieldsets_with_markup_types(
    model_admin, fieldsets=None, request=None, obj=None
):
    """ overriden to handle additional <<whatever>>_markup_type field!!! """

    def traverse_fieldsets(model, fieldsets):
        new_fieldsets = []
        for name, opts in fieldsets:
            new_opts = deepcopy(opts)
            new_opts["fields"] = traverse_fields(model, opts["fields"])
            new_fieldsets.append((name, new_opts))
        return new_fieldsets

    def traverse_fields(model, fields):
        new_fields = []
        for field in fields:
            if isinstance(field, (tuple, list)):
                if len(field) == 2 and isinstance(field[1], dict):
                    # it's a nested fieldset
                    new_fields.extend(traverse_fieldsets(model, (field,)))
                else:
                    # it's a tuple of field names
                    new_fields.extend(traverse_fields(model, field))
            else:
                # it's a field name
                try:
                    f = model._meta.get_field(field)
                except FieldDoesNotExist:  # allow readonly methods instead of fields
                    pass
                else:
                    if isinstance(f, ExtendedTextField):
                        if "%s_markup_type" % field not in fields:
                            new_fields.append("%s_markup_type" % field)
                new_fields.append(field)
        return new_fields

    def attach_markup_type(model, fieldsets):
        """ Goes through all fields and adds *_markup_type fields """
        return traverse_fieldsets(model, fieldsets)

    if fieldsets:
        return attach_markup_type(model_admin.model, fieldsets)

    return None


class MarkupTypeOptions(object):
    # default allowed markup types for TextFields in the Admin ...
    allowed_markup_admin = getattr(settings, "ALLOWED_MARKUP_TYPES", [
        MARKUP_PLAIN_TEXT,
        MARKUP_RAW_HTML,
        MARKUP_HTML_WYSIWYG,
        # MARKUP_MARKDOWN
    ])

    def get_fieldsets(self, request, obj=None):
        """
        Hook for specifying fieldsets.
        """
        fieldsets = self.fieldsets
        if not fieldsets:
            fieldsets = [(None, {"fields": self.get_fields(request, obj)})]

        return nested_fieldsets_with_markup_types(self, fieldsets, request, obj)

    def formfield_for_choice_field(self, db_field, request=None, **kwargs):
        # catch markup type fields
        if re.search("markup_type$", db_field.name):
            new_choices = ()
            for choice in db_field.choices:
                if choice[0] in self.allowed_markup_admin:
                    new_choices += (choice,)
            kwargs["choices"] = new_choices
            if len(new_choices) > 0:
                kwargs["default"] = new_choices[-1][0]
        return super(MarkupTypeOptions, self).formfield_for_choice_field(
            db_field, request, **kwargs
        )

    def formfield_for_dbfield(self, db_field, **kwargs):
        # catch markup type fields here and modify the widget to assign
        # a special css class. we need that for javascript stuff alter....
        field = super(MarkupTypeOptions, self).formfield_for_dbfield(db_field, **kwargs)
        if re.search("markup_type$", db_field.name):
            field.widget.attrs["class"] = "markupType"
        return field


class ExtendedStackedInline(MarkupTypeOptions, admin.StackedInline):
    classes = ("grp-collapse grp-closed",)


class ExtendedTabularInline(MarkupTypeOptions, admin.TabularInline):
    classes = ("grp-collapse grp-closed",)


class ExtendedModelAdmin(MarkupTypeOptions, admin.ModelAdmin):
    """
    overwritten to handle custom buttons for the admin 
    add and change view and other stuff
    """

    @classmethod
    def get_modified_fieldsets(cls, additional_fields, prefixed=True):
        """ 
        returns the fieldsets with some added fields provided by
        "additional_fields" as a tuple. 
        """
        fields = cls.fieldsets[0][1]["fields"]
        if prefixed:
            new_fields = additional_fields + fields
        else:
            new_fields = fields + additional_fields

        return [
            (
                cls.fieldsets[0][0],
                {"fields": new_fields, "classes": cls.fieldsets[0][1]["classes"]},
            ),
        ]

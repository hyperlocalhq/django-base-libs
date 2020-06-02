# -*- coding: UTF-8 -*-
"""
overridden newforms.forms. This id done, because we need a 
custom "label_tag" for template output and other customizations
"""

from django import forms
from django.forms.forms import BoundField as FormsBoundField
from django.forms.forms import DeclarativeFieldsMetaclass

# from django.utils.datastructures import SortedDict
from django.forms.utils import flatatt
from django.template.loader import render_to_string
from django.utils.html import escape


# from django.forms.fields import *


class BaseForm(forms.BaseForm):
    # This is the main implementation of all the Form logic. Note that this
    # class is different than Form. See the comments by the Form class for more
    # information. Any improvements to the form API should be made to *this*
    # class, not to the Form class.

    def __iter__(self):
        for name, field in self.fields.items():
            yield BoundField(self, field, name)

    def __getitem__(self, name):
        """Returns a BoundField with the given name."""
        try:
            field = self.fields[name]
        except KeyError:
            raise KeyError("Key %r not found in Form" % name)
        return BoundField(self, field, name)


class Form(BaseForm):
    """A collection of Fields, plus their associated data."""

    # This is a separate class from BaseForm in order to abstract the way
    # self.fields is specified. This class (Form) is the one that does the
    # fancy metaclass stuff purely for the semantic sugar -- it allows one
    # to define a form using declarative syntax.
    # BaseForm itself has no way of designating self.fields.
    __metaclass__ = DeclarativeFieldsMetaclass


class BoundField(FormsBoundField):
    """A Field plus data"""

    """
    def __init__(self, *args, **kwargs):
        super(BoundField, self).__init__(*args, **kwargs)
    """

    def label_tag(self, contents=None, attrs=None, label_suffix=None):
        contents = contents or escape(self.label)
        widget = self.field.widget
        id_ = widget.attrs.get("id") or self.auto_id
        if id_:
            attrs = attrs and flatatt(attrs) or ""
            context = {
                "attrs": attrs,
                "field_id": widget.id_for_label(id_),
                "field_label": contents,
                "is_required": self.field.required,
            }
            contents = render_to_string("utils/label_tag.html", context)
        return contents

    def inner_label_tag(self, contents=None, attrs=None):
        contents = contents or escape(self.label)
        widget = self.field.widget
        id_ = widget.attrs.get("id") or self.auto_id
        if id_:
            attrs = attrs and flatatt(attrs) or ""
            context = {
                "attrs": attrs,
                "field_id": widget.id_for_label(id_),
                "field_label": contents,
                "is_required": self.field.required,
            }
            contents = render_to_string("utils/inner_label_tag.html", context)
        return contents

    def error_tag(self, contents=None, attrs=None):
        contents = contents or self.errors
        widget = self.field.widget
        id_ = widget.attrs.get("id") or self.auto_id
        attrs = attrs and flatatt(attrs) or ""
        context = {
            "field_id": widget.id_for_label(id_),
            "field_label": self.label,
            "attrs": attrs,
            "field_errors": contents,
        }
        contents = render_to_string("utils/error_tag.html", context)
        return contents

    def help_text_tag(self, contents=None, attrs=None):
        contents = contents or escape(self.help_text)
        widget = self.field.widget
        id_ = widget.attrs.get("id") or self.auto_id

        attrs = attrs and flatatt(attrs) or ""
        context = {
            "field_id": widget.id_for_label(id_),
            "attrs": attrs,
            "field_help_text": contents,
        }
        contents = render_to_string("utils/help_text_tag.html", context)
        return contents

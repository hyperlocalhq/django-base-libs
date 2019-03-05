# -*- coding: utf-8 -*-

from itertools import chain

from django import forms
from django.forms.models import BaseInlineFormSet
from django.utils.translation import ugettext
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape

from crispy_forms import layout


class PrimarySubmit(layout.Submit):
    field_classes = "btn btn-lg btn-primary"


class SecondarySubmit(layout.Submit):
    field_classes = "btn btn-lg btn-info"


class SecondaryButton(layout.Button):
    field_classes = "btn btn-lg btn-info"


class InlineFormSet(BaseInlineFormSet):
    """ Inline formset which accepts initial values for unsaved models """

    def __init__(
        self,
        data=None,
        files=None,
        instance=None,
        save_as_new=False,
        prefix=None,
        queryset=None,
        initial=None
    ):
        if initial is None:
            initial = []
        self._initial = initial
        super(InlineFormSet, self).__init__(
            data, files, instance, save_as_new, prefix, queryset
        )

    def _construct_form(self, i, **kwargs):
        """
        Instantiates and returns the i-th form instance in a formset.
        """
        defaults = {'auto_id': self.auto_id, 'prefix': self.add_prefix(i)}
        if self.is_bound:
            defaults['data'] = self.data
            defaults['files'] = self.files
        if self._initial:
            try:
                defaults['initial'] = self._initial[i]
            except IndexError:
                pass
        # Allow extra forms to be empty.
        if i >= self.initial_form_count():
            defaults['empty_permitted'] = True
        defaults.update(kwargs)
        form = self.form(**defaults)
        self.add_fields(form, i)
        return form

    def initial_form_count(self):
        """Returns the number of forms that are required in this FormSet."""
        if not (self.data or self.files):
            return len(self._initial)
        return super(InlineFormSet, self).initial_form_count()


class SplitDateTimeWidget(forms.SplitDateTimeWidget):
    def format_output(self, rendered_widgets):
        return """
            <div class="row row-sm">
                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">
                    <div class="form-group">
                        <label>%s</label>
                        <div class="input-group">%s</div>
                    </div>
                </div>
                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">
                    <div class="form-group">
                        <label>%s</label>
                        <div class="input-group">%s</div>
                    </div>
                </div>
            </div>""" % (
            ugettext("Date"),
            rendered_widgets[0].replace('/>', ' placeholder="dd.mm.yyyy" />'),
            ugettext("Time"),
            rendered_widgets[1].replace('/>', ' placeholder="00:00" />'),
        )


class ModelMultipleChoiceTreeField(forms.ModelMultipleChoiceField):
    widget = forms.CheckboxSelectMultiple

    def label_from_instance(self, obj):
        return obj


class ModelChoiceTreeField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj

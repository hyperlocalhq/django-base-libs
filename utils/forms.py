# -*- coding: utf-8 -*-

from django import forms
from django.forms.models import BaseInlineFormSet
from django.utils.translation import ugettext

from crispy_forms import layout

class SecondarySubmit(layout.Submit):
    field_classes = "btn"

class InlineFormSet(BaseInlineFormSet):
    """ Inline formset which accepts initial values for unsaved models """
    def __init__(self, data=None, files=None, instance=None, save_as_new=False, prefix=None, queryset=None, initial=[]):
        self._initial = initial
        super(InlineFormSet, self).__init__(data, files, instance, save_as_new, prefix, queryset)
        
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
            <div class="row">
                <div class="clearfix control-group">
                    <label>%s</label>
                    %s
                </div>
                <div class="clearfix control-group">
                    <label>%s</label>
                    %s
                </div>
            </div>""" % (
                ugettext("Date"),
                rendered_widgets[0],
                ugettext("Time"),
                rendered_widgets[1],
                )


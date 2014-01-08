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
            <div class="row cols-2">
                <div>
                    <div class="clearfix control-group">
                        <label>%s</label>
                        <div class="controls">%s</div>
                    </div>
                </div>
                <div>
                    <div class="clearfix control-group">
                        <label>%s</label>
                        <div class="controls">%s</div>
                    </div>
                </div>
            </div>""" % (
                ugettext("Date"),
                rendered_widgets[0].replace('/>', ' placeholder="dd.mm.yyyy" />'),
                ugettext("Time"),
                rendered_widgets[1].replace('/>', ' placeholder="00:00" />'),
                )

class CheckboxSelectMultipleTree(forms.CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<ul class="tree">']
        # Normalize to strings
        str_values = set([force_unicode(v) for v in value])
        
        level = 0
        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            open_ul = False
            close_uls = 0
            if level < option_label.level:
                open_ul = True
            elif level > option_label.level:
                close_uls = level - option_label.level
            level = option_label.level
                
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = u' for="%s"' % final_attrs['id']
            else:
                label_for = ''

            cb = forms.CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            rendered_cb = cb.render(name, force_unicode(option_value))
            option_label_unicode = conditional_escape(force_unicode(option_label))
            
            if open_ul:
                output.append(u'<ul>')
            elif close_uls:
                output.append(u'</ul></li>' * close_uls)
            elif i > 0:
                output.append(u'</li>')
            output.append(u'<li class="level-%s"><label%s>%s %s</label>' % (level, label_for, rendered_cb, option_label_unicode))
        if level > 0:
            output.append(u'</ul></li>' * level)
        else:
            output.append(u'</li>')
        output.append(u'</ul>')
        return mark_safe(u'\n'.join(output))

class ModelMultipleChoiceTreeField(forms.ModelMultipleChoiceField):
    widget = CheckboxSelectMultipleTree
    def label_from_instance(self, obj):
        return obj

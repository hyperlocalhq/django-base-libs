from django import forms

from base_libs.forms.fields import PlainTextFormField

class TemplateForm(forms.Form):
    content = PlainTextFormField()

from django import template
from django.contrib.admin.templatetags.admin_modify import submit_row

register = template.Library()

def extended_submit_row(context):
    _submit_row = submit_row(context) 
    additional_buttons = context.get('additional_buttons', None)
    _submit_row['additional_buttons'] = additional_buttons
    return _submit_row
    
extended_submit_row = register.inclusion_tag('admin/extended_submit_line.html', takes_context=True)(extended_submit_row)
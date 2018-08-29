# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from base_libs.models.admin import get_admin_lang_section

from jetson.apps.contact_form.models import ContactFormCategory

class ContactFormCategoryOptions(admin.ModelAdmin):
    list_display = ['title', 'slug', 'sort_order', 'get_site']
    save_on_top = True
    fieldsets = [(None, {'fields': ('site',)}),]
    fieldsets += get_admin_lang_section(None, ['title'])
    fieldsets += [
        (None, {'fields': ('slug',)}),
        (None, {'fields': ('recipients', 'recipient_emails',)}),
        (None, {'fields': ('auto_answer_template', 'sort_order',)}),
    ]
    filter_horizontal = ('recipients',)
    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}

admin.site.register(ContactFormCategory, ContactFormCategoryOptions)


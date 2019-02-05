# -*- coding: UTF-8 -*-

from jetson.apps.marketplace.admin import *
from django.utils.translation import ugettext_lazy as _


class ExtendedJobOfferAdmin(JobOfferAdmin):
    list_display = ['position', 'job_type', 'get_content_provider', 'is_commercial', 'status', 'creation_date', 'talent_in_berlin']
    list_filter = ['job_type', 'is_commercial', 'status']

    def get_content_provider(self, obj):
        content_provider = obj.get_content_provider()
        if content_provider:
            return content_provider.title
        return ""
    get_content_provider.short_description = _("Content Provider")

admin.site.unregister(JobOffer)
admin.site.register(JobOffer, ExtendedJobOfferAdmin)

# -*- coding: UTF-8 -*-

from jetson.apps.marketplace.admin import *

class ExtendedJobOfferAdmin(JobOfferAdmin):
    list_display = ['position', 'job_type', 'status', 'creation_date', 'talent_in_berlin']

admin.site.unregister(JobOffer)
admin.site.register(JobOffer, ExtendedJobOfferAdmin)

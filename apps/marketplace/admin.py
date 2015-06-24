# -*- coding: UTF-8 -*-

from jetson.apps.marketplace.admin import *

class ExtendedJobOfferOptions(JobOfferOptions):
    list_display = ['position', 'job_type', 'status', 'creation_date', 'talent_in_berlin']

admin.site.unregister(JobOffer)
admin.site.register(JobOffer, ExtendedJobOfferOptions)

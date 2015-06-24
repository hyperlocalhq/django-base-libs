# -*- coding: UTF-8 -*-

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class ContactFormApphook(CMSApp):
    name = _("Contact Form")
    urls = ["jetson.apps.contact_form.urls"]

apphook_pool.register(ContactFormApphook)

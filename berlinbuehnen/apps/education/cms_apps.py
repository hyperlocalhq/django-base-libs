# -*- coding: UTF-8 -*-

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class EducationalDepartmentsApphook(CMSApp):
    name = _("Educational Departments")
    urls = ["berlinbuehnen.apps.education.urls.departments"]

apphook_pool.register(EducationalDepartmentsApphook)


class EducationalProjectsApphook(CMSApp):
    name = _("Educational Projects")
    urls = ["berlinbuehnen.apps.education.urls.projects"]

apphook_pool.register(EducationalProjectsApphook)

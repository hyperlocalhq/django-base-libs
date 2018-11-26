# -*- coding: UTF-8 -*-
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _


def patch_sites():
    def new_unicode(self):
        return "%s (%s)" % (self.name, self.domain)

    Site.__unicode__ = new_unicode
    Site.verbose_name = _("site")
    Site.verbose_name_plural = _("sites")


patch_sites()

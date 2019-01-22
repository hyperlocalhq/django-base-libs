# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

DirectoryAccess = models.get_model("public_filebrowser", "DirectoryAccess")


class DirectoryAccessOptions(admin.ModelAdmin):
    save_on_top = True
    list_display = ('group', 'accessible_root_link')

    def accessible_root_link(self, obj):
        return """<a href="%(link)s">%(text)s</a>""" % {
            'link': reverse("fb_browse") + "?dir=" + obj.accessible_root.path,
            'text': obj.accessible_root.path,
        }

    accessible_root_link.allow_tags = True


admin.site.register(DirectoryAccess, DirectoryAccessOptions)

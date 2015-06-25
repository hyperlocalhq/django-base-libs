# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

Bookmark = models.get_model("bookmarks", "Bookmark")

class BookmarkOptions(admin.ModelAdmin):
    save_on_top = True
    list_display = ('title', 'url_path', 'creation_date')
    fieldsets = []

admin.site.register(Bookmark, BookmarkOptions)

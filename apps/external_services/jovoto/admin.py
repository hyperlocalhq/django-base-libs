# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib import admin

Idea = models.get_model("jovoto", "Idea")

class IdeaOptions(admin.ModelAdmin):
    list_filter = ('pubdate',)
    list_display = ('name', 'author_username', 'rating', 'get_media0_thumb_image', 'pubdate', 'description')
    save_on_top = True

admin.site.register(Idea, IdeaOptions)


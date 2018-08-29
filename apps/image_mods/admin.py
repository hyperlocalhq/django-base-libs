# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

ImageModificationGroup = models.get_model("image_mods", "ImageModificationGroup")
ImageModification = models.get_model("image_mods", "ImageModification")
ImageCropping = models.get_model("image_mods", "ImageCropping")

import filebrowser.settings as filebrowser_settings
URL_FILEBROWSER_MEDIA = getattr(filebrowser_settings, "FILEBROWSER_DIRECTORY", 'uploads/')

class ImageModificationOptions(admin.ModelAdmin):
    save_on_top = True
    list_filter = ['crop', 'group', 'output_format']
    list_display = ['sysname', 'title', 'width', 'height', 'crop', 'group', 'notes', 'output_format']

    fieldsets = [
        (None, {'fields': ('sysname', 'title', 'group', 'notes')}),
        (_('Dimensions'), {
            'fields': ('width', 'height', 'crop', 'crop_from'),
            'classes': ('grp-collapse grp-open',),
            }),
        (_('Filters'), {
            'fields': ('color', 'brightness', 'contrast', 'sharpness', 'filters'),
            'classes': ('grp-collapse grp-closed',),
            }),
        (_('Masks'), {
            'fields': ('mask', 'frame'),
            'classes': ('grp-collapse grp-closed',),
            }),
        (_('Saving'), {
            'fields': ('output_format', 'quality'),
            'classes': ('grp-collapse grp-open',),
            }),
        ]

class ImageCroppingOptions(admin.ModelAdmin):
    save_on_top = True
    search_fields = ("original",)
    list_filter = ("mods",)
    list_display = ['original', 'coords', 'cropping_size', 'original_size', 'bgcolor', 'mods_list']
    filter_horizontal = ["mods"]
    actions = ["update_versions"]


    fieldsets = [
        (None, {'fields': ('original', 'mods',)}),
        (_('Coordinates'), {
            'fields': ('x1', 'y1', 'x2', 'y2',)
            }),
        (_('Background'), {
            'fields': ('bgcolor',)
            }),
        ]
        
    def coords(self, obj):
        return "(%d, %d) - (%d, %d)" % (obj.x1, obj.y1, obj.x2, obj.y2)
    coords.short_description = _("Cropping coordinates")
    
    def cropping_size(self, obj):
        return "%d × %d" % (obj.x2 - obj.x1, obj.y2 - obj.y1)
    cropping_size.short_description = _("Cropping size")
    
    def original_size(self, obj):
        try:
            return "%d × %d" % (obj.original.width, obj.original.height)
        except:
            return "-"
    original_size.short_description = _("Original size")

    def mods_list(self, obj):
        return ",<br />".join((el.title for el in obj.mods.all()))
    mods_list.short_description = _("Image Modifications")
    mods_list.allow_tags = True
    
    def update_versions(self, request, queryset):
        for cropping in queryset:
            cropping.update_versions()
    update_versions.short_description = _("Update image versions")
    

admin.site.register(ImageModificationGroup)
admin.site.register(ImageModification, ImageModificationOptions)
admin.site.register(ImageCropping, ImageCroppingOptions)


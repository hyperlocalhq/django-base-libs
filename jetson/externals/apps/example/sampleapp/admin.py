from django.contrib import admin
from example.sampleapp.models import Picture, Category

class PictureInline(admin.StackedInline):
    model = Picture

class CategoryAdmin(admin.ModelAdmin):
    inlines = [PictureInline]

admin.site.register(Category, CategoryAdmin)
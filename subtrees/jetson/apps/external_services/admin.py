# -*- coding: UTF-8 -*-

from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from base_libs.admin import ExtendedModelAdmin
from base_libs.models.admin import ObjectRelationMixinAdminOptions
from base_libs.models.admin import ObjectRelationMixinAdminForm

Service = models.get_model("external_services", "Service")
ObjectMapper = models.get_model("external_services", "ObjectMapper")
ServiceActionLog = models.get_model("external_services", "ServiceActionLog")

class ServiceOptions(ExtendedModelAdmin):
    save_on_top = True
    list_display = ('title', 'url', 'sysname')
    
    search_fields = ('title', 'url', 'sysname', 'user')
    
    fieldsets = (
        (None, {
            'fields':  ('title', 'url', 'sysname', )
            }),
        (_("Authentication"), {
            'fields':  ('api_key', 'user', 'password', )
            }),
        )

class ObjectMapperOptions(ObjectRelationMixinAdminOptions()):
    form = ObjectRelationMixinAdminForm()
    save_on_top = True
    list_display = ('id', 'external_id', 'get_content_object_display', 'service')
    list_display_links = ('id', 'external_id')
        
    list_filter =  ('service', 'content_type',)
    
    search_fields = ('service__title', 'external_id',)
    
    fieldsets = [
        (None, {
            'fields':  ('service', 'content_type', 'object_id', 'external_id',)
        }),
    ]

class ServiceActionLogOptions(ExtendedModelAdmin):
    save_on_top = True
    list_display = ('creation_date', 'service', 'response_code')
    
    search_fields = ('request', 'response')
    
    fieldsets = (
        (None, {
            'fields':  ('service', 'request', 'response', 'response_code')
            }),
        )

admin.site.register(Service, ServiceOptions)
admin.site.register(ObjectMapper, ObjectMapperOptions)
admin.site.register(ServiceActionLog, ServiceActionLogOptions)


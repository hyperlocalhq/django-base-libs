# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings

from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.serializers import Serializer
from tastypie.cache import SimpleCache

from base_libs.utils.misc import get_website_url
from base_libs.utils.misc import strip_html

EventCategory = models.get_model("events", "EventCategory")
Event = models.get_model("events", "Event")
EventTime = models.get_model("events", "EventTime")
Organizer = models.get_model("events", "Organizer")
MediaFile = models.get_model("events", "MediaFile")

class EventCategoryResource(ModelResource):
    class Meta:
        queryset = EventCategory.objects.all()
        resource_name = 'event_category'
        allowed_methods = ['get']
        excludes = ['title', 'slug', 'sort_order']
        authentication = ApiKeyAuthentication()
        authorization = ReadOnlyAuthorization()
        serializer = Serializer(formats=['json', 'xml'])
        cache = SimpleCache(timeout=10)

class OrganizerResource(ModelResource):
    organizing_museum = fields.ToOneField("museumsportal.apps.museums.api.resources.v2.MuseumResource", "organizing_museum", null=True)
    class Meta:
        queryset = Organizer.objects.all()
        resource_name = 'event_category'
        allowed_methods = ['get']
        excludes = []
        authentication = ApiKeyAuthentication()
        authorization = ReadOnlyAuthorization()
        serializer = Serializer(formats=['json', 'xml'])
        cache = SimpleCache(timeout=10)

class EventTimeResource(ModelResource):
    class Meta:
        queryset = EventTime.objects.all()
        resource_name = 'event_time'
        allowed_methods = ['get']
        authentication = ApiKeyAuthentication()
        authorization = ReadOnlyAuthorization()
        serializer = Serializer(formats=['json', 'xml'])
        cache = SimpleCache(timeout=10)

class MediaFileResource(ModelResource):
    class Meta:
        queryset = MediaFile.objects.all()
        resource_name = 'event_media_file'
        allowed_methods = ['get']
        excludes = ['path', 'sort_order']
        authentication = ApiKeyAuthentication()
        authorization = ReadOnlyAuthorization()
        serializer = Serializer(formats=['json', 'xml'])
        cache = SimpleCache(timeout=10)

    def dehydrate(self, bundle):
        if bundle.obj.path:
            bundle.data['url'] = "".join((
                get_website_url(),
                settings.MEDIA_URL[1:],
                bundle.obj.path.path,
                ))
        else:
            bundle.data['url'] = ""
        return bundle

class EventResource(ModelResource):
    museum = fields.ToOneField("museumsportal.apps.museums.api.resources.v2.MuseumResource", "museum", null=True)
    exhibition = fields.ToOneField("museumsportal.apps.exhibitions.api.resources.v2.ExhibitionResource", "exhibition", null=True)
    categories = fields.ToManyField(EventCategoryResource, "categories", full=True)
    event_times = fields.ToManyField(EventTimeResource, "eventtime_set", full=True)
    organizers = fields.ToManyField(OrganizerResource, "organizer_set", full=True)
    media_files = fields.ToManyField(MediaFileResource, "mediafile_set", full=True)
    
    class Meta:
        queryset = Event.objects.all()
        resource_name = 'event'
        allowed_methods = ['get']
        fields = [
            'id',
            'creation_date', 'modified_date',
            'title_en', 'title_de',
            'subtitle_en', 'subtitle_de',
            'event_type_en', 'event_type_de',
            'website_en', 'website_de',
            'meeting_place_en', 'meeting_place_de',
            'location_name', 'street_address', 'street_address2', 'postal_code', 'city', 'country',
            'latitude', 'longitude',
            'free_admission', 'admission_price', 'reduced_price',
            'categories', 'status',
            ]
        filtering = {
            'creation_date': ALL,
            'modified_date': ALL,
            'status': ALL,
            'categories': ALL_WITH_RELATIONS,
            }
        authentication = ApiKeyAuthentication()
        authorization = ReadOnlyAuthorization()
        serializer = Serializer(formats=['json', 'xml'])
        cache = SimpleCache(timeout=10)
            
    def dehydrate(self, bundle):
        bundle.data['link_en'] = "".join((
            get_website_url(),
            "en/events/",
            bundle.obj.slug,
            "/",
            ))
        bundle.data['link_de'] = "".join((
            get_website_url(),
            "de/veranstaltungen/",
            bundle.obj.slug,
            "/",
            ))
        bundle.data['press_text_en'] = strip_html(bundle.obj.get_rendered_press_text_en())
        bundle.data['press_text_de'] = strip_html(bundle.obj.get_rendered_press_text_de())
        
        bundle.data['admission_price_info_en'] = strip_html(bundle.obj.get_rendered_admission_price_info_en())
        bundle.data['admission_price_info_de'] = strip_html(bundle.obj.get_rendered_admission_price_info_de())
        
        bundle.data['booking_info_en'] = strip_html(bundle.obj.get_rendered_booking_info_en())
        bundle.data['booking_info_de'] = strip_html(bundle.obj.get_rendered_booking_info_de())
        
        return bundle
        
    def apply_filters(self, request, applicable_filters):
        from dateutil.parser import parse
        base_object_list = super(EventResource, self).apply_filters(request, applicable_filters)
        created_or_modified_since = request.GET.get('created_or_modified_since', None)
        if created_or_modified_since:
            try:
                created_or_modified_since = parse(created_or_modified_since)
            except:
                pass
            else:
                base_object_list = base_object_list.filter(
                    models.Q(creation_date__gte=created_or_modified_since) |
                    models.Q(modified_date__gte=created_or_modified_since)
                    )
        return base_object_list
        

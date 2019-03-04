# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings

from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.serializers import Serializer
from tastypie.cache import NoCache

from base_libs.utils.misc import get_website_url
from base_libs.utils.misc import strip_html

MuseumCategory = models.get_model("museums", "MuseumCategory")
Museum = models.get_model("museums", "Museum")

class MuseumCategoryResource(ModelResource):
    class Meta:
        queryset = MuseumCategory.objects.all()
        resource_name = 'museum_category'
        allowed_methods = ['get']
        excludes = ['title', 'slug', 'sort_order']
        authentication = ApiKeyAuthentication()
        authorization = ReadOnlyAuthorization()
        serializer = Serializer(formats=['json', 'xml'])
        cache = NoCache()

class MuseumResource(ModelResource):
    categories = fields.ToManyField(MuseumCategoryResource, "categories", full=True)
    
    class Meta:
        queryset = Museum.objects.all()
        max_limit = 100
        resource_name = 'museum'
        allowed_methods = ['get']
        fields = [
            'id',
            'creation_date', 'modified_date',
            'title_en', 'title_de',
            'subtitle_en', 'subtitle_de',
            'street_address', 'street_address2', 'postal_code', 'city', 'country',
            'latitude', 'longitude',
            'phone', 'fax', 'email',
            'image',
            'categories', 'status', 'open_on_mondays', 'free_entrance',
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
        cache = NoCache()
        
    def dehydrate(self, bundle):
        if bundle.obj.image:
            bundle.data['image'] = "".join((
                get_website_url(),
                settings.MEDIA_URL,
                bundle.obj.image.path,
                ))
        else:
            bundle.data['image'] = ""
        bundle.data['link_de'] = "".join((
            get_website_url(),
            "/de/museen/",
            bundle.obj.slug,
            "/",
            ))
        bundle.data['link_en'] = "".join((
            get_website_url(),
            "/en/museums/",
            bundle.obj.slug,
            "/",
            ))
        bundle.data['press_text_en'] = strip_html(bundle.obj.get_rendered_description_en())
        bundle.data['press_text_de'] = strip_html(bundle.obj.get_rendered_description_de())
        bundle.data['image_caption_en'] = strip_html(bundle.obj.get_rendered_image_caption_en())
        bundle.data['image_caption_de'] = strip_html(bundle.obj.get_rendered_image_caption_de())
        return bundle
        
        
    def apply_filters(self, request, applicable_filters):
        from dateutil.parser import parse
        base_object_list = super(MuseumResource, self).apply_filters(request, applicable_filters)
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

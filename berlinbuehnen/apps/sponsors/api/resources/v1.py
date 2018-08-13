# -*- coding: utf-8 -*-

from django.conf import settings

from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.serializers import Serializer
from tastypie.cache import SimpleCache

from base_libs.utils.misc import get_website_url


from berlinbuehnen.apps.sponsors.models import Sponsor


class BaseMetaForModelResource(object):
    allowed_methods = ['get']
    #authentication = ApiKeyAuthentication()
    #authorization = ReadOnlyAuthorization()
    serializer = Serializer(formats=['json', 'xml'])
    cache = SimpleCache(timeout=10)
    max_limit = 100


class SponsorResource(ModelResource):
    class Meta(BaseMetaForModelResource):
        queryset = Sponsor.objects.all()
        resource_name = 'sponsor'
        fields = [
            'id',
            'creation_date', 'modified_date',
            'title_de', 'title_en',
            'website',
        ]

    def dehydrate(self, bundle):
        if bundle.obj.image:
            bundle.data['image_url'] = "".join((
                get_website_url(),
                settings.MEDIA_URL[1:],
                bundle.obj.image.path,
                ))
        return bundle

# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import activate, get_language

from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.serializers import Serializer
from tastypie.cache import SimpleCache

from base_libs.utils.misc import get_website_url
from base_libs.utils.misc import strip_html as strip_html_base

from filebrowser.models import FileDescription

from berlinbuehnen.apps.locations.models import Service
from berlinbuehnen.apps.locations.models import AccessibilityOption
from berlinbuehnen.apps.locations.models import Location
from berlinbuehnen.apps.locations.models import Stage
from berlinbuehnen.apps.locations.models import Image as LocationImage
from berlinbuehnen.apps.locations.models import SocialMediaChannel

from berlinbuehnen.apps.site_specific.functions import remove_copyright_label


def valid_XML_char_ordinal(i):
    """
    Char ::= #x9 | #xA | #xD | [#x20-#xD7FF] | [#xE000-#xFFFD] | [#x10000-#x10FFFF]
    """
    return ( # conditions ordered by presumed frequency
        0x20 <= i <= 0xD7FF
        or i in (0x9, 0xA, 0xD)
        or 0xE000 <= i <= 0xFFFD
        or 0x10000 <= i <= 0x10FFFF
    )


def strip_invalid_chars(text):
    return u''.join(c for c in text if valid_XML_char_ordinal(ord(c)))


def strip_html(text):
    text = text.replace('<br />', '\n')
    return strip_html_base(text)


class BaseMetaForModelResource(object):
    allowed_methods = ['get']
    authentication = ApiKeyAuthentication()
    authorization = ReadOnlyAuthorization()
    serializer = Serializer(formats=['json', 'xml'])
    cache = SimpleCache(timeout=10)
    max_limit = 100


class ServiceResource(ModelResource):
    class Meta(BaseMetaForModelResource):
        queryset = Service.objects.all()
        resource_name = 'location_service'
        excludes = ['title', 'slug', 'sort_order', 'image']

    def dehydrate(self, bundle):
        bundle.data['title_de'] = strip_invalid_chars(bundle.obj.title_de)
        bundle.data['title_en'] = strip_invalid_chars(bundle.obj.title_en)
        if bundle.obj.image:
            bundle.data['image_url'] = "".join((
                get_website_url(),
                settings.MEDIA_URL[1:],
                bundle.obj.image.path,
                ))
        return bundle


class AccessibilityOptionResource(ModelResource):
    class Meta(BaseMetaForModelResource):
        queryset = AccessibilityOption.objects.all()
        resource_name = 'location_accessibility'
        excludes = ['title', 'slug', 'sort_order', 'image']

    def dehydrate(self, bundle):
        bundle.data['title_de'] = strip_invalid_chars(bundle.obj.title_de)
        bundle.data['title_en'] = strip_invalid_chars(bundle.obj.title_en)
        if bundle.obj.image:
            bundle.data['image_url'] = "".join((
                get_website_url(),
                settings.MEDIA_URL[1:],
                bundle.obj.image.path,
                ))
        return bundle


class StageResource(ModelResource):
    class Meta(BaseMetaForModelResource):
        queryset = Stage.objects.all()
        resource_name = 'stage'
        fields = [
            'id',
            'creation_date', 'modified_date',
            'title_de', 'title_en',
            'street_address', 'street_address2', 'postal_code', 'city', 'country',
            'latitude', 'longitude',
        ]

    def dehydrate(self, bundle):
        bundle.data['title_de'] = strip_invalid_chars(bundle.obj.title_de)
        bundle.data['title_en'] = strip_invalid_chars(bundle.obj.title_en)
        bundle.data['description_de'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_description_de()))
        bundle.data['description_en'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_description_en()))
        bundle.data['street_address'] = strip_invalid_chars(bundle.obj.street_address)
        bundle.data['street_address2'] = strip_invalid_chars(bundle.obj.street_address2)
        bundle.data['postal_code'] = strip_invalid_chars(bundle.obj.postal_code)
        bundle.data['city'] = strip_invalid_chars(bundle.obj.city)
        return bundle


class ImageResource(ModelResource):
    class Meta(BaseMetaForModelResource):
        queryset = LocationImage.objects.all()
        resource_name = 'location_image'
        fields = [
            'id',
            'creation_date', 'modified_date',
            'copyright_restrictions',
            'sort_order',
        ]

    def get_object_list(self, request):
        object_list = super(ImageResource, self).get_object_list(request)
        object_list = object_list.exclude(copyright_restrictions="protected")
        return object_list

    def dehydrate(self, bundle):
        if bundle.obj.path:
            bundle.data['url'] = "".join((
                get_website_url(),
                settings.MEDIA_URL[1:],
                bundle.obj.path.path,
                ))
            try:
                file_description = FileDescription.objects.filter(
                    file_path=bundle.obj.path,
                    ).order_by("pk")[0]
            except:
                pass
            else:
                bundle.data['title_de'] = strip_invalid_chars(file_description.title_de)
                bundle.data['title_en'] = strip_invalid_chars(file_description.title_en)
                bundle.data['description_de'] = strip_invalid_chars(file_description.description_de)
                bundle.data['description_en'] = strip_invalid_chars(file_description.description_en)
                copyright = remove_copyright_label(strip_invalid_chars(file_description.author))
                bundle.data['author'] = copyright
                bundle.data['photographer'] = copyright
                bundle.data['copyright'] = copyright
        if not bundle.data.get('copyright', None):
            bundle.data['copyright'] = "Promo"
        return bundle


class SocialMediaChannelResource(ModelResource):
    class Meta(BaseMetaForModelResource):
        queryset = SocialMediaChannel.objects.all()
        resource_name = 'location_social_media'
        excludes = []


class LocationResource(ModelResource):
    accessibility = fields.ToManyField(AccessibilityOptionResource, "accessibility_options", full=True)
    services = fields.ToManyField(ServiceResource, "services", full=True)
    stages = fields.ToManyField(StageResource, "stage_set", full=True)
    images = fields.ToManyField(ImageResource, "image_set", full=True)
    social_media = fields.ToManyField(SocialMediaChannelResource, "socialmediachannel_set", full=True)

    class Meta(BaseMetaForModelResource):
        queryset = Location.objects.all()
        resource_name = 'location'
        fields = [
            'id',
            'creation_date', 'modified_date',
            'title_de', 'title_en',
            'subtitle_de', 'subtitle_en',
            'street_address', 'street_address2', 'postal_code', 'city', 'country',
            'latitude', 'longitude',
            'email', 'website',
        ]
        filtering = {
            'creation_date': ALL,
            'modified_date': ALL,
            'status': ALL,
        }

    def dehydrate(self, bundle):
        current_language = get_language()
        for lang_code, lang_name in settings.FRONTEND_LANGUAGES:
            try:
                activate(lang_code)
                path = reverse('location_detail', kwargs={'slug': bundle.obj.slug})
                bundle.data['link_%s' % lang_code] = "".join((get_website_url()[:-1], path))
            except:
                pass
        activate(current_language)

        bundle.data['title_de'] = strip_invalid_chars(bundle.obj.title_de)
        bundle.data['title_en'] = strip_invalid_chars(bundle.obj.title_en)
        bundle.data['subtitle_de'] = strip_invalid_chars(bundle.obj.subtitle_de)
        bundle.data['subtitle_en'] = strip_invalid_chars(bundle.obj.subtitle_en)
        bundle.data['description_de'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_description_de()))
        bundle.data['description_en'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_description_en()))

        if bundle.obj.phone_number:
            bundle.data['phone'] = [strip_invalid_chars(bundle.obj.phone_country), strip_invalid_chars(bundle.obj.phone_area), strip_invalid_chars(bundle.obj.phone_number)]
        if bundle.obj.fax_number:
            bundle.data['fax'] = [strip_invalid_chars(bundle.obj.fax_country), strip_invalid_chars(bundle.obj.fax_area), strip_invalid_chars(bundle.obj.fax_number)]

        bundle.data['tickets'] = {}
        if bundle.obj.tickets_street_address:
            bundle.data['tickets']['street_address'] = strip_invalid_chars(bundle.obj.tickets_street_address)
            bundle.data['tickets']['street_address2'] = strip_invalid_chars(bundle.obj.tickets_street_address2)
            bundle.data['tickets']['postal_code'] = strip_invalid_chars(bundle.obj.tickets_postal_code)
            bundle.data['tickets']['city'] = strip_invalid_chars(bundle.obj.tickets_city)
        if bundle.obj.tickets_email:
            bundle.data['tickets']['email'] = strip_invalid_chars(bundle.obj.tickets_email)
        if bundle.obj.tickets_website:
            bundle.data['tickets']['website'] = strip_invalid_chars(bundle.obj.tickets_website)
        if bundle.obj.tickets_phone_number:
            bundle.data['tickets']['phone'] = [strip_invalid_chars(bundle.obj.tickets_phone_country), strip_invalid_chars(bundle.obj.tickets_phone_area), strip_invalid_chars(bundle.obj.tickets_phone_number)]
        if bundle.obj.tickets_fax_number:
            bundle.data['tickets']['fax'] = [strip_invalid_chars(bundle.obj.tickets_fax_country), strip_invalid_chars(bundle.obj.tickets_fax_area), strip_invalid_chars(bundle.obj.tickets_fax_number)]

        current_language = get_language()
        activate('en')
        opening_hours = []
        for weekday_hours in bundle.obj.get_opening_hours():
            del weekday_hours['times']
            opening_hours.append(weekday_hours)
        bundle.data['tickets_opening_hours'] = opening_hours
        activate(current_language)

        bundle.data['press'] = {}
        if bundle.obj.press_contact_name:
            bundle.data['press']['contact_name'] = strip_invalid_chars(bundle.obj.press_contact_name)
        if bundle.obj.press_email:
            bundle.data['press']['email'] = strip_invalid_chars(bundle.obj.press_email)
        if bundle.obj.press_website:
            bundle.data['press']['website'] = strip_invalid_chars(bundle.obj.press_website)
        if bundle.obj.press_phone_number:
            bundle.data['press']['phone'] = [strip_invalid_chars(bundle.obj.press_phone_country), strip_invalid_chars(bundle.obj.press_phone_area), strip_invalid_chars(bundle.obj.press_phone_number)]
        if bundle.obj.press_fax_number:
            bundle.data['press']['fax'] = [strip_invalid_chars(bundle.obj.press_fax_country), strip_invalid_chars(bundle.obj.press_fax_area), strip_invalid_chars(bundle.obj.press_fax_number)]

        return bundle

    def apply_filters(self, request, applicable_filters):
        from dateutil.parser import parse
        base_object_list = super(LocationResource, self).apply_filters(request, applicable_filters)
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

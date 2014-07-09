# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.utils.translation import activate

from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.serializers import Serializer
from tastypie.cache import SimpleCache

from base_libs.utils.misc import get_website_url
from base_libs.utils.misc import strip_html
from base_libs.middleware import get_current_language

from filebrowser.models import FileDescription

WorkshopType = models.get_model("workshops", "WorkshopType")
Workshop = models.get_model("workshops", "Workshop")
WorkshopTime = models.get_model("workshops", "WorkshopTime")
Organizer = models.get_model("workshops", "Organizer")
MediaFile = models.get_model("workshops", "MediaFile")


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


class WorkshopTypeResource(ModelResource):
    class Meta:
        queryset = WorkshopType.objects.all()
        max_limit = 100
        resource_name = 'workshop_type'
        allowed_methods = ['get']
        excludes = ['title', 'slug', 'sort_order']
        authentication = ApiKeyAuthentication()
        authorization = ReadOnlyAuthorization()
        serializer = Serializer(formats=['json', 'xml'])
        cache = SimpleCache(timeout=10)
        filtering = {
            "id": ALL,
        }

class OrganizerResource(ModelResource):
    organizing_museum = fields.ToOneField("museumsportal.apps.museums.api.resources.v2.MuseumResource", "organizing_museum", null=True)

    class Meta:
        queryset = Organizer.objects.all()
        max_limit = 100
        resource_name = 'workshop_organizer'
        allowed_methods = ['get']
        excludes = []
        authentication = ApiKeyAuthentication()
        authorization = ReadOnlyAuthorization()
        serializer = Serializer(formats=['json', 'xml'])
        cache = SimpleCache(timeout=10)


class WorkshopTimeResource(ModelResource):
    class Meta:
        queryset = WorkshopTime.objects.all()
        max_limit = 100
        resource_name = 'workshop_time'
        allowed_methods = ['get']
        authentication = ApiKeyAuthentication()
        authorization = ReadOnlyAuthorization()
        serializer = Serializer(formats=['json', 'xml'])
        cache = SimpleCache(timeout=10)


class MediaFileResource(ModelResource):
    class Meta:
        queryset = MediaFile.objects.all()
        max_limit = 100
        resource_name = 'workshop_media_file'
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
                bundle.data['author'] = strip_invalid_chars(file_description.author)
                bundle.data['copyright_limitations'] = strip_invalid_chars(file_description.copyright_limitations)

        return bundle


class WorkshopResource(ModelResource):
    museum = fields.ToOneField("museumsportal.apps.museums.api.resources.v2.MuseumResource", "museum", null=True)
    exhibition = fields.ToOneField("museumsportal.apps.exhibitions.api.resources.v2.ExhibitionResource", "exhibition", null=True)
    workshop_times = fields.ToManyField(WorkshopTimeResource, "workshoptime_set", full=True)
    organizers = fields.ToManyField(OrganizerResource, "organizer_set", full=True)
    media_files = fields.ToManyField(MediaFileResource, "mediafile_set", full=True)
    types = fields.ToManyField(WorkshopTypeResource, "types", full=True, null=True)
    
    class Meta:
        queryset = Workshop.objects.all()
        max_limit = 100
        resource_name = 'workshop'
        allowed_methods = ['get']
        fields = [
            'id',
            'creation_date', 'modified_date',
            'title_en', 'title_de',
            'subtitle_en', 'subtitle_de',
            'workshop_type_en', 'workshop_type_de',
            'website_en', 'website_de',
            'meeting_place_en', 'meeting_place_de',
            'has_group_offer', 'is_for_preschool', 'is_for_primary_school', 'is_for_youth', 'is_for_families', 'is_for_wheelchaired', 'is_for_deaf', 'is_for_blind', 'is_for_learning_difficulties',
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
            'types': ALL_WITH_RELATIONS,
            'is_for_preschool': ALL,
            'is_for_primary_school': ALL,
            'is_for_youth': ALL,
            'is_for_families': ALL,
        }
        authentication = ApiKeyAuthentication()
        authorization = ReadOnlyAuthorization()
        serializer = Serializer(formats=['json', 'xml'])
        cache = SimpleCache(timeout=10)
            
    def dehydrate_title_en(self, bundle):
        return strip_invalid_chars(bundle.data['title_en'])

    def dehydrate_title_de(self, bundle):
        return strip_invalid_chars(bundle.data['title_de'])

    def dehydrate_subtitle_en(self, bundle):
        return strip_invalid_chars(bundle.data['subtitle_en'])

    def dehydrate_subtitle_de(self, bundle):
        return strip_invalid_chars(bundle.data['subtitle_de'])

    def dehydrate_workshop_type_en(self, bundle):
        return strip_invalid_chars(bundle.data['workshop_type_en'])

    def dehydrate_workshop_type_de(self, bundle):
        return strip_invalid_chars(bundle.data['workshop_type_de'])

    def dehydrate_meeting_place_en(self, bundle):
        return strip_invalid_chars(bundle.data['meeting_place_en'])

    def dehydrate_meeting_place_de(self, bundle):
        return strip_invalid_chars(bundle.data['meeting_place_de'])

    def dehydrate(self, bundle):
        bundle.data['link_en'] = "".join((
            get_website_url(),
            "en/guided-tours/",
            bundle.obj.slug,
            "/",
        ))
        bundle.data['link_de'] = "".join((
            get_website_url(),
            "de/fuehrungen/",
            bundle.obj.slug,
            "/",
        ))
        bundle.data['press_text_en'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_press_text_en()))
        bundle.data['press_text_de'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_press_text_de()))

        bundle.data['admission_price_info_en'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_admission_price_info_en()))
        bundle.data['admission_price_info_de'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_admission_price_info_de()))

        bundle.data['booking_info_en'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_booking_info_en()))
        bundle.data['booking_info_de'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_booking_info_de()))
        
        current_language = get_current_language()
        activate("de")
        bundle.data['languages_de'] = bundle.obj.get_languages()
        activate(current_language)
        
        if bundle.obj.pdf_document_de:
            bundle.data['pdf_document_de'] = "".join((
                get_website_url(),
                settings.MEDIA_URL[1:],
                bundle.obj.pdf_document_de.path,
            ))
        if bundle.obj.pdf_document_en:
            bundle.data['pdf_document_en'] = "".join((
                get_website_url(),
                settings.MEDIA_URL[1:],
                bundle.obj.pdf_document_en.path,
            ))

        return bundle
        
    def apply_filters(self, request, applicable_filters):
        from dateutil.parser import parse
        base_object_list = super(WorkshopResource, self).apply_filters(request, applicable_filters)
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
        is_for_children = request.GET.get('is_for_children', None)
        if is_for_children in ('1', 'True', 'true', 'on'):
            base_object_list = base_object_list.filter(
                models.Q(is_for_preschool=True) |
                models.Q(is_for_primary_school=True) |
                models.Q(is_for_youth=True)
            )
        return base_object_list

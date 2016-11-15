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

from filebrowser.models import FileDescription

ExhibitionCategory = models.get_model("exhibitions", "ExhibitionCategory")
Exhibition = models.get_model("exhibitions", "Exhibition")
Organizer = models.get_model("exhibitions", "Organizer")
Season = models.get_model("exhibitions", "Season")
MediaFile = models.get_model("exhibitions", "MediaFile")


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


class ExhibitionCategoryResource(ModelResource):

    class Meta:
        queryset = ExhibitionCategory.objects.all()
        max_limit = 100
        resource_name = 'exhibition_category'
        allowed_methods = ['get']
        excludes = ['title', 'slug', 'sort_order']
        authentication = ApiKeyAuthentication()
        authorization = ReadOnlyAuthorization()
        serializer = Serializer(formats=['json', 'xml'])
        cache = NoCache()


class SeasonResource(ModelResource):

    class Meta:
        queryset = Season.objects.all()
        max_limit = 100
        resource_name = 'exhibition_season'
        allowed_methods = ['get']
        excludes = ['last_entry', 'exceptions', 'exceptions_markup_type', 'exceptions_de_markup_type', 'exceptions_en_markup_type']
        authentication = ApiKeyAuthentication()
        authorization = ReadOnlyAuthorization()
        serializer = Serializer(formats=['json', 'xml'])
        cache = NoCache()

    def dehydrate(self, bundle):
        bundle.data['exceptions_en'] = strip_html(bundle.obj.get_rendered_exceptions_en())
        bundle.data['exceptions_de'] = strip_html(bundle.obj.get_rendered_exceptions_de())
        return bundle


class OrganizerResource(ModelResource):
    organizing_museum = fields.ToOneField("museumsportal.apps.museums.api.resources.v2.MuseumResource", "organizing_museum", null=True)

    class Meta:
        queryset = Organizer.objects.all()
        max_limit = 100
        resource_name = 'exhibition_organizer'
        allowed_methods = ['get']
        excludes = []
        authentication = ApiKeyAuthentication()
        authorization = ReadOnlyAuthorization()
        serializer = Serializer(formats=['json', 'xml'])
        cache = NoCache()


class MediaFileResource(ModelResource):

    class Meta:
        queryset = MediaFile.objects.all()
        max_limit = 100
        resource_name = 'exhibition_media_file'
        allowed_methods = ['get']
        excludes = ['path', 'sort_order']
        authentication = ApiKeyAuthentication()
        authorization = ReadOnlyAuthorization()
        serializer = Serializer(formats=['json', 'xml'])
        cache = NoCache()

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


class ExhibitionResource(ModelResource):
    museum = fields.ToOneField("museumsportal.apps.museums.api.resources.v2.MuseumResource", "museum", null=True)
    categories = fields.ToManyField(ExhibitionCategoryResource, "categories", full=True)
    seasons = fields.ToManyField(SeasonResource, "season_set", full=True)
    organizers = fields.ToManyField(OrganizerResource, "organizer_set", full=True)
    media_files = fields.ToManyField(MediaFileResource, "mediafile_set", full=True)
    
    class Meta:
        queryset = Exhibition.objects.all()
        max_limit = 100
        resource_name = 'exhibition'
        allowed_methods = ['get']
        fields = [
            'id',
            'creation_date', 'modified_date',
            'title_en', 'title_de',
            'subtitle_en', 'subtitle_de',
            'catalog_ordering_en', 'catalog_ordering_de',
            'website_en', 'website_de',
            'start', 'end', 'vernissage', 'finissage',
            'exhibition_extended', 'permanent',
            'location_name', 'street_address', 'street_address2', 'postal_code', 'city', 'country',
            'latitude', 'longitude',
            'museum_prices', 'free_entrance', 'admission_price', 'reduced_price',
            'museum_opening_hours', 'suitable_for_disabled', 'is_for_children',
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
        cache = NoCache()

    def dehydrate_title_en(self, bundle):
        return strip_invalid_chars(bundle.data['title_en'])

    def dehydrate_title_de(self, bundle):
        return strip_invalid_chars(bundle.data['title_de'])

    def dehydrate_subtitle_en(self, bundle):
        return strip_invalid_chars(bundle.data['subtitle_en'])

    def dehydrate_subtitle_de(self, bundle):
        return strip_invalid_chars(bundle.data['subtitle_de'])

    def dehydrate_catalog_ordering_en(self, bundle):
        return strip_invalid_chars(bundle.data['catalog_ordering_en'])

    def dehydrate_catalog_ordering_de(self, bundle):
        return strip_invalid_chars(bundle.data['catalog_ordering_de'])

    def dehydrate(self, bundle):
        bundle.data['link_en'] = "".join((
            get_website_url(),
            "en/exhibitions/",
            bundle.obj.slug,
            "/",
        ))
        bundle.data['link_de'] = "".join((
            get_website_url(),
            "de/ausstellungen/",
            bundle.obj.slug,
            "/",
        ))
        bundle.data['press_text_en'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_press_text_en()))
        bundle.data['press_text_de'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_press_text_de()))
        
        bundle.data['catalog_en'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_catalog_en()))
        bundle.data['catalog_de'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_catalog_de()))
        
        bundle.data['other_locations_en'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_other_locations_en()))
        bundle.data['other_locations_de'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_other_locations_de()))
        
        bundle.data['admission_price_info_en'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_admission_price_info_en()))
        bundle.data['admission_price_info_de'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_admission_price_info_de()))
        
        bundle.data['reduced_price_info_en'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_reduced_price_info_en()))
        bundle.data['reduced_price_info_de'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_reduced_price_info_de()))
        
        bundle.data['suitable_for_disabled_info_en'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_suitable_for_disabled_info_en()))
        bundle.data['suitable_for_disabled_info_de'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_suitable_for_disabled_info_de()))
        
        if bundle.obj.permanent:
            bundle.data['end'] = "2099-12-31"

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
        base_object_list = super(ExhibitionResource, self).apply_filters(request, applicable_filters)
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

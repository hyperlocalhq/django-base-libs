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

MuseumCategory = models.get_model("museums", "MuseumCategory")
AccessibilityOption = models.get_model("museums", "AccessibilityOption")
Museum = models.get_model("museums", "Museum")
Season = models.get_model("museums", "Season")
SpecialOpeningTime = models.get_model("museums", "SpecialOpeningTime")
MediaFile = models.get_model("museums", "MediaFile")
SocialMediaChannel = models.get_model("museums", "SocialMediaChannel")


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

class AccessibilityOptionResource(ModelResource):
    class Meta:
        queryset = AccessibilityOption.objects.all()
        resource_name = 'accessibility_option'
        allowed_methods = ['get']
        excludes = ['title', 'slug', 'image', 'sort_order']
        authentication = ApiKeyAuthentication()
        authorization = ReadOnlyAuthorization()
        serializer = Serializer(formats=['json', 'xml'])
        cache = NoCache()

class SeasonResource(ModelResource):
    class Meta:
        queryset = Season.objects.all()
        resource_name = 'museum_season'
        allowed_methods = ['get']
        excludes = ['title', 'exceptions', 'last_entry', 'exceptions_markup_type', 'exceptions_de_markup_type', 'exceptions_en_markup_type']
        authentication = ApiKeyAuthentication()
        authorization = ReadOnlyAuthorization()
        serializer = Serializer(formats=['json', 'xml'])
        cache = NoCache()

    def dehydrate(self, bundle):
        bundle.data['exceptions_en'] = strip_html(bundle.obj.get_rendered_exceptions_en())
        bundle.data['exceptions_de'] = strip_html(bundle.obj.get_rendered_exceptions_de())
        return bundle
        
class SpecialOpeningTimeResource(ModelResource):
    class Meta:
        queryset = SpecialOpeningTime.objects.all()
        resource_name = 'museum_special_opening_time'
        allowed_methods = ['get']
        excludes = ['day_label', 'exceptions', 'exceptions_markup_type', 'exceptions_de_markup_type', 'exceptions_en_markup_type']
        authentication = ApiKeyAuthentication()
        authorization = ReadOnlyAuthorization()
        serializer = Serializer(formats=['json', 'xml'])
        cache = NoCache()

    def dehydrate(self, bundle):
        bundle.data['exceptions_en'] = strip_html(bundle.obj.get_rendered_exceptions_en())
        bundle.data['exceptions_de'] = strip_html(bundle.obj.get_rendered_exceptions_de())
        return bundle

class MediaFileResource(ModelResource):
    class Meta:
        queryset = MediaFile.objects.all()
        resource_name = 'museum_media_file'
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

class SocialMediaChannelResource(ModelResource):
    class Meta:
        queryset = SocialMediaChannel.objects.all()
        resource_name = 'museum_social_media_chanel'
        allowed_methods = ['get']
        excludes = []
        authentication = ApiKeyAuthentication()
        authorization = ReadOnlyAuthorization()
        serializer = Serializer(formats=['json', 'xml'])
        cache = NoCache()

class MuseumResource(ModelResource):
    categories = fields.ToManyField(MuseumCategoryResource, "categories", full=True)
    accessibility_options = fields.ToManyField(AccessibilityOptionResource, "accessibility_options", full=True)
    seasons = fields.ToManyField(SeasonResource, "season_set", full=True)
    special_opening_times = fields.ToManyField(SpecialOpeningTimeResource, "specialopeningtime_set", full=True)
    media_files = fields.ToManyField(MediaFileResource, "mediafile_set", full=True)
    social_media_channels = fields.ToManyField(SocialMediaChannelResource, "socialmediachannel_set", full=True)
    
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
            'email', 'website',
            'categories', 'status', 'open_on_mondays',
            'free_entrance', 'admission_price', 'reduced_price',
            'show_family_ticket', 'show_group_ticket', 'show_yearly_ticket', 'member_of_museumspass',
            'service_shop', 'service_restaurant', 'service_cafe', 'service_library', 'service_archive', 'service_diaper_changing_table',
            'has_audioguide', 'has_audioguide_de', 'has_audioguide_en', 'has_audioguide_fr', 'has_audioguide_it', 'has_audioguide_sp', 'has_audioguide_pl', 'has_audioguide_tr', 'audioguide_other_languages', 'has_audioguide_for_children', 'has_audioguide_for_learning_difficulties',
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
        bundle.data['link_en'] = "".join((
            get_website_url(),
            "en/museums/",
            bundle.obj.slug,
            "/",
            ))
        bundle.data['link_de'] = "".join((
            get_website_url(),
            "de/museen/",
            bundle.obj.slug,
            "/",
            ))
        #bundle.data['press_text_en'] = strip_html(bundle.obj.get_rendered_description_en())
        #bundle.data['press_text_de'] = strip_html(bundle.obj.get_rendered_description_de())
        
        bundle.data['admission_price_info_en'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_admission_price_info_en()))
        bundle.data['admission_price_info_de'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_admission_price_info_de()))
        
        bundle.data['reduced_price_info_en'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_reduced_price_info_en()))
        bundle.data['reduced_price_info_de'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_reduced_price_info_de()))
        
        bundle.data['group_ticket_en'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_group_ticket_en()))
        bundle.data['group_ticket_de'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_group_ticket_de()))
        
        bundle.data['accessibility_en'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_accessibility_en()))
        bundle.data['accessibility_de'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_accessibility_de()))
        
        bundle.data['mobidat_en'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_mobidat_en()))
        bundle.data['mobidat_de'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_mobidat_de()))
        
        if bundle.obj.phone_number:
            bundle.data['phone'] = [bundle.obj.phone_country, bundle.obj.phone_area, bundle.obj.phone_number]
        if bundle.obj.fax_number:
            bundle.data['fax'] = [bundle.obj.fax_country, bundle.obj.fax_area, bundle.obj.fax_number]
        if bundle.obj.group_bookings_phone_number:
            bundle.data['group_bookings_phone'] = [bundle.obj.group_bookings_phone_country, bundle.obj.group_bookings_phone_area, bundle.obj.group_bookings_phone_number]
        if bundle.obj.service_phone_number:
            bundle.data['service_phone'] = [bundle.obj.service_phone_country, bundle.obj.service_phone_area, bundle.obj.service_phone_number]
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

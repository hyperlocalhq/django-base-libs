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

from jetson.apps.image_mods.models import FileManager

from berlinbuehnen.apps.locations.api.resources.v1 import LocationResource
from berlinbuehnen.apps.locations.api.resources.v1 import StageResource

from berlinbuehnen.apps.productions.models import LanguageAndSubtitles
from berlinbuehnen.apps.productions.models import ProductionCategory
from berlinbuehnen.apps.productions.models import ProductionCharacteristics
from berlinbuehnen.apps.productions.models import Production
from berlinbuehnen.apps.productions.models import ProductionSocialMediaChannel
from berlinbuehnen.apps.productions.models import ProductionVideo
from berlinbuehnen.apps.productions.models import ProductionLiveStream
from berlinbuehnen.apps.productions.models import ProductionImage
from berlinbuehnen.apps.productions.models import ProductionPDF
from berlinbuehnen.apps.productions.models import ProductionLeadership
from berlinbuehnen.apps.productions.models import ProductionAuthorship
from berlinbuehnen.apps.productions.models import ProductionInvolvement
from berlinbuehnen.apps.productions.models import ProductionSponsor

from berlinbuehnen.apps.productions.models import EventCharacteristics
from berlinbuehnen.apps.productions.models import Event
from berlinbuehnen.apps.productions.models import EventSocialMediaChannel
from berlinbuehnen.apps.productions.models import EventVideo
from berlinbuehnen.apps.productions.models import EventLiveStream
from berlinbuehnen.apps.productions.models import EventImage
from berlinbuehnen.apps.productions.models import EventPDF
from berlinbuehnen.apps.productions.models import EventLeadership
from berlinbuehnen.apps.productions.models import EventAuthorship
from berlinbuehnen.apps.productions.models import EventInvolvement
from berlinbuehnen.apps.productions.models import EventSponsor

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
    max_limit = 50


class LanguageAndSubtitlesResource(ModelResource):
    class Meta(BaseMetaForModelResource):
        queryset = LanguageAndSubtitles.objects.all()
        resource_name = 'language_and_subtitles'
        fields = ['id', 'title_de', 'title_en']


class ProductionCategoryResource(ModelResource):
    parent = fields.ToOneField("self", "parent", null=True, blank=True)
    class Meta(BaseMetaForModelResource):
        queryset = ProductionCategory.objects.all()
        resource_name = 'production_category'
        fields = ['id', 'title_de', 'title_en', 'creation_date', 'modified_date']


class ProductionCharacteristicsResource(ModelResource):
    class Meta(BaseMetaForModelResource):
        queryset = ProductionCharacteristics.objects.all()
        resource_name = 'production_characteristics'
        fields = ['id', 'title_de', 'title_en', 'creation_date', 'modified_date']


class ProductionSocialMediaChannelResource(ModelResource):
    class Meta(BaseMetaForModelResource):
        queryset = ProductionSocialMediaChannel.objects.all()
        resource_name = 'production_social_media'
        excludes = []


class ProductionVideoResource(ModelResource):
    class Meta(BaseMetaForModelResource):
        queryset = ProductionVideo.objects.all()
        resource_name = 'production_video'
        fields = ['id', 'title_de', 'title_en', 'creation_date', 'modified_date', 'sort_order']

    def dehydrate(self, bundle):
        bundle.data['embed'] = bundle.obj.get_embed()
        return bundle


class ProductionLiveStreamResource(ModelResource):
    class Meta(BaseMetaForModelResource):
        queryset = ProductionLiveStream.objects.all()
        resource_name = 'production_live_stream'
        fields = ['id', 'title_de', 'title_en', 'creation_date', 'modified_date', 'sort_order']

    def dehydrate(self, bundle):
        bundle.data['embed'] = bundle.obj.get_embed()
        return bundle


class ProductionImageResource(ModelResource):
    class Meta(BaseMetaForModelResource):
        queryset = ProductionImage.objects.exclude(copyright_restrictions="protected")
        resource_name = 'production_image'
        fields = [
            'id',
            'creation_date', 'modified_date',
            'copyright_restrictions',
            'sort_order',
        ]

    def get_object_list(self, request):
        object_list = super(ProductionImageResource, self).get_object_list(request)
        object_list = object_list.exclude(copyright_restrictions="protected")
        return object_list

    def dehydrate(self, bundle):
        if bundle.obj.path:
            bundle.data['url'] = "".join((
                get_website_url(),
                settings.MEDIA_URL,
                bundle.obj.path.path,
            ))
            list_image_path, query_params = FileManager.modified_path(bundle.obj.path.path, "list_image")
            if list_image_path:
                bundle.data['list_image_url'] = "".join((
                    get_website_url(),
                    settings.MEDIA_URL,
                    list_image_path,
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


class ProductionPDFResource(ModelResource):
    class Meta(BaseMetaForModelResource):
        queryset = ProductionPDF.objects.all()
        resource_name = 'production_pdf'
        fields = [
            'id',
            'creation_date', 'modified_date',
            'sort_order',
        ]

    def dehydrate(self, bundle):
        if bundle.obj.path:
            bundle.data['url'] = "".join((
                get_website_url(),
                settings.MEDIA_URL,
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
                bundle.data['copyright'] = copyright
        if not bundle.data.get('copyright', None):
            bundle.data['copyright'] = "Promo"
        return bundle


class ProductionLeadershipResource(ModelResource):
    class Meta(BaseMetaForModelResource):
        queryset = ProductionLeadership.objects.all()
        resource_name = 'production_leadership'
        fields = ['id', 'function_de', 'function_en', 'creation_date', 'modified_date']

    def dehydrate(self, bundle):
        if bundle.obj.person.prefix:
            bundle.data['prefix_de'] = bundle.obj.person.prefix.title_de
            bundle.data['prefix_en'] = bundle.obj.person.prefix.title_en
            bundle.data['gender'] = bundle.obj.person.gender
        bundle.data['first_name'] = bundle.obj.person.first_name
        bundle.data['last_name'] = bundle.obj.person.last_name
        return bundle


class ProductionAuthorshipResource(ModelResource):
    class Meta(BaseMetaForModelResource):
        queryset = ProductionAuthorship.objects.all()
        resource_name = 'production_authorship'
        fields = ['id', 'creation_date', 'modified_date']

    def dehydrate(self, bundle):
        if bundle.obj.person.prefix:
            bundle.data['prefix_de'] = bundle.obj.person.prefix.title_de
            bundle.data['prefix_en'] = bundle.obj.person.prefix.title_en
            bundle.data['gender'] = bundle.obj.person.gender
        bundle.data['first_name'] = bundle.obj.person.first_name
        bundle.data['last_name'] = bundle.obj.person.last_name
        if bundle.obj.authorship_type:
            bundle.data['type_de'] = bundle.obj.authorship_type.title_de
            bundle.data['type_en'] = bundle.obj.authorship_type.title_en
        return bundle


class ProductionInvolvementResource(ModelResource):
    class Meta(BaseMetaForModelResource):
        queryset = ProductionInvolvement.objects.all()
        resource_name = 'production_involvement'
        fields = ['id', 'creation_date', 'modified_date']

    def dehydrate(self, bundle):
        if bundle.obj.person.prefix:
            bundle.data['prefix_de'] = bundle.obj.person.prefix.title_de
            bundle.data['prefix_en'] = bundle.obj.person.prefix.title_en
            bundle.data['gender'] = bundle.obj.person.gender
        bundle.data['first_name'] = bundle.obj.person.first_name
        bundle.data['last_name'] = bundle.obj.person.last_name
        if bundle.obj.involvement_type:
            bundle.data['type_de'] = bundle.obj.involvement_type.title_de
            bundle.data['type_en'] = bundle.obj.involvement_type.title_en
        if bundle.obj.involvement_role_de:
            bundle.data['role_de'] = bundle.obj.involvement_role_de
        if bundle.obj.involvement_role_en:
            bundle.data['role_en'] = bundle.obj.involvement_role_en
        if bundle.obj.involvement_instrument_de:
            bundle.data['instrument_de'] = bundle.obj.involvement_instrument_de
        if bundle.obj.involvement_instrument_en:
            bundle.data['instrument_en'] = bundle.obj.involvement_instrument_en
        return bundle


class ProductionSponsorResource(ModelResource):
    class Meta(BaseMetaForModelResource):
        queryset = ProductionSponsor.objects.all()
        resource_name = 'production_sponsor'
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
                settings.MEDIA_URL,
                bundle.obj.image.path,
                ))
        return bundle


class EventCharacteristicsResource(ModelResource):
    class Meta(BaseMetaForModelResource):
        queryset = EventCharacteristics.objects.all()
        resource_name = 'event_characteristics'
        fields = ['id', 'title_de', 'title_en', 'creation_date', 'modified_date']


class EventSocialMediaChannelResource(ModelResource):
    class Meta(BaseMetaForModelResource):
        queryset = EventSocialMediaChannel.objects.all()
        resource_name = 'event_social_media'
        excludes = []


class EventVideoResource(ModelResource):
    class Meta(BaseMetaForModelResource):
        queryset = EventVideo.objects.all()
        resource_name = 'event_video'
        fields = ['id', 'title_de', 'title_en', 'creation_date', 'modified_date', 'sort_order']

    def dehydrate(self, bundle):
        bundle.data['embed'] = bundle.obj.get_embed()
        return bundle


class EventLiveStreamResource(ModelResource):
    class Meta(BaseMetaForModelResource):
        queryset = EventLiveStream.objects.all()
        resource_name = 'event_live_stream'
        fields = ['id', 'title_de', 'title_en', 'creation_date', 'modified_date', 'sort_order']

    def dehydrate(self, bundle):
        bundle.data['embed'] = bundle.obj.get_embed()
        return bundle


class EventImageResource(ModelResource):
    class Meta(BaseMetaForModelResource):
        queryset = EventImage.objects.exclude(copyright_restrictions="protected")
        resource_name = 'event_image'
        fields = [
            'id',
            'creation_date', 'modified_date',
            'copyright_restrictions',
            'sort_order',
        ]

    def get_object_list(self, request):
        object_list = super(EventImageResource, self).get_object_list(request)
        object_list = object_list.exclude(copyright_restrictions="protected")
        return object_list

    def dehydrate(self, bundle):
        if bundle.obj.path:
            bundle.data['url'] = "".join((
                get_website_url(),
                settings.MEDIA_URL,
                bundle.obj.path.path,
            ))
            list_image_path, query_params = FileManager.modified_path(bundle.obj.path.path, "list_image")
            if list_image_path:
                bundle.data['list_image_url'] = "".join((
                    get_website_url(),
                    settings.MEDIA_URL,
                    list_image_path,
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


class EventPDFResource(ModelResource):
    class Meta(BaseMetaForModelResource):
        queryset = EventPDF.objects.all()
        resource_name = 'event_pdf'
        fields = [
            'id',
            'creation_date', 'modified_date',
            'sort_order',
        ]

    def dehydrate(self, bundle):
        if bundle.obj.path:
            bundle.data['url'] = "".join((
                get_website_url(),
                settings.MEDIA_URL,
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
                bundle.data['copyright'] = copyright
        if not bundle.data.get('copyright', None):
            bundle.data['copyright'] = "Promo"
        return bundle


class EventLeadershipResource(ModelResource):
    class Meta(BaseMetaForModelResource):
        queryset = EventLeadership.objects.all()
        resource_name = 'event_leadership'
        fields = ['id', 'function_de', 'function_en', 'creation_date', 'modified_date']

    def dehydrate(self, bundle):
        if bundle.obj.person.prefix:
            bundle.data['prefix_de'] = bundle.obj.person.prefix.title_de
            bundle.data['prefix_en'] = bundle.obj.person.prefix.title_en
            bundle.data['gender'] = bundle.obj.person.gender
        bundle.data['first_name'] = bundle.obj.person.first_name
        bundle.data['last_name'] = bundle.obj.person.last_name
        return bundle


class EventAuthorshipResource(ModelResource):
    class Meta(BaseMetaForModelResource):
        queryset = EventAuthorship.objects.all()
        resource_name = 'event_authorship'
        fields = ['id', 'creation_date', 'modified_date']

    def dehydrate(self, bundle):
        if bundle.obj.person.prefix:
            bundle.data['prefix_de'] = bundle.obj.person.prefix.title_de
            bundle.data['prefix_en'] = bundle.obj.person.prefix.title_en
            bundle.data['gender'] = bundle.obj.person.gender
        bundle.data['first_name'] = bundle.obj.person.first_name
        bundle.data['last_name'] = bundle.obj.person.last_name
        if bundle.obj.authorship_type:
            bundle.data['type_de'] = bundle.obj.authorship_type.title_de
            bundle.data['type_en'] = bundle.obj.authorship_type.title_en
        return bundle


class EventInvolvementResource(ModelResource):
    class Meta(BaseMetaForModelResource):
        queryset = EventInvolvement.objects.all()
        resource_name = 'event_involvement'
        fields = ['id', 'creation_date', 'modified_date']

    def dehydrate(self, bundle):
        if bundle.obj.person.prefix:
            bundle.data['prefix_de'] = bundle.obj.person.prefix.title_de
            bundle.data['prefix_en'] = bundle.obj.person.prefix.title_en
            bundle.data['gender'] = bundle.obj.person.gender
        bundle.data['first_name'] = bundle.obj.person.first_name
        bundle.data['last_name'] = bundle.obj.person.last_name
        if bundle.obj.involvement_type:
            bundle.data['type_de'] = bundle.obj.involvement_type.title_de
            bundle.data['type_en'] = bundle.obj.involvement_type.title_en
        if bundle.obj.involvement_role_de:
            bundle.data['role_de'] = bundle.obj.involvement_role_de
        if bundle.obj.involvement_role_en:
            bundle.data['role_en'] = bundle.obj.involvement_role_en
        if bundle.obj.involvement_instrument_de:
            bundle.data['instrument_de'] = bundle.obj.involvement_instrument_de
        if bundle.obj.involvement_instrument_en:
            bundle.data['instrument_en'] = bundle.obj.involvement_instrument_en
        return bundle


class EventSponsorResource(ModelResource):
    class Meta(BaseMetaForModelResource):
        queryset = EventSponsor.objects.all()
        resource_name = 'event_sponsor'
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
                settings.MEDIA_URL,
                bundle.obj.image.path,
                ))
        return bundle

class EventResource(ModelResource):
    play_locations = fields.ToManyField(LocationResource, "play_locations")
    play_stages = fields.ToManyField(StageResource, "play_stages")

    characteristics = fields.ToManyField(EventCharacteristicsResource, "characteristics", full=True)

    leaders = fields.ToManyField(EventLeadershipResource, "eventleadership_set", full=True)
    authors = fields.ToManyField(EventAuthorshipResource, "eventauthorship_set", full=True)
    participants = fields.ToManyField(EventInvolvementResource, "eventinvolvement_set", full=True)

    videos = fields.ToManyField(EventVideoResource, "eventvideo_set", full=True)
    live_streams = fields.ToManyField(EventLiveStreamResource, "eventlivestream_set", full=True)
    images = fields.ToManyField(EventImageResource, attribute=(lambda bundle: bundle.obj.eventimage_set.exclude(copyright_restrictions="protected")), full=True, null=True, blank=True)
    pdfs = fields.ToManyField(EventPDFResource, "eventpdf_set", full=True)

    language_and_subtitles = fields.ToOneField(LanguageAndSubtitlesResource, "language_and_subtitles", null=True, blank=True, full=True)

    sponsors = fields.ToManyField(EventSponsorResource, "eventsponsor_set", full=True)

    class Meta(BaseMetaForModelResource):
        queryset = Event.objects.all()
        resource_name = 'event'
        fields = [
            'id', 'creation_date', 'modified_date',
            'start_date', 'end_date',
            'start_time', 'end_time',
            'duration', 'pauses',
            'location_title',
            'street_address', 'street_address2', 'postal_code', 'city', 'country',
            'latitude', 'longitude',
            'organizers',
            'duration_text_de', 'duration_text_en',
            'subtitles_text_de', 'subtitles_text_en',
            'age_text_de', 'age_text_en',
            'free_entrance', 'price_from', 'price_till', 'tickets_website',
            'event_status', 'ticket_status', 'classiccard',
        ]

    def dehydrate(self, bundle):
        if bundle.obj.event_status == "trashed":
            bundle.data = {
                'id':  bundle.obj.id,
                'event_status': bundle.obj.event_status,
                'creation_date': bundle.obj.creation_date,
                'modified_date': bundle.obj.modified_date,
            }
            return bundle
        current_language = get_language()
        for lang_code, lang_name in settings.FRONTEND_LANGUAGES:
            try:
                activate(lang_code)
                path = reverse('event_detail', kwargs={
                    'slug': bundle.obj.production.slug,
                    'event_id': bundle.obj.pk,
                })
                bundle.data['link_%s' % lang_code] = "".join((get_website_url(), path))
            except:
                pass
        activate(current_language)

        bundle.data['description_de'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_description_de()))
        bundle.data['description_en'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_description_en()))
        bundle.data['teaser_de'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_teaser_de()))
        bundle.data['teaser_en'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_teaser_en()))
        bundle.data['work_info_de'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_work_info_de()))
        bundle.data['work_info_en'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_work_info_en()))
        bundle.data['contents_de'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_contents_de()))
        bundle.data['contents_en'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_contents_en()))
        bundle.data['press_text_de'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_press_text_de()))
        bundle.data['press_text_en'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_press_text_en()))
        bundle.data['credits_de'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_credits_de()))
        bundle.data['credits_en'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_credits_en()))
        bundle.data['concert_program_de'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_concert_program_de()))
        bundle.data['concert_program_en'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_concert_program_en()))
        bundle.data['supporting_program_de'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_supporting_program_de()))
        bundle.data['supporting_program_en'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_supporting_program_en()))
        bundle.data['remarks_de'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_remarks_de()))
        bundle.data['remarks_en'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_remarks_en()))
        bundle.data['price_information_de'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_price_information_de()))
        bundle.data['price_information_en'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_price_information_en()))
        bundle.data['other_characteristics_de'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_other_characteristics_de()))
        bundle.data['other_characteristics_en'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_other_characteristics_en()))

        return bundle


class ProductionResource(ModelResource):
    in_program_of = fields.ToManyField(LocationResource, "in_program_of")

    play_locations = fields.ToManyField(LocationResource, "play_locations")
    play_stages = fields.ToManyField(StageResource, "play_stages")

    categories = fields.ToManyField(ProductionCategoryResource, attribute=lambda bundle: bundle.obj.get_categories(), full=True, null=True, blank=True)
    characteristics = fields.ToManyField(ProductionCharacteristicsResource, "characteristics", full=True)

    leaders = fields.ToManyField(ProductionLeadershipResource, "productionleadership_set", full=True)
    authors = fields.ToManyField(ProductionAuthorshipResource, "productionauthorship_set", full=True)
    participants = fields.ToManyField(ProductionInvolvementResource, "productioninvolvement_set", full=True)

    videos = fields.ToManyField(ProductionVideoResource, "productionvideo_set", full=True)
    live_streams = fields.ToManyField(ProductionLiveStreamResource, "productionlivestream_set", full=True)
    images = fields.ToManyField(EventImageResource, attribute=(lambda bundle: bundle.obj.productionimage_set.exclude(copyright_restrictions="protected")), full=True, null=True, blank=True)
    pdfs = fields.ToManyField(ProductionPDFResource, "productionpdf_set", full=True)
    social_media = fields.ToManyField(ProductionSocialMediaChannelResource, "productionsocialmediachannel_set", full=True)

    language_and_subtitles = fields.ToOneField(LanguageAndSubtitlesResource, "language_and_subtitles", null=True, blank=True, full=True)

    sponsors = fields.ToManyField(ProductionSponsorResource, "productionsponsor_set", full=True)

    events = fields.ToManyField(EventResource, "event_set", full=True)

    class Meta(BaseMetaForModelResource):
        queryset = Production.objects.all().prefetch_related(
            'in_program_of', 'play_locations', 'play_stages', 'categories', 'characteristics',
            'productionleadership_set__person', 'productionauthorship_set__person', 'productionauthorship_set__authorship_type', 'productioninvolvement_set__person', 'productioninvolvement_set__involvement_type',
            'productionvideo_set', 'productionlivestream_set', 'productionimage_set', 'productionpdf_set',
            'productionsocialmediachannel_set', 'language_and_subtitles',
            'event_set__play_locations', 'event_set__play_stages', 'event_set__characteristics',
            'event_set__eventleadership_set__person', 'event_set__eventauthorship_set__person', 'event_set__eventauthorship_set__authorship_type', 'event_set__eventinvolvement_set__person', 'event_set__eventinvolvement_set__involvement_type',
            'event_set__eventvideo_set', 'event_set__eventlivestream_set', 'event_set__eventimage_set', 'event_set__eventpdf_set',
        )
        resource_name = 'production'
        fields = [
            'id', 'creation_date', 'modified_date',
            'ensembles', 'organizers', 'in_cooperation_with',
            'prefix_de', 'prefix_en',
            'title_de', 'title_en',
            'subtitle_de', 'subtitle_en',
            'original_de', 'original_en',
            'duration_text_de', 'duration_text_en',
            'subtitles_text_de', 'subtitles_text_en',
            'age_text_de', 'age_text_en',
            'website',
            'free_entrance', 'price_from', 'price_till', 'tickets_website',
            'age_from', 'age_till', 'edu_offer_website',
            'location_title',
            'street_address', 'street_address2', 'postal_code', 'city', 'country',
            'latitude', 'longitude',
            'status', 'classiccard',
        ]
        filtering = {
            'creation_date': ALL,
            'modified_date': ALL,
            'status': ALL,
            'categories': ALL_WITH_RELATIONS,
            'in_program_of': ALL_WITH_RELATIONS,
            'play_locations': ALL_WITH_RELATIONS,
        }

    def dehydrate(self, bundle):
        if bundle.obj.status not in ["published"]:
            bundle.data = {
                'id':  bundle.obj.id,
                'status': bundle.obj.status,
                'creation_date': bundle.obj.creation_date,
                'modified_date': bundle.obj.modified_date,
            }
            return bundle

        current_language = get_language()
        for lang_code, lang_name in settings.FRONTEND_LANGUAGES:
            try:
                activate(lang_code)
                path = reverse('production_detail', kwargs={'slug': bundle.obj.slug})
                bundle.data['link_%s' % lang_code] = "".join((get_website_url(), path))
            except:
                pass
        activate(current_language)

        bundle.data['description_de'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_description_de()))
        bundle.data['description_en'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_description_en()))
        bundle.data['teaser_de'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_teaser_de()))
        bundle.data['teaser_en'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_teaser_en()))
        bundle.data['work_info_de'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_work_info_de()))
        bundle.data['work_info_en'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_work_info_en()))
        bundle.data['contents_de'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_contents_de()))
        bundle.data['contents_en'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_contents_en()))
        bundle.data['press_text_de'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_press_text_de()))
        bundle.data['press_text_en'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_press_text_en()))
        bundle.data['credits_de'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_credits_de()))
        bundle.data['credits_en'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_credits_en()))
        bundle.data['concert_program_de'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_concert_program_de()))
        bundle.data['concert_program_en'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_concert_program_en()))
        bundle.data['supporting_program_de'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_supporting_program_de()))
        bundle.data['supporting_program_en'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_supporting_program_en()))
        bundle.data['remarks_de'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_remarks_de()))
        bundle.data['remarks_en'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_remarks_en()))
        bundle.data['price_information_de'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_price_information_de()))
        bundle.data['price_information_en'] = strip_invalid_chars(strip_html(bundle.obj.get_rendered_price_information_en()))

        return bundle

    def apply_filters(self, request, applicable_filters):
        from dateutil.parser import parse
        base_object_list = super(ProductionResource, self).apply_filters(request, applicable_filters)
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

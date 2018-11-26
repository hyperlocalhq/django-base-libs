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

from ruhrbuehnen.apps.locations.api.resources.v1 import LocationResource

from ruhrbuehnen.apps.festivals.models import Festival
from ruhrbuehnen.apps.festivals.models import SocialMediaChannel
from ruhrbuehnen.apps.festivals.models import Image
from ruhrbuehnen.apps.festivals.models import FestivalPDF

from ruhrbuehnen.apps.productions.api.resources.v1 import ProductionResource


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


class FestivalSocialMediaChannelResource(ModelResource):
    class Meta(BaseMetaForModelResource):
        queryset = SocialMediaChannel.objects.all()
        resource_name = 'festival_social_media'
        excludes = []


class FestivalImageResource(ModelResource):
    class Meta(BaseMetaForModelResource):
        queryset = Image.objects.exclude(copyright_restrictions="protected")
        resource_name = 'festival_image'
        fields = [
            'id',
            'creation_date',
            'modified_date',
            'copyright_restrictions',
            'sort_order',
        ]

    def get_object_list(self, request):
        object_list = super(FestivalImageResource,
                            self).get_object_list(request)
        object_list = object_list.exclude(copyright_restrictions="protected")
        return object_list

    def dehydrate(self, bundle):
        if bundle.obj.path:
            bundle.data['url'] = "".join(
                (
                    get_website_url(),
                    settings.MEDIA_URL[1:],
                    bundle.obj.path.path,
                )
            )
            list_image_path, query_params = FileManager.modified_path(
                bundle.obj.path.path, "list_image"
            )
            if list_image_path:
                bundle.data['list_image_url'] = "".join(
                    (
                        get_website_url(),
                        settings.MEDIA_URL[1:],
                        list_image_path,
                    )
                )
            try:
                file_description = FileDescription.objects.filter(
                    file_path=bundle.obj.path,
                ).order_by("pk")[0]
            except:
                pass
            else:
                bundle.data['title_de'] = strip_invalid_chars(
                    file_description.title_de
                )
                bundle.data['title_en'] = strip_invalid_chars(
                    file_description.title_en
                )
                bundle.data['description_de'] = strip_invalid_chars(
                    file_description.description_de
                )
                bundle.data['description_en'] = strip_invalid_chars(
                    file_description.description_en
                )
                bundle.data['author'] = strip_invalid_chars(
                    file_description.author
                )
                bundle.data['photographer'] = strip_invalid_chars(
                    file_description.author
                )
                bundle.data['copyright'] = strip_invalid_chars(
                    file_description.copyright_limitations
                )
        if not bundle.data.get('copyright', None):
            bundle.data['copyright'] = "Promo"
        return bundle


class FestivalPDFResource(ModelResource):
    class Meta(BaseMetaForModelResource):
        queryset = FestivalPDF.objects.all()
        resource_name = 'festival_pdf'
        fields = [
            'id',
            'creation_date',
            'modified_date',
            'sort_order',
        ]

    def dehydrate(self, bundle):
        if bundle.obj.path:
            bundle.data['url'] = "".join(
                (
                    get_website_url(),
                    settings.MEDIA_URL[1:],
                    bundle.obj.path.path,
                )
            )
            try:
                file_description = FileDescription.objects.filter(
                    file_path=bundle.obj.path,
                ).order_by("pk")[0]
            except:
                pass
            else:
                bundle.data['title_de'] = strip_invalid_chars(
                    file_description.title_de
                )
                bundle.data['title_en'] = strip_invalid_chars(
                    file_description.title_en
                )
                bundle.data['description_de'] = strip_invalid_chars(
                    file_description.description_de
                )
                bundle.data['description_en'] = strip_invalid_chars(
                    file_description.description_en
                )
                bundle.data['author'] = strip_invalid_chars(
                    file_description.author
                )
                bundle.data['copyright'] = strip_invalid_chars(
                    file_description.copyright_limitations
                )
        if not bundle.data.get('copyright', None):
            bundle.data['copyright'] = "Promo"
        return bundle


class FestivalResource(ModelResource):
    organizers = fields.ToManyField(LocationResource, "organizers")

    images = fields.ToManyField(FestivalImageResource, attribute=(lambda bundle: bundle.obj.image_set.exclude(copyright_restrictions="protected")), full=True, null=True, blank=True)
    pdfs = fields.ToManyField(FestivalPDFResource, "festivalpdf_set", full=True)
    social_media = fields.ToManyField(
        FestivalSocialMediaChannelResource, "socialmediachannel_set", full=True
    )

    productions = fields.ToManyField(ProductionResource, "production_set")

    class Meta(BaseMetaForModelResource):
        queryset = Festival.objects.all()
        resource_name = 'festival'
        fields = [
            'id',
            'creation_date',
            'modified_date',
            'title_de',
            'title_en',
            'subtitle_de',
            'subtitle_en',
            'street_address',
            'street_address2',
            'postal_code',
            'city',
            'country',
            'latitude',
            'longitude',
            'email',
            'website',
            'tickets_street_address',
            'tickets_street_address2',
            'tickets_postal_code',
            'tickets_city',
            'tickets_country',
            'press_contact_name',
            'press_street_address',
            'press_street_address2',
            'press_postal_code',
            'press_city',
            'press_country',
            'press_email',
            'press_website',
            'start',
            'end',
            'status',
        ]
        filtering = {
            'creation_date': ALL,
            'modified_date': ALL,
            'status': ALL,
            'organizers': ALL_WITH_RELATIONS,
            'productions': ALL_WITH_RELATIONS,
        }

    def dehydrate(self, bundle):
        current_language = get_language()
        for lang_code, lang_name in settings.FRONTEND_LANGUAGES:
            try:
                activate(lang_code)
                path = reverse(
                    'festival_detail', kwargs={'slug': bundle.obj.slug}
                )
                bundle.data['link_%s' % lang_code] = "".join(
                    (get_website_url()[:-1], path)
                )
            except:
                pass
        activate(current_language)

        if bundle.obj.logo:
            bundle.data['logo_url'] = "".join(
                (
                    get_website_url(),
                    settings.MEDIA_URL[1:],
                    bundle.obj.logo.path,
                )
            )

        bundle.data['description_de'] = strip_invalid_chars(
            strip_html(bundle.obj.get_rendered_description_de())
        )
        bundle.data['description_en'] = strip_invalid_chars(
            strip_html(bundle.obj.get_rendered_description_en())
        )

        if bundle.obj.phone_number:
            bundle.data['phone'] = [
                bundle.obj.phone_country, bundle.obj.phone_area,
                bundle.obj.phone_number
            ]
        if bundle.obj.fax_number:
            bundle.data['fax'] = [
                bundle.obj.fax_country, bundle.obj.fax_area,
                bundle.obj.fax_number
            ]

        if bundle.obj.tickets_phone_number:
            bundle.data['tickets_phone'] = [
                bundle.obj.tickets_phone_country, bundle.obj.tickets_phone_area,
                bundle.obj.tickets_phone_number
            ]
        if bundle.obj.tickets_fax_number:
            bundle.data['tickets_fax'] = [
                bundle.obj.tickets_fax_country, bundle.obj.tickets_fax_area,
                bundle.obj.tickets_fax_number
            ]

        if bundle.obj.press_phone_number:
            bundle.data['press_phone'] = [
                bundle.obj.press_phone_country, bundle.obj.press_phone_area,
                bundle.obj.press_phone_number
            ]
        if bundle.obj.press_fax_number:
            bundle.data['press_fax'] = [
                bundle.obj.press_fax_country, bundle.obj.press_fax_area,
                bundle.obj.press_fax_number
            ]

        bundle.data['tickets_calling_prices_de'] = strip_invalid_chars(
            strip_html(bundle.obj.get_rendered_tickets_calling_prices_de())
        )
        bundle.data['tickets_calling_prices_en'] = strip_invalid_chars(
            strip_html(bundle.obj.get_rendered_tickets_calling_prices_en())
        )

        return bundle

    def apply_filters(self, request, applicable_filters):
        from dateutil.parser import parse
        base_object_list = super(FestivalResource, self).apply_filters(
            request, applicable_filters
        )
        created_or_modified_since = request.GET.get(
            'created_or_modified_since', None
        )
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

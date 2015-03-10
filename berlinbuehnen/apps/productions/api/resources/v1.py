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

from filebrowser.models import FileDescription

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



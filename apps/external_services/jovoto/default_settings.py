# -*- coding: UTF-8 -*-
from django.conf import settings

""" we need that in the templates to get the absilute url to the images."""
JOVOTO_ROOT_DIR = getattr(settings, "JOVOTO_ROOT_DIR", "http://www.jovoto.com")

"""
this constant is the number of retires for getting idea details
from the webservices, before an error is raised
"""
JOVOTO_NOF_REQUEST_RETRIES = getattr(settings, "JOVOTO_NOF_REQUEST_RETRIES", 4)

"""
currently, Jovoto provides dates in RFC2822 Format.
if there is a custom date format specified, set the
IDEA_DATE_FORMAT below to a valid date formating string.
For RFC2822 format, set it to "RFC822"
"""
# IDEA_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
IDEA_DATE_FORMAT = getattr(settings, "IDEA_DATE_FORMAT", "RFC822")

JOVOTO_SERVICE_USERNAME = getattr(settings, "JOVOTO_SERVICE_USERNAME", "test_studio38")
JOVOTO_SERVICE_PASSWORD = getattr(settings, "JOVOTO_SERVICE_PASSWORD", "holladrio")

JOVOTO_WEBSERVICE = 'http://%s:%s@www.jovoto.com/contests/creative-city-berlin.{format=xml}' % (
    JOVOTO_SERVICE_USERNAME,
    JOVOTO_SERVICE_PASSWORD,
)

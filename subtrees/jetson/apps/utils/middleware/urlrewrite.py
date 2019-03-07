# -*- coding: UTF-8 -*-
import re
from django.conf import settings
from django.contrib.sites.models import Site

SUBDOMAIN_MNG_DIR = getattr(settings, "SUBDOMAIN_MNG_DIR", "profile/")
SUBDOMAINS_SUPPORTED = getattr(settings, "SUBDOMAINS_SUPPORTED", False)


class URLRewriteMiddleware(object):
    """Middleware that manages urls with subdomains
    """

    def process_request(self, request):
        """change path
        (x).example.com/(y) -> example.com/profiles/(x)/(y)
        exception: www.example.com
        """
        if SUBDOMAINS_SUPPORTED:
            site = Site.objects.get_current()
            subdomain = request.META['HTTP_HOST'][:-len(site.domain) - 1]
            if subdomain and subdomain != "www":
                path = request.path[1:]
                request.path = "/%s%s/%s" % (SUBDOMAIN_MNG_DIR, subdomain, path)
        return None

    def process_response(self, request, response):
        """change links
        "http://example.com/profiles/(x)/(y)" -> "http://(x).example.com/(y)"
        "/profiles/(x)/(y)" -> "http://(x).example.com/(y)"
        """
        if SUBDOMAINS_SUPPORTED:
            site = Site.objects.get_current()
            content = re.sub(
                r'"(https?://)(%s)(/)(%s)([^/]+)/([^"]*)"' %
                (re.escape(site.domain), re.escape(SUBDOMAIN_MNG_DIR)),
                r'"\1\5.\2\3\6"', response.content
            )
            current_protocol = int(request.META['SERVER_PORT']
                                  ) == 443 and "https" or "http"
            response.content = re.sub(
                r'"(/)(%s)([^/]+)/([^"]*)"' % re.escape(SUBDOMAIN_MNG_DIR),
                r'"%s://\3.%s\1\4"' % (current_protocol, site.domain), content
            )
        return response

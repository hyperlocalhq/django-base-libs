# -*- coding: utf-8 -*-
import re

from cms.middleware.multilingual import *
from cms.middleware.multilingual import MultilingualURLMiddleware as BaseMultilingualURLMiddleware
from cms.middleware.toolbar import ToolbarMiddleware
#from cms.middleware.media import PlaceholderMediaMiddleware

from django.conf import settings

ADMIN_PATH = getattr(settings, "ADMIN_PATH", "/admin/")
DEFAULT_ADMIN_MEDIA_PATH = getattr(settings, "DEFAULT_ADMIN_MEDIA_PATH", "/media/default_admin/")

ADMIN_SUB = re.compile(ur'<link([^>]+)href="%s([^"]*)"([^>]*)>' % (
    re.escape(settings.ADMIN_MEDIA_PREFIX)
))

ADMIN_SUB2 = re.compile(ur'<script([^>]+)src="%s([^"]*)"([^>]*)>' % (
    re.escape(settings.ADMIN_MEDIA_PREFIX)
))

class MultilingualURLMiddleware(BaseMultilingualURLMiddleware):
    """
    Applies multilingual url change only to non-admin pages
    """
    # multilingual url middleware shouldn't be active for some jetson-related paths
    def process_response(self, request, response):
        language = getattr(request, 'LANGUAGE_CODE', self.get_language_from_request(request))
        local_middleware = LocaleMiddleware()
        response =local_middleware.process_response(request, response)
        path = unicode(request.path)

        # note: pages_root is assumed to end in '/'.
        #       testing this and throwing an exception otherwise, would probably be a good idea
        pages_root = urllib.unquote(reverse("pages-root"))

        if not path.startswith(settings.MEDIA_URL) and \
                not path.startswith(settings.UPLOADS_URL) and \
                not path.startswith(settings.JETSON_MEDIA_URL) and \
                not path.startswith(ADMIN_PATH) and \
                not path.startswith(settings.ADMIN_MEDIA_PREFIX) and \
                response.status_code == 200 and \
                response._headers['content-type'][1].split(';')[0] == "text/html":
            try:
                decoded_response = response.content.decode('utf-8')
            except UnicodeDecodeError:
                decoded_response = response.content

            # Customarily user pages are served from http://the.server.com/~username/
            # When a user uses django-cms for his pages, the '~' of the url appears quoted in href links.
            # We have to quote pages_root for the regular expression to match.
            #
            # The used regex is quite complex. The exact pattern depends on the used settings.
            # The regex extracts the path of the url without the leading page root, but only matches urls
            # that don't already contain a language string or aren't considered multilingual.
            #
            # Here is an annotated example pattern (_r_ is a shorthand for the value of pages_root):
            #   pattern:        <a([^>]+)href="(?=_r_)(?!(/fr/|/de/|/en/|/pt-br/|/media/|/media/admin/))(_r_([^"]*))"([^>]*)>
            #                     |-\1--|                |---------------------\2---------------------| |   |-\4--|| |-\5--|
            #                                                                                           |----\3----|
            #   input (_r_=/):  <a href="/admin/password_change/" class="foo">
            #   matched groups: (u' ', None, u'/admin/password_change/', u'admin/password_change/', u' class="foo"')
            #
            # Notice that (?=...) and (?!=...) do not consume input or produce a group in the match object.
            # If the regex matches, the extracted path we want is stored in the fourth group (\4).
            HREF_URL_FIX_RE = re.compile(ur'<a([^>]+)href="(?=%s)(?!(%s|%s|%s|%s|%s|%s))(%s([^"]*))"([^>]*)>' % (
                urllib.quote(pages_root),
                "|".join(map(lambda l: urllib.quote(pages_root) + l[0] + "/" , settings.CMS_LANGUAGES)),
                settings.MEDIA_URL,
                settings.UPLOADS_URL,
                settings.JETSON_MEDIA_URL,
                ADMIN_PATH,
                settings.ADMIN_MEDIA_PREFIX,
                urllib.quote(pages_root)
            ))

            # Unlike in href links, the '~' (see above) the '~' in form actions appears unquoted.
            #
            # For understanding this regex, please read the documentation for HREF_URL_FIX_RE above.
            FORM_URL_FIX_RE = re.compile(ur'<form([^>]+)action="(?=%s)(?!(%s|%s|%s|%s|%s|%s))(%s([^"]*))"([^>]*)>' % (
                pages_root,
                "|".join(map(lambda l: pages_root + l[0] + "/" , settings.CMS_LANGUAGES)),
                settings.MEDIA_URL,
                settings.UPLOADS_URL,
                settings.JETSON_MEDIA_URL,
                ADMIN_PATH,
                settings.ADMIN_MEDIA_PREFIX,
                pages_root
            ))

            # Documentation comments for HREF_URL_FIX_RE above explain each match group (\1, \4, \5) represents.
            decoded_response = HREF_URL_FIX_RE.sub(ur'<a\1href="%s%s/\4"\5>' % (pages_root, request.LANGUAGE_CODE), decoded_response)
            response.content = FORM_URL_FIX_RE.sub(ur'<form\1action="%s%s/\4"\5>' % (pages_root, request.LANGUAGE_CODE), decoded_response).encode("utf8")

        if (response.status_code == 301 or response.status_code == 302 ):
            location = response['Location']
            if not has_lang_prefix(location) and location.startswith("/") and \
                    not location.startswith(settings.MEDIA_URL) and \
                    not location.startswith(settings.UPLOADS_URL) and \
                    not location.startswith(settings.JETSON_MEDIA_URL) and \
                    not location.startswith(ADMIN_PATH) and \
                    not location.startswith(settings.ADMIN_MEDIA_PREFIX):
                response['Location'] = "%s%s%s" % (pages_root, language, location[len(pages_root)-1:])
        response.set_cookie("django_language", language)
        return response

'''
if not hasattr(ToolbarMiddleware, "_patched"):
    # toolbar shouldn't be shown for some jetson-related paths
    _old_show_toolbar = ToolbarMiddleware.should_show_toolbar
    def _show_toolbar(self, request):
        path = request.path
        if (
            path.startswith(settings.UPLOADS_URL) or
            path.startswith(settings.JETSON_MEDIA_URL) or
            path.startswith(ADMIN_PATH) or 
            path.startswith(settings.ADMIN_MEDIA_PREFIX)
            ):
            return False
        return _old_show_toolbar(self, request)
    ToolbarMiddleware.should_show_toolbar = _show_toolbar
    ToolbarMiddleware._patched = True
'''

'''
if not hasattr(PlaceholderMediaMiddleware, "_patched"):
    # placeholder media shouldn't be injected for some jetson-related paths
    _old_inject_media = PlaceholderMediaMiddleware.inject_media
    def _inject_media(self, request, response):
        path = request.path
        if (
            path.startswith(settings.UPLOADS_URL) or
            path.startswith(settings.JETSON_MEDIA_URL) or
            path.startswith(ADMIN_PATH) or 
            path.startswith(settings.ADMIN_MEDIA_PREFIX)
            ):
            return False
        return _old_inject_media(self, request, response)
    PlaceholderMediaMiddleware.inject_media = _inject_media
    PlaceholderMediaMiddleware._patched = True
'''

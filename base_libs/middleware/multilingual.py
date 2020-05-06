# -*- coding: utf-8 -*-

import re
import urllib

from django import http
from django.conf import settings
from django.middleware.locale import LocaleMiddleware
from django.utils import translation
from django.utils.encoding import force_unicode

ADMIN_PATH = getattr(settings, "ADMIN_PATH", "/admin/")

PATHS_NO_REDIRECTION = getattr(
    settings,
    "PATHS_NO_REDIRECTION",
    (settings.MEDIA_URL, ADMIN_PATH, settings.ADMIN_MEDIA_PREFIX),
)

SUPPORTED = dict(settings.LANGUAGES)

HAS_LANG_PREFIX_RE = re.compile(
    r"^/(%s)/.*" % "|".join(map(lambda l: l[0], settings.LANGUAGES))
)


def has_lang_prefix(path):
    check = HAS_LANG_PREFIX_RE.match(path)
    if check is not None:
        return check.group(1)
    else:
        return False


class MultilingualURLMiddleware:
    """
    Applies multilingual url change only to non-admin and non media pages
    """

    def __init__(self):
        pass

    def get_language_from_request(self, request):
        changed = False
        prefix = has_lang_prefix(request.path_info)
        lang = None
        if prefix:
            request.path = "/" + "/".join(
                (request.META.get("SCRIPT_URL", "") or request.path).split("/")[2:]
            )
            request.path_info = "/" + "/".join(
                (request.META.get("SCRIPT_URL", "") or request.path_info).split("/")[2:]
            )
            t = prefix
            if t in SUPPORTED:
                lang = t
                if hasattr(request, "session"):
                    request.session["django_language"] = lang
                changed = True
        else:
            lang = translation.get_language_from_request(request)
        if not changed:
            if hasattr(request, "session"):
                lang = request.session.get("django_language", None)
                if lang in SUPPORTED and lang is not None:
                    return lang
            elif "django_language" in request.COOKIES.keys():
                lang = request.COOKIES.get("django_language", None)
                if lang in SUPPORTED and lang is not None:
                    return lang
            if not lang:
                lang = translation.get_language_from_request(request)
        if not lang:
            lang = settings.LANGUAGE_CODE
        return lang

    def process_request(self, request):
        # according to http://www.mail-archive.com/django-users@googlegroups.com/msg60760.html double slashes are collapsed by Apache, so restoring the original path from SCRIPT_URL
        path = request.META.get("SCRIPT_URL", "") or request.path
        language = self.get_language_from_request(request)
        translation.activate(language)
        request.LANGUAGE_CODE = language
        if not has_lang_prefix(path) and (
            True not in (path.startswith(p) for p in PATHS_NO_REDIRECTION)
        ):
            new_path = "/%s%s" % (language, path)
            return http.HttpResponsePermanentRedirect(new_path)

    # multilingual url middleware shouldn't be active for some jetson-related paths
    def process_response(self, request, response):
        language = getattr(
            request, "LANGUAGE_CODE", self.get_language_from_request(request)
        )
        local_middleware = LocaleMiddleware()
        response = local_middleware.process_response(request, response)
        path = force_unicode(request.path)

        # note: pages_root is assumed to end in '/'.
        # testing this and throwing an exception otherwise, would probably be a good idea
        pages_root = "/"

        if (
            (True not in (path.startswith(p) for p in PATHS_NO_REDIRECTION))
            and response.status_code == 200
            and response["Content-Type"].split(";")[0] == "text/html"
        ):
            try:
                decoded_response = response.content.decode("utf-8")
            except UnicodeDecodeError:
                decoded_response = response.content

            # Customarily user pages are served from http://the.server.com/~username/
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
            HREF_URL_FIX_RE = re.compile(
                ur'<a([^>]+)href="(?=%s)(?!(%s|%s))(%s([^"]*))"([^>]*)>'
                % (
                    urllib.quote(pages_root),
                    "|".join(
                        map(
                            lambda l: urllib.quote(pages_root) + l[0] + "/",
                            settings.LANGUAGES,
                        )
                    ),
                    "|".join(PATHS_NO_REDIRECTION),
                    urllib.quote(pages_root),
                )
            )

            # Unlike in href links, the '~' (see above) the '~' in form actions appears unquoted.
            #
            # For understanding this regex, please read the documentation for HREF_URL_FIX_RE above.
            FORM_URL_FIX_RE = re.compile(
                ur'<form([^>]+)action="(?=%s)(?!(%s|%s))(%s([^"]*))"([^>]*)>'
                % (
                    pages_root,
                    "|".join(
                        map(lambda l: pages_root + l[0] + "/", settings.LANGUAGES)
                    ),
                    "|".join(PATHS_NO_REDIRECTION),
                    pages_root,
                )
            )

            # Documentation comments for HREF_URL_FIX_RE above explain each match group (\1, \4, \5) represents.
            decoded_response = HREF_URL_FIX_RE.sub(
                ur'<a\1href="%s%s/\4"\5>' % (pages_root, request.LANGUAGE_CODE),
                decoded_response,
            )
            response.content = FORM_URL_FIX_RE.sub(
                ur'<form\1action="%s%s/\4"\5>' % (pages_root, request.LANGUAGE_CODE),
                decoded_response,
            ).encode("utf8")

        if response.status_code == 301 or response.status_code == 302:
            location = response["Location"]
            if (
                not has_lang_prefix(location)
                and location.startswith("/")
                and (True not in (location.startswith(p) for p in PATHS_NO_REDIRECTION))
            ):
                response["Location"] = "/%s%s" % (language, location)
        request.path = "/%s%s" % (language, path)
        request.path_info = "/%s%s" % (language, path)
        response.set_cookie("django_language", language)
        return response

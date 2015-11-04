## code taken from "Fixing Site-Wide Caching in Django":
## https://www.silviogutierrez.com/blog/fixing-site-wide-caching-django/

## update code to ignore all non-django cookies, using example from:
## http://www.stavros.io/posts/djangos-site-caching-doesnt-work/

from django.middleware.cache import UpdateCacheMiddleware

import re

class SmartUpdateCacheMiddleware(UpdateCacheMiddleware):
    def process_request(self, request):
        cookies = request.META.get('HTTP_COOKIE', '')

        # Strip all non-Django cookies.
        new_cookies = []
        for cookie in re.split("\;\s*", cookies):
            key, value = cookie.split("=")
            if "=" not in cookie:
                continue
            if key.lower().strip() in (
                "csrftoken",
                "sessionid",
                "djdt", # used by Django Debug Toolbar
                "__json_message", # used by django.contrib.messages
            ):
                new_cookies.append("%s=%s" % (key, value))
        request.META['HTTP_COOKIE'] = "; ".join(new_cookies)

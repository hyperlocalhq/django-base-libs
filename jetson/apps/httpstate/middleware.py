import time

from django.conf import settings
from django.utils.cache import patch_vary_headers
from django.utils.http import cookie_date
from django.utils.importlib import import_module

from jetson.apps.httpstate import settings as httpstate_settings

'''
LEAVE_AS_IS = (
    settings.MEDIA_URL,
    settings.JETSON_MEDIA_URL,
    settings.ADMIN_MEDIA_PREFIX,
    "/browse/",
    "/search/",
    "/simplesearch/",
    "/people/",
    "/person/",
    "/institutions/",
    "/institution/",
    "/events/",
    "/event/",
    "/documents/",
    "/document/",
    "/groups/",
    "/group/",
    "/i18n/",
    "/jsi18n/",
    "/jssettings/",
    "/helper/",
    "/admin/",
    "/gmap/",
    "/test-session/",
    )
'''

class HttpStateMiddleware(object):
    def process_request(self, request):
        engine = import_module(httpstate_settings.HTTPSTATE_ENGINE)
        httpstate_key = request.COOKIES.get(httpstate_settings.HTTPSTATE_COOKIE_NAME, None)
        request.httpstate = engine.HttpStateStore(httpstate_key)
        
        '''
        # TODO Maybe, we do not need those cleanups??????????????
        # do cleanups
        path = request.path
        remove_qs_vars = False #TODO True does not work for person lists!!!!!!!!!!!!!!!
        
        leave_as_is = LEAVE_AS_IS + tuple(
            getattr(settings, "OTHER_URLS_LEAVE_AS_IS", ())
            )
        
        for excepted in leave_as_is:
            if path.startswith(excepted):
                remove_qs_vars = False
                break
        if remove_qs_vars:
            if "source_list" in request.httpstate:
                del request.httpstate['source_list']
            if "current_object_id" in request.httpstate:
                del request.httpstate['current_object_id']                  
            if "current_queryset" in request.httpstate:
                del request.httpstate['current_queryset']
            if "current_queryset_index_dict" in request.httpstate:
                del request.httpstate['current_queryset_index_dict']
        '''

    def process_response(self, request, response):
        """
        If request.httpstate was modified, or if the configuration is to save the
        httpstate every time, save the changes and set a httpstate cookie.
        """
        try:
            accessed = request.httpstate.accessed
            modified = request.httpstate.modified
        except AttributeError:
            pass
        else:
            if accessed:
                patch_vary_headers(response, ('Cookie',))
            if modified or httpstate_settings.HTTPSTATE_SAVE_EVERY_REQUEST:
                if request.httpstate.get_expire_at_browser_close():
                    max_age = None
                    expires = None
                else:
                    max_age = request.httpstate.get_expiry_age()
                    expires_time = time.time() + max_age
                    expires = cookie_date(expires_time)
                # Save the httpstate data and refresh the client cookie.
                request.httpstate.save()
                response.set_cookie(httpstate_settings.HTTPSTATE_COOKIE_NAME,
                        request.httpstate.httpstate_key, max_age=max_age,
                        expires=expires, domain=httpstate_settings.HTTPSTATE_COOKIE_DOMAIN,
                        path=httpstate_settings.HTTPSTATE_COOKIE_PATH,
                        secure=httpstate_settings.HTTPSTATE_COOKIE_SECURE or None,
                        httponly=httpstate_settings.HTTPSTATE_COOKIE_HTTPONLY or None)
        return response

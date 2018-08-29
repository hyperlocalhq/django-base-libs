# -*- coding: UTF-8 -*-
from django.http import HttpResponseForbidden

BOT_NAMES = [
    'Googlebot',
    'Slurp',
    'Twiceler',
    'msnbot',
    'KaloogaBot',
    'YodaoBot',
    'Baiduspider',
    'googlebot',
    'Speedy Spider',
    'DotBot',
]

PARAM_NAME = 'block_bots'


class BotDetectorMiddleware:
    def process_request(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', None)

        if not user_agent:
            return HttpResponseForbidden('Requests without user agent are not supported.')

        request.is_crawler = False
        for botname in BOT_NAMES:
            if botname in user_agent:
                request.is_crawler = True
                break

    def process_view(self, request, view_func, view_args, view_kwargs):
        if PARAM_NAME in view_kwargs:
            if view_kwargs[PARAM_NAME]:
                del view_kwargs[PARAM_NAME]
                if request.is_crawler:
                    return HttpResponseForbidden('Path excluded from crawling.')

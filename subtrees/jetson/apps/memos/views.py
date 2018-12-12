# -*- coding: UTF-8 -*-
import json
from datetime import datetime, timedelta

from django.template import RequestContext
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.cache import never_cache
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode
from django.conf import settings
from django.utils.timezone import now as tz_now

from base_libs.utils.misc import ExtendedJSONEncoder
from jetson.apps.memos.models import MemoCollection, Memo, MEMO_TOKEN_NAME, MEMO_COOKIE_AGE
from jetson.apps.httpstate import settings as httpstate_settings


def json_set_memo(request, content_type_id, object_id):
    """Sets the object as a memo in a memo collection of the current client"""
    content_type = ContentType.objects.get(id=content_type_id)
    collection = MemoCollection.objects.get_updated(
        token=request.COOKIES.get(MEMO_TOKEN_NAME, None),
    )
    memo, created = collection.memo_set.get_or_create(
        content_type=content_type,
        object_id=object_id,
    )
    action = "added"
    if not created:
        memo.delete()
        action = "removed"
    result = {
        'action': action,
        'memo_count': collection.memo_set.count(),
    }
    json_str = json.dumps(result, ensure_ascii=False, cls=ExtendedJSONEncoder)
    response = HttpResponse(
        json_str, content_type='text/javascript; charset=utf-8'
    )
    if collection.memo_set.count():
        # update expiration date
        collection.expiration = tz_now() + MEMO_COOKIE_AGE
        collection.save()
        response.set_cookie(
            MEMO_TOKEN_NAME,
            collection.token,
            expires=collection.expiration_display(),
            domain=httpstate_settings.HTTPSTATE_COOKIE_DOMAIN,
        )
    else:
        collection.delete()
        response.delete_cookie(
            MEMO_TOKEN_NAME,
            domain=httpstate_settings.HTTPSTATE_COOKIE_DOMAIN,
        )
    return response


json_set_memo = never_cache(json_set_memo)


def memos(request, **kwargs):
    """ 
    Displays the list of memorized objects
    """
    collection = None
    memos = []
    delete_cookie = False
    if MEMO_TOKEN_NAME in request.COOKIES:
        try:
            collection = MemoCollection.objects.get(
                token=request.COOKIES[MEMO_TOKEN_NAME],
            )
        except:
            # if a token is set in the cookie, but has no matching memo collection, then delete the cookie
            delete_cookie = True
        else:
            if collection.memo_set.count():
                memos = collection.memo_set.all()
            else:
                # don't keep empty collections in the database
                collection.delete()
                delete_cookie = True

    response = render_to_response(
        kwargs["template_name"], {
            'object_list': memos,
        },
        context_instance=RequestContext(request)
    )
    if delete_cookie:
        response.delete_cookie(
            MEMO_TOKEN_NAME,
            domain=httpstate_settings.HTTPSTATE_COOKIE_DOMAIN,
        )
    else:
        if collection:
            # update expiration date
            collection.expiration = tz_now() + MEMO_COOKIE_AGE
            collection.save()
            response.set_cookie(
                MEMO_TOKEN_NAME,
                collection.token,
                expires=collection.expiration_display(),
                domain=httpstate_settings.HTTPSTATE_COOKIE_DOMAIN,
            )
    return response

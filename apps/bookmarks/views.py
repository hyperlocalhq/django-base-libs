# -*- coding: UTF-8 -*-
import json

from django.db import models
from django.template import RequestContext
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.cache import never_cache
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode

from base_libs.middleware import get_current_user
from base_libs.utils.misc import ExtendedJSONEncoder

Bookmark = models.get_model("bookmarks", "Bookmark")

def bookmarks(request, **kwargs):
    """
    Displays the list of memorized objects
    """
    bookmarks = Bookmark.objects.filter(creator = get_current_user())
        
    return render_to_response(kwargs["template_name"], {
        'object_list': bookmarks,
    }, context_instance=RequestContext(request))
    
    
def json_manage_bookmark(request):
    """
    Sets the given url_path as a bookmark for the current user
    
    _("...") returns a class extending string, but not a string
    so we need to convert it to string for JSON serialization below
    """
    result = {}
    if request.user.is_authenticated():
        data = {
            'action': 'add',
            'title': '',
            'id': None,
            'url_path': '',
        }
        data.update(dict([(item[0], item[1]) for item in request.GET.items()]))
        action = data['action']
        result['action'] = action
        if action in ("add", "rename"):
            if data['title']:
                title = data['title']
            else:
                result['error'] = force_unicode(_("Please enter a title for your bookmark"))
        if action == 'add' and not data['url_path']:
            return Http404, "Keep trying, hacker!"
        if action in ('rename', 'delete') and not data['id']:
            return Http404, "Keep trying, hacker!"
        if action == 'add':
            bookmark, is_created = Bookmark.objects.get_or_create(
                url_path = data['url_path'],
                creator = request.user,
                defaults = {'title': data['title']},
                )
            if is_created:
                # we only need title and url_path for all my bookmarks
                #for bookmark in Bookmark.objects.filter(creator = request.user):
                result.update({
                    'id': bookmark.id,
                    'title': bookmark.title,
                    'url_path': bookmark.url_path,
                    })
            else:
                result['error'] = force_unicode(_("This page is already bookmarked as \"%s\"" % unicode(bookmark.title)))
        elif action == 'rename':
            try:
                bookmark = Bookmark.objects.get(
                    creator = request.user,
                    id = data["id"],
                    )
            except:
                result['error'] = force_unicode(_("The bookmark doesn't exist"))
            else:
                bookmark.title = data['title']
                bookmark.save()
                result.update({
                    'id': bookmark.id,
                    'title': bookmark.title,
                    'url_path': bookmark.url_path,
                    })
        if action == 'delete':
            try:
                bookmark = Bookmark.objects.get(
                    creator = request.user,
                    id = data["id"],
                    )
            except:
                result['error'] = force_unicode(_("The bookmark doesn't exist"))
            else:
                bookmark.delete()
    else:
        result['error'] = force_unicode(_("You do not have the permission for this action."))
    json_str = json.dumps(result, ensure_ascii=False, cls=ExtendedJSONEncoder)
    return HttpResponse(json_str, content_type='text/javascript; charset=utf-8')
json_manage_bookmark = never_cache(json_manage_bookmark)

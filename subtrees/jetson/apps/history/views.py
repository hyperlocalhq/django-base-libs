# -*- coding: UTF-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404, render_to_response
from django import template
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.utils.encoding import force_unicode
from django.apps import apps
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from jetson.apps.history.models import ExtendedLogEntry


def object_history(request, app_label, model_name, object_id):
    model = apps.get_model(app_label, model_name)
    if model is None:
        raise Http404("App %r, model %r, not found" % (app_label, model_name))
    action_list = ExtendedLogEntry.objects.filter(
        object_id=object_id,
        content_type=ContentType.objects.get_for_model(model),
    ).select_related().order_by('action_time')

    # paginate results
    paginator = Paginator(action_list, 50)
    page = request.GET.get('p')
    try:
        action_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        action_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        action_list = paginator.page(paginator.num_pages)

    # If no history was found, see whether this object even exists.
    obj = get_object_or_404(model, pk=object_id)
    extra_context = {
        'title':
            _('Change history: %s') % obj,
        'action_list':
            action_list,
        'paginator':
            paginator,
        'app_label':
            app_label,
        'model_name':
            force_unicode(model._meta.verbose_name_plural).capitalize(),
        'object':
            obj,
        'opts':
            obj._meta,
    }
    return render_to_response(
        [
            "admin/%s/%s/object_history.html" %
            (app_label, model._meta.object_name.lower()),
            "admin/%s/object_history.html" % app_label,
            "admin/object_history.html",
        ],
        extra_context,
        context_instance=template.RequestContext(request),
    )


object_history = staff_member_required(never_cache(object_history))


def user_activity_history(request, object_id):
    action_list = ExtendedLogEntry.objects.filter(
        user__pk=object_id,
    ).select_related().order_by('-action_time')

    # paginate results
    paginator = Paginator(action_list, 50)
    page = request.GET.get('p')
    try:
        action_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        action_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        action_list = paginator.page(paginator.num_pages)

    # If no history was found, see whether this object even exists.
    obj = get_object_or_404(User, pk=object_id)
    extra_context = {
        'title':
            _('Change history: %s') % obj,
        'action_list':
            action_list,
        'paginator':
            paginator,
        'model_name':
            force_unicode(User._meta.verbose_name_plural).capitalize(),
        'object':
            obj,
        'opts':
            obj._meta,
    }
    return render_to_response(
        "admin/user_activity_history.html",
        extra_context,
        context_instance=template.RequestContext(request),
    )


user_activity_history = staff_member_required(
    never_cache(user_activity_history)
)

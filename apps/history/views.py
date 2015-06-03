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

from jetson.apps.history.models import ExtendedLogEntry


def object_history(request, app_label, model_name, object_id):
    model = models.get_model(app_label, model_name)
    if model is None:
        raise Http404("App %r, model %r, not found" % (app_label, model_name))
    action_list = ExtendedLogEntry.objects.filter(
        object_id=object_id,
        content_type__id__exact=ContentType.objects.get_for_model(model).id,
        ).select_related().order_by('action_time')
    # If no history was found, see whether this object even exists.
    obj = get_object_or_404(model, pk=object_id)
    extra_context = {
        'title': _('Change history: %s') % obj,
        'action_list': action_list,
        'app_label': app_label,
        'module_name': force_unicode(model._meta.verbose_name_plural).capitalize(),
        'object': obj,
    }
    return render_to_response(
        [
            "admin/%s/%s/object_history.html" % (app_label, model._meta.object_name.lower()),
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
    # If no history was found, see whether this object even exists.
    obj = get_object_or_404(User, pk=object_id)
    extra_context = {
        'title': _('Change history: %s') % obj,
        'action_list': action_list,
        'module_name': force_unicode(User._meta.verbose_name_plural).capitalize(),
        'object': obj,
    }
    return render_to_response(
        "admin/user_activity_history.html",
        extra_context,
        context_instance=template.RequestContext(request),
        )
user_activity_history = staff_member_required(never_cache(user_activity_history))


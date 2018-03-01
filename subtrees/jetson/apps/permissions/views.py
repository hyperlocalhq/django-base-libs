# -*- coding: UTF-8 -*-
from django.contrib.auth import get_permission_codename
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template import loader, RequestContext
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache
from django.utils.translation import ugettext as _
from django.forms.formsets import formset_factory
from django.apps import apps

from base_libs.views import access_denied

from jetson.apps.permissions.models import RowLevelPermission
from jetson.apps.permissions.forms import RLPForm, BaseRLPFormSet

@staff_member_required
@never_cache
def manage_row_level_permissions(request, app_label, model_name, object_id):
    """
    Displays a list of row level permisisons for the model instance
    """
    model = apps.get_model(app_label, model_name)
    
    content_type = ContentType.objects.get_for_model(model)
    obj_instance = get_object_or_404(model, pk=object_id)
    opts = obj_instance._meta
    
    if not obj_instance.row_level_permissions:
        raise Http404
    
    u = request.user
    if not u.has_perm(
        "%s.%s" % (opts.app_label, get_permission_codename("change", opts)),
        obj=obj_instance
        ):
        return access_denied(request)
    app_label = RowLevelPermission._meta.app_label
    can_change = u.has_perm("%s.%s" % (app_label, get_permission_codename("change", RowLevelPermission._meta)))
    can_add = u.has_perm("%s.%s" % (app_label, get_permission_codename("add", RowLevelPermission._meta)))
    if not (can_change or can_add):
        return access_denied(request)
    
    RLPFormSet = formset_factory(
        form=RLPForm,
        formset=BaseRLPFormSet,
        can_delete=can_change,
        extra=0)
    RLPFormSet.obj_instance = obj_instance

    if request.method == 'POST':
        permissions_formset = RLPFormSet(request.POST, request.FILES)
        if permissions_formset.is_valid():
            permissions_formset.save()
            return HttpResponseRedirect(request.META["HTTP_REFERER"])
    else:
        permissions_formset = RLPFormSet()
    
    c = RequestContext(request, {
        'title': _('Edit Row Level Permissions'),
        'object_id': object_id,
        'content_type_id': content_type.id,
        'original': obj_instance,
        'opts':opts,
        'permissions_formset': permissions_formset,
    })
    return render_to_response([
        "admin/%s/%s/row_level_permissions.html" % (app_label, model_name),
        "admin/%s/row_level_permissions.html" % app_label,
        "admin/row_level_permissions.html"], context_instance=c)


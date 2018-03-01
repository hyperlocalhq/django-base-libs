# -*- coding: utf-8 -*-

import json

from django.conf import settings as django_settings
from django.contrib import admin
from django.contrib.admin.views import main
from django.db import transaction
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound, HttpResponseServerError, HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _, ugettext
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.utils.encoding import force_unicode
from django import template
from django.shortcuts import render_to_response
from django.core.exceptions import PermissionDenied
from django.http import Http404

from mptt.exceptions import InvalidMove
from mptt.forms import MoveNodeForm

csrf_protect_m = method_decorator(csrf_protect)

# ------------------------------------------------------------------------
def _build_tree_structure(cls):
    """
    Build an in-memory representation of the item tree, trying to keep
    database accesses down to a minimum. The returned dictionary looks like
    this (as json dump):

        {"6": [7, 8, 10]
         "7": [12],
         "8": [],
         ...
         }
    """
    all_nodes = { }

    if hasattr(cls, '_mptt_meta'): # New-style MPTT
        mptt_opts = cls._mptt_meta
    else:
        mptt_opts = cls._meta

    for p_id, parent_id in cls.objects.order_by(mptt_opts.tree_id_attr, mptt_opts.left_attr).values_list("pk", "%s_id" % mptt_opts.parent_attr):
        all_nodes[p_id] = []

        if parent_id:
            if not all_nodes.has_key(parent_id):
                # This happens very rarely, but protect against parents that
                # we have yet to iteratove over.
                all_nodes[parent_id] = []
            all_nodes[parent_id].append(p_id)

    return all_nodes


# ------------------------------------------------------------------------
class ChangeList(main.ChangeList):
    """
    Custom ``ChangeList`` class which ensures that the tree entries are always
    ordered in depth-first order (order by ``tree_id``, ``lft``).
    """

    def __init__(self, request, *args, **kwargs):
        self.user = request.user
        super(ChangeList, self).__init__(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        return super(ChangeList, self).get_queryset(*args, **kwargs).order_by('tree_id', 'lft')

    #def get_results(self, request):
    #    clauses = [Q(
    #        tree_id=tree_id,
    #        lft__lte=lft,
    #        rght__gte=rght,
    #        ) for lft, rght, tree_id in \
    #            self.query_set.values_list('lft', 'rght', 'tree_id')]
    #    if clauses:
    #        self.query_set = self.query_set.filter(reduce(lambda p, q: p|q, clauses))
    #        #self.query_set = self.model._default_manager.filter(reduce(lambda p, q: p|q, clauses))
    #
    #    super(ChangeList, self).get_results(request)

# ------------------------------------------------------------------------
# MARK: -
# ------------------------------------------------------------------------

class TreeEditor(admin.ModelAdmin):
    """
    The ``TreeEditor`` modifies the standard Django administration change list
    to a drag-drop enabled interface for django-mptt_-managed Django models.

    .. _django-mptt: http://github.com/mptt/django-mptt/
    """

    # Make sure that no pagination is displayed. Slicing is disabled anyway,
    # therefore this value does not have an influence on the queryset
    list_per_page = 999999999

    def __init__(self, *args, **kwargs):
        super(TreeEditor, self).__init__(*args, **kwargs)

        self.list_display = list(self.list_display)

        if 'indented_short_title' not in self.list_display:
            if self.list_display[0] == 'action_checkbox':
                self.list_display[1] = 'indented_short_title'
            else:
                self.list_display[0] = 'indented_short_title'
        self.list_display_links = ('indented_short_title',)

        opts = self.model._meta
        self.change_list_template = [
            'admin/%s/%s/tree_editor.html' % (opts.app_label, opts.object_name.lower()),
            'admin/%s/tree_editor.html' % opts.app_label,
            'admin/tree_editor.html',
            ]

    def get_urls(self):
        from functools import update_wrapper
        from django.conf.urls import patterns, url

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name

        urlpatterns = patterns(
            '',
            url(
                r'^(.+)/move/$',
                wrap(self.move_view),
                name='%s_%s_move' % info
            ),
        )

        urlpatterns += super(TreeEditor, self).get_urls()

        return urlpatterns

    @csrf_protect_m
    @transaction.atomic
    def move_view(self, request, object_id, extra_context=None):
        """The 'move node' admin view for this model."""

        opts = self.model._meta
        app_label = opts.app_label

        obj = self.get_object(request, object_id)

        if not self.has_change_permission(request, obj):
            raise PermissionDenied

        if obj is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {'name': force_unicode(opts.verbose_name), 'key': object_id})

        if request.POST: # The user has already confirmed the deletion.
            form = MoveNodeForm(obj, request.POST)
            if form.is_valid():
                if "johnny" in django_settings.INSTALLED_APPS:
                    from johnny.cache import invalidate
                    invalidate(self.model)

                form.save()

            self.message_user(request, ugettext('%s has been moved to a new position.') %
                obj)
            return HttpResponseRedirect("../../")
        else:
            form = MoveNodeForm(obj)

        object_name = force_unicode(opts.verbose_name)

        context = {
            "title": _('Move: %s') % force_unicode(obj),
            "form": form,
            "object_name": unicode(obj),
            "object": obj,
            "opts": opts,
            #"root_path": self.admin_site.root_path,
            "app_label": app_label,
        }
        context.update(extra_context or {})
        context_instance = template.RequestContext(request, current_app=self.admin_site.name)
        return render_to_response(self.delete_confirmation_template or [
            "admin/%s/%s/move_node.html" % (app_label, opts.object_name.lower()),
            "admin/%s/move_node.html" % app_label,
            "admin/move_node.html"
        ], context, context_instance=context_instance)

    def indented_short_title(self, item):
        """
        Generate a short title for an object, indent it depending on
        the object's depth in the hierarchy.
        """
        r = ''
        if hasattr(item, 'get_absolute_url'):
            r = '<input type="hidden" class="medialibrary_file_path" value="%s" />' % item.get_absolute_url()

        editable_class = ''
        if not getattr(item, 'editable', True):
            editable_class = ' tree-item-not-editable'

        r += '<span id="page_marker-%d" class="page_marker%s" style="width: %dpx;">&nbsp;</span>&nbsp;' % (
                item.id, editable_class, 14+item.level*18)
#        r += '<span tabindex="0">'
        if hasattr(item, 'short_title'):
            if callable(item.short_title):
                r += item.short_title()
            else:
                r += item.short_title
        else:
            r += unicode(item)
#        r += '</span>'
        return mark_safe(r)
    indented_short_title.short_description = _('title')
    indented_short_title.allow_tags = True

    def _refresh_changelist_caches(self):
        """
        Refresh information used to show the changelist tree structure such as
        inherited active/inactive states etc.

        XXX: This is somewhat hacky, but since it's an internal method, so be it.
        """

        pass

    def get_changelist(self, request, **kwargs):
        return ChangeList

    @never_cache
    def changelist_view(self, request, extra_context=None, *args, **kwargs):
        """
        Handle the changelist view, the django view for the model instances
        change list/actions page.
        """

        # handle common AJAX requests
        if request.is_ajax():
            cmd = request.POST.get('__cmd')
            if cmd == 'move_node':
                return self._move_node(request)
            else:
                return HttpResponseBadRequest('Oops. AJAX request not understood.')

        self._refresh_changelist_caches()

        extra_context = extra_context or {}
        extra_context['tree_structure'] = mark_safe(
            json.dumps(_build_tree_structure(self.model))
            )

        return super(TreeEditor, self).changelist_view(request, extra_context, *args, **kwargs)

    def _move_node(self, request):
        cut_item = self.model._tree_manager.get(pk=request.POST.get('cut_item'))
        pasted_on = self.model._tree_manager.get(pk=request.POST.get('pasted_on'))
        position = request.POST.get('position')

        if position in ('last-child', 'left'):
            if "johnny" in django_settings.INSTALLED_APPS:
                from johnny.cache import invalidate
                invalidate(self.model)

            try:
                self.model._tree_manager.move_node(cut_item, pasted_on, position)
            except InvalidMove, e:
                self.message_user(request, unicode(e))
                return HttpResponse('FAIL')

            # Ensure that model save has been run
            cut_item = self.model._tree_manager.get(pk=cut_item.pk)
            cut_item.save()

            self.message_user(request, ugettext('%s has been moved to a new position.') %
                cut_item)
            return HttpResponse('OK')

        self.message_user(request, ugettext('Did not understand moving instruction.'))
        return HttpResponse('FAIL')

    def _actions_column(self, instance):
        return ['<a href="%s/move/" class="drag_handle"></a>' % instance.pk,]

    def actions_column(self, instance):
        return u' '.join(self._actions_column(instance))
    actions_column.allow_tags = True
    actions_column.short_description = " "

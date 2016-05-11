# -*- coding: UTF-8 -*-
import os
import re
import json
import datetime
from decimal import Decimal
from copy import deepcopy

from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import check_for_language, ugettext_lazy as _
from django.utils import translation
from django.utils.encoding import force_unicode
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, Page, InvalidPage
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response
from django.template import loader, RequestContext, Template, Context
from django.contrib.auth.views import redirect_to_login
from django.contrib.syndication.views import FeedDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import never_cache
from django.utils.http import urlencode
from django.contrib import messages
from django.conf import settings
from django.utils.timezone import now as tz_now
from django.shortcuts import redirect
from django import forms

from ccb.apps.events.utils import create_ics
from base_libs.utils.misc import ExtendedJSONEncoder
from base_libs.utils.betterslugify import better_slugify


class JsonResponse(HttpResponse):
    def __init__(self, obj):
        self.original_obj = obj
        HttpResponse.__init__(self, self.serialize())
        self["Content-Type"] = "text/javascript; charset=UTF-8"

    def serialize(self):
        return json.dumps(self.original_obj, ensure_ascii=False, cls=ExtendedJSONEncoder)

def json_lookup(request, queryset, field=False, limit=10, login_required=False):
    """
    Method to lookup a model field and return an array. Intended for use 
    in AJAX widgets.
    """
    if login_required and request.user.is_anonymous():
        return redirect_to_login(request.path)
    if request.GET:
        search = request.GET['q']
        obj_list = []
        if field:
            lookup = {
                '%s__istartswith' % field: search,
            }
            for obj in queryset.filter(**lookup)[:limit]:
                obj_list.append([getattr(obj, field), obj.id])
            return JsonResponse(obj_list)
        else:
            search = search.lower()
            for obj in queryset:
                if obj[1].lower().startswith(search):
                    obj_list.append([obj[1], obj[0]])
            obj_list = obj_list[:limit]
            t = Template('[{% for el in obj_list %}{% ifnotequal forloop.counter0 0 %}, {% endifnotequal %}["{{ el.0 }}", "{{ el.1 }}"]{% endfor %}]')
            c = Context({'obj_list': obj_list})
            r = HttpResponse(t.render(c))
            r['Content-Type'] = 'text/javascript; charset=UTF-8'
            return r

def jquery_autocomplete_lookup(request, queryset, field=False, limit=10, login_required=False):
    """
    Method to lookup a model field and return an array. Intended for use 
    in AJAX widgets.
    """
    if login_required and request.user.is_anonymous():
        return redirect_to_login(request.path)
    obj_list = []
    if request.GET:
        search = request.GET['q']
        if field:
            lookup = {
                '%s__istartswith' % field: search,
            }
            for obj in queryset.filter(**lookup)[:limit]:
                obj_list.append([getattr(obj, field), obj.pk])
        else:
            search = search.lower()
            for obj in queryset:
                if obj[1].lower().startswith(search):
                    obj_list.append([obj[1], obj[0]])
            obj_list = obj_list[:limit]
    t = Template('{% for el in obj_list %}{{ el.0 }}|{{ el.1 }}\n{% endfor %}')
    c = Context({'obj_list': obj_list})
    r = HttpResponse(t.render(c))
    r['Content-Type'] = 'text/plain; charset=UTF-8'
    return r

def direct_to_js_template(request, cache=True, *args, **kwargs):
    response = render(request, *args, **kwargs)
    response['Content-Type'] = "application/x-javascript"
    if cache:
        #response['Cache-Control'] = "max-age=2678400" # cached for one month
        now = datetime.datetime.utcnow()
        response['Last-Modified'] = now.strftime('%a, %d %b %Y %H:%M:%S GMT')
        expires = now + datetime.timedelta(0, 2678400)
        response['Expires'] = expires.strftime('%a, %d %b %Y %H:%M:%S GMT')
    else:
        response['Pragma'] = "No-Cache"
    return response
direct_to_js_template = cache_control( )(direct_to_js_template)

def feed(request, feed_type, language="de", **kwargs):
    
    """ generates a feed.
        Needs the following arguments in the kwargs dict:
        
        <<slug>> : <<Feedclass>> a slugname connected to a "FeedClass" 
        (see jetson.search.feeds.py)
        'extra' :  An optional dictionary containing parameters used for
        getting the appropriate Feeds from the <<Feedclass>>
    """
    if not kwargs:
        raise Http404, "No feeds are registered."
    
    try:
        feed_slug, param = feed_type.split('/', 1)
    except ValueError:
        feed_slug, param = feed_type, ''

    try:
        translation.deactivate()
        translation.activate(language) 
    except:
        raise Http404("Invalid language parameter '%s' set." % language)
        
    try:
        f = kwargs[feed_slug]
    except KeyError:
        raise Http404("Feed Slug %r isn't registered." % feed_slug)

    try:
        feedgen = f(request, **kwargs)
    except FeedDoesNotExist:
        raise Http404("Invalid feed parameters. Slug %r is valid, but other parameters, or lack thereof, are not." % feed_slug)

    feedgen.content_type = 'application/rss+xml'
    return feedgen

feed = never_cache(feed)


class CustomPaginator(Paginator):
    def __init__(self, *args, **kwargs):
        self.first_page_delta = kwargs.pop('first_page_delta', 0)
        Paginator.__init__(self, *args, **kwargs)

    def page(self, number):
        """
        Returns a Page object for the given 1-based page number.
        """
        number = self.validate_number(number)
        if number == 1:
            bottom_limit = 0
            top_limit = self.per_page - self.first_page_delta
        else:
            bottom_limit = (number - 1) * self.per_page - self.first_page_delta
            top_limit = bottom_limit + self.per_page
        if top_limit + self.orphans >= self.count:
            top_limit = self.count
        return Page(self.object_list[bottom_limit:top_limit], number, self)


def object_list(request, queryset,
    paginate_by=None, order_by=None, view_type="icons", page=None,
    allow_empty=False, template_name=None, template_loader=loader,
    extra_context=None, context_processors=None, template_object_name="object",
    content_type=None, pages_to_display=10, query="", httpstate_prefix="", paginate=True, first_page_delta=0, **kwargs):
    """
    Generic list of objects.

    Templates: ``<app_label>/<model_name>_list.html``
    Context:
        object_list
            list of objects
        is_paginated
            are the results paginated?
        results_per_page
            number of objects per page (if paginated)
        has_next
            is there a next page?
        has_previous
            is there a prev page?
        page
            the current page
        next
            the next page
        previous
            the previous page
        pages
            number of pages, total
        pagelist
            list of page numbers to display
        hits
            number of objects, total
        first_page_delta
            how many items less to show on the first page
    """

    if kwargs.has_key('ical') and kwargs['ical'] == True:
        icalstream = create_ics(queryset)
        response = HttpResponse(icalstream, content_type="text/calendar")
        response['Filename'] = "CCB-events.ics"  # IE needs this
        response['Content-Disposition'] = "attachment; filename=CCB-events.ics"
        return response

    if extra_context is None: extra_context = {}
    
    sort_order_map = getattr(queryset, "get_sort_order_map", lambda: None)()
    sort_order_mapper = getattr(queryset, "get_sort_order_mapper", lambda: None)()
    
    queryset = queryset._clone()
    queryset.sort_order_map = sort_order_map
    queryset.sort_order_mapper = sort_order_mapper

    filter_field = request.REQUEST.get("filter_field", None)
    filter_value = request.REQUEST.get("filter_value", None)
    group_by = request.REQUEST.get("group_by", None)
    
    if httpstate_prefix and not httpstate_prefix.endswith("_"):
        httpstate_prefix += "_"
    
    paginate_by = request.REQUEST.get(
        "paginate_by",
        request.httpstate.get(
            "%spaginate_by" % httpstate_prefix,
            paginate_by or 10
            )
        )
    paginate_by = int(paginate_by)
    
    order_by = request.REQUEST.get(
        "order_by",
        request.httpstate.get(
            "%sorder_by" % httpstate_prefix,
            order_by,
            )
        )
    
    view_type = request.REQUEST.get(
        "view_type",
        request.httpstate.get(
            "%sview_type" % httpstate_prefix,
            view_type,
            )
        )
       
    url_query = []
    if filter_field:
        url_query.append("filter_field=" + filter_field)
    if filter_value:
        url_query.append("filter_value=" + filter_value)
    if order_by:
        url_query.append("order_by=" + order_by)
    if group_by:
        url_query.append("group_by=" + group_by)
    if view_type:
        url_query.append("view_type=" + view_type)
   
    if filter_field and filter_value:
        queryset = queryset.filter(**{filter_field:filter_value})
    
    try:
        queryset = queryset.sort_by(order_by)
    except:
        pass
    
    request.httpstate["%spaginate_by" % httpstate_prefix] = paginate_by
    request.httpstate["%sorder_by" % httpstate_prefix] = order_by
    request.httpstate["%sview_type" % httpstate_prefix] = view_type
    
    """
    precalculate context processors
      
    we save the queryset in the httpstate, as we need that for the prev - next
    navigation in the details views. queryset_index_dict is build up once 
    for each queryset. It has an unique string containing contenttype_id and
    object_id as a key and the index of the dataset as value. The
    previous-next-processor just looks for occurrence of the appropriate key and
    gets the value from the dict. This solution seems to be much faster than
    searching the whole queryset every time!!!!
    
    IMPORTANT!!
    for any reason, we get a "PicklingError" here, when assigning 
    the queryset directly to the httpstate. So we take a list (current_queryset_list)
    """

    if context_processors and not getattr(settings, "DISABLE_CONTEXT_PROCESSORS", False):
        queryset_index_dict = {}
        index = 0
        prev_next_use_content_object = extra_context.get('prev_next_use_content_object', False)
        
        if prev_next_use_content_object:
            for obj in queryset.only("content_type", "object_id"):
                #key = '%s_%s_%s' % (obj.content_type_id, obj.object_id, request.LANGUAGE_CODE)
                key = '%s_%s' % (obj.content_type_id, obj.object_id)
                queryset_index_dict[key] = index
                index += 1
        else:
            ct = ContentType.objects.get_for_model(queryset.model)
            fields_to_select = [queryset.model._meta.pk.name] + queryset.query.extra_select.keys() + queryset.query.aggregate_select.keys()
            for d in queryset.values(*fields_to_select):
                #key = '%s_%s_%s' % (ct.pk, pk, request.LANGUAGE_CODE)
                key = '%s_%s' % (ct.pk, d[queryset.model._meta.pk.name])
                queryset_index_dict[key] = index
                index += 1

        if extra_context.get('source_list', None):
           request.httpstate['source_list'] = extra_context['source_list']

        request.httpstate['current_queryset_index_dict'] = queryset_index_dict
        request.httpstate['last_query_string'] = request.META['QUERY_STRING']

        fields_to_select = [queryset.model._meta.pk.name] + queryset.query.extra_select.keys() + queryset.query.aggregate_select.keys()
        request.httpstate['current_queryset_pk_list'] = [d[queryset.model._meta.pk.name] for d in queryset.values(*fields_to_select)]
        request.httpstate['current_queryset_model'] = u"%s.%s" % (queryset.model._meta.app_label, queryset.model.__name__)

    if paginate and paginate_by:
        paginator = CustomPaginator(queryset, paginate_by, first_page_delta=first_page_delta)
        if not page:
            page = request.GET.get('page', 1)
        try:
            page = int(page)
            current_page = paginator.page(page)
            object_list = current_page.object_list
        except (InvalidPage, ValueError):
            raise Http404
        
        page_min = max(page - pages_to_display/2, 1)
        page_max = min(paginator.num_pages + 1, page_min + pages_to_display)
        if page_max == paginator.num_pages + 1:
            page_min = max(page_max - pages_to_display, 1)
        
        next_page_number = None
        if current_page.has_next():
            next_page_number = current_page.next_page_number()
        
        previous_page_number = None
        if current_page.has_previous():
            previous_page_number = current_page.previous_page_number()
        
        c = RequestContext(request, {
            '%s_list' % template_object_name: object_list,
            'is_paginated': current_page.has_other_pages(),
            'results_per_page': paginate_by,
            'has_next': current_page.has_next(),
            'has_previous': current_page.has_previous(),
            'current_page': current_page,
            'page': page,
            'next': next_page_number,
            'previous': previous_page_number,
            'pages': paginator.num_pages,
            'pagelist': [i for i in range(page_min, page_max)],
            'page_numbers': paginator.page_range,
            'hits' : queryset.count(),
            'page_hits_min': (page-1) * paginate_by + 1,
            'page_hits_max': min(page * paginate_by, queryset.count()),
        })
    else:
        c = RequestContext(request, {
            '%s_list' % template_object_name: queryset,
            'is_paginated': False
        }, context_processors)
        if not allow_empty and len(queryset) == 0:
            raise Http404
    for key, value in extra_context.items():
        if callable(value):
            c[key] = value()
        else:
            c[key] = value
    c['filter_field'] = filter_field
    c['filter_value'] = filter_value
    c['group_by'] = group_by
    c['order_by'] = order_by
    c['view_type'] = view_type
    c['url_query'] = '&amp;'.join(url_query)
    c['sort_order_map'] = sort_order_map
    
    the_query = request.GET.copy()
    c['query'] = query or urlencode(the_query)
    
    c['path_without_page'] = re.sub('/page[0-9]+', '', request.path)
    
    if not template_name:
        model = queryset.model
        template_name = "%s/%s_list.html" % (model._meta.app_label, model._meta.object_name.lower())
    t = template_loader.get_template(template_name)
    return HttpResponse(t.render(c), content_type=content_type)

def object_detail(request, queryset, year=0, month=0, day=0, object_id=None, slug=None,
        slug_field=None, template_name=None, template_name_field=None,
        template_loader=loader, extra_context=None,
        context_processors=None, template_object_name='object',
        content_type=None, **kwargs):
    """
    Generic detail of an object.

    Templates: ``<app_label>/<model_name>_detail.html``
    Context:
        object
            the object
    """
    if extra_context is None: extra_context = {}
    model = queryset.model
    if object_id:
        queryset = queryset.filter(pk=object_id)
    elif slug and slug_field:
        queryset = queryset.filter(**{slug_field: slug})
    else:
        raise AttributeError, "Generic detail view must be called with either an object_id or a slug/slug_field."
    try:
        obj = queryset.get()
    except ObjectDoesNotExist:
        raise Http404, "%s does not exist." % force_unicode(model._meta.verbose_name).capitalize()
    if not template_name:
        template_name = "%s/%s_detail.html" % (model._meta.app_label, model._meta.object_name.lower())
    if template_name_field:
        template_name_list = [getattr(obj, template_name_field), template_name]
        t = template_loader.select_template(template_name_list)
    else:
        t = template_loader.get_template(template_name)
        
    if request.httpstate.get('current_queryset_model', None) == u"%s.%s" % (queryset.model._meta.app_label, queryset.model.__name__):
        request.httpstate['current_object_id'] = obj.pk
    elif 'current_object_id' in request.httpstate:
        del request.httpstate['current_object_id']
        
    c = RequestContext(request, {
        template_object_name: obj,
    }, context_processors)
    for key, value in extra_context.items():
        if callable(value):
            c[key] = value()
        else:
            c[key] = value

    response = HttpResponse(t.render(c), content_type=content_type)
    return response


def _get_step_list(current_step, form_steps, form_step_data):
    steps = []
    for i in form_step_data['path']:
        try:
            active = form_step_data.get(form_step_data['path'][form_step_data['path'].index(i)-1], {}).get('_filled', False)
        except KeyError:
            active = False
        steps.append({
            'title': form_steps[i].get('title', " "),
            'filled': form_step_data.get(i, {}).get('_filled', False),
            'current': current_step == i,
            'active': active,
        })
    return steps

'''
### Multistep-form configuration structure ###

FORM_STEPS = {
    'step_0': {
        'title': _("Some Title"),                           # default: ""
        'template': "path/to/some/template.html",           # required
        'form': FormClass,                                  # optional
        'formsets': {                                       # optional
            'formset_name1': FormsetClass1,
            'formset_name2': FormsetClass2,
        },
        'initial_data': {},                                 # optional
        '_filled': False,
    },
    'step_1': {
        ..
    },
    ..
    'name': "form_name",                                    # required

    'oninit': init_func,                                    # optional;
                                                            # passed args: instance=None, request;
                                                            # returns form_step_data

    'onsubmit': submit_func,                                # optional; 
                                                            # passed args: current_step, request, form_steps, instance=None;
                                                            # returns form_step_data

    'on_set_extra_context': set_extra_context,              # optional,
                                                            # passed args: current_step, form_steps, form_step_data, request, instance=None;
                                                            # returns extra context dictionary

    'onreset': return_func,                                 # optional;
                                                            # passed args: request, instance=None;
                                                            # returns HttpResponse object

    'onsave': save_func,                                    # required;
                                                            # passed args: form_steps, form_step_data, instance=None;
                                                            # returns form_step_data

    'onsuccess': success_func,                              # optional
                                                            # passed args: request, instance=None;
                                                            # returns HttpResponse object

    'success_url': "/path/to/redirect/to/",                 # optional
    'success_template': "path/to/template_of_success.html", # required if neither 'onsuccess' nor 'success_url' is not set

    'default_path': ["step_0", "step_1",..]
}

### What is saved in httpstate ###

form_step_data = {
    'step_0': {
        'field1': "value1",
        'field2': "value2",
        'get_field2_display': "humanized value2",
        ..
        'sets': {
            'formset_name1': [
                {
                    'field1': "value1",
                    'field2': "value2",
                    'get_field2_display': "humanized value2",
                },
                {
                    'field1': "value1",
                    'field2': "value2",
                    'get_field2_display': "humanized value2",
                },
                ...
            ],
            'formset_name2': [
                ...
            ],
            ...
        }
    },
    'step_1': {
    },
    ..
    'current_step': i,
    'step_counter': j,
    'path': ["step_0", "step_1",..]
}

'''

GENERAL_ERROR_MESSAGE = _("There are errors in this form. Please correct them and try to save again.")

@never_cache
def show_form_step(request, form_steps=None, extra_context=None, instance=None):
    """ 
    Show a step from a multiple-step form
    """
    if not extra_context:
        extra_context = {}
    if not form_steps:
        form_steps = {}

    if instance:
        multistep_forms_name = "%s_%s" % (form_steps['name'], instance.pk)
    else:
        multistep_forms_name = form_steps['name']
    
    form_step_data = request.httpstate.get(multistep_forms_name, {})

    if not form_step_data and 'oninit' in form_steps:
        if instance:
            form_step_data = form_steps['oninit'](instance=instance, request=request)
        else:
            form_step_data = form_steps['oninit'](request=request)

        # change all model instances to primary keys
        for step in form_step_data:
            if isinstance(form_step_data[step], dict):
                step_field_dict = form_step_data[step]
                for field_name in step_field_dict:

                    if isinstance(step_field_dict[field_name], models.Model):
                        # if ModelChoiceField is used, save primary key
                        step_field_dict[field_name] = step_field_dict[field_name].pk

                    elif isinstance(step_field_dict[field_name], QuerySet):
                        # if ModelMultipleChoiceField is used, save list of primary keys
                        step_field_dict[field_name] = [obj.pk for obj in step_field_dict[field_name]]

                    elif isinstance(step_field_dict[field_name], (list, tuple)):
                        if step_field_dict[field_name] and isinstance(step_field_dict[field_name][0], models.Model):
                            step_field_dict[field_name] = [obj.pk for obj in step_field_dict[field_name]]

                    # elif isinstance(step_field_dict[field_name], (datetime.datetime, datetime.date, datetime.time, Decimal)):
                    #     # convert dates, times, and decimals to string
                    #     step_field_dict[field_name] = unicode(step_field_dict[field_name])

                    if field_name == "sets":
                        for formset_name in step_field_dict['sets']:
                            for formset_field_dict in step_field_dict['sets'][formset_name]:
                                for ffield_name in formset_field_dict:
                                    # for every formset form field

                                    if isinstance(formset_field_dict[ffield_name], models.Model):
                                        # if ModelChoiceField is used, save primary key
                                        formset_field_dict[ffield_name] = formset_field_dict[ffield_name].pk

                                    elif isinstance(formset_field_dict[ffield_name], QuerySet):
                                        # if ModelMultipleChoiceField is used, save list of primary keys
                                        formset_field_dict[ffield_name] = [obj.pk for obj in formset_field_dict[ffield_name]]

                                    elif isinstance(formset_field_dict[ffield_name], (list, tuple)):
                                        if formset_field_dict[ffield_name] and isinstance(formset_field_dict[field_name][0], models.Model):
                                            formset_field_dict[ffield_name] = [obj.pk for obj in formset_field_dict[ffield_name]]

                                    # elif isinstance(formset_field_dict[ffield_name], (datetime.datetime, datetime.date, datetime.time, Decimal)):
                                    #     # convert dates, times, and decimals to string
                                    #     formset_field_dict[ffield_name] = unicode(formset_field_dict[ffield_name])

        request.httpstate[multistep_forms_name] = form_step_data
    
    form_step_data['path'] = form_step_data.get(
        'path',
        form_steps['default_path'],
    )
    
    # TODO: write inline documentation for the retrieval of current step
    current_step = form_step_data.get(
        'current_step',
        form_steps['default_path'][0],
    )

    # current_step:  "step_1", "step_2", "step_3", ...
    # step_counter:     1,        2,        3,     ...
    # step_counter0:    0,        1,        2,     ...

    try:
        step_counter = int(request.GET.get("step", 1))  # requested one-based step counter
    except ValueError:
        step_counter = 1

    step_counter0 = step_counter - 1  # requested zero-based step counter
    if 0 <= step_counter0 < len(form_step_data['path']):
        # checking the last previous step that was filled in:
        prev_step_counter0 = step_counter0 - 1
        while prev_step_counter0 >= 0:
            step_name = form_step_data['path'][prev_step_counter0]
            if form_step_data.get(step_name, {}).get('_filled', False):
                break
            prev_step_counter0 -= 1
        if prev_step_counter0 != step_counter0 - 1:
            # if previous step was not filled in, redirect to the next after the last filled-in step
            return redirect(u'%s?step=%s' % (request.path, prev_step_counter0 + 2))

        current_step = form_step_data['current_step'] = form_step_data['path'][step_counter0]
    else:
        return redirect(u'%s?step=1' % request.path)

    initial_data = form_steps[current_step].get('initial_data', {})
    if callable(initial_data):
        initial_data = initial_data(request=request)
    
    form_class = form_steps[current_step].get('form', None)
    formset_classes = form_steps[current_step].setdefault("formsets", {})
    formsets = {}
    
    next = ""
    
    if request.method == "POST":
        data = request.POST.copy()
        if data.get('reset', False):
            if multistep_forms_name in request.httpstate:
                del(request.httpstate[multistep_forms_name])
            if 'onreset' in form_steps:
                if instance:
                    return form_steps['onreset'](request, instance)
                else:
                    return form_steps['onreset'](request)
            return HttpResponseRedirect(request.path)

        # TODO: decide if it's still necessary to do this initial_data check
        # why can't request.POST be used instead for the form?
        #fields = form_class().fields
        #data = dict([
        #    (item[0], item[1])
        #    for item in data.items()
        #    if item[0] in fields
        #        and (item[0] not in initial_data or item[1]!=initial_data[item[0]])
        #    ])
        if form_class:
            if instance:
                f = form_class(data, request.FILES, instance=instance)
            else:
                f = form_class(data, request.FILES)
        else:
            form_class = forms.Form
            f = form_class(data, request.FILES)
        
        formsets_are_valid = True
        data = request.POST.copy()
        for formset_name, formset_class in formset_classes.items():
            formsets[formset_name] = formset_class(
                data=data,
                files=request.FILES,
                prefix=formset_name,
            )
            # bitwise "&" works as expected for boolean values
            formsets_are_valid &= formsets[formset_name].is_valid()

        if f.is_valid() and formsets_are_valid:
            form_step_data[current_step] = dict(f.cleaned_data)
            for field in f:
                # create get_XXX_display for all selection fields
                try:
                    field_value = form_step_data[current_step][field.name]
                except KeyError:
                    field_value = None
                if hasattr(field.field, 'choices') and field.field.choices:
                    d = dict([
                        (str(k), unicode(v))
                        for k, v in field.field.choices
                    ])
                    k = f.cleaned_data.get(field.name, '')
                    if not isinstance(k, (list, models.Model)):
                        form_step_data[current_step][
                            'get_%s_display' % field.name
                        ] = d.get(k, "")
                        if k == "":
                            field_value = None
                if isinstance(field_value, models.Model):
                    # if ModelChoiceField is used, save primary key
                    field_value = field_value.pk
                elif isinstance(field_value, QuerySet):
                    # if ModelMultipleChoiceField is used, save list of primary keys
                    field_value = [obj.pk for obj in field_value]
                # elif isinstance(form_step_data[current_step][field.name], (datetime.datetime, datetime.date, datetime.time, Decimal)):
                #     # convert dates, times, and decimals to string
                #     form_step_data[current_step][field.name] = unicode(form_step_data[current_step][field.name])

            # process formset data
            form_step_data[current_step]['sets'] = {}
            for formset_name, formset in formsets.items():
                form_step_data[current_step]['sets'][formset_name] = []
                for form in formset.forms:
                    if (
                        form.has_changed()
                        and hasattr(form, "cleaned_data")
                        and not form.cleaned_data.get('DELETE', False)
                    ):
                        cleaned_data = dict(form.cleaned_data)
                        for field in form:
                            # create get_XXX_display for all selection fields
                            if hasattr(field.field, 'choices') and field.field.choices:
                                k = cleaned_data.get(field.name, '') or ''
                                if not isinstance(k, (list, models.Model)):
                                    d = dict([
                                        (str(k1), unicode(v1))
                                        for k1, v1 in field.field.choices
                                    ])
                                    cleaned_data['get_%s_display' % field.name] = d[str(k)]
                                    if k == "":
                                        cleaned_data[field.name] = None
                            if isinstance(cleaned_data[field.name], models.Model):
                                # if ModelChoiceField is used, save primary key
                                cleaned_data[field.name] = cleaned_data[field.name].pk
                            elif isinstance(cleaned_data[field.name], QuerySet):
                                # if ModelMultipleChoiceField is used, save list of primary keys
                                cleaned_data[field.name] = [obj.pk for obj in cleaned_data[field.name]]
                            # elif isinstance(cleaned_data[field.name], (datetime.datetime, datetime.date, datetime.time, Decimal)):
                            #     # convert dates, times, and decimals to string
                            #     cleaned_data[field.name] = unicode(cleaned_data[field.name])
                        form_step_data[current_step]['sets'][formset_name].append(
                            cleaned_data,
                        )

            # save uploaded files in a temporary directory
            for file_field_name in request.FILES:
                file_data = request.FILES[file_field_name]
                try:
                    filename, ext = file_data.name.rsplit(".", 1)
                except:
                    filename = ""
                    ext = ""
                tmp_filename = tz_now().strftime("%d%H%I%S_") + better_slugify(filename) + "." + ext
                tmp_path = os.path.join(settings.PATH_TMP, tmp_filename)
                fd = open(tmp_path, 'wb')
                for chunk in file_data.chunks():
                    fd.write(chunk)
                fd.close()
                form_step_data[current_step][file_field_name] = {
                    'name': file_data.name,
                    'size': file_data.size,
                    'tmp_filename': tmp_filename,
                }
            form_step_data[current_step]['_filled'] = True
            if instance:
                form_step_data = form_steps['onsubmit'](current_step, form_steps, form_step_data, instance)
            else:
                form_step_data = form_steps['onsubmit'](current_step, form_steps, form_step_data)
            path = form_step_data['path']
            new_step_counter = path.index(current_step) + 1
            should_save = False
            try:
                #form_step_data['current_step'] = 
                path[new_step_counter]
            except IndexError:
                should_save = True
            if data.get('save_and_close', False):
                should_save = True
                
            if should_save:
                if 'onsave' in form_steps:
                    if instance:
                        form_step_data = form_steps['onsave'](form_steps, form_step_data, instance)
                    else:
                        form_step_data = form_steps['onsave'](form_steps, form_step_data)
                if multistep_forms_name in request.httpstate:
                    del(request.httpstate[multistep_forms_name])

                # return the user to onsuccess response, success_url or render a success_template
                if 'onsuccess' in form_steps:
                    if instance:
                        return form_steps['onsuccess'](request, instance)
                    else:
                        return form_steps['onsuccess'](request)
                elif form_steps.get('success_url', False):
                    return redirect(form_steps['success_url'])
                else:
                    form_step_data['current_step'] = None
                    current_step = None
                    return render_to_response(
                        form_steps['success_template'],
                        {
                            'form_step_data': form_step_data,
                            'steps': _get_step_list(current_step, form_steps, form_step_data),
                        },
                        context_instance=RequestContext(request),
                    )
            else:
                request.httpstate[multistep_forms_name] = form_step_data
            return HttpResponseRedirect("%s?step=%s" % (request.path, new_step_counter + 1))
        else:
            messages.error(request, form_steps.get('general_error_message', GENERAL_ERROR_MESSAGE))
        for field_name in f.fields:
            if not f.data.get(field_name, False):
                f.data[field_name] = f.fields[field_name].initial
        
    else:
        data = deepcopy(form_step_data.get(
            current_step,
            initial_data,
        ))
        # redefine initial data for model choice fields
        for k, v in data.items():
            if isinstance(v, models.Model):
                data[k] = v.pk
            elif hasattr(v, "__iter__"):
                new_v = [(not isinstance(item, models.Model) and [item] or [item.pk])[0] for item in v]
                data[k] = new_v

        if form_class:
            if instance:
                f = form_class(initial=data, instance=instance)
            else:
                f = form_class(initial=data)
        else:
            form_class = forms.Form
            f = form_class(initial=data)
        
        for formset_name, formset_class in formset_classes.items():
            data = form_step_data.get(
                current_step,
                {},
            ).setdefault(
                "sets",
                {},
            ).setdefault(
                formset_name,
                [],
            )

            formsets[formset_name] = formset_class(
                initial=data,
                prefix=formset_name,
            )
            if isinstance(formsets[formset_name].form(), forms.ModelForm):
                for formset_form in formsets[formset_name].forms:
                    if formset_form.initial.get('id', None):
                        formset_form.instance = formsets[formset_name].form._meta.model.objects.get(
                            pk=formset_form.initial['id'],
                        )
        
    try:
        form_step_data['step_counter'] = form_step_data['path'].index(form_step_data['current_step']) + 1
    except:
        pass
    else:
        if hasattr(f, "helper"):
            f.helper.form_action = "?step=%s" % form_step_data['step_counter']
    context = {
        'form': f,
        'formsets': formsets,
        'title': form_steps[current_step].get("title", ""),
        'form_step_data': form_step_data,
        'steps': _get_step_list(current_step, form_steps, form_step_data),
        'next': next,
    }
    context.update(extra_context)
    if 'on_set_extra_context' in form_steps:
        if instance:
            extra_context = form_steps['on_set_extra_context'](
                current_step=current_step,
                form_steps=form_steps,
                form_step_data=form_step_data,
                instance=instance,
                request=request,
            )
        else:
            extra_context = form_steps['on_set_extra_context'](
                current_step=current_step,
                form_steps=form_steps,
                form_step_data=form_step_data,
                request=request,
            )
        context.update(extra_context)
    
    template_file = [form_steps[current_step].setdefault("template", "utils/newform_step.html")]
    return render_to_response(template_file, context,  context_instance=RequestContext(request))


def get_abc_list(queryset, filter_field, selected = None):
    """
    help function:
    returns an alphabet list used for filtering
    """
    abc_list = [("", _("All"), queryset.count(), selected is None)]
    # we need a "key" as first column, because we have to check 
    # for "All" in the tamplates
    abc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    the_09_filter = models.Q()
    
    for letter in abc:
        the_filter = models.Q(**{filter_field + "__istartswith": letter})
        if letter == 'A':
            the_filter |= models.Q(**{filter_field + "__istartswith": "Ä"})
        elif letter == 'O':
            the_filter |= models.Q(**{filter_field + "__istartswith": "Ö"})            
        elif letter == 'U':
            the_filter |= models.Q(**{filter_field + "__istartswith": "Ü"})                        
        
        count = queryset.filter(the_filter).count()
        abc_list.append((letter, letter, count, selected == letter))

        # we prepare th 0-9 filter in the loop ...
        the_09_filter |= models.Q(**{filter_field + "__istartswith": letter})
    
    # at last, add the "0-9" filter
    the_09_filter |= models.Q(**{filter_field + "__istartswith": "Ä"}) 
    the_09_filter |= models.Q(**{filter_field + "__istartswith": "Ö"}) 
    the_09_filter |= models.Q(**{filter_field + "__istartswith": "Ü"}) 
    count = queryset.exclude(the_09_filter).count()        
    abc_list.append(("0-9", _("0-9"), count, selected == "0-9"))
                
    return abc_list

def filter_abc(queryset, filter_field, filter_value):
    """
    help function:
    filters a queryset for a specific start letter
    """
    #first the "[0-9]" case
    if filter_value == '0-9':
        abc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        the_filter = models.Q()
        for letter in abc:
            the_filter |= models.Q(**{filter_field + "__istartswith": letter})
        the_filter |= models.Q(**{filter_field + "__istartswith": "Ä"}) 
        the_filter |= models.Q(**{filter_field + "__istartswith": "Ö"}) 
        the_filter |= models.Q(**{filter_field + "__istartswith": "Ü"}) 
        return queryset.exclude(the_filter)
    else:
        the_filter = models.Q(**{filter_field + "__istartswith": filter_value})
        if filter_value == 'A':
            the_filter |= models.Q(**{filter_field + "__istartswith": "Ä"})
        elif filter_value == 'O':
            the_filter |= models.Q(**{filter_field + "__istartswith": "Ö"})            
        elif filter_value == 'U':
            the_filter |= models.Q(**{filter_field + "__istartswith": "Ü"})                        
        return queryset.filter(the_filter)

def get_year_list(queryset, filter_field, selected = None):
    """
    help function:
    returns a list of years contained in a queryset
    """
    year_list = [("all", _("All"), len(queryset), selected is None),
                 ("latest", _("Topical"), len(queryset), selected == "latest")]

    # first, we determine the smallest and largest year
    qs = queryset.order_by(filter_field)
    if len(qs) > 0:
        smallest_year = getattr(qs[0], filter_field).year
        largest_year = getattr(qs[len(qs)-1], filter_field).year
        for i in range(smallest_year, largest_year+1):
            count = queryset.filter(**{filter_field + "__year":i}).count()
            year_list.append((str(i), str(i), count, selected == str(i)))

    return year_list

def filter_year(queryset, filter_field, filter_value):
    """
    help function:
    filters a queryset for a specific year
    """
    if filter_value == "latest":
        # we cannot use the "latest function here, it's a pity! 
        # return ....latest(filter_field)
        qs = queryset.order_by("-%s" %filter_field)
        # TODO currently, latest is set to 5,
        # Maybe, we should not hardcode this
        return qs[:5]
    else:
        return queryset.filter(**{filter_field + "__year":filter_value})

def set_language(request):
    """
    Redirect to a given url while setting the chosen language in the
    httpstate or cookie. The url and the language code need to be
    specified in the request parameters.

    Since this view changes how the user will see the rest of the site, it must
    only be accessed as a POST request. If called as a GET request, it will
    redirect to the page in the request (the 'next' parameter) without changing
    any state.
    """
    next = request.REQUEST.get('next', None)
    if not next:
        next = request.META.get('HTTP_REFERER', None)
    if not next:
        next = '/'
    response = HttpResponseRedirect(next)
    lang_code = request.REQUEST.get('language', None)
    if lang_code:
        if lang_code and check_for_language(lang_code):
            if hasattr(request, 'httpstate'):
                request.session['django_language'] = lang_code
            # save the language in a cookie in any case for correct caching
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
    return response    

# -*- coding: UTF-8 -*-

from django.utils.translation import ugettext_lazy as _
from jetson.apps.media_gallery.views import *
from base_libs.models.models import STATUS_CODE_PUBLISHED
from .forms import MediaGallerySearchForm
from jetson.apps.structure.models import Category


def gallery_list(request, queryset, show="featured", paginate_by=None, order_by=None, page=None,
                 allow_empty=False, template_name=None, template_loader=loader,
                 extra_context=None, context_processors=None, template_object_name='object',
                 content_type=None, pages_to_display=10, query="", category_slug=""):
    queryset = queryset.distinct().extra(
        where=("(SELECT COUNT(*) FROM media_gallery_mediafile WHERE gallery_id=media_gallery_mediagallery.id) > 0",),
    )
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
    """

    form = MediaGallerySearchForm(data=request.REQUEST)

    category = None
    if category_slug:
        category = Category.objects.get(slug=category_slug)

    if category:
        queryset = queryset.filter(
            categories__lft__gte=category.lft,
            categories__rght__lte=category.rght,
            categories__tree_id=category.tree_id,
        ).distinct()
    elif form.is_valid():
        cat = form.cleaned_data['category']
        if cat:
            queryset = queryset.filter(
                categories__lft__gte=cat.lft,
                categories__rght__lte=cat.rght,
                categories__tree_id=cat.tree_id,
            ).distinct()

    if extra_context is None:
        extra_context = {}

    extra_context['category'] = category

    sort_order_map = getattr(queryset, "get_sort_order_map", lambda: None)()
    sort_order_mapper = getattr(queryset, "get_sort_order_mapper", lambda: None)()

    if show == "featured":
        queryset = queryset.filter(is_featured=True)
    elif show == "memos":
        from jetson.apps.memos.models import Memo, MEMO_TOKEN_NAME

        ct = ContentType.objects.get_for_model(queryset.model)
        memos_ids = map(int, Memo.objects.filter(
            collection__token=request.COOKIES.get(MEMO_TOKEN_NAME, None),
            content_type=ct,
        ).values_list("object_id", flat=True))
        queryset = queryset.filter(
            pk__in=memos_ids,
        )
    elif show == "favorites":
        if request.user.is_anonymous():
            return access_denied(request)
        queryset = queryset.extra(
            tables=["favorites_favorite"],
            where=[
                "favorites_favorite.user_id = %d" % request.user.id,
                "favorites_favorite.object_id::integer = media_gallery_mediagallery.id",
                "favorites_favorite.content_type_id = %d" % ContentType.objects.get_for_model(MediaGallery).pk,
            ],
        ).distinct()

    queryset = queryset.filter(
        status=STATUS_CODE_PUBLISHED,
    )

    queryset = queryset._clone()
    queryset.sort_order_map = sort_order_map
    queryset.sort_order_mapper = sort_order_mapper

    filter_field = request.REQUEST.get("filter_field", None)
    filter_value = request.REQUEST.get("filter_value", None)
    group_by = request.REQUEST.get("group_by", None)

    paginate_by = request.REQUEST.get(
        "paginate_by",
        request.httpstate.get(
            "paginate_galleries_by",
            paginate_by or 24
        )
    )
    paginate_by = int(paginate_by)
    order_by = request.REQUEST.get("order_by", request.httpstate.get("order_by", order_by))

    url_query = []
    if filter_field:
        url_query.append("filter_field=" + filter_field)
    if filter_value:
        url_query.append("filter_value=" + filter_value)
    if order_by:
        url_query.append("order_by=" + order_by)
    if group_by:
        url_query.append("group_by=" + group_by)

    if filter_field and filter_value:
        queryset = queryset.filter(**{filter_field: filter_value})

    try:
        queryset = queryset.sort_by(order_by)
    except Exception:
        pass

    request.httpstate["paginate_galleries_by"] = paginate_by
    request.httpstate["order_by"] = order_by

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
    if context_processors and extra_context:
        queryset_index_dict = {}
        index = 0

        prev_next_use_content_object = extra_context.get('prev_next_use_content_object', False)

        for obj in queryset.iterator():
            if prev_next_use_content_object:
                key = '%s_%s' % (obj.content_type_id, obj.object_id)
            else:
                key = '%s_%s' % (
                    ContentType.objects.get_for_model(queryset.model).id,
                    obj._get_pk_val(),
                )
            queryset_index_dict[key] = index
            index += 1

        if extra_context.get('source_list', None):
            request.httpstate['source_list'] = extra_context['source_list']

        request.httpstate['current_queryset_index_dict'] = queryset_index_dict
        request.httpstate['last_query_string'] = request.META['QUERY_STRING']

    request.httpstate['current_queryset_pk_list'] = [item.pk for item in queryset]
    request.httpstate['current_queryset_model'] = queryset.model

    if paginate_by:
        paginator = Paginator(queryset, paginate_by)
        if not page:
            page = request.GET.get('page', 1)
        try:
            page = int(page)
            current_page = paginator.page(page)
            object_list = current_page.object_list
        except (InvalidPage, ValueError):
            raise Http404

        page_min = max(page - pages_to_display / 2, 1)
        page_max = min(paginator.num_pages + 1, page_min + pages_to_display)
        if page_max == paginator.num_pages + 1:
            page_min = max(page_max - pages_to_display, 1)

        previous_page_number = None
        if current_page.has_previous():
            previous_page_number = current_page.previous_page_number()

        next_page_number = None
        if current_page.has_next():
            next_page_number = current_page.next_page_number()

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
            'hits': queryset.count(),
            'page_hits_min': (page - 1) * paginate_by + 1,
            'page_hits_max': min(page * paginate_by, queryset.count()),
        }, context_processors)
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
    c['show'] = "/{}".format(show)
    c['form'] = form
    c['filter_field'] = filter_field
    c['filter_value'] = filter_value
    c['group_by'] = group_by
    c['order_by'] = order_by
    c['url_query'] = '&amp;'.join(url_query)
    c['sort_order_map'] = sort_order_map

    the_query = request.GET.copy()
    c['query'] = query or the_query.urlencode()

    c['path_without_page'] = re.sub('/page[0-9]+', '', request.path)
    if request.is_ajax():
        c['base_template'] = "base_ajax.html"

    if not template_name:
        model = queryset.model
        template_name = "%s/%s_list.html" % (model._meta.app_label, model._meta.object_name.lower())
    t = template_loader.get_template(template_name)
    return HttpResponse(t.render(c), content_type=content_type)

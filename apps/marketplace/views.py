# -*- coding: UTF-8 -*-
import re
from datetime import datetime

from django.contrib.syndication.views import Feed
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import never_cache
from django.db import models
from django.db import transaction
from django.shortcuts import render_to_response, get_object_or_404

from base_libs.models.base_libs_settings import STATUS_CODE_PUBLISHED
from base_libs.utils.misc import get_website_url
from base_libs.views import access_denied
from jetson.apps.utils.decorators import login_required
from jetson.apps.utils.views import object_list, object_detail, show_form_step
from jetson.apps.memos.models import Memo, MEMO_TOKEN_NAME
from kb.apps.marketplace.forms import ADD_JOB_OFFER_FORM_STEPS, JobOfferSearchForm
from kb.apps.marketplace.models import JobOffer, JobSector, URL_ID_JOB_OFFERS
from jetson.apps.structure.models import Category

class JobOfferFeed(Feed):
    title = ""
    link = ""
    description = ""
    title_template = "marketplace/feeds/feed_title.html"
    description_template = "marketplace/feeds/feed_description.html"

    def get_object(self, request, *args, **kwargs):
        self.request = request
        self.kwargs = kwargs
        return None


    def items(self):
        queryset = self.kwargs['queryset'].order_by('-creation_date')[:20]
        return queryset


@never_cache
@transaction.atomic
@login_required
def add_job_offer(request):
    return show_form_step(request, ADD_JOB_OFFER_FORM_STEPS, extra_context={})


@never_cache
def job_offer_list(request, criterion="", slug="", show="", title="", job_sector_slug=None, category_slug=None, **kwargs):
    """Displays the list of events"""

    # abc_list = None
    # abc_filter = request.GET.get('by-abc', None)

    job_sector = None
    if job_sector_slug:
        job_sector = get_object_or_404(JobSector, slug=job_sector_slug)
        kwargs['queryset'] = kwargs['queryset'].filter(job_sectors__tree_id=job_sector.tree_id)

    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        kwargs['queryset'] = kwargs['queryset'].filter(categories__tree_id=category.tree_id)

    # if not (kwargs.has_key('feed') and kwargs['feed'] == True):
    #     kwargs['queryset'] = kwargs['queryset'].only("id", "published_from",
    #                                                  "job_type", "position", "offering_institution",
    #                                                  "offering_institution_title", "is_commercial",
    #                                                  "url0_type", "url0_link", "is_url0_default", "is_url0_on_hold",
    #                                                  "url1_type", "url1_link", "is_url1_default", "is_url1_on_hold",
    #                                                  "url2_type", "url2_link", "is_url2_default", "is_url2_on_hold"
    #                                                  )

    if show == "memos":
        ct = ContentType.objects.get_for_model(kwargs['queryset'].model)
        memos_ids = Memo.objects.filter(
            collection__token=request.COOKIES.get(MEMO_TOKEN_NAME, None),
            content_type=ct,
        ).values_list("object_id", flat=True)
        kwargs['queryset'] = kwargs['queryset'].filter(
            pk__in=memos_ids,
        )
    elif show == "favorites":
        queryset = kwargs['queryset']
        if not request.user.is_authenticated():
            return access_denied(request)
        tables = ["favorites_favorite"]
        condition = [
            "favorites_favorite.user_id = %d" % request.user.id,
            "favorites_favorite.object_id = marketplace_joboffer.id",
            "favorites_favorite.content_type_id = %d" % ContentType.objects.get_for_model(queryset.model).pk,
        ]
        queryset = queryset.extra(
            tables=tables,
            where=condition,
        ).distinct()
        kwargs['queryset'] = queryset
    elif not show:
        kwargs['queryset'] = kwargs['queryset'].exclude(
            job_type__is_internship=True,
        ).distinct()
    elif show == "all":
        pass
    elif show == "internships":
        kwargs['queryset'] = kwargs['queryset'].filter(
            job_type__is_internship=True,
        ).distinct()
    elif show == "own-%s" % URL_ID_JOB_OFFERS:
        if not request.user.is_authenticated():
            return access_denied(request)
        PersonGroup = models.get_model("groups_networks", "PersonGroup")
        ct = ContentType.objects.get_for_model(kwargs['queryset'].model)
        owned_inst_ids = [
            el['object_id'] for el in PersonGroup.objects.filter(
                groupmembership__user=request.user,
                content_type=ct,
            ).distinct().values("object_id")
            ]
        kwargs['queryset'] = kwargs['queryset'].filter(
            models.Q(creator=request.user)
            | models.Q(contact_person=request.user.profile)
            | models.Q(offering_institution__pk__in=owned_inst_ids)
        )
    if show not in ("related", "own-%s" % URL_ID_JOB_OFFERS, "memos"):
        kwargs['queryset'] = kwargs['queryset'].filter(
            models.Q(published_till__gt=datetime.now()) | models.Q(published_till__isnull=True),
            status=STATUS_CODE_PUBLISHED,
        )

    form = JobOfferSearchForm(data=request.REQUEST)
    if not show:
        form.fields['job_type'].queryset = form.fields['job_type'].queryset.exclude(
            is_internship=True,
        )
    if show == "internships":
        form.fields['job_type'].queryset = form.fields['job_type'].queryset.filter(
            is_internship=True,
        )
    if form.is_valid():
        js = form.cleaned_data['job_sector']
        if js:
            kwargs['queryset'] = kwargs['queryset'].filter(
                job_sectors=js,
            ).distinct()
        jt = form.cleaned_data['job_type']
        cat = form.cleaned_data['category']
        if cat:
            kwargs['queryset'] = kwargs['queryset'].filter(
                categories__lft__gte=cat.lft,
                categories__rght__lte=cat.rght,
                categories__tree_id=cat.tree_id,
            ).distinct()
        if jt:
            kwargs['queryset'] = kwargs['queryset'].filter(
                job_type=jt,
            )
        ql = form.cleaned_data['qualification']
        if ql:
            kwargs['queryset'] = kwargs['queryset'].filter(
                qualifications=ql,
            )

    queryset = kwargs['queryset']

    # abc_list = get_abc_list(queryset, "position", abc_filter)
    # if abc_filter:
    #    queryset = filter_abc(queryset, "position", abc_filter)

    view_type = request.REQUEST.get('view_type', request.httpstate.get(
        "%s_view_type" % URL_ID_JOB_OFFERS,
        "listed",
    ))
    if view_type == "map":
        queryset = queryset.filter(
            postal_address__geoposition__latitude__gte=-90,
        ).distinct()
    kwargs['view_type'] = view_type

    extra_context = kwargs.setdefault("extra_context", {})
    # extra_context['abc_list'] = abc_list
    extra_context['show'] = ("", "/%s" % show)[bool(show and show != "related")]
    extra_context['source_list'] = URL_ID_JOB_OFFERS
    extra_context['form'] = form
    extra_context['job_sector'] = job_sector
    extra_context['category'] = category
    if request.is_ajax():
        extra_context['base_template'] = "base_ajax.html"
    kwargs['extra_context'] = extra_context
    kwargs['httpstate_prefix'] = URL_ID_JOB_OFFERS
    kwargs['queryset'] = queryset

    if kwargs.has_key('feed') and kwargs['feed'] == True:
        feed_part = re.compile("/feed/[^/]+/[^/]+/$")
        url = get_website_url()
        feed_instance = JobOfferFeed()
        response = feed_instance(
            request,
            queryset=queryset,
            title=title or _("CCB Job Offers"),
            link=kwargs.get(
                "link",
                url[:-1] + feed_part.sub("/", request.path) + "?" + (request.META.get("QUERY_STRING", "") or ""),
            ),
        )
        response.content_type = 'application/rss+xml'
        return response
    else:
        return object_list(request, **kwargs)


def job_board(request):
    job_offers = JobOffer.objects.filter(
        models.Q(published_till__gt=datetime.now()) | models.Q(published_till__isnull=True),
        status=STATUS_CODE_PUBLISHED,
    ).order_by('-creation_date')[:4]

    return render_to_response(
        "marketplace/job_board.html",
        {'job_offers': job_offers},
        context_instance=RequestContext(request),
    )


@never_cache
def job_offer_list_feed(request, *args, **kwargs):
    return job_offer_list(request, feed=True, *args, **kwargs)


def job_offer_detail(request, *args, **kwargs):
    from kb.apps.marketplace.models import SECURITY_SUMMAND

    kwargs['object_id'] = int(kwargs['secure_id']) - SECURITY_SUMMAND
    return object_detail(request, *args, **kwargs)


def jobs_talent_in_berlin(request):
    from dicttoxml import dicttoxml
    from django.core.paginator import Paginator, InvalidPage, EmptyPage

    try:
        paginate_by = int(request.GET.get('paginate_by', 24))
    except ValueError as e:
        paginate_by = 24
    if paginate_by > 54:
        paginate_by = 54

    qs = JobOffer.published_objects.filter(
        talent_in_berlin=True,
    ).order_by('-modified_date', '-creation_date')

    paginator = Paginator(qs, paginate_by)  # Show <paginate_by> job offers per page
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1

    try:
        job_offers = paginator.page(page)
    except (EmptyPage, InvalidPage):
        job_offers = paginator.page(paginator.num_pages)

    result = {
        'meta': {
            'paginate_by': paginate_by,
            'total_pages': paginator.num_pages,
            'page': job_offers.number,
        },
        'objects': [],
    }
    for job_offer in job_offers.object_list:
        company = job_offer.offering_institution_title
        company_logo = ""
        if job_offer.offering_institution:
            company = job_offer.offering_institution.title
            if job_offer.offering_institution.image:
                company_logo = get_website_url(job_offer.offering_institution.image.url)
        result['objects'].append({
            'id': job_offer.pk,
            'title': job_offer.position,
            'company': company,
            'url': job_offer.get_url(),
            'description': job_offer.description,
            'company_logo': company_logo,
            'date': (job_offer.modified_date or job_offer.creation_date).strftime('%Y-%m-%d %H:%M'),
            'job_sectors': [js.title for js in job_offer.job_sectors.all()],
            'categories': [js.title for js in job_offer.categories.all()],
            'source': 'http://www.creative-city-berlin.de/',
        })
    return HttpResponse(dicttoxml(result, custom_root="job_offers", attr_type=False), content_type="text/xml")

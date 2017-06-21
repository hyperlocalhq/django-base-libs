# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, url

from kb.apps.marketplace.models import JobOffer
from jetson.apps.utils.context_processors import prev_next_processor

CATEGORY_SLUG = "tanz-theater"

job_offer_list_info = {
    'queryset': JobOffer.objects.all(),
    'template_name': 'marketplace/job_offer_list_under_category.html',
    'paginate_by': 24,
    'allow_empty': True,
    'context_processors': (prev_next_processor,),
    'order_by': "published_from_desc",
    'category_slug': CATEGORY_SLUG,
}

urlpatterns = (
    url(r'^$',
        'kb.apps.marketplace.views.job_offer_list',
        job_offer_list_info,
        name="job_offer_list_global",
        ),
    url(r'^(?P<show>internships)/$',
        'kb.apps.marketplace.views.job_offer_list',
        job_offer_list_info,
        name="job_offer_list_global",
        ),
    url(r'^(?P<show>jobs)/$',
        'kb.apps.marketplace.views.job_offer_list',
        job_offer_list_info,
        name="job_offer_list_global",
        ),
    url(r'^(?P<show>all)/$',
        'kb.apps.marketplace.views.job_offer_list',
        job_offer_list_info,
        name="job_offer_list_global",
        ),
    url(r'feed/(?P<feed_type>[^/]+)/$',
        'kb.apps.marketplace.views.job_offer_list_feed',
        job_offer_list_info,
        ),
    url(r'(?P<show>internships)/feed/(?P<feed_type>[^/]+)/$',
        'kb.apps.marketplace.views.job_offer_list_feed',
        job_offer_list_info,
        ),
    url(r'(?P<show>jobs)/feed/(?P<feed_type>[^/]+)/$',
        'kb.apps.marketplace.views.job_offer_list_feed',
        job_offer_list_info,
        ),
    url(r'(?P<show>all)/feed/(?P<feed_type>[^/]+)/$',
        'kb.apps.marketplace.views.job_offer_list_feed',
        job_offer_list_info,
        ),
)

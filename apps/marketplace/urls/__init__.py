# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, url

from ccb.apps.marketplace.models import JobOffer
from jetson.apps.utils.context_processors import prev_next_processor

job_offer_list_info = {
    'queryset': JobOffer.objects.all(),
    'template_name': 'marketplace/job_offer_list.html',
    'paginate_by': 24,
    'allow_empty': True,
    'context_processors': (prev_next_processor,),
    'order_by': "published_from_desc",
}

job_offer_details_info = {
    'queryset': JobOffer.objects.all(),
    'slug_field': 'slug',
    'template_name': 'marketplace/job_offer_details.html',
    'context_processors': (prev_next_processor,),
}

urlpatterns = (
    url(r'^$',
        'ccb.apps.marketplace.views.job_offer_list',
        job_offer_list_info,
        name="job_offer_list_global",
        ),
    url(r'^create-berlin-jobboard/$',
        'ccb.apps.marketplace.views.job_board'
        ),
    url(r'^talent-in-berlin/$',
        'ccb.apps.marketplace.views.jobs_talent_in_berlin'
        ),
    url(r'^add/$',
        'ccb.apps.marketplace.views.add_job_offer'
        ),
    url(r'^(?P<show>memos)/$',
        'ccb.apps.marketplace.views.job_offer_list',
        job_offer_list_info,
        name="job_offer_list_global",
        ),
    url(r'^(?P<show>favorites)/$',
        'ccb.apps.marketplace.views.job_offer_list',
        job_offer_list_info,
        name="job_offer_list_global",
        ),
    url(r'^(?P<show>internships)/$',
        'ccb.apps.marketplace.views.job_offer_list',
        job_offer_list_info,
        name="job_offer_list_global",
        ),
    url(r'^(?P<show>jobs)/$',
        'ccb.apps.marketplace.views.job_offer_list',
        job_offer_list_info,
        name="job_offer_list_global",
        ),
    url(r'^(?P<show>all)/$',
        'ccb.apps.marketplace.views.job_offer_list',
        job_offer_list_info,
        name="job_offer_list_global",
        ),
    url(r'^(?P<show>own-jobs)/$',
        'ccb.apps.marketplace.views.job_offer_list',
        job_offer_list_info,
        name="job_offer_list_global",
        ),
    url(r'feed/(?P<feed_type>[^/]+)/$',
        'ccb.apps.marketplace.views.job_offer_list_feed',
        job_offer_list_info,
        ),
    url(r'(?P<show>memos)/feed/(?P<feed_type>[^/]+)/$',
        'ccb.apps.marketplace.views.job_offer_list_feed',
        job_offer_list_info,
        ),
    url(r'(?P<show>internships)/feed/(?P<feed_type>[^/]+)/$',
        'ccb.apps.marketplace.views.job_offer_list_feed',
        job_offer_list_info,
        ),
    url(r'(?P<show>jobs)/feed/(?P<feed_type>[^/]+)/$',
        'ccb.apps.marketplace.views.job_offer_list_feed',
        job_offer_list_info,
        ),
    url(r'(?P<show>all)/feed/(?P<feed_type>[^/]+)/$',
        'ccb.apps.marketplace.views.job_offer_list_feed',
        job_offer_list_info,
        ),
    url(r'(?P<show>own-jobs)/feed/(?P<feed_type>[^/]+)/$',
        'ccb.apps.marketplace.views.job_offer_list_feed',
        job_offer_list_info,
        ),
    url(r'^job/(?P<secure_id>\d+)/$',
        'ccb.apps.marketplace.views.job_offer_detail',
        job_offer_details_info,
        name="job_offer_detail",
        ),
    url(r'^job/(?P<slug>[^/]+)/delete/$',
        'ccb.apps.site_specific.views.delete_object',
        {'ot_url_part': 'job'},
        ),
    url(r'^job/(?P<secure_id>[^/]+)/map/$',
        'ccb.apps.marketplace.views.job_offer_detail',
        dict(job_offer_details_info, template_name="marketplace/job_offer_map.html"),
        ),
)

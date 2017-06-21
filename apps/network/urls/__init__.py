# -*- coding: UTF-8 -*-
from django.conf.urls import *
from jetson.apps.utils.context_processors import prev_next_processor
from kb.apps.site_specific.models import ContextItem
from kb.apps.media_gallery.sites import PortfolioSite, URL_ID_PORTFOLIO
from kb.apps.events.models import Event, URL_ID_EVENTS
from kb.apps.institutions.models import Institution
from kb.apps.marketplace.models import JobOffer
from kb.apps.bulletin_board.models import Bulletin
from base_libs.models.base_libs_settings import STATUS_CODE_DRAFT, STATUS_CODE_PUBLISHED

# N.B. The commented out URLs are for working views which are not linked anywhere
# and also not styled correctly.

member_list_info = {
    'queryset': ContextItem.objects.filter(
        content_type__model__in=["person", "institution"],
    ),
    'template_name': 'network/member_list.html',
    'paginate_by': 24,
    'allow_empty': True,
    'context_processors': (prev_next_processor,),
}

member_detail_info = {
    'queryset': ContextItem.objects.filter(
        content_type__model__in=["person", "institution"],
    ),
    'template_name': '',
    'paginate_by': 24,
    'allow_empty': True,
    'context_processors': (prev_next_processor,),
    'slug_field': "slug",
}

event_list_info = {
    'queryset': Event.objects.filter(status="published"),
    'template_name': '',  # template name is defined in the view
    'paginate_by': 24,
    'allow_empty': True,
    'context_processors': (prev_next_processor,),
}

job_list_info = {
    'queryset': JobOffer.objects.filter(status=STATUS_CODE_PUBLISHED),
    'template_name': '',  # template name is defined in the view
    'paginate_by': 24,
    'allow_empty': True,
    'context_processors': (prev_next_processor,),
}

bulletin_list_info = {
    'queryset': Bulletin.objects.filter(status="published"),
    'template_name': '',  # template name is defined in the view
    'paginate_by': 24,
    'allow_empty': True,
    'context_processors': (prev_next_processor,),
}

institution_list_info = {
    'queryset': Institution.objects.filter(status="published"),
    'template_name': '',  # template name is defined in the view
    'paginate_by': 24,
    'allow_empty': True,
    'context_processors': (prev_next_processor,),
}


urlpatterns = [
    url(r'^$', 'kb.apps.network.views.member_list',
        member_list_info, name='member_list_global'),
    url(r'^(?P<show>contacts|following|memos|own-institutions|relationships)/$',
        'kb.apps.network.views.member_list',
        member_list_info),
    url(
        r'^(?P<show>invitations|requested|requests)/$',
        'kb.apps.people.views.person_invitation_list',
        dict(member_list_info, template_name="people/person_invitations_list.html")
    ),
    url(r'^add-institution/$', 'kb.apps.institutions.views.add_institution'),

    url(r'^member/(?P<slug>[^/]+)/$', 'kb.apps.network.views.member_detail', member_detail_info, name="member_detail"),
    # url(r'^member/(?P<slug>[^/]+)/network/$', 'kb.apps.network.views.member_detail',
    #     dict(member_detail_info, template_name="people/person_network.html")),
    # url(r'^member/(?P<slug>[^/]+)/network/person_contacts/$',
    #     'kb.apps.people.views.person_person_contacts_list',
    #     dict(member_list_info, template_name="people/person_person_contacts.html")),
    # url(r'^member/(?P<slug>[^/]+)/network/institution_contacts/$',
    #     'kb.apps.people.views.person_institution_contacts_list',
    #     dict(member_list_info, template_name="people/person_institution_contacts.html")),
    # url(r'^member/(?P<slug>[^/]+)/network/%s/$' % URL_ID_PERSONGROUPS,
    #     'kb.apps.people.views.person_groups_list',
    #     dict(group_list_info, template_name="people/person_groups.html")),

    url(
        r'^member/(?P<slug>[^/]+)/%s/' % URL_ID_PORTFOLIO,
        include(PortfolioSite(
            object_detail_dict=member_detail_info,
            app_name="network",
            name="member",
        ).urls),
    ),
    
    # details of institution, events, documents or persons
    url(r'^member/(?P<slug>[^/]+)/$', 'kb.apps.network.views.member_detail',
        member_detail_info, name="member_detail"),

    # url(r'^member/(?P<slug>[^/]+)/network/$', 'kb.apps.network.views.member_detail',
    #     dict(member_detail_info, template_name="institutions/institution_network.html")),
    # url(r'^member/(?P<slug>[^/]+)/network/staff/$',
    #     'kb.apps.institutions.views.institution_staff_list',
    #     dict(member_list_info, template_name="institutions/institution_staff.html")),
    # url(r'^member/(?P<slug>[^/]+)/network/partners/$',
    #     'kb.apps.institutions.views.institution_partners_list',
    #     dict(member_list_info, template_name="institutions/institution_partners.html")),
    # url(r'^member/(?P<slug>[^/]+)/network/%s/$' % URL_ID_PERSONGROUPS,
    #     'kb.apps.institutions.views.institution_groups_list',
    #     dict(group_list_info, template_name="institutions/institution_groups.html")),
    # url(r'^member/(?P<slug>[^/]+)/projects/$', 'kb.apps.network.views.member_detail',
    #     dict(member_detail_info,
    #          template_name="institutions/institution_projects.html")),

    url(
        r'^member/(?P<slug>[^/]+)/%s/'
        r'('
        r'(?P<start_date>\d{8})'
        r'((?P<unlimited>...)|-(?P<end_date>\d{8}))?/'
        r')?'
        r'$' % URL_ID_EVENTS,
        'kb.apps.network.views.member_events_list',
        event_list_info,
        name="member_event_list"
    ),
    url(
        r'^member/(?P<slug>[^/]+)/%s/'
        r'('
        r'(?P<start_date>\d{8})'
        r'((?P<unlimited>...)|-(?P<end_date>\d{8}))?/'
        r')?'
        r'ical/$' % URL_ID_EVENTS,
        'kb.apps.network.views.member_events_list_ical',
        event_list_info,
    ),
    url(
        r'^member/(?P<slug>[^/]+)/%s/'
        r'('
        r'(?P<start_date>\d{8})'
        r'((?P<unlimited>...)|-(?P<end_date>\d{8}))?/'
        r')?'
        r'feed/(?P<feed_type>[^/]+)/$' % URL_ID_EVENTS,
        'kb.apps.network.views.member_events_list_feed',
        event_list_info,
    ),

    url(
        r'^member/(?P<slug>[^/]+)/jobs/'
        r'('
        r'(?P<start_date>\d{8})'
        r'((?P<unlimited>...)|-(?P<end_date>\d{8}))?/'
        r')?'
        r'$',
        'kb.apps.network.views.member_jobs_list',
        job_list_info,
        name="member_job_list"
    ),
    url(
        r'^member/(?P<slug>[^/]+)/jobs/'
        r'('
        r'(?P<start_date>\d{8})'
        r'((?P<unlimited>...)|-(?P<end_date>\d{8}))?/'
        r')?'
        r'ical/$',
        'kb.apps.network.views.member_jobs_list_ical',
        job_list_info,
    ),
    url(
        r'^member/(?P<slug>[^/]+)/jobs/'
        r'('
        r'(?P<start_date>\d{8})'
        r'((?P<unlimited>...)|-(?P<end_date>\d{8}))?/'
        r')?'
        r'feed/(?P<feed_type>[^/]+)/$',
        'kb.apps.network.views.member_jobs_list_feed',
        job_list_info,
    ),

    url(
        r'^member/(?P<slug>[^/]+)/bulletins/'
        r'('
        r'(?P<start_date>\d{8})'
        r'((?P<unlimited>...)|-(?P<end_date>\d{8}))?/'
        r')?'
        r'$',
        'kb.apps.network.views.member_bulletins_list',
        bulletin_list_info,
        name="member_bulletin_list"
    ),
    url(
        r'^member/(?P<slug>[^/]+)/bulletins/'
        r'('
        r'(?P<start_date>\d{8})'
        r'((?P<unlimited>...)|-(?P<end_date>\d{8}))?/'
        r')?'
        r'ical/$',
        'kb.apps.network.views.member_bulletins_list_ical',
        bulletin_list_info,
    ),
    url(
        r'^member/(?P<slug>[^/]+)/bulletins/'
        r'('
        r'(?P<start_date>\d{8})'
        r'((?P<unlimited>...)|-(?P<end_date>\d{8}))?/'
        r')?'
        r'feed/(?P<feed_type>[^/]+)/$',
        'kb.apps.network.views.member_bulletins_list_feed',
        bulletin_list_info,
    ),
    url(
        r'^member/(?P<slug>[^/]+)/institutions/',
        'kb.apps.network.views.member_institution_list',
        event_list_info,
        name="member_event_list"
    ),

    # url(
    #     r'^member/(?P<slug>[^/]+)/%s/'
    #     r'$' % URL_ID_JOB_OFFERS,
    #     'kb.apps.institutions.views.institution_job_offer_list',
    #     dict(
    #         job_offer_list_info,
    #         template_name="institutions/institution_job_offers.html",
    #     ),
    #     name="institution_job_offer_list"
    # ),
    # url(
    #     r'^member/(?P<slug>[^/]+)/%s/'
    #     r'feed/(?P<feed_type>[^/]+)/$' % URL_ID_JOB_OFFERS,
    #     'kb.apps.institutions.views.institution_job_offer_list_feed',
    #     dict(
    #         job_offer_list_info,
    #         template_name="institutions/institution_job_offers.html",
    #     )
    # ),
    # url(r'^member/(?P<slug>[^/]+)/reviews/$', 'kb.apps.network.views.member_detail',
    #     dict(member_detail_info, template_name="institutions/institution_reviews.html")),

    url(r'^member/(?P<slug>[^/]+)/claim/$',
        'kb.apps.site_specific.views.claim_object',
        {'ot_url_part': 'institution'},
    ),

    url(r'^member/(?P<slug>[^/]+)/message/$',
        'jetson.apps.messaging.views.contact',
        dict(member_detail_info, template_name='network/member_message.html')),
    url(r'^member/(?P<slug>[^/]+)/message/alldone/$',
        'jetson.apps.messaging.views.contact_done',
        dict(member_detail_info, template_name='network/member_message.html')),

    url(r'^member/(?P<slug>[^/]+)/invite/',
        'kb.apps.groups_networks.views.invite_institution_members',
    ),

    url(r'^(?P<object_url_part>member/(?P<slug>[^/]+)/)(?P<url_identifier>blog)/',
        include('kb.apps.blog.urls'),
        {
            'only_for_this_site': True,
            'include': ["member"],
        }
    ),
]

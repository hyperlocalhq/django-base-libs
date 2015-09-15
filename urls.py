# -*- coding: UTF-8 -*-

from django.conf import settings
from django.conf.urls import *
from django.contrib.auth.models import User
from django.contrib import admin
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

from cms.sitemaps import CMSSitemap

from jetson.apps.utils.decorators import login_required
from jetson.apps.location.models import Address
from jetson.apps.utils.views import object_detail
from jetson.apps.utils.context_processors import prev_next_processor

from ccb.apps.media_gallery.models import URL_ID_PORTFOLIO
from ccb.apps.media_gallery.models import MediaGallery
from ccb.apps.people.models import Person, URL_ID_PERSON, URL_ID_PEOPLE
from ccb.apps.people.views import _person_list_filter
from ccb.apps.institutions.models import Institution, URL_ID_INSTITUTION, URL_ID_INSTITUTIONS
from ccb.apps.institutions.views import _institution_list_filter
from ccb.apps.resources.models import Document, URL_ID_DOCUMENT, URL_ID_DOCUMENTS
from ccb.apps.resources.views import _document_list_filter
from ccb.apps.events.models import Event, URL_ID_EVENT, URL_ID_EVENTS
from ccb.apps.marketplace.models import JobOffer, URL_ID_JOB_OFFER, URL_ID_JOB_OFFERS
from ccb.apps.groups_networks.models import PersonGroup, URL_ID_PERSONGROUP, URL_ID_PERSONGROUPS

from ccb.apps.media_gallery.sites import PortfolioSite

_project_name = "ccb"

admin.autodiscover()

handler404 = "jetson.apps.error_handler.views.page_not_found"
handler500 = "jetson.apps.error_handler.views.server_error"

"""
OBJECT_URL_MAPPER defines a map for identifiying any object from 
an url part formed as "<<model_identifier>>/<<object_identifier>>",
for instance "person/aidas/" or "insitution/studio38/".Additionally, 
a "base template" name should be provided to identify a base template 
for an app.
"""
OBJECT_URL_MAPPER = {
    URL_ID_PERSON: (Person, 'user__username', "people/details_base.html"),
    URL_ID_INSTITUTION: (Institution, 'slug', "institutions/details_base.html"),
    URL_ID_DOCUMENT: (Document, 'slug', "resources/documents/details_base.html"),
    URL_ID_EVENT: (Event, 'slug', "events/details_base.html"),
    URL_ID_PERSONGROUP: (PersonGroup, 'slug', "groups_networks/persongroups/details_base.html"),
}

country_lookup = {
    'queryset': Address._meta.get_field("country").get_choices(),
    'field': False,
    'limit': 9,
    'login_required': False,
}

institution_lookup = {
    'queryset': Institution.objects.all(),
    'field': 'title',
    'limit': 9,
    'login_required': True,
}

person_lookup = {
    'queryset': User.objects.all(),
    'field': 'username',
    'limit': 9,
    'login_required': True,
}

search_dict = {
    'template_name': 'search/search.html',
    'result_template_name': 'search/searchresults.html',
    'paginate_by': 10,
    'refine': False,
    'context_processors': (prev_next_processor,),
}

search_refine_dict = {
    'template_name': 'search/search.html',
    'result_template_name': 'search/searchresults.html',
    'paginate_by': 10,
    'refine': True,
    'context_processors': (prev_next_processor,),
}

simplesearch_dict = {
    'paginate_by': 10,
    'context_processors': (prev_next_processor,),
}

institution_list_info = {
    'queryset': Institution.objects.order_by('title'),
    'template_name': 'institutions/institution_list.html',
    'paginate_by': 10,
    'allow_empty': True,
    'context_processors': (prev_next_processor,),
}

institution_details_info = {
    'queryset': Institution.objects.all(),
    'slug_field': 'slug',
    'template_name': 'institutions/institution_details.html',
    'context_processors': (prev_next_processor,),
    'context_item_type': URL_ID_INSTITUTION,
}

document_list_info = {
    'queryset': Document.objects.filter(status__in=("published", "published_commercial")),
    'template_name': 'resources/documents/document_list.html',
    'paginate_by': 10,
    'allow_empty': True,
    'context_processors': (prev_next_processor,),
}

document_details_info = {
    'queryset': Document.objects.filter(status__in=("published", "published_commercial")),
    'slug_field': 'slug',
    'template_name': 'resources/documents/document_details.html',
    'context_processors': (prev_next_processor,),
    'context_item_type': URL_ID_DOCUMENT,
}

event_list_info = {
    'queryset': Event.objects.all(),
    'template_name': 'events/event_list.html',
    'paginate_by': 10,
    'allow_empty': True,
    'context_processors': (prev_next_processor,),
}

event_details_info = {
    'queryset': Event.objects.all(),
    'slug_field': 'slug',
    'template_name': 'events/event_details.html',
    'context_processors': (prev_next_processor,),
    'context_item_type': URL_ID_EVENT,
}

job_offer_list_info = {
    'queryset': JobOffer.objects.all(),
    'template_name': 'marketplace/job_offer_list.html',
    'paginate_by': 20,
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

person_list_info = {
    'queryset': Person.objects.select_related().order_by('auth_user.username'),
    'template_name': 'people/person_list.html',
    'paginate_by': 10,
    'allow_empty': True,
    'context_processors': (prev_next_processor,),
}

person_details_info = {
    'queryset': Person.objects.all(),
    'slug_field': 'user__username',
    'template_name': 'people/person_details.html',
    'context_processors': (prev_next_processor,),
    'context_item_type': URL_ID_PERSON,
}

gallery_list_info = {
    'queryset': MediaGallery.objects.all(),
    'template_name': 'media_gallery/gallery_list.html',
    'paginate_by': 15,
    'allow_empty': True,
}

group_list_info = {
    'queryset': PersonGroup.objects.order_by('title'),
    'template_name': 'groups_networks/persongroups/group_list.html',
    'paginate_by': 10,
    'context_processors': (prev_next_processor,),
    'allow_empty': True,
}

group_details_info = {
    'queryset': PersonGroup.objects.all().order_by('title'),
    'template_name': 'groups_networks/persongroups/group_details.html',
    'slug_field': 'slug',
    'context_processors': (prev_next_processor,),
    'context_item_type': URL_ID_PERSONGROUP,
}

list_list_info = {
    'queryset': PersonGroup.objects.none(),
    'template_name': 'site_specific/lists/list_list.html',
    'paginate_by': 10,
    'allow_empty': True,
}

from ccb.apps.site_specific.feeds import LatestPublishedObjectsRssFeed, LatestPublishedObjectsAtomFeed

# feeds for the newest persons, institutions, etc.
latest_published_objects_feeds = {
    'rss': LatestPublishedObjectsRssFeed,
    'atom': LatestPublishedObjectsAtomFeed,
}

from ccb.apps.media_gallery.feeds import MediaGalleryRssFeed, MediaGalleryAtomFeed

latest_media_galleries = {
    'rss': MediaGalleryRssFeed,
    'atom': MediaGalleryAtomFeed,
    'queryset': MediaGallery.objects.order_by("-creation_date")[:50],
}

from ccb.apps.site_specific.sitemap import ContextItemSitemap

sitemaps = {
    'contextitems': ContextItemSitemap,
}

urlpatterns = i18n_patterns(
    '',
    # root
    url(r'^$', 'ccb.apps.site_specific.views.splash_page', name="splash_page"),

    # global js settings
    url(r'^jssettings/$', 'jetson.apps.utils.views.direct_to_js_template',
        {'template_name': 'settings.js'}, name="jssettings"),

    # info subscription
    url(r'^subscribe4info/$', 'jetson.apps.mailchimp.views.subscribe_for_info',
        name="subscribe4info"),
    url(r'^subscribe4info/done/$',
        TemplateView.as_view(template_name='mailchimp/subscription_done.html'),
        name="subscribe4info_done"),

    url(r'^compatibility/$',
        TemplateView.as_view(template_name='site_specific/compatibility.html'),
        name="compatibility"),

    # info trouble-tickets
    url(r'^ticket/$', _project_name + '.apps.tracker.views.create_ticket',
        name="create_ticket"),
    url(r'^ticket/(?P<concern>[^/]+)/$', _project_name + '.apps.tracker.views.create_ticket',
        name="create_ticket"),
    url(r'^ticket/(?P<content_type_id>[0-9]+)/(?P<object_id>[0-9]+)/$',
        _project_name + '.apps.tracker.views.create_ticket', name="create_ticket"),
    url(r'^ticket/(?P<concern>[^/]+)/(?P<content_type_id>[0-9]+)/(?P<object_id>[0-9]+)/$',
        _project_name + '.apps.tracker.views.create_ticket', name="create_ticket"),

    # info search
    url(r'^search/', include("ccb.apps.search.urls")),

    # simplesearch
    url(r'^simplesearch/$', _project_name + '.apps.search.views.simplesearch',
        simplesearch_dict, name="simple_search"),
    url(r'^(?P<ot_url_part>%s|%s|%s|%s|%s)/simplesearch/$' % (
        URL_ID_DOCUMENTS, URL_ID_EVENTS, URL_ID_PERSONGROUPS, URL_ID_INSTITUTIONS,
        URL_ID_PEOPLE),
        _project_name + '.apps.search.views.simplesearch', simplesearch_dict,
        name="model_specific_simple_search"),
    url(r'^(?P<ot_url_part>%s)/simplesearch/ical/$' % URL_ID_EVENTS,
        _project_name + '.apps.search.views.simplesearch_ical', simplesearch_dict,
        name="model_specific_simple_search"),

    # simplesearch for creative sectors
    url(r'^creative-sector/[^/]+/simplesearch/$',
        _project_name + '.apps.search.views.simplesearch', simplesearch_dict,
        name="cs_simple_search"),
    url(r'^creative-sector/[^/]+/(?P<ot_url_part>%s|%s|%s|%s|%s)/simplesearch/$' % (
        URL_ID_DOCUMENTS, URL_ID_EVENTS, URL_ID_PERSONGROUPS, URL_ID_INSTITUTIONS,
        URL_ID_PEOPLE),
        _project_name + '.apps.search.views.simplesearch', simplesearch_dict,
        name="cs_model_specific_simple_search"),

    # info vCard
    url(r'^vcard/(?P<content_type_id>[0-9]+)/(?P<object_id>[0-9]+)/$',
        'ccb.apps.site_specific.views.get_vcard', name="vcard"),
)

urlpatterns += patterns(
    'django.views.static',
    # media
    url(r'^uploads/(?P<path>.*)$', 'serve', {'document_root': settings.UPLOADS_ROOT},
        name="uploads_url"),
    url(r'^media/(?P<path>.*)$', 'serve', {'document_root': settings.MEDIA_ROOT}, name="media_url"),
    # url(r'^static/\d+/(?P<path>.*)$', 'serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^jetson-media/\d+/(?P<path>.*)$', 'serve', {'document_root': settings.JETSON_MEDIA_ROOT},
        name="jetson_media_url"),
    url(
        r'^admin-media/(?P<path>.*)$',
        'serve',
        {
            'document_root': settings.GRAPPELLI_MEDIA_ROOT,
        },
        name="admin_media_url"
    ),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

### HELPERS (system urls not visible directly for the users) ###
urlpatterns += patterns(
    '',  # no views specified
    # ajax lookups
    url(r'^tagging_autocomplete/', include('tagging_autocomplete.urls')),
    url(r'^helper/country_lookup/$', 'jetson.apps.utils.views.jquery_autocomplete_lookup', country_lookup,
        name="country_lookup"),
    url(r'^helper/country/(?P<country_code>[A-Z]{2})/$', 'jetson.apps.i18n.views.json_country_name',
        name="json_country_lookup"),
    url(r'^helper/%s_lookup/$' % URL_ID_INSTITUTION, 'jetson.apps.utils.views.jquery_autocomplete_lookup',
        institution_lookup, name="institution_lookup"),
    url(r'^helper/%s_lookup/$' % URL_ID_PERSON, 'jetson.apps.utils.views.jquery_autocomplete_lookup', person_lookup,
        name="person_lookup"),

    # helper for getting related objects from given contenttype
    url(
        r'^helper/objects_to_select/(?P<app_name>[^/]+)/(?P<model_name>[^/]+)/(?P<obj_pk>[^/]+)/(?P<field_name>[^/]+)/of/(?P<content_type_id>[0-9]+)/$',
        'base_libs.views.views.json_objects_to_select'),
    url(r'^helper/favorite/(?P<content_type_id>[0-9]+)/(?P<object_id>[0-9]+)/$',
        'ccb.apps.favorites.views.json_set_favorite'),
    url(r'^helper/individual_relation/(?P<username>[^/]+)/$',
        'jetson.apps.individual_relations.views.json_manage_individual_relation'),
    url(r'^helper/memo/(?P<content_type_id>[0-9]+)/(?P<object_id>[0-9]+)/$', 'jetson.apps.memos.views.json_set_memo'),
    url(r'^helper/bookmark/$', 'jetson.apps.bookmarks.views.json_manage_bookmark'),
    # ajax lookups for review ratings
    url(r'^helper/tmpimage/(?P<filename>[^/]+)/(?P<width>\d+)x(?P<height>\d+)/$', 'jetson.apps.utils.images.image_view',
        {'mod_function': None}),
    url(r'^helper/tmpimage/(?P<width>\d+)x(?P<height>\d+)/$', 'jetson.apps.utils.images.image_view',
        {'mod_function': None}),

    url(r'^helper/popup-window/(?P<window_type>[^/]+)/$', 'ccb.apps.site_specific.views.popup_window'),
    url(
        r'^helper/individual-relation/(?P<action>edit|invite|accept|cancel|deny|block|unblock|remove)/(?P<username>[^/]+)/$',
        'jetson.apps.individual_relations.views.manage_individual_relationship'),
    url(r'^helper/%s-membership/(?P<action>edit|request|cancel|remove|accept-%s|deny-%s)/(?P<slug>[^/]+)/$' % (
        URL_ID_PERSONGROUP, URL_ID_PERSONGROUP, URL_ID_PERSONGROUP),
        'ccb.apps.groups_networks.views.manage_group_membership'),
    url(
        r'^helper/%s-membership/(?P<action>accept-user|deny-user|remove-user|cancel-user)/(?P<slug>[^/]+)/(?P<username>[^/]+)/$' % URL_ID_PERSONGROUP,
        'ccb.apps.groups_networks.views.manage_group_membership'),
    url(r'^helper/edit-%s-member/(?P<slug>[^/]+)/(?P<user_id>[0-9]+)/$' % URL_ID_PERSONGROUP,
        'ccb.apps.groups_networks.views.edit_group_member'),

    url(r'^helper/edit-(?P<object_type>%s|%s|%s|%s|%s|%s)-profile/(?P<slug>[^/]+)/$' % (
        URL_ID_JOB_OFFER, URL_ID_EVENT, URL_ID_DOCUMENT, URL_ID_PERSONGROUP, URL_ID_INSTITUTION, URL_ID_PERSON),
        'ccb.apps.site_specific.views.edit_profile'),

    url(
        r'^helper/edit-(?P<object_type>%s|%s|%s|%s|%s|%s)-profile/'
        r'(?P<slug>[^/]+)/(?P<section_name>'
        r'organizer|'
        r'opening_hours|'
        r'payment|'
        r'identity|'
        r'fees_opening_hours|'
        r'fees|'
        r'event_times|'
        r'details|'
        r'description|'
        r'categories|'
        r'avatar|'
        r'additional_info'
        r')/$' % (
            URL_ID_JOB_OFFER,
            URL_ID_EVENT,
            URL_ID_DOCUMENT,
            URL_ID_PERSONGROUP,
            URL_ID_INSTITUTION,
            URL_ID_PERSON,
        ),
        'ccb.apps.site_specific.views.edit_profile',
    ),
    url(r'^helper/edit-(?P<object_type>%s|%s)-profile/(?P<slug>[^/]+)/(?P<section_name>contact)/$' % (
        URL_ID_JOB_OFFER, URL_ID_EVENT), 'ccb.apps.site_specific.views.edit_profile'),
    url(r'^helper/edit-(?P<object_type>%s|%s)-profile/(?P<slug>[^/]+)/(?P<section_name>contact)/(?P<index>[^/]+)/$' % (
        URL_ID_INSTITUTION, URL_ID_PERSON), 'ccb.apps.site_specific.views.edit_profile'),
    url(r'^helper/(?P<object_type>%s|%s|%s|%s)-profile/(?P<slug>[^/]+)/contact/(?P<index>[^/]+)/$' % (
        URL_ID_JOB_OFFER, URL_ID_EVENT, URL_ID_INSTITUTION, URL_ID_PERSON,),
        'ccb.apps.site_specific.views.show_contact'),

    url(
        r'^helper/autocomplete/(?P<app>[^/]+)/(?P<qs_function>[^/]+)/(?P<display_attr>[^/]+)/(?P<add_display_attr>[^/]+)/$',
        'base_libs.views.ajax_autocomplete'),

    url(r'^helper/accounts/%s_attrs/(?P<institution_id>[0-9]+)/$' % URL_ID_INSTITUTION,
        _project_name + '.apps.institutions.ajax.json_get_institution_attrs'),

    url(r'^helper/%s/%s_attrs/(?P<institution_id>[0-9]+)/$' % (URL_ID_EVENT, URL_ID_INSTITUTION),
        _project_name + '.apps.events.ajax.json_get_institution_attrs'),

    url(r'^helper/%s/%s_attrs/(?P<institution_id>[0-9]+)/$' % (URL_ID_JOB_OFFER, URL_ID_INSTITUTION),
        _project_name + '.apps.marketplace.ajax.json_get_institution_attrs'),

    url(r'^helper/site-visitors/$', "ccb.apps.site_specific.views.site_visitors"),
)

urlpatterns += i18n_patterns(
    '',
    url(r'^recrop/', include('jetson.apps.image_mods.urls')),
    url(r'^%s/$' % URL_ID_INSTITUTIONS,
        _project_name + '.apps.institutions.views.institution_list',
        dict(list_filter=_institution_list_filter, **institution_list_info)),
    url(r'^%s/(?P<show>favorites|memos|own-%s)/$' % (URL_ID_INSTITUTIONS, URL_ID_INSTITUTIONS),
        _project_name + '.apps.institutions.views.institution_list',
        dict(list_filter=_institution_list_filter, **institution_list_info)),
    url(r'^%s/add/$' % URL_ID_INSTITUTIONS,
        _project_name + '.apps.institutions.views.add_institution'),

    # details of institution, events, documents or persons
    url(r'^%s/(?P<slug>[^/]+)/$' % URL_ID_INSTITUTION, object_detail,
        institution_details_info),
    url(r'^%s/(?P<slug>[^/]+)/map/$' % URL_ID_INSTITUTION, object_detail,
        dict(institution_details_info, template_name="institutions/institution_map.html")),
    url(r'^%s/(?P<slug>[^/]+)/network/$' % URL_ID_INSTITUTION, object_detail,
        dict(institution_details_info, template_name="institutions/institution_network.html")),
    url(r'^%s/(?P<slug>[^/]+)/network/staff/$' % URL_ID_INSTITUTION,
        _project_name + '.apps.institutions.views.institution_staff_list',
        dict(person_list_info, template_name="institutions/institution_staff.html")),
    url(r'^%s/(?P<slug>[^/]+)/network/partners/$' % URL_ID_INSTITUTION,
        _project_name + '.apps.institutions.views.institution_partners_list',
        dict(institution_list_info, template_name="institutions/institution_partners.html")),
    url(r'^%s/(?P<slug>[^/]+)/network/%s/$' % (URL_ID_INSTITUTION, URL_ID_PERSONGROUPS),
        _project_name + '.apps.institutions.views.institution_groups_list',
        dict(group_list_info, template_name="institutions/institution_groups.html")),

    url(
        r'^%s/(?P<slug>[^/]+)/%s/fb-sync/$' % (URL_ID_INSTITUTION, URL_ID_PORTFOLIO),
        "ccb.apps.facebook_app.views.sync_institutional_portfolio"
    ),
    url(
        r'^%s/(?P<slug>[^/]+)/%s/' % (URL_ID_INSTITUTION, URL_ID_PORTFOLIO),
        include(PortfolioSite(
            object_detail_dict=institution_details_info,
            app_name="institutions",
            name="institution",
        ).urls),
    ),

    url(r'^%s/(?P<slug>[^/]+)/projects/$' % URL_ID_INSTITUTION, object_detail,
        dict(institution_details_info,
             template_name="institutions/institution_projects.html")),

    url(
        r'^%s/(?P<slug>[^/]+)/%s/'
        r'('
        r'(?P<start_date>\d{8})'
        r'((?P<unlimited>...)|-(?P<end_date>\d{8}))?/'
        r')?'
        r'$' % (URL_ID_INSTITUTION, URL_ID_EVENTS),
        _project_name + '.apps.institutions.views.institution_events_list',
        dict(
            event_list_info,
            template_name="institutions/institution_events.html",
        ),
        name="institution_events_list"
    ),
    url(
        r'^%s/(?P<slug>[^/]+)/%s/'
        r'('
        r'(?P<start_date>\d{8})'
        r'((?P<unlimited>...)|-(?P<end_date>\d{8}))?/'
        r')?'
        r'ical/$' % (URL_ID_INSTITUTION, URL_ID_EVENTS),
        _project_name + '.apps.institutions.views.institution_events_list_ical',
        dict(
            event_list_info,
            template_name="institutions/institution_events.html",
        )
    ),
    # FIXME
    # url(
    #     r'^%s/(?P<slug>[^/]+)/%s/'
    #     r'('
    #     r'(?P<start_date>\d{8})'
    #     r'((?P<unlimited>...)|-(?P<end_date>\d{8}))?/'
    #     r')?'
    #     r'feed/(?P<feed_type>[^/]+)/$' % (URL_ID_INSTITUTION, URL_ID_EVENTS),
    #     _project_name + '.apps.institutions.views.institution_events_list_feed',
    #     dict(
    #         event_list_info,
    #         template_name="institutions/institution_events.html",
    #     )
    # ),

    url(
        r'^%s/(?P<slug>[^/]+)/%s/'
        r'$' % (URL_ID_INSTITUTION, URL_ID_JOB_OFFERS),
        _project_name + '.apps.institutions.views.institution_job_offer_list',
        dict(
            job_offer_list_info,
            template_name="institutions/institution_job_offers.html",
        ),
        name="institution_job_offer_list"
    ),
    # FIXME
    # url(
    #     r'^%s/(?P<slug>[^/]+)/%s/'
    #     r'feed/(?P<feed_type>[^/]+)/$' % (URL_ID_INSTITUTION, URL_ID_JOB_OFFERS),
    #     _project_name + '.apps.institutions.views.institution_job_offer_list_feed',
    #     dict(
    #         job_offer_list_info,
    #         template_name="institutions/institution_job_offers.html",
    #     )
    # ),

    url(r'^%s/(?P<slug>[^/]+)/reviews/$' % URL_ID_INSTITUTION, object_detail,
        dict(institution_details_info, template_name="institutions/institution_reviews.html")),
    url(r'^%s/(?P<slug>[^/]+)/message/$' % URL_ID_INSTITUTION,
        'jetson.apps.messaging.views.contact',
        dict(institution_details_info, template_name='institutions/institution_message.html')),
    url(r'^%s/(?P<slug>[^/]+)/message/alldone/$' % URL_ID_INSTITUTION,
        'jetson.apps.messaging.views.contact_done',
        dict(institution_details_info, template_name='institutions/institution_message.html')),

    url(r'^%s/(?P<slug>[^/]+)/invite/' % URL_ID_INSTITUTION,
        'ccb.apps.groups_networks.views.invite_institution_members',
        ),

    url(r'^%s/$' % URL_ID_DOCUMENTS, _project_name + '.apps.resources.views.document_list',
        dict(list_filter=_document_list_filter, **document_list_info)),
    url(
        r'^%s/(?P<show>favorites|memos|cultural-funding|scholarship|support-programme|information-founders|other)/$' % URL_ID_DOCUMENTS,
        _project_name + '.apps.resources.views.document_list',
        dict(list_filter=_document_list_filter, **document_list_info)),

    url(r'^%s/(?P<slug>[^/]+)/$' % URL_ID_DOCUMENT, object_detail, document_details_info),
    url(r'^%s/(?P<slug>[^/]+)/reviews/$' % URL_ID_DOCUMENT, object_detail,
        dict(document_details_info,
             template_name="resources/documents/document_reviews.html")),
    url(r'^%s/(?P<slug>[^/]+)/network/$' % URL_ID_DOCUMENT, object_detail,
        dict(document_details_info,
             template_name="resources/documents/document_network.html")),

    url(
        r'^%s/'
        r'((?P<show>favorites|memos|own-%s)/)?'
        r'('
        r'(?P<start_date>\d{8})'
        r'((?P<unlimited>...)|-(?P<end_date>\d{8}))?/'
        r')?'
        r'$' % (URL_ID_EVENTS, URL_ID_EVENTS),
        _project_name + '.apps.events.views.event_list',
        event_list_info,
        name="event_list_global",
    ),
    url(
        r'^%s/'
        r'((?P<show>favorites|memos|own-%s)/)?'
        '('
        r'(?P<start_date>\d{8})'
        r'((?P<unlimited>...)|-(?P<end_date>\d{8}))?/'
        r')?'
        r'ical/$' % (URL_ID_EVENTS, URL_ID_EVENTS),
        _project_name + '.apps.events.views.event_list_ical',
        event_list_info,
    ),
    # FIXME
    # url(
    #     r'^%s/'
    #     r'((?P<show>favorites|memos|own-%s)/)?'
    #     '('
    #     r'(?P<start_date>\d{8})'
    #     r'((?P<unlimited>...)|-(?P<end_date>\d{8}))?/'
    #     r')?'
    #     r'feed/(?P<feed_type>[^/]+)/$' % (URL_ID_EVENTS, URL_ID_EVENTS),
    #     _project_name + '.apps.events.views.event_list_feed',
    #     event_list_info,
    # ),
    url(r'^%s/add/$' % URL_ID_EVENTS, _project_name + '.apps.events.views.add_event'),

    # events have their dates prefixed (or not, if there aren't any)
    url(
        r'^%s/(?P<slug>[^/]+)/((?P<event_time>\d+)/)?$' % URL_ID_EVENT,
        _project_name + '.apps.events.views.event_detail',
        event_details_info,
    ),
    url(
        r'^%s/(?P<slug>[^/]+)/claim/$' % URL_ID_EVENT,
        'ccb.apps.site_specific.views.claim_object',
        {'ot_url_part': URL_ID_EVENT},
    ),
    url(
        r'^%s/(?P<slug>[^/]+)/delete/$' % URL_ID_EVENT,
        'ccb.apps.site_specific.views.delete_object',
        {'ot_url_part': URL_ID_EVENT},
    ),
    url(
        r'^%s/(?P<slug>[^/]+)/map/$' % URL_ID_EVENT,
        object_detail,
        dict(event_details_info, template_name="events/event_map.html"),
    ),
    url(
        r'^%s/(?P<slug>[^/]+)/reviews/$' % URL_ID_EVENT,
        object_detail,
        dict(
            event_details_info,
            template_name="events/event_reviews.html",
        ),
    ),
    url(
        r'^%s/(?P<slug>[^/]+)/network/$' % URL_ID_EVENT,
        object_detail,
        dict(
            event_details_info,
            template_name="events/event_network.html",
        ),
    ),
    url(
        r'^%s/(?P<slug>[^/]+)/((?P<event_time>\d+)/)?ical/$' % URL_ID_EVENT,
        _project_name + '.apps.events.views.event_ical',
    ),

    url(
        r'^%s/(?P<slug>[^/]+)/%s/' % (URL_ID_EVENT, URL_ID_PORTFOLIO),
        include(PortfolioSite(
            object_detail_dict=event_details_info,
            app_name="events",
            name="event",
        ).urls),
    ),

    url(r'^%s/$' % URL_ID_PEOPLE, _project_name + '.apps.people.views.person_list',
        dict(list_filter=_person_list_filter, **person_list_info)),
    url(r'^%s/(?P<show>contacts|relationships|memos)/$' % URL_ID_PEOPLE,
        _project_name + '.apps.people.views.person_list',
        dict(list_filter=_person_list_filter, **person_list_info)),
    url(
        r'^%s/(?P<show>invitations|requested|requests)/$' % URL_ID_PEOPLE,
        _project_name + '.apps.people.views.person_invitation_list',
        dict(person_list_info, template_name="people/person_invitations_list.html")
    ),

    url(r'^%s/(?P<slug>[^/]+)/$' % URL_ID_PERSON, object_detail, person_details_info),
    url(r'^%s/(?P<slug>[^/]+)/map/$' % URL_ID_PERSON, object_detail,
        dict(person_details_info, template_name="people/person_map.html")),
    url(r'^%s/(?P<slug>[^/]+)/network/$' % URL_ID_PERSON, object_detail,
        dict(person_details_info, template_name="people/person_network.html")),
    url(r'^%s/(?P<slug>[^/]+)/network/person_contacts/$' % URL_ID_PERSON,
        _project_name + '.apps.people.views.person_person_contacts_list',
        dict(person_list_info, template_name="people/person_person_contacts.html")),
    url(r'^%s/(?P<slug>[^/]+)/network/institution_contacts/$' % URL_ID_PERSON,
        _project_name + '.apps.people.views.person_institution_contacts_list',
        dict(institution_list_info, template_name="people/person_institution_contacts.html")),
    url(r'^%s/(?P<slug>[^/]+)/network/%s/$' % (URL_ID_PERSON, URL_ID_PERSONGROUPS),
        _project_name + '.apps.people.views.person_groups_list',
        dict(group_list_info, template_name="people/person_groups.html")),

    url(
        r'^%s/(?P<slug>[^/]+)/%s/fb-sync/$' % (URL_ID_PERSON, URL_ID_PORTFOLIO),
        "ccb.apps.facebook_app.views.sync_personal_portfolio"
    ),
    url(
        r'^%s/(?P<slug>[^/]+)/%s/' % (URL_ID_PERSON, URL_ID_PORTFOLIO),
        include(PortfolioSite(
            object_detail_dict=person_details_info,
            app_name="people",
            name="person",
        ).urls),
    ),

    url(r'^%s/create-berlin-jobboard/$' % URL_ID_JOB_OFFERS,
        _project_name + '.apps.marketplace.views.job_board'),
    url(r'^%s/talent-in-berlin/$' % URL_ID_JOB_OFFERS,
        _project_name + '.apps.marketplace.views.jobs_talent_in_berlin'),
    url(r'^%s/add/$' % URL_ID_JOB_OFFERS,
        _project_name + '.apps.marketplace.views.add_job_offer'),
    url(
        r'^%s/'
        r'((?P<show>memos|internships|jobs|all|own-%s)/)?'
        r'$' % (URL_ID_JOB_OFFERS, URL_ID_JOB_OFFERS),
        _project_name + '.apps.marketplace.views.job_offer_list',
        job_offer_list_info,
        name="job_offer_list_global",
    ),
    # FIXME
    # url(
    #     r'^%s/'
    #     r'((?P<show>memos|internships|jobs|all|own-%s)/)?'
    #     r'feed/(?P<feed_type>[^/]+)/$' % (URL_ID_JOB_OFFERS, URL_ID_JOB_OFFERS),
    #     _project_name + '.apps.marketplace.views.job_offer_list_feed',
    #     job_offer_list_info,
    # ),

    url(
        r'^%s/(?P<secure_id>\d+)/$' % URL_ID_JOB_OFFER,
        _project_name + '.apps.marketplace.views.job_offer_detail',
        job_offer_details_info,
    ),
    url(
        r'^%s/(?P<slug>[^/]+)/delete/$' % URL_ID_JOB_OFFER,
        'ccb.apps.site_specific.views.delete_object',
        {'ot_url_part': URL_ID_JOB_OFFER},
    ),
    url(
        r'^%s/(?P<secure_id>[^/]+)/map/$' % URL_ID_JOB_OFFER,
        _project_name + '.apps.marketplace.views.job_offer_detail',
        dict(job_offer_details_info, template_name="marketplace/job_offer_map.html"),
    ),

    url(r'^%s/(?P<slug>[^/]+)/projects/$' % URL_ID_PERSON, object_detail,
        dict(person_details_info, template_name="people/person_projects.html")),
    url(
        r'^%s/(?P<slug>[^/]+)/%s/'
        r'('
        r'(?P<start_date>\d{8})'
        r'((?P<unlimited>...)|-(?P<end_date>\d{8}))?/'
        r')?'
        r'$' % (URL_ID_PERSON, URL_ID_EVENTS),
        _project_name + '.apps.people.views.person_events_list',
        dict(event_list_info, template_name="people/person_events.html"),
        name="person_events_list"
    ),
    url(
        r'^%s/(?P<slug>[^/]+)/%s/'
        r'('
        r'(?P<start_date>\d{8})'
        r'((?P<unlimited>...)|-(?P<end_date>\d{8}))?/'
        r')?'
        r'ical/$' % (URL_ID_PERSON, URL_ID_EVENTS),
        _project_name + '.apps.people.views.person_events_list_ical',
        dict(event_list_info, template_name="people/person_events.html")
    ),
    # FIXME
    # url(
    #     r'^%s/(?P<slug>[^/]+)/%s/'
    #     r'('
    #     r'(?P<start_date>\d{8})'
    #     r'((?P<unlimited>...)|-(?P<end_date>\d{8}))?/'
    #     r')?'
    #     r'feed/(?P<feed_type>[^/]+)/$' % (URL_ID_PERSON, URL_ID_EVENTS),
    #     _project_name + '.apps.people.views.person_events_list_feed',
    #     dict(event_list_info, template_name="people/person_events.html")
    # ),

    url(
        r'^%s/(?P<slug>[^/]+)/%s/'
        r'$' % (URL_ID_PERSON, URL_ID_JOB_OFFERS),
        _project_name + '.apps.people.views.person_job_offer_list',
        dict(job_offer_list_info, template_name="people/person_job_offers.html"),
        name="person_job_offer_list"
    ),
    # FIXME
    # url(
    #     r'^%s/(?P<slug>[^/]+)/%s/'
    #     r'feed/(?P<feed_type>[^/]+)/$' % (URL_ID_PERSON, URL_ID_JOB_OFFERS),
    #     _project_name + '.apps.people.views.person_job_offer_list_feed',
    #     dict(job_offer_list_info, template_name="people/person_job_offers.html")
    # ),

    url(r'^%s/(?P<slug>[^/]+)/reviews/$' % URL_ID_PERSON, object_detail,
        dict(person_details_info, template_name="people/person_reviews.html")),
    url(r'^%s/(?P<slug>[^/]+)/message/$' % URL_ID_PERSON,
        'jetson.apps.messaging.views.contact',
        dict(person_details_info, template_name='people/person_message.html')),
    url(r'^%s/(?P<slug>[^/]+)/message/alldone/$' % URL_ID_PERSON,
        'jetson.apps.messaging.views.contact_done',
        dict(person_details_info, template_name='people/person_message.html')),

    url(r'^%s/$' % URL_ID_PERSONGROUPS, 'ccb.apps.groups_networks.views.persongroup_list',
        group_list_info),
    url(
        r'^%s/(?P<show>favorites|memos)/$' % URL_ID_PERSONGROUPS,
        'ccb.apps.groups_networks.views.persongroup_list',
        group_list_info,
    ),

    url(
        r'^%s/(?P<show>own-groups)/$' % URL_ID_PERSONGROUPS,
        'ccb.apps.groups_networks.views.persongroup_list',
        dict(
            group_list_info,
            template_name="groups_networks/persongroups/group_list_own.html",
        ),
    ),

    url(r'^%s/invitations/$' % URL_ID_PERSONGROUPS,
        'ccb.apps.groups_networks.views.persongroup_invitation_list'),
    url(r'^%s/invitations/(?P<group_ind>my-%s|other-%s|invite-to-%s)/$' % (
        URL_ID_PERSONGROUPS, URL_ID_PERSONGROUPS, URL_ID_PERSONGROUPS, URL_ID_PERSONGROUP),
        'ccb.apps.groups_networks.views.persongroup_invitation_list'),

    url(
        r'^%s/invitations/(?P<group_ind>my-%s|other-%s|invite-to-%s)/(?P<show>invitations|requests)/$' % (
            URL_ID_PERSONGROUPS, URL_ID_PERSONGROUPS, URL_ID_PERSONGROUPS, URL_ID_PERSONGROUP),
        'ccb.apps.groups_networks.views.persongroup_invitation_list',
        dict(
            group_list_info,
            template_name="groups_networks/persongroups/group_invitations_list.html",
        ),
    ),

    url(r'^%s/add/$' % URL_ID_PERSONGROUPS, 'ccb.apps.groups_networks.views.add_group'),

    url(r'^%s/(?P<slug>[^/]+)/$' % URL_ID_PERSONGROUP, object_detail, group_details_info),
    url(
        r'^%s/(?P<slug>[^/]+)/(?P<section>admins|moderators|members|unconfirmed|invited)/$' % URL_ID_PERSONGROUP,
        'ccb.apps.groups_networks.views.view_persongroup_members',
    ),
    url(
        r'^%s/(?P<slug>[^/]+)/members/invite/$' % URL_ID_PERSONGROUP,
        'ccb.apps.groups_networks.views.invite_persongroup_members',
    ),
    url(r'^%s/(?P<slug>[^/]+)/member/(?P<user_id>[0-9]+)/edit/$' % URL_ID_PERSONGROUP,
        'ccb.apps.groups_networks.views.edit_group_member'),

    url(r'^%s/(?P<slug>[^/]+)/projects/$' % URL_ID_PERSONGROUP, object_detail,
        dict(group_details_info,
             template_name="groups_networks/persongroups/group_projects.html")),
    url(r'^%s/(?P<slug>[^/]+)/%s/$' % (URL_ID_PERSONGROUP, URL_ID_EVENTS), object_detail,
        group_details_info),

    url(r'^lists/$', 'jetson.apps.utils.views.object_list', list_list_info),

    url(r'^(?P<section>%s|%s)/(?P<slug>[^/]+)/invited/(?P<encrypted_email>.+)/$' % (
        URL_ID_INSTITUTION, URL_ID_PERSON),
        'ccb.apps.groups_networks.views.confirm_invitation'),

    # used for wrapping the reviews see
    url(r'^(%s|%s|%s|%s|%s)/(?P<slug>[^/]+)/post/$' % (
        URL_ID_EVENT, URL_ID_DOCUMENT, URL_ID_PERSONGROUP, URL_ID_INSTITUTION, URL_ID_PERSON),
        'ccb.apps.site_specific.views.wrap_post_comment'),

    url(r'^(%s|%s|%s|%s|%s)/(?P<slug>[^/]+)/deletereview/(?P<id>\d+)/$' % (
        URL_ID_EVENT, URL_ID_DOCUMENT, URL_ID_PERSONGROUP, URL_ID_INSTITUTION, URL_ID_PERSON),
        'ccb.apps.site_specific.views.delete_review'),

    # i18n
    url(r'^i18n/setlang/$', 'jetson.apps.utils.views.set_language'),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', {'packages': 'ccb'}),

    # gmap
    url(r'^gmap/$', TemplateView.as_view(template_name='gmap/index.html')),
    url(r'^map/$', TemplateView.as_view(template_name='gmap/object_list.html')),
    url(r'^map/object-list/$', 'ccb.apps.site_specific.views.object_list_for_map'),

    url(r'^admin/site_specific/claimrequest/(?P<object_id>.+)/(?P<action>approve|deny)/$',
        'ccb.apps.site_specific.views.claim_action', name="admin_claim_action"),
    url(r'^admin/', include('jetson.apps.extendedadmin.urls')),
    url(r'^grappelli/', include('grappelli.urls')),

    url(r'^dashboard/$', login_required(
        TemplateView.as_view(template_name='accounts/my_profile/view_profile.html')),
        name="dashboard"),
    url(r'^my-profile/$', "ccb.apps.site_specific.views.my_profile", name="my_profile"),
    url(r'^my-profile/memos/$', 'jetson.apps.memos.views.memos',
        {'template_name': 'memos/memos.html'}),
    url(r'^my-profile/favorites/$', 'ccb.apps.favorites.views.favorites',
        {'template_name': 'generic/favorites.html'}),
    url(r'^my-profile/bookmarks/$', 'jetson.apps.bookmarks.views.bookmarks',
        {'template_name': 'generic/bookmarklist.html'}),
    url(r'^my-profile/privacy/$',
        _project_name + '.apps.people.views.change_privacy_settings'),
    url(r'^my-profile/delete/$', _project_name + '.apps.site_specific.views.delete_profile'),
    url(r'^my-profile/delete/done/$',
        TemplateView.as_view(template_name='accounts/my_profile/delete_profile_done.html')),

    url(r'^my-messages/', include("jetson.apps.messaging.urls")),

    # accounts and registration
    url(r'^account/$', TemplateView.as_view(template_name='accounts/index.html')),
    url(r'^login', _project_name + '.apps.people.views.login',
        {'template_name': 'accounts/login.html'}, name="login"),
    url(r'^logout', 'ccb.apps.facebook_app.views.logout', {'next_page': "/"}),
    url(r'^changeuser/', 'django.contrib.auth.views.logout_then_login'),
    url(r'^register/$', _project_name + '.apps.people.views.register'),
    url(r'^register/done/$',
        TemplateView.as_view(template_name='accounts/register_verify_required.html')),
    url(r'^register/alldone/$',
        login_required(TemplateView.as_view(template_name='accounts/register_done.html'))),
    url(r'^register/(?P<encrypted_email>[a-zA-Z0-9\+/_\-=]+)/$',
        _project_name + '.apps.people.views.confirm_registration'),
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset',
        {'template_name': 'accounts/password_reset_form.html',
         'email_template_name': 'accounts/password_reset_email.html'}),
    url(r'^password_reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'template_name': 'accounts/password_reset_confirm.html'}),
    url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done',
        {'template_name': 'accounts/password_reset_done.html'}, name="password_reset_done"),
    url(r'^password_reset/complete/$', 'django.contrib.auth.views.password_reset_complete',
        {'template_name': 'accounts/password_reset_complete.html'}),
    url(r'^password_change/$', 'django.contrib.auth.views.password_change',
        {'template_name': 'accounts/password_change_form.html'}),
    url(r'^password_change/done/$',
        'django.contrib.auth.views.password_change_done',
        {'template_name': 'accounts/password_change_done.html'},
        name='password_change_done'),
    url(r'^facebook/', include('ccb.apps.facebook_app.urls')),

    # articles
    url(r'^news/', include('ccb.apps.articles.urls')),

    #
    url(r'^creative-sector/$',
        'ccb.apps.site_specific.views.redirect_to_creative_sector',
        ),

    # articles for creative sector overview
    url(r'^creative-sector/(?P<creative_sector_slug>[^/]+)/$',
        TemplateView.as_view(template_name='site_specific/creative_sector_overview.html')
        ),

    url(r'^creative-sector/[^/]+/(?P<url>.*)$',
        'jetson.apps.flatpages.views.flatpage'
        ),

    url(r'^contact/', include("jetson.apps.contact_form.urls")),

    url(r'^invite/$', "ccb.apps.site_specific.views.invite", name="invite"),
    url(r'^invite/done/$',
        TemplateView.as_view(template_name="site_specific/invitation_done.html"),
        name="invite_done"),

    url(r'^notification/', include("jetson.apps.notification.urls")),

    # claiming
    url(r'^(?P<ot_url_part>%s|%s|%s)/(?P<slug>[^/]+)/claim/$' % (
        URL_ID_INSTITUTION, URL_ID_EVENT, URL_ID_DOCUMENT),
        'ccb.apps.site_specific.views.claim_object'
        ),

    # latest object feeds
    # FIXME
    # url(r'^(?P<ot_url_part>%s|%s|%s|%s|%s)/latest_published/feeds/(?P<feed_type>.*)/$' % (
    #     URL_ID_DOCUMENTS, URL_ID_EVENTS, URL_ID_PERSONGROUPS, URL_ID_INSTITUTIONS,
    #     URL_ID_PEOPLE),
    #     'jetson.apps.utils.views.feed', latest_published_objects_feeds),

    # sitemaps
    url(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),

    url(r'^portfolios/((?P<show>favorites|memos|featured)/)?$',
        'ccb.apps.media_gallery.views.gallery_list', gallery_list_info),
    url(r'^portfolios/feeds/(?P<feed_type>.*)/$', 'jetson.apps.utils.views.feed',
        latest_media_galleries),

    # style guide
    url(r'^styleguide/', include('jetson.apps.styleguide.urls')),

    # blog! (must be placed after admin urls!!!!!!)
    url(r'^(?P<object_url_part>([^/]+/[^/]+/)?)(?P<url_identifier>blog)/',
        include('jetson.apps.blog.urls'),
        {
            'only_for_this_site': True,
            'include': [None, URL_ID_PERSON, URL_ID_INSTITUTION],
        }
        ),

    url(r'^kreativarbeiten/$', lambda request: redirect("/kreativarbeiten/blog/")),

    url(r'^kreativarbeiten/blog/', include('jetson.apps.blog.urls'),
        {
            'url_identifier': "kreativarbeiten/blog",
            'object_url_part': None,
            'only_for_this_site': True,
            'include': [None],
            'base_template': "site_specific/kreativarbeiten_blog_base.html",
        }
        ),
    url(
        r'^kreativarbeiten/events/'
        r'('
        r'(?P<start_date>\d{8})'
        r'((?P<unlimited>...)|-(?P<end_date>\d{8}))?/'
        r')?'
        r'$',
        'ccb.apps.people.views.person_events_list',
        dict(event_list_info, template_name="site_specific/kreativarbeiten_events.html",
             slug="NellyHolle"),
        name="kreativarbeiten_events_list"
    ),
    url(r'^kreativarbeiten/best-practice/$',
        "ccb.apps.site_specific.views.kreativarbeiten_best_practice"),
    url(r'^kreativarbeiten/contact/$',
        "ccb.apps.site_specific.views.kreativarbeiten_contact_form"),
    url(r'^kreativarbeiten/contact/done/$', TemplateView.as_view(
        template_name='site_specific/kreativarbeiten_contact_form_done.html')),

    (r'^kreativarbeiten/tweets/$', 'ccb.apps.twitter.views.latest_tweets', {
        'twitter_username': "dirkkiefer",
        'number_of_tweets': 5,
    }),
    # FIXME
    # (r'^kreativarbeiten/newsfeed/$', 'ccb.apps.site_specific.views.newsfeed', {
    #     'rss': "http://www.kultur-kreativ-wirtschaft.de/KuK/Navigation/Service/RSS/rss-aktuelles.xml",
    #     'number_of_news': 5,
    # }),

    url(r'^livestream/$', TemplateView.as_view(template_name='site_specific/livestream.html')),

    # general FAQs and Help
    url(r'^(?P<object_url_part>([^/]+/[^/]+/)?)(?P<url_identifier>faqs|help|contacts)/',
        include('ccb.apps.faqs.urls'),
        {
            'only_for_this_site': True,
            'include': [None],
        }
        ),

    (r'^tweets/$', 'ccb.apps.twitter.views.latest_tweets', {
        'twitter_username': settings.TWITTER_USERNAME,
        'number_of_tweets': settings.TWITTER_NUMBER_OF_TWEETS,
    }),

    url(r'^select2/', include('django_select2.urls')),
    url(r'^relaunch2015/sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': {'cmspages': CMSSitemap}}),
    url(r'^relaunch2015/', include('cms.urls')),
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += i18n_patterns(
        '',
        url(r'^rosetta/', include('rosetta.urls')),
    )

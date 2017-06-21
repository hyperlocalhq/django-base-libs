# -*- coding: UTF-8 -*-
from django.conf import settings
from django.conf.urls import *
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

from cms.sitemaps import CMSSitemap

from jetson.apps.location.models import Address
from jetson.apps.utils.views import object_detail
from jetson.apps.utils.context_processors import prev_next_processor

from kb.apps.media_gallery.models import MediaGallery
from kb.apps.people.models import Person, URL_ID_PERSON, URL_ID_PEOPLE
from kb.apps.institutions.models import Institution, URL_ID_INSTITUTION, URL_ID_INSTITUTIONS
from kb.apps.resources.models import Document, URL_ID_DOCUMENT, URL_ID_DOCUMENTS
from kb.apps.resources.views import _document_list_filter
from kb.apps.events.models import Event, URL_ID_EVENT, URL_ID_EVENTS
from kb.apps.marketplace.models import URL_ID_JOB_OFFER, URL_ID_JOB_OFFERS
from kb.apps.groups_networks.models import PersonGroup, URL_ID_PERSONGROUP, URL_ID_PERSONGROUPS
from kb.apps.site_specific.models import ContextItem

_project_name = "kb"

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
    "member": (ContextItem, 'slug', "network/details_base.html"),
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


# begin TODO: remote these variables after migrating app to django-cms
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
# end


from kb.apps.site_specific.feeds import LatestPublishedObjectsRssFeed, LatestPublishedObjectsAtomFeed

# feeds for the newest persons, institutions, etc.
latest_published_objects_feeds = {
    'rss': LatestPublishedObjectsRssFeed(),
    'atom': LatestPublishedObjectsAtomFeed(),
}

# begin TODO: remote these variables after migrating app to django-cms
from kb.apps.media_gallery.feeds import MediaGalleryRssFeed, MediaGalleryAtomFeed

latest_media_galleries = {
    'rss': MediaGalleryRssFeed(),
    'atom': MediaGalleryAtomFeed(),
    'queryset': MediaGallery.objects.order_by("-creation_date")[:50],
}
# end

from kb.apps.site_specific.sitemap import ContextItemSitemap

sitemaps = {
    'contextitems': ContextItemSitemap,
}

urlpatterns = i18n_patterns(
    '',

    # global js settings
    url(r'^jssettings/$', 'jetson.apps.utils.views.direct_to_js_template',
        {'template_name': 'settings.js'}, name="jssettings"),

    # info subscription
    url(r'^subscribe-to-newsletter/$', 'jetson.apps.mailchimp.views.subscribe_for_info',
        name="subscribe4info"),
    url(r'^subscribe-to-newsletter/done/$',
        TemplateView.as_view(template_name='mailchimp/subscription_done.html'),
        name="subscribe4info_done"),

    url(r'^compatibility/$',
        TemplateView.as_view(template_name='site_specific/compatibility.html'),
        name="compatibility"),

    url(r'^500/$',
        TemplateView.as_view(template_name='500.html'),
        name="error_500"),

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
    url(r'^search/', include("kb.apps.search.urls")),

    # info vCard
    url(r'^vcard/(?P<content_type_id>[0-9]+)/(?P<object_id>[0-9]+)/$',
        'kb.apps.site_specific.views.get_vcard', name="vcard"),

    url(r'kreativkultur/events/$', 'kb.apps.kreativkultur.views.event_list'),
    url(r'kreativkultur/events/js/$', 'kb.apps.kreativkultur.views.event_list_js'),
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
urlpatterns += i18n_patterns(
    '',  # no views specified
    # ajax lookups
    url(r'^tagging_autocomplete/', include('tagging_autocomplete.urls')),
    url(r'^helper/country_lookup/$', 'jetson.apps.utils.views.jquery_autocomplete_lookup', country_lookup,
        name="country_lookup"),
    url(r'^helper/country/(?P<country_code>[A-Z]{2})/$', 'jetson.apps.i18n.views.json_country_name',
        name="json_country_lookup"),
    url(r'^helper/%s_lookup/$' % URL_ID_INSTITUTION, 'jetson.apps.utils.views.jquery_autocomplete_lookup',
        institution_lookup, name="institution_lookup"),

    # helper for getting related objects from given contenttype
    url(
        r'^helper/objects_to_select/(?P<app_name>[^/]+)/(?P<model_name>[^/]+)/(?P<obj_pk>[^/]+)/(?P<field_name>[^/]+)/of/(?P<content_type_id>[0-9]+)/$',
        'base_libs.views.views.json_objects_to_select'),
    url(r'^helper/favorite/(?P<content_type_id>[0-9]+)/(?P<object_id>[0-9]+)/$',
        'kb.apps.favorites.views.json_set_favorite'),
    url(r'^helper/individual_relation/(?P<username>[^/]+)/$',
        'jetson.apps.individual_relations.views.json_manage_individual_relation'),
    # ajax lookups for review ratings
    url(r'^helper/tmpimage/(?P<filename>[^/]+)/(?P<width>\d+)x(?P<height>\d+)/$', 'jetson.apps.utils.images.image_view',
        {'mod_function': None}),
    url(r'^helper/tmpimage/(?P<width>\d+)x(?P<height>\d+)/$', 'jetson.apps.utils.images.image_view',
        {'mod_function': None}),

    url(r'^helper/popup-window/(?P<window_type>[^/]+)/$', 'kb.apps.site_specific.views.popup_window'),
    url(
        r'^helper/individual-relation/(?P<action>edit|invite|accept|cancel|deny|block|unblock|remove)/(?P<username>[^/]+)/$',
        'jetson.apps.individual_relations.views.manage_individual_relationship'),
    url(r'^helper/%s-membership/(?P<action>edit|request|cancel|remove|accept-%s|deny-%s)/(?P<slug>[^/]+)/$' % (
        URL_ID_PERSONGROUP, URL_ID_PERSONGROUP, URL_ID_PERSONGROUP),
        'kb.apps.groups_networks.views.manage_group_membership'),
    url(
        r'^helper/%s-membership/(?P<action>accept-user|deny-user|remove-user|cancel-user)/(?P<slug>[^/]+)/(?P<username>[^/]+)/$' % URL_ID_PERSONGROUP,
        'kb.apps.groups_networks.views.manage_group_membership'),
    url(r'^helper/edit-%s-member/(?P<slug>[^/]+)/(?P<user_id>[0-9]+)/$' % URL_ID_PERSONGROUP,
        'kb.apps.groups_networks.views.edit_group_member'),

    url(r'^helper/edit-(?P<object_type>%s|%s|%s|%s|%s|%s)-profile/(?P<slug>[^/]+)/$' % (
        URL_ID_JOB_OFFER, URL_ID_EVENT, URL_ID_DOCUMENT, URL_ID_PERSONGROUP, URL_ID_INSTITUTION, URL_ID_PERSON),
        'kb.apps.site_specific.views.edit_profile', name="edit_profile"),

    url(r'^helper/edit-(?P<object_type>%s|%s)-profile/(?P<slug>[^/]+)/contact/$' % (
        URL_ID_INSTITUTION, URL_ID_PERSON), 'kb.apps.site_specific.views.show_contacts', name="show_profile_contacts"),
    url(r'^helper/edit-(?P<object_type>%s|%s)-profile/(?P<slug>[^/]+)/contact/add/$' % (
        URL_ID_INSTITUTION, URL_ID_PERSON), 'kb.apps.site_specific.views.edit_profile', {'section_name': 'contact'}, name="add_profile_contact"),
    url(r'^helper/edit-(?P<object_type>%s|%s)-profile/(?P<slug>[^/]+)/contact/(?P<index>\d+)/$' % (
        URL_ID_INSTITUTION, URL_ID_PERSON), 'kb.apps.site_specific.views.edit_profile', {'section_name': 'contact'}, name="change_profile_contact"),
    url(r'^helper/edit-(?P<object_type>%s|%s)-profile/(?P<slug>[^/]+)/contact/(?P<index>\d+)/delete/$' % (
        URL_ID_INSTITUTION, URL_ID_PERSON), 'kb.apps.site_specific.views.delete_contact', name="delete_profile_contact"),

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
        r'contact|'
        r'additional_info'
        r')/$' % (
            URL_ID_JOB_OFFER,
            URL_ID_EVENT,
            URL_ID_DOCUMENT,
            URL_ID_PERSONGROUP,
            URL_ID_INSTITUTION,
            URL_ID_PERSON,
        ),
        'kb.apps.site_specific.views.edit_profile',
    ),
    url(r'^helper/edit-(?P<object_type>%s|%s)-profile/(?P<slug>[^/]+)/(?P<section_name>contact)/$' % (
        URL_ID_JOB_OFFER, URL_ID_EVENT), 'kb.apps.site_specific.views.edit_profile'),
    url(r'^helper/edit-(?P<object_type>%s|%s)-profile/(?P<slug>[^/]+)/(?P<section_name>contact)/add/$' % (
        URL_ID_JOB_OFFER, URL_ID_EVENT), 'kb.apps.site_specific.views.edit_profile'),

    # TODO: check if the following rule is being used anywhere
    url(r'^helper/(?P<object_type>%s|%s|%s|%s)-profile/(?P<slug>[^/]+)/contact/(?P<index>\d+)/$' % (
        URL_ID_JOB_OFFER, URL_ID_EVENT, URL_ID_INSTITUTION, URL_ID_PERSON,),
        'kb.apps.site_specific.views.show_contact'),

    url(
        r'^helper/autocomplete/(?P<app>[^/]+)/(?P<qs_function>[^/]+)/(?P<display_attr>[^/]+)/(?P<add_display_attr>[^/]+)/$',
        'base_libs.views.ajax_autocomplete'),

    url(r'^helper/accounts/%s_attrs/(?P<institution_id>[0-9]+)/$' % URL_ID_INSTITUTION,
        _project_name + '.apps.institutions.ajax.json_get_institution_attrs'),

    url(r'^helper/%s/%s_attrs/(?P<institution_id>[0-9]+)/$' % (URL_ID_EVENT, URL_ID_INSTITUTION),
        _project_name + '.apps.events.ajax.json_get_institution_attrs'),

    url(r'^helper/%s/%s_attrs/(?P<institution_id>[0-9]+)/$' % (URL_ID_JOB_OFFER, URL_ID_INSTITUTION),
        _project_name + '.apps.marketplace.ajax.json_get_institution_attrs'),

    url(r'^helper/site-visitors/$', "kb.apps.site_specific.views.site_visitors"),

    # iframely wrapper
    url(r'^helper/iframely/$', 'jetson.apps.iframely.views.iframely_wrapper', name="iframely_wrapper"),
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += i18n_patterns(
        '',
        url(r'^rosetta/', include('rosetta.urls')),
    )

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += patterns(
        '',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )

urlpatterns += i18n_patterns(
    '',
    url(r'^recrop/', include('jetson.apps.image_mods.urls')),

    # begin TODO: remote these URLs after migrating app to django-cms
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

    url(r'^%s/create-berlin-jobboard/$' % URL_ID_JOB_OFFERS,
        _project_name + '.apps.marketplace.views.job_board'),
    url(r'^%s/talent-in-berlin/$' % URL_ID_JOB_OFFERS,
        _project_name + '.apps.marketplace.views.jobs_talent_in_berlin'),

    url(r'^(?P<section>%s|%s)/(?P<slug>[^/]+)/invited/(?P<encrypted_email>.+)/$' % (
        URL_ID_INSTITUTION, URL_ID_PERSON),
        'kb.apps.groups_networks.views.confirm_invitation'),

    # i18n
    url(r'^i18n/setlang/$', 'jetson.apps.utils.views.set_language'),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', {'packages': 'kb'}),

    # gmap
    url(r'^gmap/$', TemplateView.as_view(template_name='gmap/index.html')),

    url(r'^admin/site_specific/claimrequest/(?P<object_id>.+)/(?P<action>approve|deny)/$',
        'kb.apps.site_specific.views.claim_action', name="admin_claim_action"),
    url(r'^admin/', include('jetson.apps.extendedadmin.urls')),
    url(r'^grappelli/', include('grappelli.urls')),

    url(r'^my-profile/$', "kb.apps.site_specific.views.my_profile", name="my_profile"),
    url(r'^my-profile/privacy/$',
        'kb.apps.accounts.views.change_privacy_settings', name="privacy_settings"),
    url(r'^my-profile/delete/$', _project_name + '.apps.site_specific.views.delete_profile'),
    url(r'^my-profile/delete/done/$',
        TemplateView.as_view(template_name='accounts/my_profile/delete_profile_done.html')),

    url(r'^my-messages/', include("jetson.apps.messaging.urls")),

    # accounts and registration
    url(r'^', include('kb.apps.accounts.urls')),

    url(r'^contact/', include("jetson.apps.contact_form.urls")),

    url(r'^notification/', include("jetson.apps.notification.urls")),

    # claiming
    url(r'^(?P<ot_url_part>%s|%s|%s)/(?P<slug>[^/]+)/claim/$' % (
        URL_ID_INSTITUTION, URL_ID_EVENT, URL_ID_DOCUMENT),
        'kb.apps.site_specific.views.claim_object'
        ),

    # latest object feeds
    url(r'^(?P<ot_url_part>%s|%s|%s|%s|%s)/latest_published/feeds/(?P<feed_type>.*)/$' % (
        URL_ID_DOCUMENTS, URL_ID_EVENTS, URL_ID_PERSONGROUPS, URL_ID_INSTITUTIONS,
        URL_ID_PEOPLE),
        'jetson.apps.utils.views.feed', latest_published_objects_feeds),

    # style guide
    url(r'^styleguide/', include('jetson.apps.styleguide.urls')),

    # general FAQs and Help
    url(r'^(?P<object_url_part>([^/]+/[^/]+/)?)(?P<url_identifier>faqs|help)/',
        include('kb.apps.faqs.urls'),
        {
            'only_for_this_site': True,
            'include': [None],
        }
    ),
    url(r'^(?P<url_identifier>contacts)/',
        include('kb.apps.faqs.urls'),
        {
            'object_url_part': None,
            'only_for_this_site': True,
            'include': [None],
        }
    ),

    url(r'^tweets/$', 'kb.apps.twitter.views.latest_tweets', {
        'twitter_username': settings.TWITTER_USERNAME,
        'number_of_tweets': settings.TWITTER_NUMBER_OF_TWEETS,
    }),
    url(r'^tweets/(?P<twitter_username>.+)/$', 'kb.apps.twitter.views.latest_tweets', {
        'number_of_tweets': settings.TWITTER_NUMBER_OF_TWEETS,
    }),

    url(r'^select2/', include('django_select2.urls')),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': {'cmspages': CMSSitemap}}),
    url(r'^activity/', include('actstream.urls')),
    url(r'^', include('cms.urls')),
)

# -*- coding: UTF-8 -*-
import os

import django
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib.auth.models import User
from django.contrib import admin
from django.db import models

from filebrowser.settings import MEDIA_ROOT as UPLOADS_ROOT
from filebrowser.settings import MEDIA_URL as UPLOADS_URL

from jetson.apps.location.models import Address
from jetson.apps.media_gallery.models import URL_ID_PORTFOLIO

app = models.get_app("people")
Person, URL_ID_PERSON, URL_ID_PEOPLE = (
    app.Person, app.URL_ID_PERSON, app.URL_ID_PEOPLE,
    )

app = models.get_app("institutions")
Institution, URL_ID_INSTITUTION, URL_ID_INSTITUTIONS = (
    app.Institution, app.URL_ID_INSTITUTION, app.URL_ID_INSTITUTIONS,
    )

app = models.get_app("events")
Event, URL_ID_EVENT, URL_ID_EVENTS = (
    app.Event, app.URL_ID_EVENT, app.URL_ID_EVENTS,
    )

app = models.get_app("resources")
Document, URL_ID_DOCUMENT, URL_ID_DOCUMENTS = (
    app.Document, app.URL_ID_DOCUMENT, app.URL_ID_DOCUMENTS
    )

app = models.get_app("groups_networks")
PersonGroup, URL_ID_PERSONGROUP, URL_ID_PERSONGROUPS = (
    app.PersonGroup, app.URL_ID_PERSONGROUP, app.URL_ID_PERSONGROUPS
    )

admin.autodiscover()

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

person_dict = {
    'queryset': Person.objects.all(),
    'template_name': 'people/view_profile.html',
    'slug_field': 'user__username',
}

place_dict = {
    'queryset': Institution.objects.select_related().order_by('title'),
    'template_name': 'venue/view_place.html',
    'slug_field': 'node__slug',
}

funded_projects_dict = {
    'queryset': User.objects.all(),
    'template_name': 'fundraising/project_list.html',
    'slug_field': 'username',
}

institution_list_info = {
    'queryset': Institution.objects.select_related().order_by('title'),
    'template_name': 'institutions/institution_list.html',
    'paginate_by': 5,
    'allow_empty': True,
}

institution_details_info = {
    'queryset': Institution.objects.all(),
    'slug_field': 'slug',
    'template_name': 'institutions/institution_details.html',
    'context_item_type': URL_ID_INSTITUTION,
}


document_list_info = {
    'queryset': Document.objects.all(),
    'template_name': 'resources/documents/document_list.html',
    'paginate_by': 5,
    'allow_empty': True,
}

document_details_info = {
    'queryset': Document.objects.all(),
    'slug_field': 'slug',
    'template_name': 'resources/documents/document_details.html',
    'context_item_type': URL_ID_DOCUMENT,
}


event_list_info = {
    'queryset': Event.objects.all(),
    'template_name': 'events/event_list.html',
    'paginate_by': 5,
    'allow_empty': True,
}

event_details_info = {
    'queryset': Event.objects.all(),
    'slug_field': 'slug',
    'template_name': 'events/event_details.html',
    'context_item_type': URL_ID_EVENT,
}


person_list_info = {
    'queryset': Person.objects.select_related().order_by('auth_user.username'),
    'template_name': 'people/person_list.html',
    'paginate_by': 5,
    'allow_empty': True,
}

person_details_info = {
    'queryset': Person.objects.all(),
    'slug_field': 'user__username',
    'template_name': 'people/person_details.html',
    'context_item_type': URL_ID_PERSON,
}

group_list_info = {
    'queryset': PersonGroup.objects.order_by('title'),
    'template_name': 'groups_networks/persongroups/group_list.html',
    'paginate_by': 5,
    'allow_empty': True,
}

group_details_info = {
    'queryset': PersonGroup.objects.order_by('title'),
    'template_name': 'groups_networks/persongroups/group_details.html',
    'slug_field': 'slug',
    'context_item_type': URL_ID_PERSONGROUP,
}

from jetson.apps.articles.feeds import ArticleRssFeed, ArticleAtomFeed

article_feeds = {
    'rss': ArticleRssFeed,
    'atom': ArticleAtomFeed,
    }

my_messages_dict = {
    'template_name' : 'messaging/messages_list.html',
    'paginate_by' : 10,
    'allow_empty' : True, 
}

urlpatterns = []

urlpatterns += patterns('',
    # global js settings
    url(r'^jssettings/$', 'jetson.apps.utils.views.direct_to_js_template', {'template': 'settings.js'}),
    
     # info trouble-tickets
    url(r'^ticket/$', 'jetson.apps.tracker.views.create_ticket'),
    url(r'^ticket/(?P<concern>[^/]+)/$', 'jetson.apps.tracker.views.create_ticket'),
    url(r'^ticket/(?P<content_type_id>[0-9]+)/(?P<object_id>[0-9]+)/$', 'jetson.apps.tracker.views.create_ticket'),
    url(r'^ticket/(?P<concern>[^/]+)/(?P<content_type_id>[0-9]+)/(?P<object_id>[0-9]+)/$', 'jetson.apps.tracker.views.create_ticket'),
    
)

urlpatterns += patterns('django.views.static',
    # media
    url(r'^uploads/(?P<path>.*)$', 'serve', {'document_root': UPLOADS_ROOT}),
    url(r'^media/\d+/(?P<path>.*)$', 'serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^jetson-media/\d+/(?P<path>.*)$', 'serve', {'document_root': settings.JETSON_MEDIA_ROOT}),
    url(
        r'^admin-media/(?P<path>.*)$',
        'serve',
        {
            'document_root': settings.GRAPPELLI_MEDIA_ROOT,
            },
        name="admin_media_url"
        ),
    )    

### HELPERS (system urls not visible directly for the users) ###
urlpatterns += patterns('',
    # default document for TinyMCE iframe
    url(r'^helper/blank_doc/$', 'django.views.generic.simple.direct_to_template', {'template': 'admin/blank_doc.html'}),
    url(r'^helper/objects_to_select/(?P<app_name>[^/]+)/(?P<model_name>[^/]+)/(?P<obj_pk>[^/]+)/(?P<field_name>[^/]+)/of/(?P<content_type_id>[0-9]+)/$', 'base_libs.views.views.json_objects_to_select'),    
    
    # ajax lookups
    url(r'^helper/country_lookup/$', 'jetson.apps.utils.views.jquery_autocomplete_lookup', country_lookup),
    
    url(r'^helper/country/(?P<country_code>[A-Z]{2})/$', 'jetson.apps.i18n.views.json_country_name'),

    # helper for getting related objects from given contenttype
    url(r'^helper/getobjectsfromcontenttype/(?P<content_type_id>[0-9]+)/$', 'base_libs.views.views.json_get_objects_from_contenttype'),    
    url(r'^helper/%s_lookup/$' % URL_ID_INSTITUTION, 'jetson.apps.utils.views.jquery_autocomplete_lookup', institution_lookup),
    url(r'^helper/%s_lookup/$' % URL_ID_PERSON, 'jetson.apps.utils.views.jquery_autocomplete_lookup', person_lookup),
    url(r'^helper/rating/(?P<content_type_id>[0-9]+)/(?P<object_id>[0-9]+)/(?P<points>[1-5])/$', 'jetson.apps.ratings.views.json_set_rating'),
    url(r'^helper/favorite/(?P<content_type_id>[0-9]+)/(?P<object_id>[0-9]+)/$', 'jetson.apps.favorites.views.json_set_favorite'),
    url(r'^helper/bookmark/$', 'jetson.apps.bookmarks.views.json_manage_bookmark'),
    # ajax lookups for review ratings
    url(r'^helper/tmpimage/(?P<filename>[^/]+)/(?P<width>\d+)x(?P<height>\d+)/$', 'jetson.apps.utils.images.image_view', {'mod_function': None}),
    url(r'^helper/tmpimage/(?P<width>\d+)x(?P<height>\d+)/$', 'jetson.apps.utils.images.image_view', {'mod_function': None}),
    
    
    url(r'^helper/individual-relation/(?P<action>edit|invite|accept|cancel|deny|block|unblock|remove)/(?P<username>[^/]+)/$', 'jetson.apps.individual_relations.views.manage_individual_relationship'),        
    url(r'^helper/%s-membership/(?P<action>edit|request|cancel|remove|accept-%s|deny-%s)/(?P<slug>[^/]+)/$' % (URL_ID_PERSONGROUP, URL_ID_PERSONGROUP, URL_ID_PERSONGROUP), 'jetson.apps.groups_networks.views.manage_group_membership'),        
    url(r'^helper/%s-membership/(?P<action>accept-user|deny-user|remove-user|cancel-user)/(?P<slug>[^/]+)/(?P<username>[^/]+)/$' % URL_ID_PERSONGROUP, 'jetson.apps.groups_networks.views.manage_group_membership'),        
    url(r'^helper/edit-%s-member/(?P<slug>[^/]+)/(?P<user_id>[0-9]+)/$' % URL_ID_PERSONGROUP, 'jetson.apps.groups_networks.views.edit_group_member'),        

    url(r'^helper/autocomplete/(?P<app>[^/]+)/(?P<qs_function>[^/]+)/(?P<display_attr>[^/]+)/(?P<add_display_attr>[^/]+)/$', 'base_libs.views.ajax_autocomplete'),
    
    url(r'^helper/accounts/%s_attrs/(?P<institution_id>[0-9]+)/$' % URL_ID_INSTITUTION, 'jetson.apps.institutions.ajax.json_get_institution_attrs'),
        
    url(r'^helper/%s/%s_attrs/(?P<institution_id>[0-9]+)/$' % (URL_ID_EVENT, URL_ID_INSTITUTION), 'jetson.apps.events.ajax.json_get_institution_attrs'),
)

urlpatterns += patterns('',
    url(r'^%s/$' % URL_ID_INSTITUTIONS, 'jetson.apps.institutions.views.institution_list', institution_list_info),
    url(r'^%s/add/$' % URL_ID_INSTITUTIONS, 'jetson.apps.institutions.views.add_institution'),
    
    # details of institution, events, documents or persons
    url(r'^%s/(?P<slug>[^/]+)/$' % URL_ID_INSTITUTION, 'jetson.apps.utils.views.object_detail', institution_details_info),
    url(r'^%s/(?P<slug>[^/]+)/map/$' % URL_ID_INSTITUTION, 'jetson.apps.utils.views.object_detail', dict(institution_details_info, template_name="institutions/institution_map.html")),
    url(r'^%s/(?P<slug>[^/]+)/network/$' % URL_ID_INSTITUTION, 'jetson.apps.utils.views.object_detail', dict(institution_details_info, template_name="institutions/institution_network.html")),
    
    url(r'^%s/(?P<slug>[^/]+)/%s/$' % (URL_ID_INSTITUTION, URL_ID_PORTFOLIO), 'jetson.apps.media_gallery.views.gallery_detail', dict(institution_details_info, template_name="institutions/institution_portfolio.html")),
    url(r'^%s/(?P<slug>[^/]+)/%s/add/$' % (URL_ID_INSTITUTION, URL_ID_PORTFOLIO), 'jetson.apps.media_gallery.views.create_update_mediafile', dict(institution_details_info, template_name="institutions/institution_portfolio_change.html")),
    url(r'^%s/(?P<slug>[^/]+)/%s/file_(?P<token>[^/]+)/$' % (URL_ID_INSTITUTION, URL_ID_PORTFOLIO), 'jetson.apps.media_gallery.views.create_update_mediafile', dict(institution_details_info, template_name="institutions/institution_portfolio_change.html")),
    url(r'^%s/(?P<slug>[^/]+)/%s/file_(?P<token>[^/]+)/delete/$' % (URL_ID_INSTITUTION, URL_ID_PORTFOLIO), 'jetson.apps.media_gallery.views.delete_mediafile', dict(institution_details_info, template_name="institutions/institution_portfolio_delete.html")),
    url(r'^%s/(?P<slug>[^/]+)/%s/file_(?P<token>[^/]+)/popup_delete/$' % (URL_ID_INSTITUTION, URL_ID_PORTFOLIO), 'jetson.apps.media_gallery.views.delete_mediafile_popup', dict(institution_details_info, template_name="media_gallery/includes/delete_media_file.html")),
    url(r'^%s/(?P<slug>[^/]+)/%s/file_(?P<token>[^/]+)/json/$' % (URL_ID_INSTITUTION, URL_ID_PORTFOLIO), 'jetson.apps.media_gallery.views.json_show_file', dict(institution_details_info, template="media_gallery/includes/media_file.js")),

    
    url(r'^%s/(?P<slug>[^/]+)/projects/$' % URL_ID_INSTITUTION, 'jetson.apps.utils.views.object_detail', dict(institution_details_info, template_name="institutions/institution_projects.html")),
    url(r'^%s/(?P<slug>[^/]+)/jobs/$' % URL_ID_INSTITUTION, 'jetson.apps.utils.views.object_detail', dict(institution_details_info, template_name="institutions/institution_jobs.html")),
    url(r'^%s/(?P<slug>[^/]+)/reviews/$' % URL_ID_INSTITUTION, 'jetson.apps.utils.views.object_detail', dict(institution_details_info, template_name="institutions/institution_reviews.html")),
    url(r'^%s/(?P<slug>[^/]+)/message/alldone/$' % URL_ID_INSTITUTION, 'jetson.apps.utils.views.object_detail', dict(institution_details_info, template_name='institutions/institution_message.html')),
    url(
        r'^(?P<rel_url_part>%s/(?P<slug>[^/]+)/blog/)' % URL_ID_INSTITUTION,
        include('jetson.apps.blog.urls'),
        {
           'rel_obj_content_type_var' : 'institutions.institution', 
            'sysname' : "blog", 
            'template_dir' : 'institutions/blogs/'
            } 
        ),
    url(r'^%s/(?P<slug>[^/]+)/invite/' % URL_ID_INSTITUTION, 'jetson.apps.groups_networks.views.invite_institution_members',),
    
    url(r'^%s/$' % URL_ID_DOCUMENTS, 'jetson.apps.resources.views.document_list', document_list_info),
    
    url(r'^%s/(?P<slug>[^/]+)/$' % URL_ID_DOCUMENT, 'jetson.apps.utils.views.object_detail', document_details_info),
    url(r'^%s/(?P<slug>[^/]+)/reviews/$' % URL_ID_DOCUMENT, 'jetson.apps.utils.views.object_detail', dict(document_details_info, template_name="resources/documents/document_reviews.html")),
    url(r'^%s/(?P<slug>[^/]+)/network/$' % URL_ID_DOCUMENT, 'jetson.apps.utils.views.object_detail', dict(document_details_info, template_name="resources/documents/document_network.html")),
    
    url(r'^%s/$' % URL_ID_EVENTS, 'jetson.apps.events.views.event_list', event_list_info),
    url(r'^%s/add/$' % URL_ID_EVENTS, 'jetson.apps.events.views.add_event'), 
    
    # events have their dates prefixed (or not, if there aren't any)
    url(
        r'^%s/(\d{4}/(\d{1,2}/){0,2})?(?P<slug>[^/]+)/$' % URL_ID_EVENT,
        'jetson.apps.utils.views.object_detail',
        event_details_info,
        ),
    url(
        r'^%s/(\d{4}/(\d{1,2}/){0,2})?(?P<slug>[^/]+)/map/$' % URL_ID_EVENT,
        'jetson.apps.utils.views.object_detail',
        dict(event_details_info, template_name="events/event_map.html"),
        ),
    url(
        r'^%s/(\d{4}/(\d{1,2}/){0,2})?(?P<slug>[^/]+)/reviews/$' % URL_ID_EVENT,
        'jetson.apps.utils.views.object_detail',
        dict(
            event_details_info,
            template_name="events/event_reviews.html",
            ),
        ),
    url(
        r'^%s/(\d{4}/(\d{1,2}/){0,2})?(?P<slug>[^/]+)/reviews/$' % URL_ID_EVENT,
        'jetson.apps.utils.views.object_detail',
        dict(
            event_details_info,
            template_name="events/event_reviews.html",
            ),
        ),
    url(
        r'^%s/(\d{4}/(\d{1,2}/){0,2})?(?P<slug>[^/]+)/network/$' % URL_ID_EVENT,
        'jetson.apps.utils.views.object_detail',
        dict(
            event_details_info,
            template_name="events/event_network.html",
            ),
        ),
    
    
    url(
        r'^%s/(\d{4}/(\d{1,2}/){0,2})?(?P<slug>[^/]+)/%s/$' % (URL_ID_EVENT, URL_ID_PORTFOLIO),
        'jetson.apps.media_gallery.views.gallery_detail',
        dict(
            event_details_info,
            template_name="events/event_portfolio.html",
            ),
        ),
    url(
        r'^%s/(\d{4}/(\d{1,2}/){0,2})?(?P<slug>[^/]+)/%s/add/$' % (URL_ID_EVENT, URL_ID_PORTFOLIO),
        'jetson.apps.media_gallery.views.create_update_mediafile',
        dict(
            event_details_info,
            template_name="events/event_portfolio_change.html",
            ),
        ),
    url(
        r'^%s/(\d{4}/(\d{1,2}/){0,2})?(?P<slug>[^/]+)/%s/file_(?P<token>[^/]+)/$' % (URL_ID_EVENT, URL_ID_PORTFOLIO),
        'jetson.apps.media_gallery.views.create_update_mediafile',
        dict(
            event_details_info,
            template_name="events/event_portfolio_change.html",
            ),
        ),
    url(
        r'^%s/(\d{4}/(\d{1,2}/){0,2})?(?P<slug>[^/]+)/%s/file_(?P<token>[^/]+)/delete/$' % (URL_ID_EVENT, URL_ID_PORTFOLIO),
        'jetson.apps.media_gallery.views.delete_mediafile',
        dict(
            event_details_info,
            template_name="events/event_portfolio_delete.html",
            ),
        ),
    url(
        r'^%s/(\d{4}/(\d{1,2}/){0,2})?(?P<slug>[^/]+)/%s/file_(?P<token>[^/]+)/popup_delete/$' % (URL_ID_EVENT, URL_ID_PORTFOLIO),
        'jetson.apps.media_gallery.views.delete_mediafile_popup',
        dict(
            event_details_info,
            template_name="media_gallery/includes/delete_media_file.html",
            ),
        ),
    url(
        r'^%s/(\d{4}/(\d{1,2}/){0,2})?(?P<slug>[^/]+)/%s/file_(?P<token>[^/]+)/json/$' % (URL_ID_EVENT, URL_ID_PORTFOLIO),
        'jetson.apps.media_gallery.views.json_show_file',
        dict(
            event_details_info,
            template="media_gallery/includes/media_file.js",
            ),
        ),
    

    url(r'^%s/$' % URL_ID_PEOPLE, 'jetson.apps.people.views.person_list', person_list_info),
    
    url(r'^%s/(?P<slug>[^/]+)/$' % URL_ID_PERSON, 'jetson.apps.utils.views.object_detail', person_details_info),
    url(r'^%s/(?P<slug>[^/]+)/map/$' % URL_ID_PERSON, 'jetson.apps.utils.views.object_detail', dict(person_details_info, template_name="people/person_map.html")),
    url(r'^%s/(?P<slug>[^/]+)/network/$' % URL_ID_PERSON, 'jetson.apps.utils.views.object_detail', dict(person_details_info, template_name="people/person_network.html")),
    
    url(r'^%s/(?P<slug>[^/]+)/%s/$' % (URL_ID_PERSON, URL_ID_PORTFOLIO), 'jetson.apps.media_gallery.views.gallery_detail', dict(person_details_info, template_name="people/person_portfolio.html")),
    url(r'^%s/(?P<slug>[^/]+)/%s/add/$' % (URL_ID_PERSON, URL_ID_PORTFOLIO), 'jetson.apps.media_gallery.views.create_update_mediafile', dict(person_details_info, template_name="people/person_portfolio_change.html")),
    url(r'^%s/(?P<slug>[^/]+)/%s/file_(?P<token>[^/]+)/$' % (URL_ID_PERSON, URL_ID_PORTFOLIO), 'jetson.apps.media_gallery.views.create_update_mediafile', dict(person_details_info, template_name="people/person_portfolio_change.html")),
    url(r'^%s/(?P<slug>[^/]+)/%s/file_(?P<token>[^/]+)/delete/$' % (URL_ID_PERSON, URL_ID_PORTFOLIO), 'jetson.apps.media_gallery.views.delete_mediafile', dict(person_details_info, template_name="people/person_portfolio_delete.html")),
    url(r'^%s/(?P<slug>[^/]+)/%s/file_(?P<token>[^/]+)/popup_delete/$' % (URL_ID_PERSON, URL_ID_PORTFOLIO), 'jetson.apps.media_gallery.views.delete_mediafile_popup', dict(person_details_info, template_name="media_gallery/includes/delete_media_file.html")),
    url(r'^%s/(?P<slug>[^/]+)/%s/file_(?P<token>[^/]+)/json/$' % (URL_ID_PERSON, URL_ID_PORTFOLIO), 'jetson.apps.media_gallery.views.json_show_file', dict(person_details_info, template="media_gallery/includes/media_file.js")),
    
    
    url(r'^%s/(?P<slug>[^/]+)/projects/$' % URL_ID_PERSON, 'jetson.apps.utils.views.object_detail', dict(person_details_info, template_name="people/person_projects.html")),
    url(r'^%s/(?P<slug>[^/]+)/reviews/$' % URL_ID_PERSON, 'jetson.apps.utils.views.object_detail', dict(person_details_info, template_name="people/person_reviews.html")),
    url(r'^%s/(?P<slug>[^/]+)/message/alldone/$' % URL_ID_PERSON, 'jetson.apps.utils.views.object_detail', dict(person_details_info, template_name='people/person_message.html')),
    url(r'^(?P<rel_url_part>%s/(?P<user__username>[^/]+)/blog/)' % URL_ID_PERSON, include('jetson.apps.blog.urls'),
        {
            'rel_obj_content_type_var': 'people.person',
            'rel_obj_slug_field': 'user__username',
            'sysname': "blog", 
            'template_dir': 'people/blogs/'
            } 
        ),

    url(r'^%s/$' % URL_ID_PERSONGROUPS, 'jetson.apps.groups_networks.views.persongroup_list', group_list_info),
 
    url(
        r'^%s/(?P<show>own-groups)/$' % URL_ID_PERSONGROUPS,
        'jetson.apps.groups_networks.views.persongroup_list',
        dict(
            group_list_info,
            template_name="groups_networks/persongroups/group_list_own.html",
            ),
        ),
        
        
    url(r'^%s/invitations/$' % URL_ID_PERSONGROUPS, 'jetson.apps.groups_networks.views.persongroup_invitation_list'),
    url(r'^%s/invitations/(?P<group_ind>my-%s|other-%s|invite-to-%s)/$' % (URL_ID_PERSONGROUPS, URL_ID_PERSONGROUPS, URL_ID_PERSONGROUPS, URL_ID_PERSONGROUP), 'jetson.apps.groups_networks.views.persongroup_invitation_list'),    
    
    url(
        r'^%s/invitations/(?P<group_ind>my-%s|other-%s|invite-to-%s)/(?P<show>invitations|requests)/$' % (URL_ID_PERSONGROUPS, URL_ID_PERSONGROUPS, URL_ID_PERSONGROUPS, URL_ID_PERSONGROUP),
        'jetson.apps.groups_networks.views.persongroup_invitation_list',
        dict(
            group_list_info,
            template_name="groups_networks/persongroups/group_invitations_list.html",
            ),
        ),
        
        
    url(r'^%s/add/$' % URL_ID_PERSONGROUPS, 'jetson.apps.groups_networks.views.add_group'),

    url(r'^%s/(?P<slug>[^/]+)/$' % URL_ID_PERSONGROUP, 'jetson.apps.utils.views.object_detail', group_details_info),
    url(
        r'^%s/(?P<slug>[^/]+)/(?P<section>admins|moderators|members|unconfirmed|invited)/$' % URL_ID_PERSONGROUP,
        'jetson.apps.groups_networks.views.view_persongroup_members',
        ),
    url(
        r'^%s/(?P<slug>[^/]+)/members/invite/$' % URL_ID_PERSONGROUP,
        'jetson.apps.groups_networks.views.invite_persongroup_members',
        ),
    url(r'^%s/(?P<slug>[^/]+)/member/(?P<user_id>[0-9]+)/edit/$' % URL_ID_PERSONGROUP, 'jetson.apps.groups_networks.views.edit_group_member'),
    
    
    url(r'^%s/(?P<slug>[^/]+)/%s/$' % (URL_ID_PERSONGROUP, URL_ID_PORTFOLIO), 'jetson.apps.media_gallery.views.gallery_detail', dict(group_details_info, template_name="groups_networks/persongroups/group_portfolio.html")),
    url(r'^%s/(?P<slug>[^/]+)/%s/add/$' % (URL_ID_PERSONGROUP, URL_ID_PORTFOLIO), 'jetson.apps.media_gallery.views.create_update_mediafile', dict(group_details_info, template_name="groups_networks/persongroups/group_portfolio_change.html")),
    url(r'^%s/(?P<slug>[^/]+)/%s/file_(?P<token>[^/]+)/$' % (URL_ID_PERSONGROUP, URL_ID_PORTFOLIO), 'jetson.apps.media_gallery.views.create_update_mediafile', dict(group_details_info, template_name="groups_networks/persongroups/group_portfolio_change.html")),
    url(r'^%s/(?P<slug>[^/]+)/%s/file_(?P<token>[^/]+)/delete/$' % (URL_ID_PERSONGROUP, URL_ID_PORTFOLIO), 'jetson.apps.media_gallery.views.delete_mediafile', dict(group_details_info, template_name="groups_networks/persongroups/group_portfolio_delete.html")),
    url(r'^%s/(?P<slug>[^/]+)/%s/file_(?P<token>[^/]+)/popup_delete/$' % (URL_ID_PERSONGROUP, URL_ID_PORTFOLIO), 'jetson.apps.media_gallery.views.delete_mediafile_popup', dict(group_details_info, template_name="media_gallery/includes/delete_media_file.html")),
    url(r'^%s/(?P<slug>[^/]+)/%s/file_(?P<token>[^/]+)/json/$' % (URL_ID_PERSONGROUP, URL_ID_PORTFOLIO), 'jetson.apps.media_gallery.views.json_show_file', dict(group_details_info, template="media_gallery/includes/media_file.js")),
    
    
    
    url(r'^%s/(?P<slug>[^/]+)/projects/$' % URL_ID_PERSONGROUP, 'jetson.apps.utils.views.object_detail', dict(group_details_info, template_name="groups_networks/persongroups/group_projects.html")),
    url(r'^%s/(?P<slug>[^/]+)/%s/$' % (URL_ID_PERSONGROUP, URL_ID_EVENTS), 'jetson.apps.utils.views.object_detail', group_details_info),
    url(r'^%s/(?P<slug>[^/]+)/forum/' % URL_ID_PERSONGROUP, include('jetson.apps.forum.urls'), 
         {
             'rel_obj_content_type_var' : "groups_networks.persongroup",
             'rel_referer' : "forum/", 
             'template_dir' : 'groups_networks/persongroups/forum/',
             'extra_context' : group_details_info,
             } 
         ),
    
    
    url(r'^%s/(?P<slug>[^/]+)/invited/(?P<encrypted_email>.+)/$' % URL_ID_INSTITUTION, 'jetson.apps.groups_networks.views.confirm_invitation'),
    url(r'^%s/(?P<slug>[^/]+)/invited/(?P<encrypted_email>.+)/$' % URL_ID_PERSON, 'jetson.apps.individual_relations.views.confirm_invitation'),


     # info blog
    url(r'^(?P<rel_url_part>blog/)', include('jetson.apps.blog.urls'), 
        {
             'rel_obj_content_type_var': None, 
             'sysname': "blog", 
             'template_dir': "blog/",
             }
         ),
    
    
    # i18n
    #url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', {'packages': 'jetson'}),

    # gmap
    url(r'^gmap/$', 'django.views.generic.simple.direct_to_template', {'template': 'gmap/index.html'}),

    url(r'^admin/', include('jetson.apps.extendedadmin.urls')),
    url(r'^grappelli/', include('grappelli.urls')),

    # accounts and registration 
    url(r'^account/$', 'django.views.generic.simple.direct_to_template', {'template': 'accounts/index.html'}),
    url(r'^login', 'jetson.apps.people.views.login', {'template_name': 'accounts/login.html'}),
    url(r'^logout', 'django.contrib.auth.views.logout', {'next_page': "/"}),
    url(r'^changeuser/', 'django.contrib.auth.views.logout_then_login' ),
    url(r'^register/$', 'jetson.apps.people.views.register' ),
    url(r'^register/done/$', 'django.views.generic.simple.direct_to_template', {'template': 'accounts/register_verify_required.html'}),
    url(r'^register/alldone/$', 'django.views.generic.simple.direct_to_template', {'template': 'accounts/register_done.html'}),
    url(r'^register/(?P<encrypted_email>[a-zA-Z0-9\+\/=]+)/$', 'jetson.apps.people.views.confirm_registration'),
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset', {'template_name': 'accounts/password_reset_form.html', 'email_template_name': 'accounts/password_reset_email.html'}),
    url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'accounts/password_reset_done.html'}),
    url(r'^password_change/$', 'django.contrib.auth.views.password_change', {'template_name': 'accounts/password_change_form.html'}),
    url(r'^password_change/done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'accounts/password_change_done.html'}),

    # articles
    
    # articles aggregated overview
    url(r'^articles/', include("jetson.apps.articles.urls")),
    
    url(r'^contact/', include("jetson.apps.contact_form.urls")),
        
)

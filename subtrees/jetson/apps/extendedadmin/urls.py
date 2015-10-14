# -*- coding: UTF-8 -*-
from django.conf import settings
from django.conf.urls import *
from django.contrib import admin

from base_libs.utils.misc import path_in_installed_app
from base_libs.utils.misc import is_installed

urlpatterns = []

URL_ID_INSTITUTION = getattr(settings, "URL_ID_INSTITUTION", "institution")

urlpatterns += patterns("",
    (r'^doc/', include('django.contrib.admindocs.urls')),
    )

# extendedadmin for people
if is_installed("people.models"):
    urlpatterns += patterns(path_in_installed_app('extendedadmin.views'),
        # modified people administration    
        url(r'^people/person/add/$', 'person_add', name="admin_person_add"),
        url(r'^people/person/(?P<object_id>[0-9]+)/$', 'person_change', name="admin_person_change"),
        )
    
# extendedadmin for institutions
if is_installed("institutions.models"):
    urlpatterns += patterns(path_in_installed_app('extendedadmin.views'),
        # modified institution administration    
        url(r'^institutions/institution/add/$', 'institution_add', name="admin_institution_add"),
        url(r'^institutions/institution/(?P<object_id>[0-9]+)/$', 'institution_change', name="admin_institution_change"),
        
        # helpers
        url(r'^institutions/institution/(?P<object_id>[0-9]+)/json/$', 'json_institutional_contacts', name="admin_institutional_contacts"),
        url(r'^helper/%s_lookup/(?P<object_id>[0-9]+)/$' % URL_ID_INSTITUTION, 'json_institutional_contacts'), # TODO: is this used somewhere at all?
        )


# extendedadmin for resources
if is_installed("resources.models"):
    urlpatterns += patterns(path_in_installed_app('extendedadmin.views'),
        # modified document administration    
        url(r'^resources/document/add/$', 'document_add', name="admin_document_add"),
        url(r'^resources/document/(?P<object_id>[0-9]+)/$', 'document_change', name="admin_document_change"),
        )

# extendedadmin for events
'''
if is_installed("events.models"):
    urlpatterns += patterns(path_in_installed_app('extendedadmin.views'),
        # modified event administration    
        url(r'^events/event/add/$', 'event_add', name="admin_event_add"),
        url(r'^events/event/(?P<object_id>[0-9]+)/$', 'event_change', name="admin_event_change"),
        )
'''

# extendedadmin for mailing
if is_installed("mailing.models"):
    # extendedadmin for mailing
    urlpatterns += patterns(path_in_installed_app('extendedadmin.views'),
        # mails to persons in admin
        url(r'^auth/user/send-email/$', 'person_send_mail', name="admin_person_send_mail"),
        url(r'^auth/user/send-email/(?P<email_template_slug>[^/]+)/', 'user_send_mail', name="admin_user_send_mail"),
        )
    if is_installed("people.models"):
        urlpatterns += patterns(path_in_installed_app('extendedadmin.views'),
            # mails to persons in admin
            url(r'^people/person/send-email/$', 'person_send_mail', name="admin_person_send_mail"),
            url(r'^people/person/send-email/(?P<email_template_slug>[^/]+)/', 'person_send_mail', name="admin_person_send_mail"),
            )
    if is_installed("institutions.models"):
        urlpatterns += patterns(path_in_installed_app('extendedadmin.views'),
            # mails to institutions in admin
            url(r'^institutions/institution/send-email/$', 'institution_send_mail', name="admin_institution_send_mail"),
            url(r'^institutions/institution/send-email/(?P<email_template_slug>[^/]+)/', 'institution_send_mail', name="admin_institution_send_mail"),
            )

# history
urlpatterns += patterns(path_in_installed_app('history.views'),
    # history views
    url(r'^(?P<app_label>[^/]+)/(?P<model_name>[^/]+)/(?P<object_id>.+)/history/$', 'object_history', name="admin_object_history"),
    url(r'^auth/user/(?P<object_id>.+)/activities/$', 'user_activity_history', name="admin_user_activity_history"),
    )

# file browser
if is_installed("filebrowser.models"):
    urlpatterns += patterns(path_in_installed_app('image_mods.views'),
        url(r'^filebrowser/versions/$', 'versions', name="fb_versions"),
        url(r'^filebrowser/get-version/$', 'get_or_create_modified_path', name="fb_get_version"),
        url(r'^filebrowser/adjust-version/$', 'adjust_version', name="fb_adjust_version"),
        url(r'^filebrowser/delete-version/$', 'delete_version', name="fb_delete_version"),
        )
    from filebrowser.sites import site
    urlpatterns += patterns("",
        (
            r'^filebrowser/',
            include(include(site.urls)),
            ),
        )


# row-level-permissions
if is_installed("permissions.models"):
    urlpatterns += patterns("",
        (
            r'^(?P<app_label>(?:(?!cms)[^/])+)/(?P<model_name>(?:(?!page)[^/])+)/(?P<object_id>[^/]+)/permissions/',
            include(path_in_installed_app('permissions.urls')),
            ),
        )


# django admin
urlpatterns += patterns("",
    (r'', include(admin.site.urls)),
    )


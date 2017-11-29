# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import os
import sys
import unittest

FULL_TESTS = False  # will test more than 11,000 URLs if set to True, taking more than one hour


def get_extended_client_class():
    from django.test import Client
    class ExtendedClient(Client):
        def login_as(self, filter_params=None):
            from importlib import import_module
            from django.contrib.auth import get_user_model, login
            from django.conf import settings
            from django.http import HttpRequest
            if not filter_params:
                filter_params = {}

            User = get_user_model()
            user = User.objects.filter(**filter_params).order_by("date_joined")[0]
            user.backend = settings.AUTHENTICATION_BACKENDS[0]

            engine = import_module(settings.SESSION_ENGINE)

            # Create a fake request to store login details.
            request = HttpRequest()

            if self.session:
                request.session = self.session
            else:
                request.session = engine.SessionStore()
            login(request, user)

            # Save the session values.
            request.session.save()

            # Set the cookie to represent the session.
            session_cookie = settings.SESSION_COOKIE_NAME
            self.cookies[session_cookie] = request.session.session_key
            cookie_data = {
                'max-age': None,
                'path': '/',
                'domain': settings.SESSION_COOKIE_DOMAIN,
                'secure': settings.SESSION_COOKIE_SECURE or None,
                'expires': None,
            }
            self.cookies[session_cookie].update(cookie_data)
    return ExtendedClient


class PageTest(unittest.TestCase):
    is_authenticated = False

    def __init__(self, url_path='', expected_status_code=200, client=None):
        super(PageTest, self).__init__()
        self.url_path = url_path
        self.expected_status_code = expected_status_code
        self.client = client

    def setUp(self):
        from django.test.utils import setup_test_environment
        setup_test_environment()
        if not self.client:
            ExtendedClient = get_extended_client_class()
            self.client = ExtendedClient()

    def tearDown(self):
        pass

    def runTest(self):
        self.assertTrue(
            isinstance(self.url_path, (str, unicode)) and len(self.url_path) > 0,
            "{!r} is not a valid URL path.".format(self.url_path),
        )
        response = self.client.get(
            self.url_path,
            **{'HTTP_USER_AGENT': 'silly-human', 'REMOTE_ADDR': '127.0.0.1'}
        )
        self.assertEqual(
            response.status_code,
            self.expected_status_code,
            '{} returned {} status code with {} user, expected {}'.format(
                self.url_path,
                response.status_code,
                "authenticated" if self.is_authenticated else "anonymous",
                self.expected_status_code,
            )
        )


class AuthenticatedPageTest(PageTest):
    is_authenticated = True


class Urls(object):
    def __init__(self, limit_detail_pages_to=None):
        from berlinbuehnen.apps.locations.models import Location
        from berlinbuehnen.apps.productions.models import Event
        from berlinbuehnen.apps.festivals.models import Festival
        from berlinbuehnen.apps.education.models import Department, Project
        from berlinbuehnen.apps.articles.models import Article

        # OK (default)
        self.anonymous_200_authenticated_200 = [
            "/tweets/",
            "/tweets/berlinbuehnen/",
            "/tweets/thisuserdoesnotexist/",
            "/de/",
            "/de/buehnen/",
            "/de/spielplan/",
            "/de/festivals/",
            "/de/mitmachen/abteilungen/",
            "/de/aktuelles/",
            "/de/umfrage/",
            "/de/suche/",
            "/de/meta/ueber-uns/",
            "/de/meta/jobs-redirect/",
            "/de/meta/impressum/",
            "/de/filebrowser/get-version/",
            '/de/admin/filebrowser/browse/',  # shouldn't this redirect to login screen instead of opening one?
            '/de/admin/filebrowser/createdir/',  # shouldn't this redirect to login screen instead of opening one?
            '/de/admin/filebrowser/upload/',  # shouldn't this redirect to login screen instead of opening one?
            '/de/admin/filebrowser/delete_confirm/',  # shouldn't this redirect to login screen instead of opening one?
            '/de/admin/filebrowser/detail/',  # shouldn't this redirect to login screen instead of opening one?
            '/de/admin/filebrowser/version/',  # shouldn't this redirect to login screen instead of opening one?
            '/de/recrop/cropping-preview/fff/',
            '/de/sitemap.xml',
            '/de/sitemap-events.xml',
            '/de/sitemap-festivals.xml',
            '/de/sitemap-pages.xml',
            '/de/sitemap-locations.xml',
            '/de/api/changelog/',
            '/de/api/changelog/feed/',
            '/de/api/v1/?format=json',
            '/de/culturebase-export/locations/acker-stadt-palast/productions/',
            '/de/tagging_autocomplete/list',
            '/de/helper/autocomplete/i18n/get_countries/name/get_name/',
            '/de/helper/modified-path/',
            '/de/helper/menu/',
            '/de/jsi18n/',
            '/de/jssettings/',
            '/de/grappelli/grp-doc/change-form/',
            '/de/grappelli/grp-doc/change-list/',
            '/de/grappelli/grp-doc/admin-index/',
            '/de/grappelli/grp-doc/tables/',
            '/de/grappelli/grp-doc/pagination/',
            '/de/grappelli/grp-doc/search-form/',
            '/de/grappelli/grp-doc/filter/',
            '/de/grappelli/grp-doc/date-hierarchy/',
            '/de/grappelli/grp-doc/fieldsets/',
            '/de/grappelli/grp-doc/errors/',
            '/de/grappelli/grp-doc/form-fields/',
            '/de/grappelli/grp-doc/submit-rows/',
            '/de/grappelli/grp-doc/modules/',
            '/de/grappelli/grp-doc/groups/',
            '/de/grappelli/grp-doc/navigation/',
            '/de/grappelli/grp-doc/context-navigation/',
            '/de/grappelli/grp-doc/basic-page-structure/',
            '/de/grappelli/grp-doc/tools/',
            '/de/grappelli/grp-doc/object-tools/',
            '/de/grappelli/grp-doc/mueller-grid-system/',
            '/de/grappelli/grp-doc/mueller-grid-system-layouts/',
            '/de/grappelli/grp-doc',
        ]

        self.anonymous_200 = [
            '/de/admin/filebrowser/delete/',  # shouldn't this redirect to login screen instead of opening one?
            "/de/admin/filebrowser/upload_file/",  # shouldn't this redirect to login screen instead of opening one?
        ]

        querysets = [
            Location.objects.filter(status="published").order_by("?"),
            Event.objects.filter(production__status="published").order_by("?"),
            Festival.objects.filter(status="published").order_by("?"),
            Department.objects.filter(status="published").order_by("?"),
            Project.objects.filter(status="published").order_by("?"),
            Article.published_objects.order_by("?"),
        ]
        for qs in querysets:
            if limit_detail_pages_to:
                qs = qs[:3]
            for obj in qs:
                self.anonymous_200_authenticated_200.append(obj.get_url_path())

        # Redirect (to language-specific or other page)
        self.anonymous_302_authenticated_302 = [
            '/de/i18n/',
            '/de/logout/',  # keep the logout last, because it changes the request user
            '/logout/',  # keep the logout last, because it changes the request user
        ]

        # Redirect (to login or other page) if anonymous; OK otherwise
        self.anonymous_302 = [
            '/de/dashboard/',  # login required
            '/de/dashboard/productions/',
            '/de/dashboard/multiparts/',
            '/de/dashboard/locations/',
            '/de/dashboard/festivals/',
            '/de/dashboard/jobs/',
            '/de/dashboard/educational_departments/',
            '/de/dashboard/educational_projects/',
            '/de/spielplan/add/',
            '/de/multiparts/add/',
            '/de/buehnen/add/',
            '/de/festivals/add/',
            '/de/meta/jobs-redirect/add/',
            '/de/mitmachen/abteilungen/add/',
            '/de/mitmachen/projekte/add/',
            '/de/admin/logout/',  # keep the logout last, because it changes the request user
        ]

        self.authenticated_200 = [
            "/de/admin/filebrowser/upload_file/",
            '/de/grappelli/lookup/m2m/',
            '/de/grappelli/lookup/autocomplete/',
            '/de/grappelli/lookup/related/',
        ]

        self.authenticated_302 = [
            '/de/admin/filebrowser/delete/',  # shouldn't this redirect to login screen instead of opening one?
        ]

        # Bad request paramethers
        self.authenticated_400 = [
            "/de/admin/filebrowser/upload_file/",
        ]

        self.anonymous_401_authenticated_401 = [
            '/de/api/v1/event_characteristics/',
            '/de/api/v1/event_characteristics/schema/',
            '/de/api/v1/festival/',
            '/de/api/v1/festival/schema/',
            '/de/api/v1/language_and_subtitles/',
            '/de/api/v1/language_and_subtitles/schema/',
            '/de/api/v1/location/',
            '/de/api/v1/location/schema/',
            '/de/api/v1/location_accessibility/',
            '/de/api/v1/location_accessibility/schema/',
            '/de/api/v1/location_service/',
            '/de/api/v1/location_service/schema/',
            '/de/api/v1/production/',
            '/de/api/v1/production/schema/',
            '/de/api/v1/production_category/',
            '/de/api/v1/production_category/schema/',
            '/de/api/v1/production_characteristics/',
            '/de/api/v1/production_characteristics/schema/',
            '/de/api/v1/stage/',
            '/de/api/v1/stage/schema/',
        ]

        # Access Denied
        self.anonymous_403 = [
            '/de/grappelli/lookup/related/',
            '/de/grappelli/lookup/autocomplete/',
            '/de/grappelli/lookup/m2m/',
        ]

        # Page not found
        self.authenticated_404 = [
            "/de/admin/filebrowser/delete-version/",
        ]

        self.anonymous_404_authenticated_404 = [
            "/de/recrop/",
            "/de/autocomplete/location/",
        ]

        self.anonymous_405_authenticated_405 = [
            "/de/helper/ajax-upload/",
        ]

        self.anonymous_500_authenticated_500 = [
            #'/de/grappelli/grp-doc/mueller-grid-system-tests/',
        ]


def suite():
    ExtendedClient = get_extended_client_class()
    suite = unittest.TestSuite()

    if FULL_TESTS:
        urls = Urls()
    else:
        urls = Urls(limit_detail_pages_to=3)

    url_lists_by_expected_status_code = (
        (200, urls.anonymous_200_authenticated_200),
        (200, urls.anonymous_200),
        (302, urls.anonymous_302_authenticated_302),
        (302, urls.anonymous_302),
        (401, urls.anonymous_401_authenticated_401),
        (403, urls.anonymous_403),
        (404, urls.anonymous_404_authenticated_404),
        (405, urls.anonymous_405_authenticated_405),
        (500, urls.anonymous_500_authenticated_500),
    )
    client = ExtendedClient()
    for expected_status_code, url_list in url_lists_by_expected_status_code:
        suite.addTests(
            PageTest(url_path, expected_status_code, client=client)
            for url_path in url_list
        )
    authenticated_url_lists_by_expected_status_code = (
        (200, urls.anonymous_200_authenticated_200),
        (302, urls.anonymous_302_authenticated_302),
        (302, urls.authenticated_302),
        (400, urls.authenticated_400),
        (401, urls.anonymous_401_authenticated_401),
        (404, urls.authenticated_404),
        (404, urls.anonymous_404_authenticated_404),
        (405, urls.anonymous_405_authenticated_405),
        (500, urls.anonymous_500_authenticated_500),
    )
    for expected_status_code, url_list in authenticated_url_lists_by_expected_status_code:
        client = ExtendedClient()
        client.login_as(filter_params=dict(
            is_active=True,
            is_superuser=True,
        ))
        suite.addTests(
            AuthenticatedPageTest(url_path, expected_status_code, client=client)
            for url_path in url_list
        )
    return suite


if __name__ == "__main__":
    PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sys.path = ["", PROJECT_PATH] + sys.path
    os.chdir(os.path.dirname(__file__))
    os.environ["DJANGO_SETTINGS_MODULE"] = "berlinbuehnen.settings"
    unittest.TextTestRunner(verbosity=1).run(suite())

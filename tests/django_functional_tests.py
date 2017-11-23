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

        # Errorous pages that need fixing
        self.urls_which_should_return_200_but_dont = [
        ]

        # Errorous pages that need fixing
        self.urls_which_should_return_301_but_dont = [
        ]

        # Errorous pages that need fixing
        self.urls_which_should_return_302_but_dont = [
        ]

        # OK (default)
        self.feed_urls_which_should_return_200 = [
        ]

        # OK (default)
        self.urls_which_should_return_200 = [
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
                self.urls_which_should_return_200.append(obj.get_url_path())

        # Redirect (to language-specific or other page)
        self.urls_which_should_return_302 = [
            "/de/logout/",  # keep the logout last, because it changes the request user
            '/logout/',  # keep the logout last, because it changes the request user
        ]

        # Redirect (to login or other page) if anonymous; OK otherwise
        self.urls_which_should_return_302_when_anonymous = [
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

        # Bad request paramethers
        self.urls_which_should_return_400 = [
        ]

        # Unauthorized
        self.urls_which_should_return_401 = [
            #'/de/notification/feed/'
        ]

        # Access Denied
        self.urls_which_should_return_403_when_anonymous = [
        ]

        # Page not found
        self.urls_which_should_return_404 = [
        ]

        # Method not allowed
        self.urls_which_should_return_405_when_authenticated = [
        ]

        # Internal server error
        self.urls_which_should_return_500 = [
        ]


def suite():
    ExtendedClient = get_extended_client_class()
    suite = unittest.TestSuite()

    if FULL_TESTS:
        urls = Urls()
    else:
        urls = Urls(limit_detail_pages_to=3)

    url_lists_by_expected_status_code = (
        (200, urls.feed_urls_which_should_return_200),
        (200, urls.urls_which_should_return_200_but_dont),
        (301, urls.urls_which_should_return_301_but_dont),
        (302, urls.urls_which_should_return_302_but_dont),
        (200, urls.urls_which_should_return_200),
        (302, urls.urls_which_should_return_302),
        (302, urls.urls_which_should_return_302_when_anonymous),
        (302, urls.urls_which_should_return_405_when_authenticated),
        (400, urls.urls_which_should_return_400),
        (401, urls.urls_which_should_return_401),
        (403, urls.urls_which_should_return_403_when_anonymous),
        (404, urls.urls_which_should_return_404),
        (500, urls.urls_which_should_return_500),
    )
    client = ExtendedClient()
    for expected_status_code, url_list in url_lists_by_expected_status_code:
        suite.addTests(
            PageTest(url_path, expected_status_code, client=client)
            for url_path in url_list
        )
    authenticated_url_lists_by_expected_status_code = (
        (200, urls.urls_which_should_return_200),
        (302, urls.urls_which_should_return_302),
        (200, urls.urls_which_should_return_302_when_anonymous),
        (200, urls.urls_which_should_return_403_when_anonymous),
        (401, urls.urls_which_should_return_401),
        (405, urls.urls_which_should_return_405_when_authenticated),
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

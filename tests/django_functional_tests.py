# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import os
import sys
import unittest

from django.test.utils import setup_test_environment
from django.test import Client

FULL_TESTS = False  # will test more than 11,000 URLs if set to True, taking more than one hour


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


class PageTest(unittest.TestCase):
    is_authenticated = False

    def __init__(self, url_path='', expected_status_code=200, client=None):
        super(PageTest, self).__init__()
        self.url_path = url_path
        self.expected_status_code = expected_status_code
        self.client = client

    def setUp(self):
        setup_test_environment()
        if not self.client:
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
            "/de/filebrowser/get-version/",
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
            '/de/tagging_autocomplete/list/',
            '/de/helper/autocomplete/i18n/get_countries/name/get_name/',
            '/de/helper/modified-path/',
            '/de/helper/menu/',
            '/de/jsi18n/',
            '/de/jssettings/',
            '/de/styleguide/',
            '/de/styleguide/grid/',
            '/de/styleguide/typography/',
            '/de/styleguide/colors/',
            '/de/styleguide/images/',
            '/de/styleguide/forms/',
            '/de/login/',
            '/de/signup/',
            '/de/signup/almost-done/',
            '/de/password-reset/',
            '/de/password-reset/done/',
            '/de/password-reset/complete/',
            '/de/claiming-invitation/done/',
            '/de/festivities/',
            '/de/aktuelles/',
            '/de/aktuelles/feeds/rss/',
            '/de/aktuelles/2017/',
            '/de/aktuelles/2017/9/',
            '/de/aktuelles/2017/9/18/',
            '/de/aktuelles/2017/9/18/95-thesen-zu-theaterimnetz/',
            '/de/suche/',
            '/de/suche/full/',
            '/de/multiparts/',
            '/de/jobs/',
            # '/de/blog/',
            # '/de/blog/2015/',
            # '/de/blog/2015/04/',
            # '/de/blog/2015/04/07/',
            # '/de/blog/2015/04/07/hello-world/',
            # '/de/blog/all/',
            # '/de/blog/tag/one/',
            #'/de/blog/feeds/rss/',  # TODO: enable after upgrade
            '/de/mitmachen/abteilungen/',
            '/de/meta/jobs-redirect/',
            '/de/buehnen/',
            '/de/buehnen/map/',
            '/de/spielplan/',
            '/de/festivals/',
            #'/de/theater-der-woche/',
            #'/de/theater-der-woche/feeds/rss/',
        ]

        self.anonymous_200 = [
        ]

        querysets = [
            Location.objects.filter(status="published").order_by("?"),
            # Randomizing events takes too long, so just get the last created ones
            Event.objects.filter(production__status="published").only(
                'production__slug', 'production__status', 'id'
            ).order_by("-id"),
            Festival.objects.filter(status="published").order_by("?"),
            Department.objects.filter(status="published").order_by("?"),
            Project.objects.filter(status="published").order_by("?"),
            # exclude the articles from English which is not the current language
            Article.published_objects.exclude(language="en").order_by("?"),
        ]
        for qs in querysets:
            if limit_detail_pages_to:
                qs = qs[:3]
            for obj in qs:
                self.anonymous_200_authenticated_200.append(obj.get_url_path())

        # Redirect (to language-specific or other page)
        self.anonymous_302_authenticated_302 = [
            '/de/i18n/',
            '/de/my-profile/favorites/',
            '/de/rosetta/download/',
            '/de/mitmachen/projekte/',
            '/de/logout/',  # keep the logout last, because it changes the request user
            '/logout/',  # keep the logout last, because it changes the request user
        ]

        # Redirect (to login or other page) if anonymous; OK otherwise
        self.anonymous_302 = [
            '/de/dashboard/',
            '/de/dashboard/locations/',
            '/de/dashboard/productions/',
            '/de/dashboard/multiparts/',
            '/de/dashboard/festivals/',
            '/de/dashboard/jobs/',
            '/de/dashboard/educational_departments/',
            '/de/dashboard/educational_projects/',
            '/de/dashboard/info-files/',
            '/de/spielplan/add/',
            '/de/multiparts/add/',
            '/de/buehnen/add/',
            '/de/festivals/add/',
            '/de/meta/jobs-redirect/add/',
            '/de/mitmachen/abteilungen/add/',
            '/de/mitmachen/projekte/add/',
            '/de/signup/welcome/',
            '/de/password-change/',
            '/de/password-change/done/',
            '/de/rosetta/',
            '/de/rosetta/pick/',
            '/de/festivities/add/',
            '/de/multiparts/add/',
            '/de/jobs/add/',
            '/de/mitmachen/abteilungen/add/',
            '/de/mitmachen/projekte/add/',
            '/de/meta/jobs-redirect/add/',
            '/de/buehnen/add/',
            '/de/spielplan/add/',
            '/de/festivals/add/',
            '/de/admin/',
            '/de/admin/password_change/',
            '/de/admin/password_change/done/',
            '/de/admin/jsi18n/',
            '/de/admin/image_mods/',
            '/de/admin/image_mods/imagemodificationgroup/',
            '/de/admin/image_mods/imagemodificationgroup/add/',
            '/de/admin/i18n/countrylanguage/',
            '/de/admin/i18n/countrylanguage/add/',
            '/de/admin/advertising/adcategory/',
            '/de/admin/advertising/adcategory/add/',
            '/de/admin/auth/user/',
            '/de/admin/auth/user/1/password/',
            '/de/admin/auth/user/add/',
            '/de/admin/multiparts/parent/',
            '/de/admin/multiparts/parent/2/owners/',
            '/de/admin/multiparts/parent/add/',
            '/de/admin/mailchimp/subscription/',
            '/de/admin/mailchimp/subscription/add/',
            '/de/admin/locations/location/',
            '/de/admin/locations/location/68/owners/',
            '/de/admin/locations/location/add/',
            '/de/admin/locations/service/',
            '/de/admin/locations/service/add/',
            '/de/admin/articles/article/',
            '/de/admin/articles/article/add/',
            '/de/admin/productions/production/',
            '/de/admin/productions/production/38976/owners/',
            '/de/admin/productions/production/add/',
            '/de/admin/i18n/phone/',
            '/de/admin/i18n/phone/add/',
            '/de/admin/people/prefix/',
            '/de/admin/people/prefix/add/',
            '/de/admin/education/projecttargetgroup/',
            '/de/admin/education/projecttargetgroup/add/',
            '/de/admin/sites/site/',
            '/de/admin/sites/site/add/',
            '/de/admin/favorites/favoritelistoptions/',
            '/de/admin/favorites/favoritelistoptions/add/',
            '/de/admin/i18n/country/',
            '/de/admin/i18n/country/add/',
            '/de/admin/productions/productioncharacteristics/',
            '/de/admin/productions/productioncharacteristics/add/',
            '/de/admin/comments/moderatordeletion/',
            '/de/admin/comments/moderatordeletion/add/',
            # '/de/admin/blog/blog/',
            # '/de/admin/blog/blog/add/',
            '/de/admin/mega_menu/menublock/',
            '/de/admin/mega_menu/menublock/add/',
            '/de/admin/advertising/adimpression/',
            '/de/admin/advertising/adimpression/add/',
            '/de/admin/locations/accessibilityoption/',
            '/de/admin/locations/accessibilityoption/add/',
            '/de/admin/cms/globalpagepermission/',
            '/de/admin/cms/globalpagepermission/add/',
            '/de/admin/marketplace/jobtype/',
            '/de/admin/marketplace/jobtype/add/',
            '/de/admin/productions/event/',
            '/de/admin/productions/event/add/',
            '/de/admin/i18n/language/',
            '/de/admin/i18n/language/add/',
            '/de/admin/services/banner/',
            '/de/admin/services/banner/add/',
            '/de/admin/people/person/',
            '/de/admin/people/person/add/',
            '/de/admin/education/projectformat/',
            '/de/admin/education/projectformat/add/',
            '/de/admin/permissions/perobjectgroup/',
            '/de/admin/permissions/perobjectgroup/add/',
            '/de/admin/people/authorshiptype/',
            '/de/admin/people/authorshiptype/add/',
            '/de/admin/auth/group/',
            '/de/admin/auth/group/add/',
            '/de/admin/festivals/festival/',
            '/de/admin/festivals/festival/2/owners/',
            '/de/admin/festivals/festival/add/',
            '/de/admin/blocks/infoblock/',
            '/de/admin/blocks/infoblock/add/',
            '/de/admin/i18n/area/',
            '/de/admin/i18n/area/add/',
            '/de/admin/cms/pageusergroup/',
            '/de/admin/cms/pageusergroup/add/',
            '/de/admin/mailchimp/mlist/',
            '/de/admin/mailchimp/mlist/add/',
            '/de/admin/mailing/emailmessage/',
            '/de/admin/mailing/emailmessage/add/',
            '/de/admin/education/project/',
            '/de/admin/education/project/1/owners/',
            '/de/admin/education/project/add/',
            '/de/admin/locations/locationcategory/',
            '/de/admin/locations/locationcategory/1/move/',
            '/de/admin/locations/locationcategory/add/',
            '/de/admin/mailing/emailtemplate/',
            '/de/admin/mailing/emailtemplate/add/',
            '/de/admin/advertising/adclick/',
            '/de/admin/advertising/adclick/add/',
            '/de/admin/configuration/sitesettings/',
            '/de/admin/configuration/sitesettings/add/',
            '/de/admin/people/involvementtype/',
            '/de/admin/people/involvementtype/add/',
            '/de/admin/advertising/bannerad/',
            '/de/admin/advertising/bannerad/add/',
            '/de/admin/marketplace/jobcategory/',
            '/de/admin/marketplace/jobcategory/5/move/',
            '/de/admin/marketplace/jobcategory/add/',
            '/de/admin/external_services/service/',
            '/de/admin/external_services/service/add/',
            '/de/admin/permissions/rowlevelpermission/',
            '/de/admin/permissions/rowlevelpermission/add/',
            '/de/admin/slideshows/slideshow/',
            '/de/admin/slideshows/slideshow/add/',
            '/de/admin/tagging/taggeditem/',
            '/de/admin/tagging/taggeditem/add/',
            '/de/admin/i18n/timezone/',
            '/de/admin/i18n/timezone/add/',
            '/de/admin/articles/articlecategory/',
            '/de/admin/articles/articlecategory/1/move/',
            '/de/admin/articles/articlecategory/add/',
            '/de/admin/mailchimp/campaign/',
            '/de/admin/mailchimp/campaign/template-content/text/',
            '/de/admin/mailchimp/campaign/15/preview/',
            '/de/admin/mailchimp/campaign/add/',
            '/de/admin/cms/pageuser/',
            '/de/admin/cms/pageuser/2/password/',
            '/de/admin/cms/pageuser/add/',
            '/de/admin/productions/languageandsubtitles/',
            '/de/admin/productions/languageandsubtitles/add/',
            '/de/admin/comments/comment/',
            '/de/admin/comments/comment/add/',
            '/de/admin/advertising/textad/',
            '/de/admin/advertising/textad/add/',
            '/de/admin/infobanners/infobanner/',
            '/de/admin/infobanners/infobanner/add/',
            '/de/admin/favorites/favorite/',
            '/de/admin/favorites/favorite/add/',
            '/de/admin/filebrowser/browse/',
            '/de/admin/filebrowser/createdir/',
            '/de/admin/filebrowser/upload/',
            '/de/admin/filebrowser/delete_confirm/',
            '/de/admin/filebrowser/detail/',
            '/de/admin/filebrowser/version/',
            '/de/admin/tastypie/apikey/',
            '/de/admin/tastypie/apikey/add/',
            '/de/admin/cms/page/',
            '/de/admin/cms/page/copy-plugins/',
            '/de/admin/cms/page/add-plugin/',
            '/de/admin/cms/page/remove-plugin/',
            '/de/admin/cms/page/move-plugin/',
            '/de/admin/cms/page/5/delete-translation/',
            '/de/admin/cms/page/5/permissions/',
            '/de/admin/cms/page/5/moderation-states/',
            '/de/admin/cms/page/5/descendants/',
            '/de/admin/cms/page/add/',
            '/de/admin/image_mods/imagemodification/',
            '/de/admin/image_mods/imagemodification/add/',
            '/de/admin/external_services/serviceactionlog/',
            '/de/admin/external_services/serviceactionlog/add/',
            '/de/admin/marketplace/joboffer/',
            '/de/admin/marketplace/joboffer/1/owners/',
            '/de/admin/marketplace/joboffer/add/',
            '/de/admin/tagging/tag/',
            '/de/admin/tagging/tag/add/',
            '/de/admin/productions/eventcharacteristics/',
            '/de/admin/productions/eventcharacteristics/add/',
            '/de/admin/education/department/',
            '/de/admin/education/department/1/owners/',
            '/de/admin/education/department/add/',
            '/de/admin/comments/moderatordeletionreason/',
            '/de/admin/comments/moderatordeletionreason/add/',
            '/de/admin/locations/district/',
            '/de/admin/locations/district/add/',
            '/de/admin/external_services/objectmapper/',
            '/de/admin/external_services/objectmapper/add/',
            '/de/admin/mailchimp/settings/',
            '/de/admin/mailchimp/settings/add/',
            '/de/admin/i18n/nationality/',
            '/de/admin/i18n/nationality/add/',
            '/de/admin/mailing/emailtemplateplaceholder/',
            '/de/admin/mailing/emailtemplateplaceholder/add/',
            '/de/admin/productions/productioncategory/',
            '/de/admin/productions/productioncategory/1/move/',
            '/de/admin/productions/productioncategory/add/',
            '/de/admin/advertising/advertiser/',
            '/de/admin/advertising/advertiser/add/',
            # '/de/admin/blog/post/',
            # '/de/admin/blog/post/add/',
            '/de/admin/advertising/adzone/',
            '/de/admin/advertising/adzone/add/',
            '/de/admin/image_mods/imagecropping/',
            '/de/admin/image_mods/imagecropping/add/',
            '/de/admin/theater_of_the_week/theateroftheweek/',
            '/de/admin/theater_of_the_week/theateroftheweek/add/',
            '/de/admin/cms/page/5/copy-page/',
            '/de/admin/cms/page/5/change-navigation/',
            '/de/admin/multiparts/parent/2/owners/',
            '/de/admin/locations/location/68/owners/',
            '/de/admin/productions/production/38976/owners/',
            '/de/admin/festivals/festival/2/owners/',
            '/de/admin/education/project/1/owners/',
            '/de/admin/marketplace/joboffer/1/owners/',
            '/de/admin/education/department/1/owners/',
            '/de/claiming-invitation/',
            '/de/admin/logout/',  # keep the logout last, because it changes the request user
        ]

        self.authenticated_200 = [
            "/de/admin/filebrowser/upload_file/",
            '/de/grappelli/lookup/m2m/',
            '/de/grappelli/lookup/autocomplete/',
            '/de/grappelli/lookup/related/',
            '/de/signup/welcome/',
            '/de/password-change/',
            '/de/password-change/done/',
            '/de/dashboard/',
            '/de/dashboard/locations/',
            '/de/dashboard/productions/',
            '/de/dashboard/multiparts/',
            '/de/dashboard/festivals/',
            '/de/dashboard/jobs/',
            '/de/dashboard/educational_departments/',
            '/de/dashboard/educational_projects/',
            '/de/dashboard/info-files/',
            '/de/rosetta/',
            '/de/rosetta/pick/',
            '/de/festivities/add/',
            '/de/multiparts/add/',
            '/de/jobs/add/',
            '/de/mitmachen/abteilungen/add/',
            '/de/mitmachen/projekte/add/',
            '/de/meta/jobs-redirect/add/',
            '/de/buehnen/add/',
            '/de/spielplan/add/',
            '/de/festivals/add/',
            '/de/claiming-invitation/',
        ]

        self.authenticated_302 = [
            '/de/admin/filebrowser/delete/',  # shouldn't this redirect to login screen instead of opening one?
        ]

        # Bad request paramethers
        self.authenticated_400 = [
        ]

        # Bad request paramethers
        self.urls_which_should_return_400 = [
            '/de/recrop/'
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
            "/de/admin/filebrowser/delete-version/",
        ]

        self.anonymous_404_authenticated_404 = [
            "/de/autocomplete/location/",
        ]

        self.anonymous_405_authenticated_405 = [
            "/de/helper/ajax-upload/",
        ]

        # Method not allowed
        self.urls_which_should_return_405_when_authenticated = [
            '/de/admin/cms/page/5/change-navigation/',
            '/de/admin/cms/page/5/move-page/',
            '/de/admin/cms/page/5/copy-page/',
            '/de/admin/filebrowser/upload_file/'
        ]

        self.anonymous_500_authenticated_500 = [
        ]


def suite():
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
        (400, urls.urls_which_should_return_400),
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
        (400, urls.urls_which_should_return_400),
        (400, urls.authenticated_400),
        (401, urls.anonymous_401_authenticated_401),
        (404, urls.authenticated_404),
        (404, urls.anonymous_404_authenticated_404),
        (405, urls.anonymous_405_authenticated_405),
        (405, urls.urls_which_should_return_405_when_authenticated),
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
    os.environ["DJANGO_SETTINGS_MODULE"] = "berlinbuehnen.settings.test"

    import django
    django.setup()
    unittest.TextTestRunner(verbosity=1, failfast=True).run(suite())

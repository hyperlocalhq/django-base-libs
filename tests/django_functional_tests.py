# -*- coding: UTF-8 -*-
# inspired by http://stackoverflow.com/a/3772008
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

    def shortDescription(self):
        return 'page {} should return {} status code'.format(
            self.url_path,
            self.expected_status_code,
        )

    def runTest(self):
        assert isinstance(self.url_path, unicode)
        response = self.client.get(
            self.url_path,
            **{'HTTP_USER_AGENT': 'silly-human', 'REMOTE_ADDR': '127.0.0.1'}
        )
        self.assertEqual(
            response.status_code,
            self.expected_status_code,
            '{} returned {} status code, expected {}'.format(
                self.url_path,
                response.status_code,
                self.expected_status_code,
            )
        )


class AuthenticatedPageTest(PageTest):
    def shortDescription(self):
        return 'page {} should return {} status code when authenticated'.format(
            self.url_path,
            self.expected_status_code,
        )


class Urls(object):
    def __init__(self, limit_detail_pages_to=None):
        from ccb.apps.marketplace.models import JobOffer
        from ccb.apps.bulletin_board.models import Bulletin
        from ccb.apps.media_gallery.models import MediaGallery
        from ccb.apps.events.models import Event
        from ccb.apps.articles.models import Article
        from ccb.apps.site_specific.models import ContextItem

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
            '/de/blog/feeds/rss/',
            '/de/documents/latest_published/feeds/rss/',
            '/de/events/latest_published/feeds/rss/',
            '/de/groups/latest_published/feeds/rss/',
            '/de/institutions/latest_published/feeds/rss/',
            '/de/jobs/feed/rss/',
            '/de/kreativwirtschaftsberatung-berlin/blog/feeds/rss/',
            '/de/news/feeds/rss/',
            #'/de/notification/feed/',  # TODO: update the feed mechanism
            '/de/people/latest_published/feeds/rss/',
            '/de/portfolios/feeds/rss/',
        ]

        # OK (default)
        self.urls_which_should_return_200 = [
            '/de/',
            '/de/blog/',
            '/de/compatibility/',
            '/de/contact/',
            '/de/contact/alldone/',
            '/de/documents/',  # TODO: do we still need them?
            '/de/faqs/',
            '/de/gmap/',
            '/de/help/',
            '/de/meta/impressum/',
            '/de/network/',
            '/de/jobs/',
            '/de/jobs/create-berlin-jobboard/',
            '/de/jobs/talent-in-berlin/',
            '/de/jsi18n/',
            '/de/jssettings/',
            '/de/kreativwirtschaftsberatung-berlin/',
            '/de/kreativwirtschaftsberatung-berlin/uber-uns/',
            '/de/kreativwirtschaftsberatung-berlin/direktberatung/',
            '/de/kreativwirtschaftsberatung-berlin/tipps-tricks/',
            '/de/kreativwirtschaftsberatung-berlin/termine-veranstaltungen/',
            '/de/kreativwirtschaftsberatung-berlin/blog/',
            '/de/kreativwirtschaftsberatung-berlin/news/',
            '/de/login/',
            '/de/my-messages/json/',
            '/de/my-profile/delete/done/',
            '/de/news/',
            '/de/news/category/industry-news-and-market-trends/',
            '/de/news/category/tenders-competitions/',
            '/de/news/category/studies-and-publications/',
            '/de/news/category/surveys/',
            '/de/password-reset/',
            '/de/password-reset/complete/',
            '/de/password-reset/done/',
            '/de/portfolios/',
            '/de/privacy/',
            '/de/register/',
            '/de/register/done/',
            '/de/search/',
            '/de/search/full/',
            '/de/sitemap.xml',
            '/de/styleguide/',
            '/de/styleguide/constants/',
            '/de/styleguide/fonts/',
            '/de/styleguide/icons/',
            '/de/styleguide/buttons/',
            '/de/styleguide/elements/',
            '/de/styleguide/form/',
            '/de/styleguide/navigation/',
            '/de/styleguide/layout/',
            '/de/subscribe-to-newsletter/',
            '/de/subscribe-to-newsletter/done/',
            '/de/terms-of-use/',
            '/de/ticket/',
            '/de/tweets/',
            '/de/tweets/CREATIVEBERLIN/',
            '/de/helper/country_lookup/',
            '/de/helper/site-visitors/',
            '/de/creative-sectors/architektur/ubersicht/',
            '/de/creative-sectors/architektur/network/',
            '/de/creative-sectors/architektur/zahlen-fakten/',
            '/de/creative-sectors/architektur/fragen-antworten/',
            '/de/creative-sectors/architektur/ansprechpartner-netzwerke/',
            '/de/creative-sectors/architektur/portfolios/',
            '/de/creative-sectors/architektur/events/',
            '/de/creative-sectors/architektur/news/',
        ]

        querysets = [
            JobOffer.published_objects.order_by("?"),
            Bulletin.published_objects.order_by("?"),
            MediaGallery.published_objects.order_by("?"),
            Event.objects.nearest_published().order_by("?"),
            Article.site_published_objects.order_by("?"),
            ContextItem.objects.filter(content_type__model__in=("person", "institution"), status="published").order_by("?"),
        ]
        for qs in querysets:
            if limit_detail_pages_to:
                qs = qs[:3]
            for obj in qs:
                self.urls_which_should_return_200.append(obj.get_url_path())

        # Redirect (to language-specific or other page)
        self.urls_which_should_return_302 = [
            '/helper/institution_lookup/',
            '/tagging_autocomplete/list/',
            '/',
            '/admin/',
            '/admin/articles/article/',
            '/admin/articles/article/add/',
            '/admin/articles/articlecontentprovider/',
            '/admin/articles/articlecontentprovider/add/',
            '/admin/articles/articletype/',
            '/admin/articles/articletype/add/',
            '/admin/auth/group/',
            '/admin/auth/group/add/',
            '/admin/auth/user/',
            '/admin/auth/user/add/',
            '/admin/auth/user/send-email/',
            '/admin/blocks/infoblock/',
            '/admin/blocks/infoblock/add/',
            '/admin/blog/blog/',
            '/admin/blog/blog/add/',
            '/admin/blog/post/',
            '/admin/blog/post/add/',
            '/admin/bookmarks/bookmark/',
            '/admin/bookmarks/bookmark/add/',
            '/admin/comments/comment/',
            '/admin/comments/comment/add/',
            '/admin/comments/moderatordeletion/',
            '/admin/comments/moderatordeletion/add/',
            '/admin/comments/moderatordeletionreason/',
            '/admin/comments/moderatordeletionreason/add/',
            '/admin/configuration/sitesettings/',
            '/admin/configuration/sitesettings/add/',
            '/admin/contact_form/contactformcategory/',
            '/admin/contact_form/contactformcategory/add/',
            '/admin/djcelery/crontabschedule/',
            '/admin/djcelery/crontabschedule/add/',
            '/admin/djcelery/intervalschedule/',
            '/admin/djcelery/intervalschedule/add/',
            '/admin/djcelery/periodictask/',
            '/admin/djcelery/periodictask/add/',
            '/admin/djcelery/taskstate/',
            '/admin/djcelery/taskstate/add/',
            '/admin/djcelery/workerstate/',
            '/admin/djcelery/workerstate/add/',
            '/admin/doc/',
            '/admin/doc/bookmarklets/',
            '/admin/doc/filters/',
            '/admin/doc/models/',
            '/admin/doc/tags/',
            '/admin/doc/views/',
            '/admin/events/event/',
            '/admin/events/event/add/',
            '/admin/events/eventtimelabel/',
            '/admin/events/eventtimelabel/add/',
            '/admin/events/eventtype/',
            '/admin/events/eventtype/add/',
            '/admin/external_services/articleimportsource/',
            '/admin/external_services/articleimportsource/add/',
            '/admin/external_services/objectmapper/',
            '/admin/external_services/objectmapper/add/',
            '/admin/external_services/service/',
            '/admin/external_services/service/add/',
            '/admin/external_services/serviceactionlog/',
            '/admin/external_services/serviceactionlog/add/',
            '/admin/faqs/faqcategory/',
            '/admin/faqs/faqcategory/add/',
            '/admin/faqs/faqcontainer/',
            '/admin/faqs/faqcontainer/add/',
            '/admin/favorites/favorite/',
            '/admin/favorites/favorite/add/',
            '/admin/filebrowser/adjust-version/',
            '/admin/filebrowser/browse/',
            '/admin/filebrowser/delete-version/',
            '/admin/filebrowser/delete/',
            '/admin/filebrowser/delete_confirm/',
            '/admin/filebrowser/detail/',
            '/admin/filebrowser/get-version/',
            '/admin/filebrowser/version/',
            '/admin/filebrowser/versions/',
            '/admin/filebrowser/upload_file/',
            '/admin/flatpages/flatpage/',
            '/admin/flatpages/flatpage/add/',
            '/admin/groups_networks/grouptype/',
            '/admin/groups_networks/grouptype/add/',
            '/admin/groups_networks/persongroup/',
            '/admin/groups_networks/persongroup/add/',
            '/admin/i18n/area/',
            '/admin/i18n/area/add/',
            '/admin/i18n/country/',
            '/admin/i18n/country/add/',
            '/admin/i18n/countrylanguage/',
            '/admin/i18n/countrylanguage/add/',
            '/admin/i18n/language/',
            '/admin/i18n/language/add/',
            '/admin/i18n/nationality/',
            '/admin/i18n/nationality/add/',
            '/admin/i18n/phone/',
            '/admin/i18n/phone/add/',
            '/admin/i18n/timezone/',
            '/admin/i18n/timezone/add/',
            '/admin/image_mods/imagecropping/',
            '/admin/image_mods/imagecropping/add/',
            '/admin/image_mods/imagemodification/',
            '/admin/image_mods/imagemodification/add/',
            '/admin/image_mods/imagemodificationgroup/',
            '/admin/image_mods/imagemodificationgroup/add/',
            '/admin/individual_relations/individualrelation/',
            '/admin/individual_relations/individualrelation/add/',
            '/admin/individual_relations/individualrelationtype/',
            '/admin/individual_relations/individualrelationtype/add/',
            '/admin/institutions/institution/',
            '/admin/institutions/institution/add/',
            '/admin/institutions/institution/send-email/',
            '/admin/institutions/institutiontype/',
            '/admin/institutions/institutiontype/add/',
            '/admin/institutions/legalform/',
            '/admin/institutions/legalform/add/',
            '/admin/jsi18n/',
            '/admin/location/address/',
            '/admin/location/address/add/',
            '/admin/mailchimp/campaign/',
            '/admin/mailchimp/campaign/add/',
            '/admin/mailchimp/mlist/',
            '/admin/mailchimp/mlist/add/',
            '/admin/mailchimp/settings/',
            '/admin/mailchimp/settings/add/',
            '/admin/mailchimp/subscription/',
            '/admin/mailchimp/subscription/add/',
            '/admin/mailing/emailmessage/',
            '/admin/mailing/emailmessage/add/',
            '/admin/mailing/emailtemplate/',
            '/admin/mailing/emailtemplate/add/',
            '/admin/mailing/emailtemplateplaceholder/',
            '/admin/mailing/emailtemplateplaceholder/add/',
            '/admin/marketplace/joboffer/',
            '/admin/marketplace/joboffer/add/',
            '/admin/marketplace/jobqualification/',
            '/admin/marketplace/jobqualification/add/',
            '/admin/marketplace/jobsector/',
            '/admin/marketplace/jobsector/add/',
            '/admin/marketplace/jobtype/',
            '/admin/marketplace/jobtype/add/',
            '/admin/media_gallery/mediagallery/',
            '/admin/media_gallery/mediagallery/add/',
            '/admin/media_gallery/portfoliosettings/',
            '/admin/media_gallery/portfoliosettings/add/',
            '/admin/media_gallery/section/',
            '/admin/media_gallery/section/add/',
            '/admin/memos/memocollection/',
            '/admin/memos/memocollection/add/',
            '/admin/messaging/internalmessage/',
            '/admin/messaging/internalmessage/add/',
            '/admin/navigation/navigationlink/',
            '/admin/navigation/navigationlink/add/',
            '/admin/notification/digest/',
            '/admin/notification/digest/add/',
            '/admin/notification/notice/',
            '/admin/notification/notice/add/',
            '/admin/notification/noticeemailtemplate/',
            '/admin/notification/noticeemailtemplate/add/',
            '/admin/notification/noticesetting/',
            '/admin/notification/noticesetting/add/',
            '/admin/notification/noticetype/',
            '/admin/notification/noticetype/add/',
            '/admin/notification/noticetypecategory/',
            '/admin/notification/noticetypecategory/add/',
            '/admin/optionset/emailtype/',
            '/admin/optionset/emailtype/add/',
            '/admin/optionset/imtype/',
            '/admin/optionset/imtype/add/',
            '/admin/optionset/individuallocationtype/',
            '/admin/optionset/individuallocationtype/add/',
            '/admin/optionset/institutionallocationtype/',
            '/admin/optionset/institutionallocationtype/add/',
            '/admin/optionset/phonetype/',
            '/admin/optionset/phonetype/add/',
            '/admin/optionset/prefix/',
            '/admin/optionset/prefix/add/',
            '/admin/optionset/salutation/',
            '/admin/optionset/salutation/add/',
            '/admin/optionset/urltype/',
            '/admin/optionset/urltype/add/',
            '/admin/password_change/',
            '/admin/password_change/done/',
            '/admin/people/individualtype/',
            '/admin/people/individualtype/add/',
            '/admin/people/person/',
            '/admin/people/person/add/',
            '/admin/people/person/send-email/',
            '/admin/permissions/perobjectgroup/',
            '/admin/permissions/perobjectgroup/add/',
            '/admin/permissions/rowlevelpermission/',
            '/admin/permissions/rowlevelpermission/add/',
            '/admin/profanity_filter/swearingcase/',
            '/admin/profanity_filter/swearingcase/add/',
            '/admin/profanity_filter/swearword/',
            '/admin/profanity_filter/swearword/add/',
            '/admin/redirects/redirect/',
            '/admin/redirects/redirect/add/',
            '/admin/resources/document/',
            '/admin/resources/document/add/',
            '/admin/resources/documenttype/',
            '/admin/resources/documenttype/add/',
            '/admin/resources/medium/',
            '/admin/resources/medium/add/',
            '/admin/site_specific/claimrequest/',
            '/admin/site_specific/claimrequest/add/',
            '/admin/site_specific/contextitem/',
            '/admin/site_specific/contextitem/add/',
            '/admin/site_specific/visit/',
            '/admin/site_specific/visit/add/',
            '/admin/sites/site/',
            '/admin/sites/site/add/',
            '/admin/slideshows/slideshow/',
            '/admin/slideshows/slideshow/add/',
            '/admin/structure/contextcategory/',
            '/admin/structure/contextcategory/add/',
            '/admin/structure/term/',
            '/admin/structure/term/add/',
            '/admin/structure/vocabulary/',
            '/admin/structure/vocabulary/add/',
            '/admin/tagging/tag/',
            '/admin/tagging/tag/add/',
            '/admin/tagging/taggeditem/',
            '/admin/tagging/taggeditem/add/',
            '/admin/tracker/concern/',
            '/admin/tracker/concern/add/',
            '/admin/tracker/ticket/',
            '/admin/tracker/ticket/add/',
            '/blog/',
            '/compatibility/',
            '/contact/',
            '/contact/alldone/',
            '/dashboard/',
            '/documents/',
            '/events/',
            '/events/add/',
            '/faqs/',
            '/gmap/',
            '/help/',
            '/i18n/setlang/',
            '/jobs/',
            '/jobs/add/',
            '/jobs/create-berlin-jobboard/',
            '/jobs/talent-in-berlin/',
            '/jsi18n/',
            '/jssettings/',
            '/kreativwirtschaftsberatung-berlin/',
            '/kreativwirtschaftsberatung-berlin/uber-uns/',
            '/kreativwirtschaftsberatung-berlin/direktberatung/',
            '/kreativwirtschaftsberatung-berlin/tipps-tricks/',
            '/kreativwirtschaftsberatung-berlin/termine-veranstaltungen/',
            '/kreativwirtschaftsberatung-berlin/blog/',
            '/kreativwirtschaftsberatung-berlin/news/',
            '/login/',
            '/my-messages/json/',
            '/my-messages/new/',
            '/my-profile/',
            '/my-profile/delete/',
            '/my-profile/delete/done/',
            '/my-profile/privacy/',
            '/news/',
            '/news/category/industry-news-and-market-trends/',
            '/news/category/tenders-competitions/',
            '/news/category/studies-and-publications/',
            '/news/category/surveys/',
            '/notification/',
            #'/notification/feed/',
            '/notification/settings/',
            '/password-change/',
            '/password-change/done/',
            '/password-reset/',
            '/password-reset/complete/',
            '/password-reset/done/',
            '/network/',
            '/network/member/aidas/',
            '/portfolios/',
            '/register/',
            '/register/alldone/',
            '/register/done/',
            '/rosetta/',
            '/rosetta/download/',
            '/rosetta/pick/',
            '/de/rosetta/download/',
            '/search/',
            '/search/full/',
            '/sitemap.xml',
            '/styleguide/',
            '/styleguide/constants/',
            '/styleguide/fonts/',
            '/styleguide/icons/',
            '/styleguide/buttons/',
            '/styleguide/elements/',
            '/styleguide/form/',
            '/styleguide/navigation/',
            '/styleguide/layout/',
            '/subscribe-to-newsletter/',
            '/subscribe-to-newsletter/done/',
            '/ticket/',
            '/tweets/',
            "/de/my-profile/",
            '/de/i18n/setlang/',
            "/de/logout/",  # keep the logout last, because it changes the request user
            '/logout/',  # keep the logout last, because it changes the request user
        ]

        # Redirect (to login or other page) if anonymous; OK otherwise
        self.urls_which_should_return_302_when_anonymous = [
            '/de/dashboard/',  # login required
            '/de/events/event/workshop-booking-tour-rockpop/claim/',  # login required
            '/de/events/event/workshop-booking-tour-rockpop/delete/',  # login required
            '/de/events/add/',  # login required
            '/de/jobs/add/',  # login required
            '/de/my-messages/new/',  # login required
            '/de/my-profile/delete/',  # login required
            '/de/my-profile/privacy/',  # login required
            '/de/notification/',  # login required
            '/de/notification/settings/',  # login required
            '/de/password-change/',  # login required
            '/de/network/member/aidas/message/',  # login required
            '/de/register/alldone/',  # login required
            '/de/helper/institution_lookup/',  # login required
            '/de/rosetta/',  # login required
            '/de/rosetta/pick/',  # login required
            '/de/admin/',  # login required
            '/de/admin/cms/page/',  # login required
            '/de/admin/people/person/add/',  # login required
            '/de/admin/logout/',  # keep the logout last, because it changes the request user
        ]

        # Bad request paramethers
        self.urls_which_should_return_400 = [
            '/de/recrop/'
        ]

        # Unauthorized
        self.urls_which_should_return_401 = [
            #'/de/notification/feed/'
        ]

        # Access Denied
        self.urls_which_should_return_403_when_anonymous = [
            '/de/events/event/workshop-booking-tour-rockpop/portfolio/album/add/',
            '/de/events/event/workshop-booking-tour-rockpop/portfolio/manage/',
            '/de/events/event/workshop-booking-tour-rockpop/portfolio/section/add/',
            '/de/events/event/workshop-booking-tour-rockpop/portfolio/settings/',
            '/de/events/event/workshop-booking-tour-rockpop/portfolio/settings/delete-landing-page-image/',
            '/de/network/member/aidas/portfolio/album/add/',
            '/de/network/member/aidas/portfolio/manage/',
            '/de/network/member/aidas/portfolio/section/add/',
            '/de/network/member/aidas/portfolio/settings/',
            '/de/network/member/aidas/portfolio/settings/delete-landing-page-image/',
        ]

        # Page not found
        self.urls_which_should_return_404 = [
        ]

        # Method not allowed
        self.urls_which_should_return_405_when_authenticated = [
            '/de/notification/mark-all-seen/',
        ]

        # Internal server error
        self.urls_which_should_return_500 = [
        ]


def suite():
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
    os.environ["DJANGO_SETTINGS_MODULE"] = "settings"
    import django

    django.setup()
    unittest.TextTestRunner(verbosity=1).run(suite())

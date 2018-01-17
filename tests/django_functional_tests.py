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
        from museumsportal.apps.museums.models import Museum
        from museumsportal.apps.exhibitions.models import Exhibition
        from museumsportal.apps.events.models import Event
        from museumsportal.apps.workshops.models import Workshop
        from museumsportal.apps.shop.models import ShopProduct

        # OK (default)
        self.anonymous_200_authenticated_200 = [
            "/de/",
            "/de/tweets/",
            "/de/tweets/museumsportal/",
            "/de/tweets/thisuserdoesnotexist/",
            "/de/filebrowser/get-version/",
            '/de/admin/filebrowser/browse/',  # shouldn't this redirect to login screen instead of opening one?
            '/de/admin/filebrowser/createdir/',  # shouldn't this redirect to login screen instead of opening one?
            '/de/admin/filebrowser/upload/',  # shouldn't this redirect to login screen instead of opening one?
            '/de/admin/filebrowser/delete_confirm/',  # shouldn't this redirect to login screen instead of opening one?
            '/de/admin/filebrowser/detail/',  # shouldn't this redirect to login screen instead of opening one?
            '/de/admin/filebrowser/version/',  # shouldn't this redirect to login screen instead of opening one?
            '/de/recrop/cropping-preview/fff/',
            '/de/sitemap.xml',
            '/de/api/v1/?format=json',
            '/de/api/v2/?format=json',
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
            '/de/claiming-invitation/',
            '/de/claiming-invitation/done/',
            '/autocomplete/OwnEventAutocomplete/',
            '/autocomplete/MuseumAutocomplete/',
            '/autocomplete/OwnMuseumAutocomplete/',
            '/autocomplete/ExhibitionAutocomplete/',
            '/autocomplete/WorkshopAutocomplete/',
            '/autocomplete/OwnWorkshopAutocomplete/',
            '/autocomplete/OwnExhibitionAutocomplete/',
            '/autocomplete/EventAutocomplete/',
            '/de/shop/',
            '/de/blog/',
            '/de/blog/all/',
            '/de/suche/',
            '/de/suche/full/',
            '/de/museen/',
            '/de/museen/map/',
            '/de/museen/export-json-museums/',
            '/de/ausstellungen/?smart=actual',
            '/de/ausstellungen/map/',
            '/de/ausstellungen/export-json-exhibitions/',
            '/de/ausstellungen/rss/',
            '/de/veranstaltungen/',
            '/de/veranstaltungen/map/',
            '/de/veranstaltungen/rss/',
            '/de/fuehrungen/',
            '/de/fuehrungen/map/',
            '/de/fuehrungen/rss/',
            '/de/museumsummer-copy/map/',  # What is this?
        ]

        self.anonymous_200 = [
            '/de/admin/',
            '/de/admin/accounts/',
            '/de/admin/accounts/privacysettings/',
            '/de/admin/accounts/privacysettings/add/',
            '/de/admin/advertising/',
            '/de/admin/advertising/adcategory/',
            '/de/admin/advertising/adcategory/add/',
            '/de/admin/advertising/adclick/',
            '/de/admin/advertising/adclick/add/',
            '/de/admin/advertising/adimpression/',
            '/de/admin/advertising/adimpression/add/',
            '/de/admin/advertising/advertiser/',
            '/de/admin/advertising/advertiser/add/',
            '/de/admin/advertising/adzone/',
            '/de/admin/advertising/adzone/add/',
            '/de/admin/advertising/bannerad/',
            '/de/admin/advertising/bannerad/add/',
            '/de/admin/advertising/textad/',
            '/de/admin/advertising/textad/add/',
            '/de/admin/articles/',
            '/de/admin/articles/article/',
            '/de/admin/articles/article/add/',
            '/de/admin/articles/articlecategory/',
            '/de/admin/articles/articlecategory/1/move/',
            '/de/admin/articles/articlecategory/add/',
            '/de/admin/auth/',
            '/de/admin/auth/group/',
            '/de/admin/auth/group/add/',
            '/de/admin/auth/user/',
            '/de/admin/auth/user/1/password/',
            '/de/admin/auth/user/add/',
            '/de/admin/blocks/',
            '/de/admin/blocks/infoblock/',
            '/de/admin/blocks/infoblock/add/',
            '/de/admin/blog/',
            '/de/admin/blog/blog/',
            '/de/admin/blog/blog/add/',
            '/de/admin/blog/post/',
            '/de/admin/blog/post/add/',
            '/de/admin/cms/',
            '/de/admin/cms/globalpagepermission/',
            '/de/admin/cms/globalpagepermission/add/',
            '/de/admin/cms/page/',
            '/de/admin/cms/page/5/change-navigation/',
            '/de/admin/cms/page/5/change-status/',
            '/de/admin/cms/page/5/change_template/',
            '/de/admin/cms/page/5/copy-page/',
            '/de/admin/cms/page/5/delete-translation/',
            '/de/admin/cms/page/5/descendants/',
            '/de/admin/cms/page/5/moderation-states/',
            '/de/admin/cms/page/5/move-page/',
            '/de/admin/cms/page/5/permissions/',
            '/de/admin/cms/page/5/preview/',
            '/de/admin/cms/page/add-plugin/',
            '/de/admin/cms/page/add/',
            '/de/admin/cms/page/copy-plugins/',
            '/de/admin/cms/page/move-plugin/',
            '/de/admin/cms/page/remove-plugin/',
            '/de/admin/cms/pageuser/',
            '/de/admin/cms/pageuser/4/password/',
            '/de/admin/cms/pageuser/add/',
            '/de/admin/cms/pageusergroup/',
            '/de/admin/cms/pageusergroup/add/',
            '/de/admin/comments/',
            '/de/admin/comments/comment/',
            '/de/admin/comments/comment/add/',
            '/de/admin/comments/moderatordeletion/',
            '/de/admin/comments/moderatordeletion/add/',
            '/de/admin/comments/moderatordeletionreason/',
            '/de/admin/comments/moderatordeletionreason/add/',
            '/de/admin/configuration/',
            '/de/admin/configuration/sitesettings/',
            '/de/admin/configuration/sitesettings/add/',
            '/de/admin/events/',
            '/de/admin/events/event/',
            '/de/admin/events/event/add/',
            '/de/admin/events/eventcategory/',
            '/de/admin/events/eventcategory/1/move/',
            '/de/admin/events/eventcategory/add/',
            '/de/admin/exhibitions/',
            '/de/admin/exhibitions/exhibition/',
            '/de/admin/exhibitions/exhibition/add/',
            '/de/admin/exhibitions/exhibitioncategory/',
            '/de/admin/exhibitions/exhibitioncategory/1/move/',
            '/de/admin/exhibitions/exhibitioncategory/add/',
            '/de/admin/external_services/',
            '/de/admin/external_services/objectmapper/',
            '/de/admin/external_services/objectmapper/add/',
            '/de/admin/external_services/service/',
            '/de/admin/external_services/service/add/',
            '/de/admin/external_services/serviceactionlog/',
            '/de/admin/external_services/serviceactionlog/add/',
            '/de/admin/favorites/',
            '/de/admin/favorites/favorite/',
            '/de/admin/favorites/favorite/add/',
            '/de/admin/filebrowser/delete/',
            '/de/admin/filebrowser/upload_file/',
            '/de/admin/i18n/',
            '/de/admin/i18n/area/',
            '/de/admin/i18n/area/add/',
            '/de/admin/i18n/country/',
            '/de/admin/i18n/country/add/',
            '/de/admin/i18n/countrylanguage/',
            '/de/admin/i18n/countrylanguage/add/',
            '/de/admin/i18n/language/',
            '/de/admin/i18n/language/add/',
            '/de/admin/i18n/nationality/',
            '/de/admin/i18n/nationality/add/',
            '/de/admin/i18n/phone/',
            '/de/admin/i18n/phone/add/',
            '/de/admin/i18n/timezone/',
            '/de/admin/i18n/timezone/add/',
            '/de/admin/image_mods/',
            '/de/admin/image_mods/imagecropping/',
            '/de/admin/image_mods/imagecropping/add/',
            '/de/admin/image_mods/imagemodification/',
            '/de/admin/image_mods/imagemodification/add/',
            '/de/admin/image_mods/imagemodificationgroup/',
            '/de/admin/image_mods/imagemodificationgroup/add/',
            '/de/admin/internal_links/',
            '/de/admin/internal_links/linkgroup/',
            '/de/admin/internal_links/linkgroup/add/',
            '/de/admin/jsi18n/',
            '/de/admin/mailchimp/',
            '/de/admin/mailchimp/campaign/',
            '/de/admin/mailchimp/campaign/15/preview/',
            '/de/admin/mailchimp/campaign/add/',
            '/de/admin/mailchimp/campaign/template-content/text/',
            '/de/admin/mailchimp/mlist/',
            '/de/admin/mailchimp/mlist/add/',
            '/de/admin/mailchimp/settings/',
            '/de/admin/mailchimp/settings/add/',
            '/de/admin/mailchimp/subscription/',
            '/de/admin/mailchimp/subscription/add/',
            '/de/admin/mailing/',
            '/de/admin/mailing/emailmessage/',
            '/de/admin/mailing/emailmessage/add/',
            '/de/admin/mailing/emailtemplate/',
            '/de/admin/mailing/emailtemplate/add/',
            '/de/admin/mailing/emailtemplateplaceholder/',
            '/de/admin/mailing/emailtemplateplaceholder/add/',
            '/de/admin/media_gallery/',
            '/de/admin/media_gallery/mediagallery/',
            '/de/admin/media_gallery/mediagallery/add/',
            '/de/admin/mega_menu/',
            '/de/admin/mega_menu/menublock/',
            '/de/admin/mega_menu/menublock/add/',
            '/de/admin/museums/',
            '/de/admin/museums/accessibilityoption/',
            '/de/admin/museums/accessibilityoption/add/',
            '/de/admin/museums/museum/',
            '/de/admin/museums/museum/add/',
            '/de/admin/museums/museumcategory/',
            '/de/admin/museums/museumcategory/1/move/',
            '/de/admin/museums/museumcategory/add/',
            '/de/admin/museumssummer/',
            '/de/admin/museumssummer/location/',
            '/de/admin/museumssummer/location/add/',
            '/de/admin/password_change/',
            '/de/admin/password_change/done/',
            '/de/admin/permissions/',
            '/de/admin/permissions/perobjectgroup/',
            '/de/admin/permissions/perobjectgroup/add/',
            '/de/admin/permissions/rowlevelpermission/',
            '/de/admin/permissions/rowlevelpermission/add/',
            '/de/admin/shop/',
            '/de/admin/shop/shopproduct/',
            '/de/admin/shop/shopproduct/add/',
            '/de/admin/shop/shopproductcategory/',
            '/de/admin/shop/shopproductcategory/add/',
            '/de/admin/shop/shopproducttype/',
            '/de/admin/shop/shopproducttype/2/move/',
            '/de/admin/shop/shopproducttype/add/',
            '/de/admin/sites/',
            '/de/admin/sites/site/',
            '/de/admin/sites/site/add/',
            '/de/admin/slideshows/',
            '/de/admin/slideshows/slideshow/',
            '/de/admin/slideshows/slideshow/add/',
            '/de/admin/snippet/',
            '/de/admin/snippet/snippet/',
            '/de/admin/snippet/snippet/add/',
            '/de/admin/tagging/',
            '/de/admin/tagging/tag/',
            '/de/admin/tagging/tag/add/',
            '/de/admin/tagging/taggeditem/',
            '/de/admin/tagging/taggeditem/add/',
            '/de/admin/tastypie/',
            '/de/admin/tastypie/apikey/',
            '/de/admin/tastypie/apikey/add/',
            '/de/admin/tips/',
            '/de/admin/tips/tipoftheday/',
            '/de/admin/tips/tipoftheday/add/',
            '/de/admin/tips/tipoftheday/details-json/59/768/',
            '/de/admin/tracker/',
            '/de/admin/tracker/concern/',
            '/de/admin/tracker/concern/add/',
            '/de/admin/tracker/ticket/',
            '/de/admin/tracker/ticket/add/',
            '/de/admin/twitterwall/',
            '/de/admin/twitterwall/searchsettings/',
            '/de/admin/twitterwall/searchsettings/add/',
            '/de/admin/twitterwall/tweet/',
            '/de/admin/twitterwall/tweet/add/',
            '/de/admin/twitterwall/twitteruser/',
            '/de/admin/twitterwall/twitteruser/add/',
            '/de/admin/twitterwall/usertimelinesettings/',
            '/de/admin/twitterwall/usertimelinesettings/add/',
            '/de/admin/workshops/',
            '/de/admin/workshops/workshop/',
            '/de/admin/workshops/workshop/add/',
            '/de/admin/workshops/workshoptype/',
            '/de/admin/workshops/workshoptype/add/',
        ]

        querysets = [
            Museum.objects.filter(status="published").order_by("?"),
            Exhibition.objects.filter(status="published").order_by("?"),
            Event.objects.filter(status="published").order_by("?"),
            Workshop.objects.filter(status="published").order_by("?"),
            ShopProduct.objects.filter(status="published").order_by("?"),
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
            '/de/logout/',  # keep the logout last, because it changes the request user
            '/logout/',  # keep the logout last, because it changes the request user
        ]

        # Redirect (to login or other page) if anonymous; OK otherwise
        self.anonymous_302 = [
            '/de/dashboard/',
            '/de/dashboard/museums/',
            '/de/dashboard/exhibitions/',
            '/de/dashboard/events/',
            '/de/dashboard/guided-tours/',
            '/de/dashboard/shop/',
            '/de/signup/welcome/',
            '/de/password-change/',
            '/de/password-change/done/',
            '/de/rosetta/',
            '/de/rosetta/pick/',
            '/de/shop/add/',
            '/de/museen/add/',
            '/de/ausstellungen/add/',
            '/de/veranstaltungen/add/',
            '/de/fuehrungen/add/',
            '/de/admin/logout/',  # keep the logout last, because it changes the request user
        ]

        self.authenticated_200 = [
            "/autocomplete/",
            "/de/admin/filebrowser/upload_file/",
            '/de/grappelli/lookup/m2m/',
            '/de/grappelli/lookup/autocomplete/',
            '/de/grappelli/lookup/related/',
            '/de/signup/welcome/',
            '/de/password-change/',
            '/de/password-change/done/',
            '/de/dashboard/',
            '/de/dashboard/museums/',
            '/de/dashboard/exhibitions/',
            '/de/dashboard/events/',
            '/de/dashboard/guided-tours/',
            '/de/dashboard/shop/',
            '/de/rosetta/',
            '/de/rosetta/pick/',
            '/de/admin/',
            '/de/admin/accounts/',
            '/de/admin/accounts/privacysettings/',
            '/de/admin/accounts/privacysettings/add/',
            '/de/admin/advertising/',
            '/de/admin/advertising/adcategory/',
            '/de/admin/advertising/adcategory/add/',
            '/de/admin/advertising/adclick/',
            '/de/admin/advertising/adclick/add/',
            '/de/admin/advertising/adimpression/',
            '/de/admin/advertising/adimpression/add/',
            '/de/admin/advertising/advertiser/',
            '/de/admin/advertising/advertiser/add/',
            '/de/admin/advertising/adzone/',
            '/de/admin/advertising/adzone/add/',
            '/de/admin/advertising/bannerad/',
            '/de/admin/advertising/bannerad/add/',
            '/de/admin/advertising/textad/',
            '/de/admin/advertising/textad/add/',
            '/de/admin/articles/',
            '/de/admin/articles/article/',
            '/de/admin/articles/article/add/',
            '/de/admin/articles/articlecategory/',
            '/de/admin/articles/articlecategory/1/move/',
            '/de/admin/articles/articlecategory/add/',
            '/de/admin/auth/',
            '/de/admin/auth/group/',
            '/de/admin/auth/group/add/',
            '/de/admin/auth/user/',
            '/de/admin/auth/user/1/password/',
            '/de/admin/auth/user/add/',
            '/de/admin/blocks/',
            '/de/admin/blocks/infoblock/',
            '/de/admin/blocks/infoblock/add/',
            '/de/admin/blog/',
            '/de/admin/blog/blog/',
            '/de/admin/blog/blog/add/',
            '/de/admin/blog/post/',
            '/de/admin/blog/post/add/',
            '/de/admin/cms/',
            '/de/admin/cms/globalpagepermission/',
            '/de/admin/cms/globalpagepermission/add/',
            '/de/admin/cms/page/',
            '/de/admin/cms/page/5/change-navigation/',
            '/de/admin/cms/page/5/change-status/',
            '/de/admin/cms/page/5/change_template/',
            '/de/admin/cms/page/5/copy-page/',
            '/de/admin/cms/page/5/delete-translation/',
            '/de/admin/cms/page/5/descendants/',
            '/de/admin/cms/page/5/moderation-states/',
            '/de/admin/cms/page/5/move-page/',
            '/de/admin/cms/page/5/permissions/',
            '/de/admin/cms/page/5/preview/',
            '/de/admin/cms/page/add-plugin/',
            '/de/admin/cms/page/add/',
            '/de/admin/cms/page/copy-plugins/',
            '/de/admin/cms/page/move-plugin/',
            '/de/admin/cms/page/remove-plugin/',
            '/de/admin/cms/pageuser/',
            '/de/admin/cms/pageuser/4/password/',
            '/de/admin/cms/pageuser/add/',
            '/de/admin/cms/pageusergroup/',
            '/de/admin/cms/pageusergroup/add/',
            '/de/admin/comments/',
            '/de/admin/comments/comment/',
            '/de/admin/comments/comment/add/',
            '/de/admin/comments/moderatordeletion/',
            '/de/admin/comments/moderatordeletion/add/',
            '/de/admin/comments/moderatordeletionreason/',
            '/de/admin/comments/moderatordeletionreason/add/',
            '/de/admin/configuration/',
            '/de/admin/configuration/sitesettings/',
            '/de/admin/configuration/sitesettings/add/',
            '/de/admin/events/',
            '/de/admin/events/event/',
            '/de/admin/events/event/add/',
            '/de/admin/events/eventcategory/',
            '/de/admin/events/eventcategory/1/move/',
            '/de/admin/events/eventcategory/add/',
            '/de/admin/exhibitions/',
            '/de/admin/exhibitions/exhibition/',
            '/de/admin/exhibitions/exhibition/add/',
            '/de/admin/exhibitions/exhibitioncategory/',
            '/de/admin/exhibitions/exhibitioncategory/1/move/',
            '/de/admin/exhibitions/exhibitioncategory/add/',
            '/de/admin/external_services/',
            '/de/admin/external_services/objectmapper/',
            '/de/admin/external_services/objectmapper/add/',
            '/de/admin/external_services/service/',
            '/de/admin/external_services/service/add/',
            '/de/admin/external_services/serviceactionlog/',
            '/de/admin/external_services/serviceactionlog/add/',
            '/de/admin/favorites/',
            '/de/admin/favorites/favorite/',
            '/de/admin/favorites/favorite/add/',
            '/de/admin/filebrowser/delete/',
            '/de/admin/filebrowser/upload_file/',
            '/de/admin/i18n/',
            '/de/admin/i18n/area/',
            '/de/admin/i18n/area/add/',
            '/de/admin/i18n/country/',
            '/de/admin/i18n/country/add/',
            '/de/admin/i18n/countrylanguage/',
            '/de/admin/i18n/countrylanguage/add/',
            '/de/admin/i18n/language/',
            '/de/admin/i18n/language/add/',
            '/de/admin/i18n/nationality/',
            '/de/admin/i18n/nationality/add/',
            '/de/admin/i18n/phone/',
            '/de/admin/i18n/phone/add/',
            '/de/admin/i18n/timezone/',
            '/de/admin/i18n/timezone/add/',
            '/de/admin/image_mods/',
            '/de/admin/image_mods/imagecropping/',
            '/de/admin/image_mods/imagecropping/add/',
            '/de/admin/image_mods/imagemodification/',
            '/de/admin/image_mods/imagemodification/add/',
            '/de/admin/image_mods/imagemodificationgroup/',
            '/de/admin/image_mods/imagemodificationgroup/add/',
            '/de/admin/internal_links/',
            '/de/admin/internal_links/linkgroup/',
            '/de/admin/internal_links/linkgroup/add/',
            '/de/admin/jsi18n/',
            '/de/admin/mailchimp/',
            '/de/admin/mailchimp/campaign/',
            '/de/admin/mailchimp/campaign/15/preview/',
            '/de/admin/mailchimp/campaign/add/',
            '/de/admin/mailchimp/campaign/template-content/text/',
            '/de/admin/mailchimp/mlist/',
            '/de/admin/mailchimp/mlist/add/',
            '/de/admin/mailchimp/settings/',
            '/de/admin/mailchimp/settings/add/',
            '/de/admin/mailchimp/subscription/',
            '/de/admin/mailchimp/subscription/add/',
            '/de/admin/mailing/',
            '/de/admin/mailing/emailmessage/',
            '/de/admin/mailing/emailmessage/add/',
            '/de/admin/mailing/emailtemplate/',
            '/de/admin/mailing/emailtemplate/add/',
            '/de/admin/mailing/emailtemplateplaceholder/',
            '/de/admin/mailing/emailtemplateplaceholder/add/',
            '/de/admin/media_gallery/',
            '/de/admin/media_gallery/mediagallery/',
            '/de/admin/media_gallery/mediagallery/add/',
            '/de/admin/mega_menu/',
            '/de/admin/mega_menu/menublock/',
            '/de/admin/mega_menu/menublock/add/',
            '/de/admin/museums/',
            '/de/admin/museums/accessibilityoption/',
            '/de/admin/museums/accessibilityoption/add/',
            '/de/admin/museums/museum/',
            '/de/admin/museums/museum/3/owners/',
            '/de/admin/museums/museum/add/',
            '/de/admin/museums/museumcategory/',
            '/de/admin/museums/museumcategory/1/move/',
            '/de/admin/museums/museumcategory/add/',
            '/de/admin/museumssummer/',
            '/de/admin/museumssummer/location/',
            '/de/admin/museumssummer/location/add/',
            '/de/admin/password_change/',
            '/de/admin/password_change/done/',
            '/de/admin/permissions/',
            '/de/admin/permissions/perobjectgroup/',
            '/de/admin/permissions/perobjectgroup/add/',
            '/de/admin/permissions/rowlevelpermission/',
            '/de/admin/permissions/rowlevelpermission/add/',
            '/de/admin/shop/',
            '/de/admin/shop/shopproduct/',
            '/de/admin/shop/shopproduct/add/',
            '/de/admin/shop/shopproductcategory/',
            '/de/admin/shop/shopproductcategory/add/',
            '/de/admin/shop/shopproducttype/',
            '/de/admin/shop/shopproducttype/2/move/',
            '/de/admin/shop/shopproducttype/add/',
            '/de/admin/sites/',
            '/de/admin/sites/site/',
            '/de/admin/sites/site/add/',
            '/de/admin/slideshows/',
            '/de/admin/slideshows/slideshow/',
            '/de/admin/slideshows/slideshow/add/',
            '/de/admin/snippet/',
            '/de/admin/snippet/snippet/',
            '/de/admin/snippet/snippet/add/',
            '/de/admin/tagging/',
            '/de/admin/tagging/tag/',
            '/de/admin/tagging/tag/add/',
            '/de/admin/tagging/taggeditem/',
            '/de/admin/tagging/taggeditem/add/',
            '/de/admin/tastypie/',
            '/de/admin/tastypie/apikey/',
            '/de/admin/tastypie/apikey/add/',
            '/de/admin/tips/',
            '/de/admin/tips/tipoftheday/',
            '/de/admin/tips/tipoftheday/add/',
            '/de/admin/tips/tipoftheday/details-json/59/768/',
            '/de/admin/tracker/',
            '/de/admin/tracker/concern/',
            '/de/admin/tracker/concern/add/',
            '/de/admin/tracker/ticket/',
            '/de/admin/tracker/ticket/add/',
            '/de/admin/twitterwall/',
            '/de/admin/twitterwall/searchsettings/',
            '/de/admin/twitterwall/searchsettings/add/',
            '/de/admin/twitterwall/tweet/',
            '/de/admin/twitterwall/tweet/add/',
            '/de/admin/twitterwall/twitteruser/',
            '/de/admin/twitterwall/twitteruser/add/',
            '/de/admin/twitterwall/usertimelinesettings/',
            '/de/admin/twitterwall/usertimelinesettings/add/',
            '/de/admin/workshops/',
            '/de/admin/workshops/workshop/',
            '/de/admin/workshops/workshop/add/',
            '/de/admin/workshops/workshoptype/',
            '/de/admin/workshops/workshoptype/add/',
            '/de/shop/add/',
            '/de/museen/add/',
            '/de/ausstellungen/add/',
            '/de/veranstaltungen/add/',
            '/de/fuehrungen/add/',
        ]

        self.authenticated_302 = [
            '/de/admin/cms/page/5/move-page/',
            '/de/admin/cms/page/5/copy-page/',
            '/de/admin/cms/page/5/preview/',
            '/de/admin/filebrowser/delete/',  # shouldn't this redirect to login screen instead of opening one?
        ]

        # Bad request paramethers
        self.authenticated_400 = [
            "/de/admin/filebrowser/upload_file/",
        ]

        self.anonymous_401_authenticated_401 = [
            '/de/api/v1/exhibition/',
            '/de/api/v1/exhibition/schema/',
            '/de/api/v1/exhibition_category/',
            '/de/api/v1/exhibition_category/schema/',
            '/de/api/v1/museum/',
            '/de/api/v1/museum/schema/',
            '/de/api/v1/museum_category/',
            '/de/api/v1/museum_category/schema/',
            '/de/api/v2/accessibility_option/',
            '/de/api/v2/accessibility_option/schema/',
            '/de/api/v2/event/',
            '/de/api/v2/event/schema/',
            '/de/api/v2/event_category/',
            '/de/api/v2/event_category/schema/',
            '/de/api/v2/event_media_file/',
            '/de/api/v2/event_media_file/schema/',
            '/de/api/v2/event_time/',
            '/de/api/v2/event_time/schema/',
            '/de/api/v2/exhibition/',
            '/de/api/v2/exhibition/schema/',
            '/de/api/v2/exhibition_category/',
            '/de/api/v2/exhibition_category/schema/',
            '/de/api/v2/exhibition_media_file/',
            '/de/api/v2/exhibition_media_file/schema/',
            '/de/api/v2/exhibition_organizer/',
            '/de/api/v2/exhibition_organizer/schema/',
            '/de/api/v2/exhibition_season/',
            '/de/api/v2/exhibition_season/schema/',
            '/de/api/v2/museum/',
            '/de/api/v2/museum/schema/',
            '/de/api/v2/museum_category/',
            '/de/api/v2/museum_category/schema/',
            '/de/api/v2/museum_media_file/',
            '/de/api/v2/museum_media_file/schema/',
            '/de/api/v2/museum_season/',
            '/de/api/v2/museum_season/schema/',
            '/de/api/v2/museum_social_media_chanel/',
            '/de/api/v2/museum_social_media_chanel/schema/',
            '/de/api/v2/museum_special_opening_time/',
            '/de/api/v2/museum_special_opening_time/schema/',
            '/de/api/v2/workshop/',
            '/de/api/v2/workshop/schema/',
            '/de/api/v2/workshop_media_file/',
            '/de/api/v2/workshop_media_file/schema/',
            '/de/api/v2/workshop_organizer/',
            '/de/api/v2/workshop_organizer/schema/',
            '/de/api/v2/workshop_time/',
            '/de/api/v2/workshop_time/schema/',
        ]

        # Access Denied
        self.anonymous_403 = [
            "/autocomplete/",
            '/de/grappelli/lookup/related/',
            '/de/grappelli/lookup/autocomplete/',
            '/de/grappelli/lookup/m2m/',
            '/de/admin/museums/museum/3/owners/',
        ]

        # Page not found
        self.authenticated_404 = [
            "/de/admin/filebrowser/delete-version/",
        ]

        self.anonymous_404_authenticated_404 = [
            "/de/recrop/",
        ]

        self.anonymous_405_authenticated_405 = [
            "/de/helper/ajax-upload/",
        ]

        self.authenticated_405 = [
            '/de/admin/cms/page/1/change-status/',
            '/de/admin/cms/page/1/change-navigation/',
            '/de/admin/cms/page/1/change_template/',
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
        (405, urls.authenticated_405),
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
    os.environ["DJANGO_SETTINGS_MODULE"] = "settings.local"
    unittest.TextTestRunner(verbosity=1).run(suite())

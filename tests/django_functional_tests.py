# -*- coding: UTF-8 -*-
# inspired by http://stackoverflow.com/a/3772008

from django.test.utils import setup_test_environment
from django.test import Client
import unittest

class PageTest(unittest.TestCase):
    def __init__(self, url_path='', expected_status_code=200):
        super(PageTest, self).__init__()
        self.url_path = url_path
        self.expected_status_code = expected_status_code

    def setUp(self):
        setup_test_environment()
        self.client = Client()

    def tearDown(self):
        pass

    def shortDescription(self):
        return 'page {} should return {} status code'.format(
            self.url_path,
            self.expected_status_code,
        )

    def runTest(self):
        assert isinstance(self.url_path, str)
        response = self.client.get(
            self.url_path,
            **{'HTTP_USER_AGENT':'silly-human', 'REMOTE_ADDR':'127.0.0.1'}
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


def suite():
    non_localized_slug_urls = ( # most should redirect, i.e. return 301
        # /contact/(?P<slug>[-\w]+)/
        # /contact/(?P<slug>[-\w]+)/alldone/
        # /creative-sector/(?P<creative_sector_slug>[^/]+)/
        # /(event|document|group|institution|person)/(?P<slug>[^/]+)/post/
        # /document/(?P<slug>[^/]+)/
        # /document/(?P<slug>[^/]+)/network/
        # /document/(?P<slug>[^/]+)/reviews/
        # /(event|document|group|institution|person)/(?P<slug>[^/]+)/post/
        ('/event/workshop-booking-tour-rockpop/post/', 301),
        # /event/(?P<slug>[^/]+)/claim/
        ('/event/workshop-booking-tour-rockpop/claim/', 301),
        # /event/(?P<slug>[^/]+)/delete/
        ('/event/workshop-booking-tour-rockpop/delete/', 301),
        # /event/(?P<slug>[^/]+)/map/
        ('/event/workshop-booking-tour-rockpop/map/', 301),
        # /event/(?P<slug>[^/]+)/network/
        ('/event/workshop-booking-tour-rockpop/network/', 301),
        # /event/(?P<slug>[^/]+)/portfolio/
        ('/event/workshop-booking-tour-rockpop/portfolio/', 301),
        # /event/(?P<slug>[^/]+)/portfolio/album/add/
        ('/event/workshop-booking-tour-rockpop/portfolio/album/add/', 301),
        # /event/(?P<slug>[^/]+)/portfolio/manage/
        ('/event/workshop-booking-tour-rockpop/portfolio/manage/', 301),
        # /event/(?P<slug>[^/]+)/portfolio/section/add/
        ('/event/workshop-booking-tour-rockpop/portfolio/section/add/', 301),
        # /event/(?P<slug>[^/]+)/portfolio/settings/
        ('/event/workshop-booking-tour-rockpop/portfolio/settings/', 301),
        # /event/(?P<slug>[^/]+)/portfolio/settings/delete-landing-page-image/
        ('/event/workshop-booking-tour-rockpop/portfolio/settings/delete-landing-page-image/', 301),
        # /event/(?P<slug>[^/]+)/reviews/
        ('/event/workshop-booking-tour-rockpop/reviews/', 301),
        # /(event|document|group|institution|person)/(?P<slug>[^/]+)/post/
        # /group/(?P<slug>[^/]+)/
        # /group/(?P<slug>[^/]+)/events/
        # /group/(?P<slug>[^/]+)/members/invite/
        # /group/(?P<slug>[^/]+)/projects/
        # /(event|document|group|institution|person)/(?P<slug>[^/]+)/post/
        ('/institution/a_s_theater_film_ltd/post/', 301),
        # /institution/(?P<slug>[^/]+)/
        ('/institution/a_s_theater_film_ltd/', 301),
        # /institution/(?P<slug>[^/]+)/jobs/
        ('/institution/a_s_theater_film_ltd/jobs/', 301),
        # /institution/(?P<slug>[^/]+)/map/
        ('/institution/a_s_theater_film_ltd/map/', 301),
        # /institution/(?P<slug>[^/]+)/message/
        ('/institution/a_s_theater_film_ltd/message/', 301),
        # /institution/(?P<slug>[^/]+)/message/alldone/
        ('/institution/a_s_theater_film_ltd/message/alldone/', 301),
        # /institution/(?P<slug>[^/]+)/network/
        ('/institution/a_s_theater_film_ltd/network/', 301),
        # /institution/(?P<slug>[^/]+)/network/groups/
        ('/institution/a_s_theater_film_ltd/network/groups/', 301),
        # /institution/(?P<slug>[^/]+)/network/partners/
        ('/institution/a_s_theater_film_ltd/network/partners/', 301),
        # /institution/(?P<slug>[^/]+)/network/staff/
        ('/institution/a_s_theater_film_ltd/network/staff/', 301),
        # /institution/(?P<slug>[^/]+)/portfolio/
        ('/institution/a_s_theater_film_ltd/portfolio/', 301),
        # /institution/(?P<slug>[^/]+)/portfolio/album/add/
        ('/institution/a_s_theater_film_ltd/portfolio/album/add/', 301),
        # /institution/(?P<slug>[^/]+)/portfolio/fb-sync/
        ('/institution/a_s_theater_film_ltd/portfolio/fb-sync/', 301),
        # /institution/(?P<slug>[^/]+)/portfolio/manage/
        ('/institution/a_s_theater_film_ltd/portfolio/manage/', 301),
        # /institution/(?P<slug>[^/]+)/portfolio/section/add/
        ('/institution/a_s_theater_film_ltd/portfolio/section/add/', 301),
        # /institution/(?P<slug>[^/]+)/portfolio/settings/
        ('/institution/a_s_theater_film_ltd/portfolio/settings/', 301),
        # /institution/(?P<slug>[^/]+)/portfolio/settings/delete-landing-page-image/
        ('/institution/a_s_theater_film_ltd/portfolio/settings/delete-landing-page-image/', 301),
        # /institution/(?P<slug>[^/]+)/projects/
        ('/institution/a_s_theater_film_ltd/projects/', 301),
        # /institution/(?P<slug>[^/]+)/reviews/
        ('/institution/a_s_theater_film_ltd/reviews/', 301),
        # /job/(?P<slug>[^/]+)/delete/
        ('/job/7654237/delete/', 301),
        # /news/creative-sector/(?P<creative_sector_slug>[^/]+)/
        # /news/creative-sector/(?P<creative_sector_slug>[^/]+)/features/
        # /(event|document|group|institution|person)/(?P<slug>[^/]+)/post/
        ('/person/aidas_bendoraitis/post/', 301),
        # /person/(?P<slug>[^/]+)/
        ('/person/aidas_bendoraitis/', 301),
        # /person/(?P<slug>[^/]+)/jobs/
        ('/person/aidas_bendoraitis/jobs/', 301),
        # /person/(?P<slug>[^/]+)/map/
        ('/person/aidas_bendoraitis/map/', 301),
        # /person/(?P<slug>[^/]+)/message/
        ('/person/aidas_bendoraitis/message/', 301),
        # /person/(?P<slug>[^/]+)/message/alldone/
        ('/person/aidas_bendoraitis/message/alldone/', 301),
        # /person/(?P<slug>[^/]+)/network/
        ('/person/aidas_bendoraitis/network/', 301),
        # /person/(?P<slug>[^/]+)/network/groups/
        ('/person/aidas_bendoraitis/network/groups/', 301),
        # /person/(?P<slug>[^/]+)/network/institution_contacts/
        ('/person/aidas_bendoraitis/network/institution_contacts/', 301),
        # /person/(?P<slug>[^/]+)/network/person_contacts/
        ('/person/aidas_bendoraitis/network/person_contacts/', 301),
        # /person/(?P<slug>[^/]+)/portfolio/
        ('/person/aidas_bendoraitis/portfolio/', 301),
        # /person/(?P<slug>[^/]+)/portfolio/album/add/
        ('/person/aidas_bendoraitis/portfolio/album/add/', 301),
        # /person/(?P<slug>[^/]+)/portfolio/fb-sync/
        ('/person/aidas_bendoraitis/portfolio/fb-sync/', 301),
        # /person/(?P<slug>[^/]+)/portfolio/manage/
        ('/person/aidas_bendoraitis/portfolio/manage/', 301),
        # /person/(?P<slug>[^/]+)/portfolio/section/add/
        ('/person/aidas_bendoraitis/portfolio/section/add/', 301),
        # /person/(?P<slug>[^/]+)/portfolio/settings/
        ('/person/aidas_bendoraitis/portfolio/settings/', 301),
        # /person/(?P<slug>[^/]+)/portfolio/settings/delete-landing-page-image/
        ('/person/aidas_bendoraitis/portfolio/settings/delete-landing-page-image/', 301),
        # /person/(?P<slug>[^/]+)/projects/
        ('/person/aidas_bendoraitis/projects/', 301),
        # /person/(?P<slug>[^/]+)/reviews/
        ('/person/aidas_bendoraitis/reviews/', 301),
    )

    localized_slug_urls = (
        # /contact/(?P<slug>[-\w]+)/
        # /contact/(?P<slug>[-\w]+)/alldone/
        # /creative-sector/(?P<creative_sector_slug>[^/]+)/
        # /(event|document|group|institution|person)/(?P<slug>[^/]+)/post/
        # /document/(?P<slug>[^/]+)/
        # /document/(?P<slug>[^/]+)/network/
        # /document/(?P<slug>[^/]+)/reviews/
        # /(event|document|group|institution|person)/(?P<slug>[^/]+)/post/
        ('/de/event/workshop-booking-tour-rockpop/post/', 302), # login required
        # /event/(?P<slug>[^/]+)/claim/
        ('/de/event/workshop-booking-tour-rockpop/claim/', 302), # login required
        # /event/(?P<slug>[^/]+)/delete/
        ('/de/event/workshop-booking-tour-rockpop/delete/', 302), # login required
        # /event/(?P<slug>[^/]+)/map/
        ('/de/event/workshop-booking-tour-rockpop/map/', 200),
        # /event/(?P<slug>[^/]+)/network/
        ('/de/event/workshop-booking-tour-rockpop/network/', 200),
        # /event/(?P<slug>[^/]+)/portfolio/
        ('/de/event/workshop-booking-tour-rockpop/portfolio/', 200),
        # /event/(?P<slug>[^/]+)/portfolio/album/add/
        ('/de/event/workshop-booking-tour-rockpop/portfolio/album/add/', 403), # access denied
        # /event/(?P<slug>[^/]+)/portfolio/manage/
        ('/de/event/workshop-booking-tour-rockpop/portfolio/manage/', 403), # access denied
        # /event/(?P<slug>[^/]+)/portfolio/section/add/
        ('/de/event/workshop-booking-tour-rockpop/portfolio/section/add/', 403), # access denied
        # /event/(?P<slug>[^/]+)/portfolio/settings/
        ('/de/event/workshop-booking-tour-rockpop/portfolio/settings/', 403), # access denied
        # /event/(?P<slug>[^/]+)/portfolio/settings/delete-landing-page-image/
        ('/de/event/workshop-booking-tour-rockpop/portfolio/settings/delete-landing-page-image/', 403), # access denied
        # /event/(?P<slug>[^/]+)/reviews/
        ('/de/event/workshop-booking-tour-rockpop/reviews/', 200),
        # /(event|document|group|institution|person)/(?P<slug>[^/]+)/post/
        # /group/(?P<slug>[^/]+)/
        # /group/(?P<slug>[^/]+)/events/
        # /group/(?P<slug>[^/]+)/members/invite/
        # /group/(?P<slug>[^/]+)/projects/
        # /(event|document|group|institution|person)/(?P<slug>[^/]+)/post/
        ('/de/institution/a_s_theater_film_ltd/post/', 302), # login required
        # /institution/(?P<slug>[^/]+)/
        ('/de/institution/a_s_theater_film_ltd/', 200),
        # /institution/(?P<slug>[^/]+)/jobs/
        ('/de/institution/a_s_theater_film_ltd/jobs/', 200),
        # /institution/(?P<slug>[^/]+)/map/
        ('/de/institution/a_s_theater_film_ltd/map/', 200),
        # /institution/(?P<slug>[^/]+)/message/
        ('/de/institution/a_s_theater_film_ltd/message/', 302), # login required
        # /institution/(?P<slug>[^/]+)/message/alldone/
        ('/de/institution/a_s_theater_film_ltd/message/alldone/', 200),
        # /institution/(?P<slug>[^/]+)/network/
        ('/de/institution/a_s_theater_film_ltd/network/', 200),
        # /institution/(?P<slug>[^/]+)/network/groups/
        ('/de/institution/a_s_theater_film_ltd/network/groups/', 200),
        # /institution/(?P<slug>[^/]+)/network/partners/
        ('/de/institution/a_s_theater_film_ltd/network/partners/', 404), # page not found
        # /institution/(?P<slug>[^/]+)/network/staff/
        ('/de/institution/a_s_theater_film_ltd/network/staff/', 200),
        # /institution/(?P<slug>[^/]+)/portfolio/
        ('/de/institution/a_s_theater_film_ltd/portfolio/', 200),
        # /institution/(?P<slug>[^/]+)/portfolio/album/add/
        ('/de/institution/a_s_theater_film_ltd/portfolio/album/add/', 403), # access denied
        # /institution/(?P<slug>[^/]+)/portfolio/fb-sync/
        ('/de/institution/a_s_theater_film_ltd/portfolio/fb-sync/', 302), # login required
        # /institution/(?P<slug>[^/]+)/portfolio/manage/
        ('/de/institution/a_s_theater_film_ltd/portfolio/manage/', 403), # access denied
        # /institution/(?P<slug>[^/]+)/portfolio/section/add/
        ('/de/institution/a_s_theater_film_ltd/portfolio/section/add/', 403), # access denied
        # /institution/(?P<slug>[^/]+)/portfolio/settings/
        ('/de/institution/a_s_theater_film_ltd/portfolio/settings/', 403), # access denied
        # /institution/(?P<slug>[^/]+)/portfolio/settings/delete-landing-page-image/
        ('/de/institution/a_s_theater_film_ltd/portfolio/settings/delete-landing-page-image/', 403), # access denied
        # /institution/(?P<slug>[^/]+)/projects/
        ('/de/institution/a_s_theater_film_ltd/projects/', 200),
        # /institution/(?P<slug>[^/]+)/reviews/
        ('/de/institution/a_s_theater_film_ltd/reviews/', 200),
        # /job/(?P<slug>[^/]+)/delete/
        ('/de/job/7654237/delete/', 302), # login required
        # /news/creative-sector/(?P<creative_sector_slug>[^/]+)/
        # /news/creative-sector/(?P<creative_sector_slug>[^/]+)/features/
        # /(event|document|group|institution|person)/(?P<slug>[^/]+)/post/
        ('/de/person/aidas_bendoraitis/post/', 302), # login required
        # /person/(?P<slug>[^/]+)/
        ('/de/person/aidas_bendoraitis/', 200),
        # /person/(?P<slug>[^/]+)/jobs/
        ('/de/person/aidas_bendoraitis/jobs/', 200),
        # /person/(?P<slug>[^/]+)/map/
        ('/de/person/aidas_bendoraitis/map/', 200),
        # /person/(?P<slug>[^/]+)/message/
        ('/de/person/aidas_bendoraitis/message/', 302), # login required
        # /person/(?P<slug>[^/]+)/message/alldone/
        ('/de/person/aidas_bendoraitis/message/alldone/', 200),
        # /person/(?P<slug>[^/]+)/network/
        ('/de/person/aidas_bendoraitis/network/', 200),
        # /person/(?P<slug>[^/]+)/network/groups/
        ('/de/person/aidas_bendoraitis/network/groups/', 200),
        # /person/(?P<slug>[^/]+)/network/institution_contacts/
        ('/de/person/aidas_bendoraitis/network/institution_contacts/', 200),
        # /person/(?P<slug>[^/]+)/network/person_contacts/
        ('/de/person/aidas_bendoraitis/network/person_contacts/', 200),
        # /person/(?P<slug>[^/]+)/portfolio/
        ('/de/person/aidas_bendoraitis/portfolio/', 302), # login required
        # /person/(?P<slug>[^/]+)/portfolio/album/add/
        ('/de/person/aidas_bendoraitis/portfolio/album/add/', 403), # access denied
        # /person/(?P<slug>[^/]+)/portfolio/fb-sync/
        ('/de/person/aidas_bendoraitis/portfolio/fb-sync/', 302), # login required
        # /person/(?P<slug>[^/]+)/portfolio/manage/
        ('/de/person/aidas_bendoraitis/portfolio/manage/', 403), # access denied
        # /person/(?P<slug>[^/]+)/portfolio/section/add/
        ('/de/person/aidas_bendoraitis/portfolio/section/add/', 403), # access denied
        # /person/(?P<slug>[^/]+)/portfolio/settings/
        ('/de/person/aidas_bendoraitis/portfolio/settings/', 403), # access denied
        # /person/(?P<slug>[^/]+)/portfolio/settings/delete-landing-page-image/
        ('/de/person/aidas_bendoraitis/portfolio/settings/delete-landing-page-image/', 403), # access denied
        # /person/(?P<slug>[^/]+)/projects/
        ('/de/person/aidas_bendoraitis/projects/', 200),
        # /person/(?P<slug>[^/]+)/reviews/
        ('/de/person/aidas_bendoraitis/reviews/', 200),
    )

    non_localized_constant_urls  = ( # most should redirect, i.e. return 301
        ('/', 301),
        ('/account/', 301),
        ('/compatibility/', 301),
        ('/contact/', 301),
        ('/contact/alldone/', 301),
        ('/creative-sector/', 301),
        ('/dashboard/', 301),
        ('/documents/', 301),
        ('/events/add/', 301),
        ('/facebook/', 301),
        ('/facebook/data-exchange/', 301),
        ('/facebook/link/', 301),
        ('/facebook/link/login/', 301),
        ('/facebook/link/register/', 301),
        ('/facebook/manage/', 301),
        ('/facebook/pages/', 301),
        ('/gmap/', 301),
        ('/groups/', 301),
        ('/groups/add/', 301),
        ('/groups/invitations/', 301),
        ('/helper/bookmark/', 200),
        ('/helper/country_lookup/', 200),
        ('/helper/institution_lookup/', 302),
        ('/helper/person_lookup/', 302),
        ('/helper/site-visitors/', 200),
        ('/i18n/setlang/', 301),
        ('/institutions/', 301),
        ('/institutions/add/', 301),
        ('/invite/', 301),
        ('/invite/done/', 301),
        ('/jobs/add/', 301),
        ('/jobs/create-berlin-jobboard/', 301),
        ('/jobs/talent-in-berlin/', 301),
        ('/jsi18n/', 301),
        ('/jssettings/', 301),
        ('/kreativarbeiten/', 301),
        ('/kreativarbeiten/best-practice/', 301),
        ('/kreativarbeiten/blog/', 301),
        ('/kreativarbeiten/blog/all/', 301),
        ('/kreativarbeiten/blog/drafts/', 301),
        ('/kreativarbeiten/contact/', 301),
        ('/kreativarbeiten/contact/done/', 301),
        ('/kreativarbeiten/newsfeed/', 301),
        ('/kreativarbeiten/tweets/', 301),
        ('/lists/', 301),
        ('/livestream/', 301),
        ('/login', 301),
        ('/logout', 301),
        ('/map/', 301),
        ('/map/object-list/', 301),
        ('/my-messages/json/', 301),
        ('/my-messages/new/', 301),
        ('/my-profile/', 301),
        ('/my-profile/bookmarks/', 301),
        ('/my-profile/delete/', 301),
        ('/my-profile/delete/done/', 301),
        ('/my-profile/favorites/', 301),
        ('/my-profile/memos/', 301),
        ('/my-profile/privacy/', 301),
        ('/news/', 301),
        ('/news/articles/', 301),
        ('/news/interviews/', 301),
        ('/notification/', 301),
        ('/notification/feed/', 301),
        ('/notification/mark_all_seen/', 301),
        ('/notification/settings/', 301),
        ('/password_change/', 301),
        ('/password_change/done/', 301),
        ('/password_reset/', 301),
        ('/password_reset/complete/', 301),
        ('/password_reset/done/', 301),
        ('/people/', 301),
        # ('/recrop/', 200), # TODO rethink this test, /recrop/ requires URL parameters
        ('/register/', 301),
        ('/register/alldone/', 301),
        ('/register/done/', 301),
        ('/rosetta/', 301),
        ('/rosetta/download/', 301),
        ('/rosetta/pick/', 301),
        ('/search/', 301),
        ('/search/full/', 301),
        ('/simplesearch/', 301),
        # ('/sitemap.xml', 301), # FIXME AttributeError in apps/site_specific/models.py line 274
        ('/styleguide/', 301),
        ('/styleguide/colors/', 301),
        ('/styleguide/forms/', 301),
        ('/styleguide/grid/', 301),
        ('/styleguide/images/', 301),
        ('/styleguide/typography/', 301),
        ('/subscribe4info/', 301),
        ('/subscribe4info/done/', 301),
        ('/tagging_autocomplete/list', 200), # FIXME NameError: global name 'MultiValueDictKeyError' is not defined ####
        ('/ticket/', 301),
        ('/tweets/', 301),
    )

    localized_constant_urls = ( # most should work, i.e. return 200
        ('/de/', 200),
        ('/de/account/', 200),
        ('/de/compatibility/', 200),
        ('/de/contact/', 200),
        ('/de/contact/alldone/', 200),
        ('/de/creative-sector/', 302),
        ('/de/dashboard/', 302),
        ('/de/documents/', 200),
        ('/de/events/add/', 302),
        ('/de/facebook/', 302),
        ('/de/facebook/data-exchange/', 302),
        ('/de/facebook/link/', 302),
        ('/de/facebook/link/login/', 302),
        ('/de/facebook/link/register/', 302),
        ('/de/facebook/manage/', 302),
        ('/de/facebook/pages/', 302),
        ('/de/gmap/', 200),
        ('/de/groups/', 200),
        ('/de/groups/add/', 302),
        ('/de/groups/invitations/', 302),
        # ('/de/helper/blank_doc/', 200), # included in PATHS_NO_REDIRECTION
        # ('/de/helper/bookmark/', 200), # included in PATHS_NO_REDIRECTION
        # ('/de/helper/country_lookup/', 200), # included in PATHS_NO_REDIRECTION
        # ('/de/helper/institution_lookup/', 302), # included in PATHS_NO_REDIRECTION
        # ('/de/helper/person_lookup/', 302), # included in PATHS_NO_REDIRECTION
        # ('/de/helper/site-visitors/', 200), # included in PATHS_NO_REDIRECTION
        ('/de/i18n/setlang/', 302),
        ('/de/institutions/', 200),
        ('/de/institutions/add/', 302),
        ('/de/invite/', 302),
        ('/de/invite/done/', 200),
        ('/de/jobs/add/', 302),
        ('/de/jobs/create-berlin-jobboard/', 200),
        ('/de/jobs/talent-in-berlin/', 200),
        ('/de/jsi18n/', 200),
        ('/de/jssettings/', 200),
        ('/de/kreativarbeiten/', 302), # redirects to /de/kreativarbeiten/blog/
        ('/de/kreativarbeiten/best-practice/', 200),
        ('/de/kreativarbeiten/blog/', 200),
        ('/de/kreativarbeiten/blog/all/', 200),
        ('/de/kreativarbeiten/blog/drafts/', 200), # FIXME currently returns 403, should probably redirect to login page
        ('/de/kreativarbeiten/contact/', 200),
        ('/de/kreativarbeiten/contact/done/', 200),
        ('/de/kreativarbeiten/newsfeed/', 200),
        ('/de/kreativarbeiten/tweets/', 200),
        ('/de/lists/', 200),
        ('/de/livestream/', 200),
        ('/de/login', 200),
        ('/de/logout', 302),
        ('/de/map/', 200),
        ('/de/map/object-list/', 200), # FIXME currently returns 403, should probably redirect to login page
        ('/de/my-messages/json/', 200),
        ('/de/my-messages/new/', 302),
        ('/de/my-profile/', 302),
        ('/de/my-profile/bookmarks/', 200),
        ('/de/my-profile/delete/', 302),
        ('/de/my-profile/delete/done/', 200),
        ('/de/my-profile/favorites/', 200),
        ('/de/my-profile/memos/', 200),
        ('/de/my-profile/privacy/', 302),
        ('/de/news/', 200),
        ('/de/news/articles/', 200),
        ('/de/news/interviews/', 200),
        ('/de/notification/', 302),
        ('/de/notification/feed/', 200), # FIXME currently returns 401 (HTTP login dialog)
        ('/de/notification/mark_all_seen/', 302),
        ('/de/notification/settings/', 302),
        ('/de/password_change/', 302),
        ('/de/password_change/done/', 200),
        ('/de/password_reset/', 200),
        ('/de/password_reset/complete/', 200),
        ('/de/password_reset/done/', 200),
        ('/de/people/', 200),
        # ('/de/recrop/', 200), # included in PATHS_NO_REDIRECTION
        ('/de/register/', 200),
        ('/de/register/alldone/', 302),
        ('/de/register/done/', 200),
        ('/de/rosetta/', 302),
        ('/de/rosetta/download/', 302),
        ('/de/rosetta/pick/', 302),
        ('/de/search/', 200),
        ('/de/search/full/', 200),
        ('/de/simplesearch/', 200),
        # ('/de/sitemap.xml', 200), # FIXME AttributeError in apps/site_specific/models.py line 274
        ('/de/styleguide/', 200),
        ('/de/styleguide/colors/', 200),
        ('/de/styleguide/forms/', 200),
        ('/de/styleguide/grid/', 200),
        ('/de/styleguide/images/', 200),
        ('/de/styleguide/typography/', 200),
        ('/de/subscribe4info/', 200),
        ('/de/subscribe4info/done/', 200),
        # ('/de/tagging_autocomplete/list', 200), # included in PATHS_NO_REDIRECTION
        ('/de/ticket/', 200),
        ('/de/tweets/', 200),
    )

    admin_urls = ( # most should work, i.e. return 200
        ('/admin/', 200),
        ('/admin/articles/article/', 200),
        ('/admin/articles/article/add/', 200),
        ('/admin/articles/articlecontentprovider/', 200),
        ('/admin/articles/articlecontentprovider/add/', 200),
        ('/admin/articles/articletype/', 200),
        ('/admin/articles/articletype/add/', 200),
        ('/admin/auth/group/', 200),
        ('/admin/auth/group/add/', 200),
        ('/admin/auth/user/', 200),
        ('/admin/auth/user/add/', 200),
        ('/admin/auth/user/send_mail/', 200),
        ('/admin/blocks/infoblock/', 200),
        ('/admin/blocks/infoblock/add/', 200),
        ('/admin/blog/blog/', 200),
        ('/admin/blog/blog/add/', 200),
        ('/admin/blog/post/', 200),
        ('/admin/blog/post/add/', 200),
        ('/admin/bookmarks/bookmark/', 200),
        ('/admin/bookmarks/bookmark/add/', 200),
        ('/admin/comments/comment/', 200),
        ('/admin/comments/comment/add/', 200),
        ('/admin/comments/moderatordeletion/', 200),
        ('/admin/comments/moderatordeletion/add/', 200),
        ('/admin/comments/moderatordeletionreason/', 200),
        ('/admin/comments/moderatordeletionreason/add/', 200),
        ('/admin/configuration/sitesettings/', 200),
        ('/admin/configuration/sitesettings/add/', 200),
        ('/admin/contact_form/contactformcategory/', 200),
        ('/admin/contact_form/contactformcategory/add/', 200),
        ('/admin/djcelery/crontabschedule/', 200),
        ('/admin/djcelery/crontabschedule/add/', 200),
        ('/admin/djcelery/intervalschedule/', 200),
        ('/admin/djcelery/intervalschedule/add/', 200),
        ('/admin/djcelery/periodictask/', 200),
        ('/admin/djcelery/periodictask/add/', 200),
        ('/admin/djcelery/taskstate/', 200),
        ('/admin/djcelery/taskstate/add/', 200),
        ('/admin/djcelery/workerstate/', 200),
        ('/admin/djcelery/workerstate/add/', 200),
        ('/admin/doc/', 200),
        ('/admin/doc/bookmarklets/', 200),
        ('/admin/doc/filters/', 200),
        ('/admin/doc/models/', 200),
        ('/admin/doc/tags/', 200),
        ('/admin/doc/views/', 200),
        ('/admin/email_campaigns/campaign/', 200),
        ('/admin/email_campaigns/campaign/add/', 200),
        ('/admin/email_campaigns/infosubscription/', 200),
        ('/admin/email_campaigns/infosubscription/add/', 200),
        ('/admin/email_campaigns/infosubscription/send_mail/', 200),
        ('/admin/email_campaigns/mailing/', 200),
        ('/admin/email_campaigns/mailing/add/', 200),
        ('/admin/email_campaigns/mailinglist/', 200),
        ('/admin/email_campaigns/mailinglist/add/', 200),
        ('/admin/events/event/', 200),
        ('/admin/events/event/add/', 200),
        ('/admin/events/eventtimelabel/', 200),
        ('/admin/events/eventtimelabel/add/', 200),
        ('/admin/events/eventtype/', 200),
        ('/admin/events/eventtype/add/', 200),
        ('/admin/external_services/articleimportsource/', 200),
        ('/admin/external_services/articleimportsource/add/', 200),
        ('/admin/external_services/objectmapper/', 200),
        ('/admin/external_services/objectmapper/add/', 200),
        ('/admin/external_services/service/', 200),
        ('/admin/external_services/service/add/', 200),
        ('/admin/external_services/serviceactionlog/', 200),
        ('/admin/external_services/serviceactionlog/add/', 200),
        ('/admin/facebook_app/facebookappsettings/', 200),
        ('/admin/facebook_app/facebookappsettings/add/', 200),
        ('/admin/faqs/faqcategory/', 200),
        ('/admin/faqs/faqcategory/add/', 200),
        ('/admin/faqs/faqcontainer/', 200),
        ('/admin/faqs/faqcontainer/add/', 200),
        ('/admin/favorites/favorite/', 200),
        ('/admin/favorites/favorite/add/', 200),
        ('/admin/filebrowser/adjust-version/', 200),
        ('/admin/filebrowser/browse/', 200),
        ('/admin/filebrowser/delete-version/', 200),
        ('/admin/filebrowser/delete/', 200),
        ('/admin/filebrowser/delete_confirm/', 200),
        ('/admin/filebrowser/detail/', 200),
        ('/admin/filebrowser/get-version/', 200),
        ('/admin/filebrowser/upload_file/', 200), # FIXME AttributeError
        ('/admin/filebrowser/version/', 200),
        ('/admin/filebrowser/versions/', 200),
        ('/admin/flatpages/flatpage/', 200),
        ('/admin/flatpages/flatpage/add/', 200),
        ('/admin/groups_networks/grouptype/', 200),
        ('/admin/groups_networks/grouptype/add/', 200),
        ('/admin/groups_networks/persongroup/', 200),
        ('/admin/groups_networks/persongroup/add/', 200),
        ('/admin/i18n/area/', 200),
        ('/admin/i18n/area/add/', 200),
        ('/admin/i18n/country/', 200),
        ('/admin/i18n/country/add/', 200),
        ('/admin/i18n/countrylanguage/', 200),
        ('/admin/i18n/countrylanguage/add/', 200),
        ('/admin/i18n/language/', 200),
        ('/admin/i18n/language/add/', 200),
        ('/admin/i18n/nationality/', 200),
        ('/admin/i18n/nationality/add/', 200),
        ('/admin/i18n/phone/', 200),
        ('/admin/i18n/phone/add/', 200),
        ('/admin/i18n/timezone/', 200),
        ('/admin/i18n/timezone/add/', 200),
        ('/admin/image_mods/imagecropping/', 200),
        ('/admin/image_mods/imagecropping/add/', 200),
        ('/admin/image_mods/imagemodification/', 200),
        ('/admin/image_mods/imagemodification/add/', 200),
        ('/admin/image_mods/imagemodificationgroup/', 200),
        ('/admin/image_mods/imagemodificationgroup/add/', 200),
        ('/admin/individual_relations/individualrelation/', 200),
        ('/admin/individual_relations/individualrelation/add/', 200),
        ('/admin/individual_relations/individualrelationtype/', 200),
        ('/admin/individual_relations/individualrelationtype/add/', 200),
        ('/admin/institutions/institution/', 200),
        ('/admin/institutions/institution/add/', 200),
        ('/admin/institutions/institution/send_mail/', 200),
        ('/admin/institutions/institutiontype/', 200),
        ('/admin/institutions/institutiontype/add/', 200),
        ('/admin/institutions/legalform/', 200),
        ('/admin/institutions/legalform/add/', 200),
        ('/admin/jsi18n/', 200),
        ('/admin/location/address/', 200),
        ('/admin/location/address/add/', 200),
        ('/admin/logout/', 200),
        ('/admin/mailchimp/campaign/', 200),
        ('/admin/mailchimp/campaign/add/', 200),
        ('/admin/mailchimp/mlist/', 200),
        ('/admin/mailchimp/mlist/add/', 200),
        ('/admin/mailchimp/settings/', 200),
        ('/admin/mailchimp/settings/add/', 200),
        ('/admin/mailchimp/subscription/', 200),
        ('/admin/mailchimp/subscription/add/', 200),
        ('/admin/mailing/emailmessage/', 200),
        ('/admin/mailing/emailmessage/add/', 200),
        ('/admin/mailing/emailtemplate/', 200),
        ('/admin/mailing/emailtemplate/add/', 200),
        ('/admin/mailing/emailtemplateplaceholder/', 200),
        ('/admin/mailing/emailtemplateplaceholder/add/', 200),
        ('/admin/marketplace/joboffer/', 200),
        ('/admin/marketplace/joboffer/add/', 200),
        ('/admin/marketplace/jobqualification/', 200),
        ('/admin/marketplace/jobqualification/add/', 200),
        ('/admin/marketplace/jobsector/', 200),
        ('/admin/marketplace/jobsector/add/', 200),
        ('/admin/marketplace/jobtype/', 200),
        ('/admin/marketplace/jobtype/add/', 200),
        ('/admin/media_gallery/mediagallery/', 200),
        ('/admin/media_gallery/mediagallery/add/', 200),
        ('/admin/media_gallery/portfoliosettings/', 200),
        ('/admin/media_gallery/portfoliosettings/add/', 200),
        ('/admin/media_gallery/section/', 200),
        ('/admin/media_gallery/section/add/', 200),
        ('/admin/memos/memocollection/', 200),
        ('/admin/memos/memocollection/add/', 200),
        ('/admin/messaging/internalmessage/', 200),
        ('/admin/messaging/internalmessage/add/', 200),
        ('/admin/navigation/navigationlink/', 200),
        ('/admin/navigation/navigationlink/add/', 200),
        ('/admin/notification/digest/', 200),
        ('/admin/notification/digest/add/', 200),
        ('/admin/notification/notice/', 200),
        ('/admin/notification/notice/add/', 200),
        ('/admin/notification/noticeemailtemplate/', 200),
        ('/admin/notification/noticeemailtemplate/add/', 200),
        ('/admin/notification/noticesetting/', 200),
        ('/admin/notification/noticesetting/add/', 200),
        ('/admin/notification/noticetype/', 200),
        ('/admin/notification/noticetype/add/', 200),
        ('/admin/notification/noticetypecategory/', 200),
        ('/admin/notification/noticetypecategory/add/', 200),
        ('/admin/optionset/emailtype/', 200),
        ('/admin/optionset/emailtype/add/', 200),
        ('/admin/optionset/imtype/', 200),
        ('/admin/optionset/imtype/add/', 200),
        ('/admin/optionset/individuallocationtype/', 200),
        ('/admin/optionset/individuallocationtype/add/', 200),
        ('/admin/optionset/institutionallocationtype/', 200),
        ('/admin/optionset/institutionallocationtype/add/', 200),
        ('/admin/optionset/phonetype/', 200),
        ('/admin/optionset/phonetype/add/', 200),
        ('/admin/optionset/prefix/', 200),
        ('/admin/optionset/prefix/add/', 200),
        ('/admin/optionset/salutation/', 200),
        ('/admin/optionset/salutation/add/', 200),
        ('/admin/optionset/urltype/', 200),
        ('/admin/optionset/urltype/add/', 200),
        ('/admin/password_change/', 200),
        ('/admin/password_change/done/', 200),
        ('/admin/people/individualtype/', 200),
        ('/admin/people/individualtype/add/', 200),
        ('/admin/people/person/', 200),
        ('/admin/people/person/add/', 200),
        ('/admin/people/person/send_mail/', 200),
        ('/admin/permissions/perobjectgroup/', 200),
        ('/admin/permissions/perobjectgroup/add/', 200),
        ('/admin/permissions/rowlevelpermission/', 200),
        ('/admin/permissions/rowlevelpermission/add/', 200),
        ('/admin/profanity_filter/swearingcase/', 200),
        ('/admin/profanity_filter/swearingcase/add/', 200),
        ('/admin/profanity_filter/swearword/', 200),
        ('/admin/profanity_filter/swearword/add/', 200),
        ('/admin/redirects/redirect/', 200),
        ('/admin/redirects/redirect/add/', 200),
        ('/admin/resources/document/', 200),
        ('/admin/resources/document/add/', 200),
        ('/admin/resources/documenttype/', 200),
        ('/admin/resources/documenttype/add/', 200),
        ('/admin/resources/medium/', 200),
        ('/admin/resources/medium/add/', 200),
        ('/admin/site_specific/claimrequest/', 200),
        ('/admin/site_specific/claimrequest/add/', 200),
        ('/admin/site_specific/contextitem/', 200),
        ('/admin/site_specific/contextitem/add/', 200),
        ('/admin/site_specific/visit/', 200),
        ('/admin/site_specific/visit/add/', 200),
        ('/admin/sites/site/', 200),
        ('/admin/sites/site/add/', 200),
        ('/admin/slideshows/slideshow/', 200),
        ('/admin/slideshows/slideshow/add/', 200),
        ('/admin/structure/contextcategory/', 200),
        ('/admin/structure/contextcategory/add/', 200),
        ('/admin/structure/term/', 200),
        ('/admin/structure/term/add/', 200),
        ('/admin/structure/vocabulary/', 200),
        ('/admin/structure/vocabulary/add/', 200),
        ('/admin/tagging/tag/', 200),
        ('/admin/tagging/tag/add/', 200),
        ('/admin/tagging/taggeditem/', 200),
        ('/admin/tagging/taggeditem/add/', 200),
        ('/admin/templates/', 200), # FIXME currently returns 302
        ('/admin/tracker/concern/', 200),
        ('/admin/tracker/concern/add/', 200),
        ('/admin/tracker/ticket/', 200),
        ('/admin/tracker/ticket/add/', 200),
    )

    url_lists = (
        non_localized_slug_urls,
        localized_slug_urls,
        non_localized_constant_urls,
        localized_constant_urls,
        admin_urls,
    )

    suite = unittest.TestSuite()
    for url_list in url_lists:
        suite.addTests(
            PageTest(url_path, expected_status_code) for url_path, expected_status_code in url_list
        )
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())


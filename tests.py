from django.test.utils import setup_test_environment
from django.test import Client
import unittest

class PageTest(unittest.TestCase):
    def __init__(self, url_path='', expected_status_code=200):
        # print 'initing with {}'.format(url_path)
        super(PageTest, self).__init__()
        self.url_path = url_path
        self.expected_status_code = expected_status_code
        # self.__doc__ = url_path

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

    def __unicode__(self):
        return 'OpenPage({})'.format(self.url_path)

    def runTest(self):
        assert isinstance(self.url_path, str)
        response = self.client.get(
            self.url_path,
            **{'HTTP_USER_AGENT':'silly-human', 'REMOTE_ADDR':'127.0.0.1'}
        )
        # print self.url_path
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
    constant_urls = (
        # ('/admin/', 302),
        # ('/admin/articles/article/', 302),
        # ('/admin/articles/article/add/', 302),
        # ('/admin/articles/articlecontentprovider/', 302),
        # ('/admin/articles/articlecontentprovider/add/', 302),
        # ('/admin/articles/articletype/', 302),
        # ('/admin/articles/articletype/add/', 302),
        # ('/admin/auth/group/', 302),
        # ('/admin/auth/group/add/', 302),
        # ('/admin/auth/user/', 302),
        # ('/admin/auth/user/add/', 302),
        # ('/admin/auth/user/send_mail/', 302),
        # ('/admin/blocks/infoblock/', 302),
        # ('/admin/blocks/infoblock/add/', 302),
        # ('/admin/blog/blog/', 302),
        # ('/admin/blog/blog/add/', 302),
        # ('/admin/blog/post/', 302),
        # ('/admin/blog/post/add/', 302),
        # ('/admin/bookmarks/bookmark/', 302),
        # ('/admin/bookmarks/bookmark/add/', 302),
        # ('/admin/comments/comment/', 302),
        # ('/admin/comments/comment/add/', 302),
        # ('/admin/comments/moderatordeletion/', 302),
        # ('/admin/comments/moderatordeletion/add/', 302),
        # ('/admin/comments/moderatordeletionreason/', 302),
        # ('/admin/comments/moderatordeletionreason/add/', 302),
        # ('/admin/configuration/sitesettings/', 302),
        # ('/admin/configuration/sitesettings/add/', 302),
        # ('/admin/contact_form/contactformcategory/', 302),
        # ('/admin/contact_form/contactformcategory/add/', 302),
        # ('/admin/djcelery/crontabschedule/', 302),
        # ('/admin/djcelery/crontabschedule/add/', 302),
        # ('/admin/djcelery/intervalschedule/', 302),
        # ('/admin/djcelery/intervalschedule/add/', 302),
        # ('/admin/djcelery/periodictask/', 302),
        # ('/admin/djcelery/periodictask/add/', 302),
        # ('/admin/djcelery/taskstate/', 302),
        # ('/admin/djcelery/taskstate/add/', 302),
        # ('/admin/djcelery/workerstate/', 302),
        # ('/admin/djcelery/workerstate/add/', 302),
        # ('/admin/doc/', 302),
        # ('/admin/doc/bookmarklets/', 302),
        # ('/admin/doc/filters/', 302),
        # ('/admin/doc/models/', 302),
        # ('/admin/doc/tags/', 302),
        # ('/admin/doc/views/', 302),
        # ('/admin/email_campaigns/campaign/', 302),
        # ('/admin/email_campaigns/campaign/add/', 302),
        # ('/admin/email_campaigns/infosubscription/', 302),
        # ('/admin/email_campaigns/infosubscription/add/', 302),
        # ('/admin/email_campaigns/infosubscription/send_mail/', 302),
        # ('/admin/email_campaigns/mailing/', 302),
        # ('/admin/email_campaigns/mailing/add/', 302),
        # ('/admin/email_campaigns/mailinglist/', 302),
        # ('/admin/email_campaigns/mailinglist/add/', 302),
        # ('/admin/events/event/', 302),
        # ('/admin/events/event/add/', 302),
        # ('/admin/events/eventtimelabel/', 302),
        # ('/admin/events/eventtimelabel/add/', 302),
        # ('/admin/events/eventtype/', 302),
        # ('/admin/events/eventtype/add/', 302),
        # ('/admin/external_services/articleimportsource/', 302),
        # ('/admin/external_services/articleimportsource/add/', 302),
        # ('/admin/external_services/objectmapper/', 302),
        # ('/admin/external_services/objectmapper/add/', 302),
        # ('/admin/external_services/service/', 302),
        # ('/admin/external_services/service/add/', 302),
        # ('/admin/external_services/serviceactionlog/', 302),
        # ('/admin/external_services/serviceactionlog/add/', 302),
        # ('/admin/facebook_app/facebookappsettings/', 302),
        # ('/admin/facebook_app/facebookappsettings/add/', 302),
        # ('/admin/faqs/faqcategory/', 302),
        # ('/admin/faqs/faqcategory/add/', 302),
        # ('/admin/faqs/faqcontainer/', 302),
        # ('/admin/faqs/faqcontainer/add/', 302),
        # ('/admin/favorites/favorite/', 302),
        # ('/admin/favorites/favorite/add/', 302),
        # ('/admin/filebrowser/adjust-version/', 302),
        # ('/admin/filebrowser/browse/', 302),
        # ('/admin/filebrowser/delete-version/', 302),
        # ('/admin/filebrowser/delete/', 302),
        # ('/admin/filebrowser/delete_confirm/', 302),
        # ('/admin/filebrowser/detail/', 302),
        # ('/admin/filebrowser/get-version/', 302),
        # ('/admin/filebrowser/upload_file/', 302),
        # ('/admin/filebrowser/version/', 302),
        # ('/admin/filebrowser/versions/', 302),
        # ('/admin/flatpages/flatpage/', 302),
        # ('/admin/flatpages/flatpage/add/', 302),
        # ('/admin/groups_networks/grouptype/', 302),
        # ('/admin/groups_networks/grouptype/add/', 302),
        # ('/admin/groups_networks/persongroup/', 302),
        # ('/admin/groups_networks/persongroup/add/', 302),
        # ('/admin/i18n/area/', 302),
        # ('/admin/i18n/area/add/', 302),
        # ('/admin/i18n/country/', 302),
        # ('/admin/i18n/country/add/', 302),
        # ('/admin/i18n/countrylanguage/', 302),
        # ('/admin/i18n/countrylanguage/add/', 302),
        # ('/admin/i18n/language/', 302),
        # ('/admin/i18n/language/add/', 302),
        # ('/admin/i18n/nationality/', 302),
        # ('/admin/i18n/nationality/add/', 302),
        # ('/admin/i18n/phone/', 302),
        # ('/admin/i18n/phone/add/', 302),
        # ('/admin/i18n/timezone/', 302),
        # ('/admin/i18n/timezone/add/', 302),
        # ('/admin/image_mods/imagecropping/', 302),
        # ('/admin/image_mods/imagecropping/add/', 302),
        # ('/admin/image_mods/imagemodification/', 302),
        # ('/admin/image_mods/imagemodification/add/', 302),
        # ('/admin/image_mods/imagemodificationgroup/', 302),
        # ('/admin/image_mods/imagemodificationgroup/add/', 302),
        # ('/admin/individual_relations/individualrelation/', 302),
        # ('/admin/individual_relations/individualrelation/add/', 302),
        # ('/admin/individual_relations/individualrelationtype/', 302),
        # ('/admin/individual_relations/individualrelationtype/add/', 302),
        # ('/admin/institutions/institution/', 302),
        # ('/admin/institutions/institution/add/', 302),
        # ('/admin/institutions/institution/send_mail/', 302),
        # ('/admin/institutions/institutiontype/', 302),
        # ('/admin/institutions/institutiontype/add/', 302),
        # ('/admin/institutions/legalform/', 302),
        # ('/admin/institutions/legalform/add/', 302),
        # ('/admin/jsi18n/', 302),
        # ('/admin/location/address/', 302),
        # ('/admin/location/address/add/', 302),
        # ('/admin/logout/', 302),
        # ('/admin/mailchimp/campaign/', 302),
        # ('/admin/mailchimp/campaign/add/', 302),
        # ('/admin/mailchimp/mlist/', 302),
        # ('/admin/mailchimp/mlist/add/', 302),
        # ('/admin/mailchimp/settings/', 302),
        # ('/admin/mailchimp/settings/add/', 302),
        # ('/admin/mailchimp/subscription/', 302),
        # ('/admin/mailchimp/subscription/add/', 302),
        # ('/admin/mailing/emailmessage/', 302),
        # ('/admin/mailing/emailmessage/add/', 302),
        # ('/admin/mailing/emailtemplate/', 302),
        # ('/admin/mailing/emailtemplate/add/', 302),
        # ('/admin/mailing/emailtemplateplaceholder/', 302),
        # ('/admin/mailing/emailtemplateplaceholder/add/', 302),
        # ('/admin/marketplace/joboffer/', 302),
        # ('/admin/marketplace/joboffer/add/', 302),
        # ('/admin/marketplace/jobqualification/', 302),
        # ('/admin/marketplace/jobqualification/add/', 302),
        # ('/admin/marketplace/jobsector/', 302),
        # ('/admin/marketplace/jobsector/add/', 302),
        # ('/admin/marketplace/jobtype/', 302),
        # ('/admin/marketplace/jobtype/add/', 302),
        # ('/admin/media_gallery/mediagallery/', 302),
        # ('/admin/media_gallery/mediagallery/add/', 302),
        # ('/admin/media_gallery/portfoliosettings/', 302),
        # ('/admin/media_gallery/portfoliosettings/add/', 302),
        # ('/admin/media_gallery/section/', 302),
        # ('/admin/media_gallery/section/add/', 302),
        # ('/admin/memos/memocollection/', 302),
        # ('/admin/memos/memocollection/add/', 302),
        # ('/admin/messaging/internalmessage/', 302),
        # ('/admin/messaging/internalmessage/add/', 302),
        # ('/admin/navigation/navigationlink/', 302),
        # ('/admin/navigation/navigationlink/add/', 302),
        # ('/admin/notification/digest/', 302),
        # ('/admin/notification/digest/add/', 302),
        # ('/admin/notification/notice/', 302),
        # ('/admin/notification/notice/add/', 302),
        # ('/admin/notification/noticeemailtemplate/', 302),
        # ('/admin/notification/noticeemailtemplate/add/', 302),
        # ('/admin/notification/noticesetting/', 302),
        # ('/admin/notification/noticesetting/add/', 302),
        # ('/admin/notification/noticetype/', 302),
        # ('/admin/notification/noticetype/add/', 302),
        # ('/admin/notification/noticetypecategory/', 302),
        # ('/admin/notification/noticetypecategory/add/', 302),
        # ('/admin/optionset/emailtype/', 302),
        # ('/admin/optionset/emailtype/add/', 302),
        # ('/admin/optionset/imtype/', 302),
        # ('/admin/optionset/imtype/add/', 302),
        # ('/admin/optionset/individuallocationtype/', 302),
        # ('/admin/optionset/individuallocationtype/add/', 302),
        # ('/admin/optionset/institutionallocationtype/', 302),
        # ('/admin/optionset/institutionallocationtype/add/', 302),
        # ('/admin/optionset/phonetype/', 302),
        # ('/admin/optionset/phonetype/add/', 302),
        # ('/admin/optionset/prefix/', 302),
        # ('/admin/optionset/prefix/add/', 302),
        # ('/admin/optionset/salutation/', 302),
        # ('/admin/optionset/salutation/add/', 302),
        # ('/admin/optionset/urltype/', 302),
        # ('/admin/optionset/urltype/add/', 302),
        # ('/admin/password_change/', 302),
        # ('/admin/password_change/done/', 302),
        # ('/admin/people/individualtype/', 302),
        # ('/admin/people/individualtype/add/', 302),
        # ('/admin/people/person/', 302),
        # ('/admin/people/person/add/', 302),
        # ('/admin/people/person/send_mail/', 302),
        # ('/admin/permissions/perobjectgroup/', 302),
        # ('/admin/permissions/perobjectgroup/add/', 302),
        # ('/admin/permissions/rowlevelpermission/', 302),
        # ('/admin/permissions/rowlevelpermission/add/', 302),
        # ('/admin/profanity_filter/swearingcase/', 302),
        # ('/admin/profanity_filter/swearingcase/add/', 302),
        # ('/admin/profanity_filter/swearword/', 302),
        # ('/admin/profanity_filter/swearword/add/', 302),
        # ('/admin/redirects/redirect/', 302),
        # ('/admin/redirects/redirect/add/', 302),
        # ('/admin/resources/document/', 302),
        # ('/admin/resources/document/add/', 302),
        # ('/admin/resources/documenttype/', 302),
        # ('/admin/resources/documenttype/add/', 302),
        # ('/admin/resources/medium/', 302),
        # ('/admin/resources/medium/add/', 302),
        # ('/admin/site_specific/claimrequest/', 302),
        # ('/admin/site_specific/claimrequest/add/', 302),
        # ('/admin/site_specific/contextitem/', 302),
        # ('/admin/site_specific/contextitem/add/', 302),
        # ('/admin/site_specific/visit/', 302),
        # ('/admin/site_specific/visit/add/', 302),
        # ('/admin/sites/site/', 302),
        # ('/admin/sites/site/add/', 302),
        # ('/admin/slideshows/slideshow/', 302),
        # ('/admin/slideshows/slideshow/add/', 302),
        # ('/admin/structure/contextcategory/', 302),
        # ('/admin/structure/contextcategory/add/', 302),
        # ('/admin/structure/term/', 302),
        # ('/admin/structure/term/add/', 302),
        # ('/admin/structure/vocabulary/', 302),
        # ('/admin/structure/vocabulary/add/', 302),
        # ('/admin/tagging/tag/', 302),
        # ('/admin/tagging/tag/add/', 302),
        # ('/admin/tagging/taggeditem/', 302),
        # ('/admin/tagging/taggeditem/add/', 302),
        # ('/admin/templates/', 302),
        # ('/admin/tracker/concern/', 302),
        # ('/admin/tracker/concern/add/', 302),
        # ('/admin/tracker/ticket/', 302),
        # ('/admin/tracker/ticket/add/', 302),
        # non-admin top-level URLs
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
        ('/sitemap.xml', 301),
        ('/styleguide/', 301),
        ('/styleguide/colors/', 301),
        ('/styleguide/forms/', 301),
        ('/styleguide/grid/', 301),
        ('/styleguide/images/', 301),
        ('/styleguide/typography/', 301),
        ('/subscribe4info/', 301),
        ('/subscribe4info/done/', 301),
        ('/tagging_autocomplete/list', 200),
        ('/ticket/', 301),
        ('/tweets/', 301),
        # German URLs
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
        # ('/de/sitemap.xml', 200), # TODO reenable this test, currently disabled due to being very slow
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

    suite = unittest.TestSuite()
    # suite.addTests(OpenPage(url_path) for url_path in constant_urls)
    suite.addTests(
        PageTest(url_path, expected_status_code) for url_path, expected_status_code in constant_urls
    )
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())


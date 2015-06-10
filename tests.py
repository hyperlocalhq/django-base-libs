from django.test.utils import setup_test_environment
from django.test import Client
import unittest

class OpenPage(unittest.TestCase):
    def __init__(self, url_path='', expected_status_code=200):
        # print 'initing with {}'.format(url_path)
        super(OpenPage, self).__init__()
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
        response = self.client.get(self.url_path)
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
        ('/', 200),
        ('/account/', 200),
        # ('/admin/', 200)
        # ('/admin/articles/article/', 200)
        # ('/admin/articles/article/add/', 200)
        # ('/admin/articles/articlecontentprovider/', 200)
        # ('/admin/articles/articlecontentprovider/add/', 200)
        # ('/admin/articles/articletype/', 200)
        # ('/admin/articles/articletype/add/', 200)
        # ('/admin/auth/group/', 200)
        # ('/admin/auth/group/add/', 200)
        # ('/admin/auth/user/', 200)
        # ('/admin/auth/user/add/', 200)
        # ('/admin/auth/user/send_mail/', 200)
        # ('/admin/blocks/infoblock/', 200)
        # ('/admin/blocks/infoblock/add/', 200)
        # ('/admin/blog/blog/', 200)
        # ('/admin/blog/blog/add/', 200)
        # ('/admin/blog/post/', 200)
        # ('/admin/blog/post/add/', 200)
        # ('/admin/bookmarks/bookmark/', 200)
        # ('/admin/bookmarks/bookmark/add/', 200)
        # ('/admin/comments/comment/', 200)
        # ('/admin/comments/comment/add/', 200)
        # ('/admin/comments/moderatordeletion/', 200)
        # ('/admin/comments/moderatordeletion/add/', 200)
        # ('/admin/comments/moderatordeletionreason/', 200)
        # ('/admin/comments/moderatordeletionreason/add/', 200)
        # ('/admin/configuration/sitesettings/', 200)
        # ('/admin/configuration/sitesettings/add/', 200)
        # ('/admin/contact_form/contactformcategory/', 200)
        # ('/admin/contact_form/contactformcategory/add/', 200)
        # ('/admin/djcelery/crontabschedule/', 200)
        # ('/admin/djcelery/crontabschedule/add/', 200)
        # ('/admin/djcelery/intervalschedule/', 200)
        # ('/admin/djcelery/intervalschedule/add/', 200)
        # ('/admin/djcelery/periodictask/', 200)
        # ('/admin/djcelery/periodictask/add/', 200)
        # ('/admin/djcelery/taskstate/', 200)
        # ('/admin/djcelery/taskstate/add/', 200)
        # ('/admin/djcelery/workerstate/', 200)
        # ('/admin/djcelery/workerstate/add/', 200)
        # ('/admin/doc/', 200)
        # ('/admin/doc/bookmarklets/', 200)
        # ('/admin/doc/filters/', 200)
        # ('/admin/doc/models/', 200)
        # ('/admin/doc/tags/', 200)
        # ('/admin/doc/views/', 200)
        # ('/admin/email_campaigns/campaign/', 200)
        # ('/admin/email_campaigns/campaign/add/', 200)
        # ('/admin/email_campaigns/infosubscription/', 200)
        # ('/admin/email_campaigns/infosubscription/add/', 200)
        # ('/admin/email_campaigns/infosubscription/send_mail/', 200)
        # ('/admin/email_campaigns/mailing/', 200)
        # ('/admin/email_campaigns/mailing/add/', 200)
        # ('/admin/email_campaigns/mailinglist/', 200)
        # ('/admin/email_campaigns/mailinglist/add/', 200)
        # ('/admin/events/event/', 200)
        # ('/admin/events/event/add/', 200)
        # ('/admin/events/eventtimelabel/', 200)
        # ('/admin/events/eventtimelabel/add/', 200)
        # ('/admin/events/eventtype/', 200)
        # ('/admin/events/eventtype/add/', 200)
        # ('/admin/external_services/articleimportsource/', 200)
        # ('/admin/external_services/articleimportsource/add/', 200)
        # ('/admin/external_services/objectmapper/', 200)
        # ('/admin/external_services/objectmapper/add/', 200)
        # ('/admin/external_services/service/', 200)
        # ('/admin/external_services/service/add/', 200)
        # ('/admin/external_services/serviceactionlog/', 200)
        # ('/admin/external_services/serviceactionlog/add/', 200)
        # ('/admin/facebook_app/facebookappsettings/', 200)
        # ('/admin/facebook_app/facebookappsettings/add/', 200)
        # ('/admin/faqs/faqcategory/', 200)
        # ('/admin/faqs/faqcategory/add/', 200)
        # ('/admin/faqs/faqcontainer/', 200)
        # ('/admin/faqs/faqcontainer/add/', 200)
        # ('/admin/favorites/favorite/', 200)
        # ('/admin/favorites/favorite/add/', 200)
        # ('/admin/filebrowser/adjust-version/', 200)
        # ('/admin/filebrowser/browse/', 200)
        # ('/admin/filebrowser/delete-version/', 200)
        # ('/admin/filebrowser/delete/', 200)
        # ('/admin/filebrowser/delete_confirm/', 200)
        # ('/admin/filebrowser/detail/', 200)
        # ('/admin/filebrowser/get-version/', 200)
        # ('/admin/filebrowser/upload_file/', 200)
        # ('/admin/filebrowser/version/', 200)
        # ('/admin/filebrowser/versions/', 200)
        # ('/admin/flatpages/flatpage/', 200)
        # ('/admin/flatpages/flatpage/add/', 200)
        # ('/admin/groups_networks/grouptype/', 200)
        # ('/admin/groups_networks/grouptype/add/', 200)
        # ('/admin/groups_networks/persongroup/', 200)
        # ('/admin/groups_networks/persongroup/add/', 200)
        # ('/admin/i18n/area/', 200)
        # ('/admin/i18n/area/add/', 200)
        # ('/admin/i18n/country/', 200)
        # ('/admin/i18n/country/add/', 200)
        # ('/admin/i18n/countrylanguage/', 200)
        # ('/admin/i18n/countrylanguage/add/', 200)
        # ('/admin/i18n/language/', 200)
        # ('/admin/i18n/language/add/', 200)
        # ('/admin/i18n/nationality/', 200)
        # ('/admin/i18n/nationality/add/', 200)
        # ('/admin/i18n/phone/', 200)
        # ('/admin/i18n/phone/add/', 200)
        # ('/admin/i18n/timezone/', 200)
        # ('/admin/i18n/timezone/add/', 200)
        # ('/admin/image_mods/imagecropping/', 200)
        # ('/admin/image_mods/imagecropping/add/', 200)
        # ('/admin/image_mods/imagemodification/', 200)
        # ('/admin/image_mods/imagemodification/add/', 200)
        # ('/admin/image_mods/imagemodificationgroup/', 200)
        # ('/admin/image_mods/imagemodificationgroup/add/', 200)
        # ('/admin/individual_relations/individualrelation/', 200)
        # ('/admin/individual_relations/individualrelation/add/', 200)
        # ('/admin/individual_relations/individualrelationtype/', 200)
        # ('/admin/individual_relations/individualrelationtype/add/', 200)
        # ('/admin/institutions/institution/', 200)
        # ('/admin/institutions/institution/add/', 200)
        # ('/admin/institutions/institution/send_mail/', 200)
        # ('/admin/institutions/institutiontype/', 200)
        # ('/admin/institutions/institutiontype/add/', 200)
        # ('/admin/institutions/legalform/', 200)
        # ('/admin/institutions/legalform/add/', 200)
        # ('/admin/jsi18n/', 200)
        # ('/admin/location/address/', 200)
        # ('/admin/location/address/add/', 200)
        # ('/admin/logout/', 200)
        # ('/admin/mailchimp/campaign/', 200)
        # ('/admin/mailchimp/campaign/add/', 200)
        # ('/admin/mailchimp/mlist/', 200)
        # ('/admin/mailchimp/mlist/add/', 200)
        # ('/admin/mailchimp/settings/', 200)
        # ('/admin/mailchimp/settings/add/', 200)
        # ('/admin/mailchimp/subscription/', 200)
        # ('/admin/mailchimp/subscription/add/', 200)
        # ('/admin/mailing/emailmessage/', 200)
        # ('/admin/mailing/emailmessage/add/', 200)
        # ('/admin/mailing/emailtemplate/', 200)
        # ('/admin/mailing/emailtemplate/add/', 200)
        # ('/admin/mailing/emailtemplateplaceholder/', 200)
        # ('/admin/mailing/emailtemplateplaceholder/add/', 200)
        # ('/admin/marketplace/joboffer/', 200)
        # ('/admin/marketplace/joboffer/add/', 200)
        # ('/admin/marketplace/jobqualification/', 200)
        # ('/admin/marketplace/jobqualification/add/', 200)
        # ('/admin/marketplace/jobsector/', 200)
        # ('/admin/marketplace/jobsector/add/', 200)
        # ('/admin/marketplace/jobtype/', 200)
        # ('/admin/marketplace/jobtype/add/', 200)
        # ('/admin/media_gallery/mediagallery/', 200)
        # ('/admin/media_gallery/mediagallery/add/', 200)
        # ('/admin/media_gallery/portfoliosettings/', 200)
        # ('/admin/media_gallery/portfoliosettings/add/', 200)
        # ('/admin/media_gallery/section/', 200)
        # ('/admin/media_gallery/section/add/', 200)
        # ('/admin/memos/memocollection/', 200)
        # ('/admin/memos/memocollection/add/', 200)
        # ('/admin/messaging/internalmessage/', 200)
        # ('/admin/messaging/internalmessage/add/', 200)
        # ('/admin/navigation/navigationlink/', 200)
        # ('/admin/navigation/navigationlink/add/', 200)
        # ('/admin/notification/digest/', 200)
        # ('/admin/notification/digest/add/', 200)
        # ('/admin/notification/notice/', 200)
        # ('/admin/notification/notice/add/', 200)
        # ('/admin/notification/noticeemailtemplate/', 200)
        # ('/admin/notification/noticeemailtemplate/add/', 200)
        # ('/admin/notification/noticesetting/', 200)
        # ('/admin/notification/noticesetting/add/', 200)
        # ('/admin/notification/noticetype/', 200)
        # ('/admin/notification/noticetype/add/', 200)
        # ('/admin/notification/noticetypecategory/', 200)
        # ('/admin/notification/noticetypecategory/add/', 200)
        # ('/admin/optionset/emailtype/', 200)
        # ('/admin/optionset/emailtype/add/', 200)
        # ('/admin/optionset/imtype/', 200)
        # ('/admin/optionset/imtype/add/', 200)
        # ('/admin/optionset/individuallocationtype/', 200)
        # ('/admin/optionset/individuallocationtype/add/', 200)
        # ('/admin/optionset/institutionallocationtype/', 200)
        # ('/admin/optionset/institutionallocationtype/add/', 200)
        # ('/admin/optionset/phonetype/', 200)
        # ('/admin/optionset/phonetype/add/', 200)
        # ('/admin/optionset/prefix/', 200)
        # ('/admin/optionset/prefix/add/', 200)
        # ('/admin/optionset/salutation/', 200)
        # ('/admin/optionset/salutation/add/', 200)
        # ('/admin/optionset/urltype/', 200)
        # ('/admin/optionset/urltype/add/', 200)
        # ('/admin/password_change/', 200)
        # ('/admin/password_change/done/', 200)
        # ('/admin/people/individualtype/', 200)
        # ('/admin/people/individualtype/add/', 200)
        # ('/admin/people/person/', 200)
        # ('/admin/people/person/add/', 200)
        # ('/admin/people/person/send_mail/', 200)
        # ('/admin/permissions/perobjectgroup/', 200)
        # ('/admin/permissions/perobjectgroup/add/', 200)
        # ('/admin/permissions/rowlevelpermission/', 200)
        # ('/admin/permissions/rowlevelpermission/add/', 200)
        # ('/admin/profanity_filter/swearingcase/', 200)
        # ('/admin/profanity_filter/swearingcase/add/', 200)
        # ('/admin/profanity_filter/swearword/', 200)
        # ('/admin/profanity_filter/swearword/add/', 200)
        # ('/admin/redirects/redirect/', 200)
        # ('/admin/redirects/redirect/add/', 200)
        # ('/admin/resources/document/', 200)
        # ('/admin/resources/document/add/', 200)
        # ('/admin/resources/documenttype/', 200)
        # ('/admin/resources/documenttype/add/', 200)
        # ('/admin/resources/medium/', 200)
        # ('/admin/resources/medium/add/', 200)
        # ('/admin/site_specific/claimrequest/', 200)
        # ('/admin/site_specific/claimrequest/add/', 200)
        # ('/admin/site_specific/contextitem/', 200)
        # ('/admin/site_specific/contextitem/add/', 200)
        # ('/admin/site_specific/visit/', 200)
        # ('/admin/site_specific/visit/add/', 200)
        # ('/admin/sites/site/', 200)
        # ('/admin/sites/site/add/', 200)
        # ('/admin/slideshows/slideshow/', 200)
        # ('/admin/slideshows/slideshow/add/', 200)
        # ('/admin/structure/contextcategory/', 200)
        # ('/admin/structure/contextcategory/add/', 200)
        # ('/admin/structure/term/', 200)
        # ('/admin/structure/term/add/', 200)
        # ('/admin/structure/vocabulary/', 200)
        # ('/admin/structure/vocabulary/add/', 200)
        # ('/admin/tagging/tag/', 200)
        # ('/admin/tagging/tag/add/', 200)
        # ('/admin/tagging/taggeditem/', 200)
        # ('/admin/tagging/taggeditem/add/', 200)
        # ('/admin/templates/', 200)
        # ('/admin/tracker/concern/', 200)
        # ('/admin/tracker/concern/add/', 200)
        # ('/admin/tracker/ticket/', 200)
        # ('/admin/tracker/ticket/add/', 200)
        ('/compatibility/', 200),
        ('/contact/', 200),
        ('/contact/alldone/', 200),
        ('/creative-sector/', 302),
        ('/dashboard/', 302),
        ('/documents/', 200),
        ('/events/add/', 302),
        ('/facebook/', 200),
        ('/facebook/data-exchange/', 302),
        ('/facebook/link/', 200),
        ('/facebook/link/login/', 200),
        ('/facebook/link/register/', 200),
        ('/facebook/manage/', 302),
        ('/facebook/pages/', 302),
        ('/gmap/', 200),
        ('/groups/', 200),
        ('/groups/add/', 302),
        ('/groups/invitations/', 302),
        ('/helper/blank_doc/', 200),
        ('/helper/bookmark/', 200),
        ('/helper/country_lookup/', 200),
        ('/helper/institution_lookup/', 302),
        ('/helper/person_lookup/', 302),
        ('/helper/site-visitors/', 200),
        ('/i18n/setlang/', 302),
        ('/institutions/', 200),
        ('/institutions/add/', 302),
        ('/invite/', 302),
        ('/invite/done/', 200),
        ('/jobs/add/', 302),
        ('/jobs/create-berlin-jobboard/', 200),
        ('/jobs/talent-in-berlin/', 200),
        ('/jsi18n/', 200),
        ('/jssettings/', 200),
        ('/kreativarbeiten/', 200),
        ('/kreativarbeiten/best-practice/', 200),
        ('/kreativarbeiten/blog/', 200),
        ('/kreativarbeiten/blog/all/', 200),
        ('/kreativarbeiten/blog/drafts/', 200),
        ('/kreativarbeiten/contact/', 200),
        ('/kreativarbeiten/contact/done/', 200),
        ('/kreativarbeiten/newsfeed/', 200),
        ('/kreativarbeiten/tweets/', 200),
        ('/lists/', 200),
        ('/livestream/', 200),
        ('/login', 200),
        ('/logout', 302),
        ('/map/', 200),
        ('/map/object-list/', 200),
        ('/my-messages/json/', 200),
        ('/my-messages/new/', 302),
        ('/my-profile/', 302),
        ('/my-profile/bookmarks/', 200),
        ('/my-profile/delete/', 302),
        ('/my-profile/delete/done/', 200),
        ('/my-profile/favorites/', 200),
        ('/my-profile/memos/', 200),
        ('/my-profile/privacy/', 302),
        ('/news/', 200),
        ('/news/articles/', 200),
        ('/news/interviews/', 200),
        ('/notification/', 302),
        ('/notification/feed/', 200),
        ('/notification/mark_all_seen/', 302),
        ('/notification/settings/', 302),
        ('/password_change/', 302),
        ('/password_change/done/', 200),
        ('/password_reset/', 200),
        ('/password_reset/complete/', 200),
        ('/password_reset/done/', 200),
        ('/people/', 200),
        ('/recrop/', 200),
        ('/register/', 200),
        ('/register/alldone/', 302),
        ('/register/done/', 200),
        ('/rosetta/', 302),
        ('/rosetta/download/', 302),
        ('/rosetta/pick/', 302),
        ('/search/', 200),
        ('/search/full/', 200),
        ('/simplesearch/', 200),
        ('/sitemap.xml', 200),
        ('/styleguide/', 200),
        ('/styleguide/colors/', 200),
        ('/styleguide/forms/', 200),
        ('/styleguide/grid/', 200),
        ('/styleguide/images/', 200),
        ('/styleguide/typography/', 200),
        ('/subscribe4info/', 200),
        ('/subscribe4info/done/', 200),
        ('/tagging_autocomplete/list', 200),
        ('/ticket/', 200),
        ('/tweets/', 200),
    )

    suite = unittest.TestSuite()
    # suite.addTests(OpenPage(url_path) for url_path in constant_urls)
    suite.addTests(
        OpenPage('/de' + url_path, expected_status_code) for url_path, expected_status_code in constant_urls
    )
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())


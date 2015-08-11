#! /usr/bin/env sh
set -eu

## Make sure the following tables do not exist before doing a dump:
# drop table email_campaigns_campaign;
# drop table email_campaigns_infosubscription;
# drop table email_campaigns_mailing;
# drop table email_campaigns_mailinglist;
# drop table email_campaigns_mailing_mailinglists;
# drop table email_campaigns_mailingcontentblock;
# drop table events_event_creative_industries;
# drop table filebrowser_file;
# drop table filebrowser_imagemodification;
# drop table forum_forum;
# drop table forum_forumcategory;
# drop table forum_forumcontainer;
# drop table forum_forumcontainer_sites;
# drop table forum_forumreply;
# drop table forum_forumthread;
# drop table forum_moderatordeletion;
# drop table forum_moderatordeletionreason;
# drop table forum_post;
# drop table forum_thread;
# drop table forum_threadcategory;
# drop table generic_bookmark;
# drop table grappelli_bookmark;
# drop table grappelli_bookmarkitem;
# drop table grappelli_help;
# drop table grappelli_helpitem;
# drop table grappelli_navigation;
# drop table grappelli_navigationitem;
# drop table grappelli_navigationitem_groups;
# drop table grappelli_navigationitem_users;
# drop table institutions_institution_creative_industries;
# drop table jovoto_idea;
# drop table new_articles_newarticle;
# drop table people_person_creative_industries;
# drop table rating_userrating;
# drop table recommendations_recommendation;
# drop table resources_document_document_types;
# drop table south_migrationhistory;
# drop table system_contextitem_creative_industries;
# drop table tagging_synonym;
mysqldump -u root -p --complete-insert --replace --no-create-info  -R --triggers ccb > ccb_data.sql

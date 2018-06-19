#! /usr/bin/env sh
set -eu

while read app; do
    echo $app
    ./manage.py dumpdata --indent=4 --natural-foreign $app > $app.json
done << EOM
babeldjango
captcha
articles
celerytest
events
external_services
facebook_app
faqs
favorites
groups_networks
institutions
marketplace
media_gallery
people
resources
search
site_specific
slideshows
tracker
crispy_forms
admin
auth
contenttypes
messages
redirects
sessions
sitemaps
sites
staticfiles
djcelery
filebrowser
grappelli
haystack
blocks
blog
bookmarks
comments
compress_jetson
configuration
contact_form
extendedadmin
flatpages
history
httpstate
i18n
image_mods
individual_relations
location
mailchimp
mailing
memos
messaging
navigation
notification
optionset
permissions
profanity_filter
structure
utils
mptt
picklefield
pipeline
rosetta
tagging
tagging_autocomplete
uni_form
EOM

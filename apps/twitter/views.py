import re
import calendar
from datetime import datetime
from dateutil.parser import parse as datetime_parse
from urllib2 import urlopen, HTTPError, URLError

from django.conf import settings
from django.http import HttpResponse
from django.utils.html import urlize
from django.utils import dateformat
from django.utils import simplejson as json
from django.views.decorators.cache import cache_page
from django.template.defaultfilters import timesince
from django.utils.translation import ugettext_lazy as _, ugettext

def latest_tweets(request, twitter_username, number_of_tweets):
    try:
        url = urlopen('https://api.twitter.com/1/statuses/user_timeline.json?include_entities=true&include_rts=true&screen_name=' + twitter_username + '&count=' + str(number_of_tweets))
        json_string = url.read()
    except (HTTPError, URLError):
        json_string = ""
    try:
        tweets = json.loads(json_string)
    except ValueError:
        tweets = []
    for tweet in tweets:
        tweet['text_urlized'] = urlize(tweet['text'])
        tmp = []
        username_re = re.compile(r'@([\w\d_]+)(.*)')
        for word in re.split(re.compile(r'\s+'), tweet['text_urlized']):
            match = username_re.match(word)
            if match:
                word = '<a href="http://twitter.com/' + match.group(1) + '">@' + match.group(1) + '</a>' + match.group(2)
            tmp.append(word)
        tweet['text_urlized_atlinked'] = ' '.join(tmp)
        tweet['created_at_formatted'] = dateformat.format(datetime_parse(tweet['created_at']), 'd.m.Y H:i')
        tweet['created_timesince'] = ugettext("%s ago") % timesince(datetime_parse(tweet['created_at']))
    # cache the response only if tweets were retrieved
    f = lambda request: HttpResponse(json.dumps(tweets), mimetype="application/json")
    if tweets:
        return cache_page(f, 60*15)(request)
    return f(request)

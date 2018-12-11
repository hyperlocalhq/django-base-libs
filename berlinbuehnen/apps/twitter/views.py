import json
import re
from dateutil.parser import parse as datetime_parse
from twython import Twython, TwythonError

from django.conf import settings
from django.http import HttpResponse
from django.utils.html import urlize
from django.utils import dateformat
from django.views.decorators.cache import cache_page
from django.template.defaultfilters import timesince
from django.utils.translation import ugettext


@cache_page(60*15)
def latest_tweets(request, twitter_username, number_of_tweets):
    twitter = Twython(
        settings.TWITTER_CONSUMER_KEY,
        settings.TWITTER_CONSUMER_SECRET,
        settings.TWITTER_ACCESS_TOKEN,
        settings.TWITTER_ACCESS_TOKEN_SECRET,
        )
    try:
        tweets = twitter.get_user_timeline(
            include_entities="true",
            include_rts="true",
            screen_name=twitter_username,
            count=number_of_tweets,
        )
    except TwythonError:
        return HttpResponse(json.dumps([]), content_type="application/json")
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
        
    return HttpResponse(json.dumps(tweets), content_type="application/json")


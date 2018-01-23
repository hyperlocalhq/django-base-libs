# -*- coding: UTF-8 -*-
from django.core.management.base import BaseCommand
from django.db import models
from django.conf import settings
from django.core.management import call_command
from optparse import make_option

SILENT, NORMAL, VERBOSE = 0, 1, 2

class Command(BaseCommand):
    help = "imports tweets"
    def handle(self, *args, **options):
        print "This command is outdated. Use stream_tweets instead."

        from twython import Twython
        from datetime import timedelta
        from dateutil.parser import parse as parse_datetime
        from pprint import pprint
        from django.utils.encoding import force_unicode
        from django.utils.encoding import smart_str
        verbosity = int(options.get('verbosity', NORMAL))
        SearchSettings = models.get_model("twitterwall", "SearchSettings")
        UserTimelineSettings = models.get_model("twitterwall", "UserTimelineSettings")
        TwitterUser = models.get_model("twitterwall", "TwitterUser")
        Tweet = models.get_model("twitterwall", "Tweet")

        def format_html(text, entities):
            html = text
            for hashtag_dict in entities.get('hashtags', []):
                html = html.replace(
                    "#%s" % hashtag_dict['text'],
                    '<span class="hashtag">#%s</span>' % hashtag_dict['text'],
                )
            for user_dict in entities.get('user_mentions', []):
                html = html.replace(
                    "@%s" % user_dict['screen_name'],
                    '<a href="http://twitter.com/%(screen_name)s/" target="_blank" title="%(name)s" class="twitter_user">@%(screen_name)s</a>' % user_dict,
                )
            for media_dict in entities.get('media', []):
                html = html.replace(
                    media_dict['url'],
                    '<a href="%(expanded_url)s" target="_blank" class="media">%(display_url)s</a>' % media_dict
                )
            for url_dict in entities.get('urls', []):
                html = html.replace(
                    url_dict['url'],
                    '<a href="%(expanded_url)s" target="_blank">%(display_url)s</a>' % url_dict
                )
            return html

        twitter = Twython(
            settings.TWITTER_CONSUMER_KEY,
            settings.TWITTER_CONSUMER_SECRET,
            settings.TWITTER_ACCESS_TOKEN,
            settings.TWITTER_ACCESS_TOKEN_SECRET,
        )

        ### import tweets by search ###
        last_tweets = Tweet.objects.filter(from_search=True).order_by('-id')
        params = {
            'result_type': "recent",
            'count': 100,
            'include_entities': "true",
        }
        if last_tweets:
            params['since_id'] = last_tweets[0].id
        
        for ss in SearchSettings.objects.all():
            
            params['q'] = smart_str(ss.query)
            
            search_results = twitter.search(**params)
            while search_results.get('statuses', []):
                # save search results
                for tweet_dict in search_results['statuses']:
                    try:
                        twitter_user = TwitterUser.objects.get(
                            id=tweet_dict['user']['id_str'],
                        )
                    except:
                        twitter_user = TwitterUser(
                            id=tweet_dict['user']['id_str'],
                        )
                    twitter_user.id_str = tweet_dict['user']['id_str']
                    twitter_user.screen_name = tweet_dict['user']['screen_name']
                    twitter_user.name = tweet_dict['user']['name']
                    twitter_user.profile_image_url = tweet_dict['user']['profile_image_url']
                    twitter_user.language = tweet_dict['metadata']['iso_language_code']
                    twitter_user.save()

                    try:
                        tweet = Tweet.objects.get(
                            id=tweet_dict['id']
                        )
                    except:
                        tweet = Tweet(
                            id=tweet_dict['id']
                        )
                        tweet.id_str = tweet_dict['id_str']
                        tweet.user = twitter_user
                        tweet.creation_date = parse_datetime(
                            tweet_dict['created_at'],
                            ignoretz=True,
                        ) + timedelta(hours=2)  # Berlin time
                        tweet.text = tweet_dict['text']
                        tweet.html = format_html(tweet.text, tweet_dict.get('entities', {}))
                        geo = tweet_dict.get('geo', None)
                        if geo and geo.get('type', "") == "Point":
                            tweet.latitude = geo['coordinates'][0]
                            tweet.longitude = geo['coordinates'][1]
                        tweet.from_search = True
                        try:
                            tweet.save()
                        except:
                            tweet.text = force_unicode(tweet.text.encode("ascii", "xmlcharrefreplace"))
                            tweet.html = force_unicode(tweet.html.encode("ascii", "xmlcharrefreplace"))
                            tweet.save()
                        for media_dict in tweet_dict.get('entities', {}).get('media', []):
                            tweet.tweetmedia_set.create(
                                media_url=media_dict['media_url'],
                            )
                    else:
                        tweet.from_search = True
                        tweet.save()
                        
                if verbosity == 2:
                    pprint(search_results)

                # load next page results
                max_id = search_results['search_metadata']['max_id']
                if max_id:
                    params['since_id'] = max_id
                    search_results = twitter.search(**params)
                else:
                    search_results = {}
            

        ### import tweets by users ###
        last_tweets = Tweet.objects.filter(by_user=True).order_by('-id')
        params = {
            'count': 200,
            'include_entities': "true",
        }
        if last_tweets:
            params['since_id'] = last_tweets[0].id
            
        for uts in UserTimelineSettings.objects.all():
            params['screen_name'] = uts.screen_name
            params['include_rts'] = 'true'
            params['exclude_replies'] = 'true'

            user_timeline = twitter.get_user_timeline(**params)
            # save search results
            for tweet_dict in user_timeline:
                try:
                    twitter_user = TwitterUser.objects.get(
                        id=tweet_dict['user']['id'],
                    )
                except:
                    twitter_user = TwitterUser(
                        id=tweet_dict['user']['id'],
                    )
                twitter_user.id_str = tweet_dict['user']['id_str']
                twitter_user.screen_name = tweet_dict['user']['screen_name']
                twitter_user.name = tweet_dict['user']['name']
                twitter_user.profile_image_url = tweet_dict['user']['profile_image_url']
                twitter_user.language = tweet_dict['user']['lang']
                twitter_user.location = tweet_dict['user']['location']
                twitter_user.url = tweet_dict['user']['url']
                twitter_user.description = tweet_dict['user']['description']
                twitter_user.save()
                
                try:
                    tweet = Tweet.objects.get(
                        id=tweet_dict['id']
                    )
                except:
                    tweet = Tweet(
                        id=tweet_dict['id']
                    )
                    tweet.id_str = tweet_dict['id_str']
                    tweet.user = twitter_user
                    tweet.creation_date = parse_datetime(
                        tweet_dict['created_at'],
                        ignoretz=True,
                    ) + timedelta(hours=2)  # Berlin time
                    tweet.text = tweet_dict['text']
                    tweet.html = format_html(tweet.text, tweet_dict.get('entities', {}))
                    if tweet_dict.get('coordinates', None):
                        tweet.latitude = tweet_dict['coordinates'][0]
                        tweet.longitude = tweet_dict['coordinates'][1]
                    tweet.by_user = True
                    try:
                        tweet.save()
                    except:
                        tweet.text = force_unicode(tweet.text.encode("ascii", "xmlcharrefreplace"))
                        tweet.html = force_unicode(tweet.html.encode("ascii", "xmlcharrefreplace"))
                        tweet.save()
                    for media_dict in tweet_dict.get('entities', {}).get('media', []):
                        tweet.tweetmedia_set.create(
                            media_url=media_dict['media_url'],
                        )
                else:
                    tweet.by_user = True
                    tweet.save()
                
            if verbosity == 2:
                pprint(user_timeline)


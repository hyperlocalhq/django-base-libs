# -*- coding: UTF-8 -*-

import os
from optparse import make_option

from twython import TwythonStreamer, Twython
from ._daemon_command import DaemonCommand

from django.core.management.base import NoArgsCommand
from django.conf import settings
from django.utils.encoding import force_unicode
from django.utils.encoding import smart_str
from django.db import models


class MyStreamer(TwythonStreamer):
    def format_html(self, text, entities):
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

    def set_filter_options(self, follow_query, track_query):
        self._follow_query = follow_query
        self._track_query = track_query

    def is_from_search(self, text):
        # self._track_query is a list of space-separated keywords
        for query in self._track_query:
            success = True
            for keyword in query.split(' '):
                success = success and (keyword in text)
            if success:
                return True
        return False

    def is_by_user(self, screen_name):
        # self._follow_query is a list of twitter screen_names
        return screen_name in self._follow_query

    def on_success(self, data):
        from datetime import timedelta
        from dateutil.parser import parse as parse_datetime
        TwitterUser = models.get_model("twitterwall", "TwitterUser")
        Tweet = models.get_model("twitterwall", "Tweet")

        if 'text' in data:
            # print data['text'].encode('utf-8')
            tweet_dict = data
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
            twitter_user.language = tweet_dict['user']['lang']
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
                tweet.html = self.format_html(tweet.text, tweet_dict.get('entities', {}))
                geo = tweet_dict.get('geo', None)
                if geo and geo.get('type', "") == "Point":
                    tweet.latitude = geo['coordinates'][0]
                    tweet.longitude = geo['coordinates'][1]

                if self.is_from_search(tweet.text):
                    tweet.from_search = True

                if self.is_by_user(twitter_user.screen_name):
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

    def on_error(self, status_code, data):
        print status_code, data


class Command(DaemonCommand):
    requires_model_validation = True
    WORKDIR = '.'
    UMASK = 0
    STDOUT = os.path.join(settings.PATH_TMP, "log/tweets.out")
    STDERR = '/dev/null'
    LOGFILE = os.path.join(settings.PATH_TMP, "log/tweets.log")
    PID_FILE = os.path.join(settings.PATH_TMP, "pid/tweets.pid")
    
    option_list = NoArgsCommand.option_list + (
        make_option('--start', action='store_const', const='start', dest='action',
                    help='Start the daemon'),
        make_option('--stop', action='store_const', const='stop', dest='action',
                    help='Stop the daemon'),
        make_option('--restart', action='store_const', const='restart', dest='action',
                    help='Stop and restart the daemon'),
        make_option('--workdir', action='store', dest='workdir', default=WORKDIR,
            help='Full path of the working directory to which the process should '
            'change on daemon start.'),
        make_option('--umask', action='store', dest='umask', default=UMASK, type="int",
            help='File access creation mask ("umask") to set for the process on '
            'daemon start.'),
        make_option('--pidfile', action='store', dest='pid_file', 
                    default=PID_FILE, help='PID filename.'),
        make_option('--logfile', action='store', dest='log_file',
                    default=LOGFILE, help='Path to log file'),
        make_option('--stdout', action='store', dest='stdout', default=STDOUT,
                    help='Destination to redirect standard out'),
        make_option('--stderr', action='store', dest='stderr', default=STDERR,
                    help='Destination to redirect standard error'),
    )
    
    stream = None
    
    def loop_callback(self):
        
        # Requires Authentication as of Twitter API v1.1
        self.stream = MyStreamer(
            settings.TWITTER_STREAMING_CONSUMER_KEY,
            settings.TWITTER_STREAMING_CONSUMER_SECRET,
            settings.TWITTER_STREAMING_ACCESS_TOKEN,
            settings.TWITTER_STREAMING_ACCESS_TOKEN_SECRET,
        )

        UserTimelineSettings = models.get_model("twitterwall", "UserTimelineSettings")
        SearchSettings = models.get_model("twitterwall", "SearchSettings")

        follow_query = []
        for uts in UserTimelineSettings.objects.all():
            for screen_name in uts.screen_name.split(','):
                follow_query.append(screen_name.strip())

        track_query = []
        for ss in SearchSettings.objects.all():
            for query in ss.query.split(','):
                track_query.append(query.strip())

        self.stream.set_filter_options(
            follow_query=follow_query,
            track_query=track_query,
        )

        # get twitter user ids from screen names
        self.api = Twython(
            settings.TWITTER_STREAMING_CONSUMER_KEY,
            settings.TWITTER_STREAMING_CONSUMER_SECRET,
            settings.TWITTER_STREAMING_ACCESS_TOKEN,
            settings.TWITTER_STREAMING_ACCESS_TOKEN_SECRET,
        )
        user_ids = []
        if follow_query:
            for user_dict in self.api.lookup_user(screen_name=smart_str(u",".join(follow_query))):
                user_ids.append(force_unicode(user_dict['id']))

        self.stream.statuses.filter(
            follow=smart_str(u",".join(user_ids)),
            track=smart_str(u",".join(track_query)),
        )
    
    def exit_callback(self):
        if self.stream:
            self.stream.disconnect()

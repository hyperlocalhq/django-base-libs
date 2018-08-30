# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SearchSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('query', models.CharField(help_text=b'\nA comma-separated list of phrases which will be used to determine what Tweets will be delivered on the stream.\nA phrase may be one or more terms separated by spaces, and a phrase will match if all of the terms in the phrase\nare present in the Tweet, regardless of order and ignoring case.\n', max_length=140, verbose_name='Search query')),
            ],
            options={
                'verbose_name': 'Twitter search settings',
                'verbose_name_plural': 'Twitter search settings',
            },
        ),
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.CharField(max_length=20, serialize=False, verbose_name='ID', primary_key=True)),
                ('id_str', models.CharField(help_text='Used in URLs', max_length=20, verbose_name='ID String')),
                ('creation_date', models.DateTimeField(verbose_name='Creation date')),
                ('text', models.TextField(help_text='Text as imported from twitter', verbose_name='Text')),
                ('html', models.TextField(verbose_name='HTML')),
                ('latitude', models.FloatField(help_text='Latitude (Lat.) is the angle between any point and the equator (north pole is at 90; south pole is at -90).', null=True, verbose_name='Latitude', blank=True)),
                ('longitude', models.FloatField(help_text='Longitude (Long.) is the angle east or west of an arbitrary point on Earth from Greenwich (UK), which is the international zero-longitude point (longitude=0 degrees). The anti-meridian of Greenwich is both 180 (direction to east) and -180 (direction to west).', null=True, verbose_name='Longitude', blank=True)),
                ('from_search', models.BooleanField(verbose_name='from search by query')),
                ('by_user', models.BooleanField(verbose_name='by twitter user from user timeline settings')),
                ('status', models.CharField(default=b'published', max_length=20, verbose_name='Status', blank=True, choices=[(b'published', 'Published'), (b'not_listed', 'Not Listed')])),
            ],
            options={
                'ordering': ('-creation_date',),
                'verbose_name': 'Tweet',
                'verbose_name_plural': 'Tweets',
            },
        ),
        migrations.CreateModel(
            name='TweetMedia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('media_url', base_libs.models.fields.URLField(verbose_name='Media URL')),
                ('media_type', models.CharField(default=b'photo', max_length=20, verbose_name='MediaType', choices=[(b'photo', 'Photo')])),
                ('tweet', models.ForeignKey(verbose_name='Tweet', to='twitterwall.Tweet')),
            ],
            options={
                'ordering': ('id',),
                'verbose_name': 'Tweet media',
                'verbose_name_plural': 'Tweet media',
            },
        ),
        migrations.CreateModel(
            name='TwitterUser',
            fields=[
                ('id', models.CharField(max_length=20, serialize=False, verbose_name='ID', primary_key=True)),
                ('id_str', models.CharField(help_text='Used in URLs', max_length=20, verbose_name='ID String')),
                ('screen_name', models.CharField(max_length=20, verbose_name='Screen name')),
                ('name', models.CharField(max_length=20, verbose_name='Name', blank=True)),
                ('location', models.CharField(max_length=100, verbose_name='Location', blank=True)),
                ('profile_image_url', base_libs.models.fields.URLField(max_length=255, verbose_name='Profile image URL')),
                ('url', base_libs.models.fields.URLField(max_length=255, verbose_name='URL', blank=True)),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('language', models.CharField(blank=True, max_length=5, verbose_name='Language', choices=[(b'ar', 'Arabic'), (b'ca', 'Catalan'), (b'da', 'Danish'), (b'nl', 'Dutch'), (b'en', 'English'), (b'fa', 'Farsi'), (b'fil', 'Filipino'), (b'fi', 'Finnish'), (b'fr', 'French'), (b'de', 'German'), (b'he', 'Hebrew'), (b'hi', 'Hindi'), (b'hu', 'Hungarian'), (b'id', 'Indonesian'), (b'it', 'Italian'), (b'ja', 'Japanese'), (b'ko', 'Korean'), (b'msa', 'Malay'), (b'no', 'Norwegian'), (b'pl', 'Polish'), (b'pt', 'Portuguese'), (b'ru', 'Russian'), (b'zh-cn', 'Simplified Chinese'), (b'es', 'Spanish'), (b'sv', 'Swedish'), (b'th', 'Thai'), (b'zh-tw', 'Traditional Chinese'), (b'tr', 'Turkish'), (b'uk', 'Ukrainian'), (b'ur', 'Urdu')])),
            ],
            options={
                'ordering': ('screen_name',),
                'verbose_name': 'Twitter user',
                'verbose_name_plural': 'Twitter users',
            },
        ),
        migrations.CreateModel(
            name='UserTimelineSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('screen_name', models.CharField(max_length=20, verbose_name='Screen name')),
            ],
            options={
                'verbose_name': 'Twitter user timeline settings',
                'verbose_name_plural': 'Twitter user timeline settings',
            },
        ),
        migrations.AddField(
            model_name='tweet',
            name='user',
            field=models.ForeignKey(verbose_name='Twitter user', to='twitterwall.TwitterUser'),
        ),
    ]

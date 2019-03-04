# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_urlconfrevision'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpenGraph',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('og_title', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('og_description', models.TextField(help_text='No HTML and no new lines', verbose_name='Description', blank=True)),
                ('og_image', filebrowser.fields.FileBrowseField(max_length=255, verbose_name='Image', blank=True)),
                ('og_type', models.CharField(default=b'article', max_length=20, verbose_name='Type', choices=[(b'article', b'article'), (b'books.author', b'books.author'), (b'books.book', b'books.book'), (b'books.genre', b'books.genre'), (b'business.business', b'business.business'), (b'fitness.course', b'fitness.course'), (b'game.achievement', b'game.achievement'), (b'music.album', b'music.album'), (b'music.playlist', b'music.playlist'), (b'music.radio_station', b'music.radio_station'), (b'music.song', b'music.song'), (b'place', b'place'), (b'product', b'product'), (b'product.group', b'product.group'), (b'product.item', b'product.item'), (b'profile', b'profile'), (b'restaurant.menu', b'restaurant.menu'), (b'restaurant.menu_item', b'restaurant.menu_item'), (b'restaurant.menu_section', b'restaurant.menu_section'), (b'restaurant.restaurant', b'restaurant.restaurant'), (b'video.episode', b'video.episode'), (b'video.movie', b'video.movie'), (b'video.other', b'video.other'), (b'video.tv_show', b'video.tv_show'), (b'website', b'website')])),
                ('extended_object', models.OneToOneField(editable=False, to='cms.Title')),
                ('public_extension', models.OneToOneField(related_name='draft_extension', null=True, editable=False, to='cms_extensions.OpenGraph')),
            ],
            options={
                'verbose_name': 'Open Graph for Social Sharing',
                'verbose_name_plural': 'Open Graph for Social Sharing',
            },
            bases=(models.Model,),
        ),
    ]

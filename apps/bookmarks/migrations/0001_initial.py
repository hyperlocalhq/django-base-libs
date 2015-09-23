# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('title', models.CharField(max_length=80, verbose_name='title')),
                ('url_path', models.CharField(max_length=255, verbose_name='URL')),
                ('creator', models.ForeignKey(related_name='bookmark_creator', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='creator')),
            ],
            options={
                'ordering': ['creation_date'],
                'verbose_name': 'bookmark',
                'verbose_name_plural': 'bookmarks',
            },
            bases=(models.Model,),
        ),
    ]

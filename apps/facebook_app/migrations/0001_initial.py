# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FacebookAppSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('fb_id', models.BigIntegerField(verbose_name='User ID on Facebook')),
                ('name', models.CharField(max_length=255, verbose_name='Full name')),
                ('profile_url', models.URLField(max_length=255, verbose_name='User Link')),
                ('access_token', models.CharField(max_length=255, verbose_name='Access Token')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Facebook App Settings',
                'verbose_name_plural': 'Facebook App Settings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FacebookPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('fb_id', models.BigIntegerField(verbose_name='Page ID on Facebook')),
                ('name', models.CharField(max_length=255, verbose_name='Full name')),
                ('profile_url', models.URLField(max_length=255, verbose_name='Page Link')),
                ('access_token', models.CharField(max_length=255, verbose_name='Page Access Token')),
                ('institution', models.ForeignKey(to='institutions.Institution')),
                ('owner_settings', models.ForeignKey(to='facebook_app.FacebookAppSettings')),
            ],
            options={
                'verbose_name': 'Facebook Page',
                'verbose_name_plural': 'Facebook Pages',
            },
            bases=(models.Model,),
        ),
    ]

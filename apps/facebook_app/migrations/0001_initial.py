# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
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
            ],
            options={
                'verbose_name': 'Facebook Page',
                'verbose_name_plural': 'Facebook Pages',
            },
            bases=(models.Model,),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactFormCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('title', models.CharField(verbose_name='title', max_length=255, null=True, editable=False)),
                ('recipient_emails', base_libs.models.fields.PlainTextModelField(null=True, verbose_name='Recipient email(s)', blank=True)),
                ('sort_order', models.IntegerField(default=0, verbose_name='Sort order')),
                ('title_de', models.CharField(max_length=255, verbose_name='title')),
                ('title_en', models.CharField(max_length=255, verbose_name='title', blank=True)),
            ],
            options={
                'ordering': ['sort_order', 'title'],
                'verbose_name': 'contact form category',
                'verbose_name_plural': 'contact form categories',
            },
            bases=(models.Model,),
        ),
    ]

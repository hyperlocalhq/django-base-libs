# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('mailing', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                ('auto_answer_template', models.ForeignKey(blank=True, to='mailing.EmailTemplate', help_text='Nothing is sent back to the sender if the template is not selected', null=True, verbose_name='Email template for the automatic answer')),
                ('recipients', models.ManyToManyField(to=settings.AUTH_USER_MODEL, null=True, verbose_name='Recipient(s)', blank=True)),
                ('site', models.ForeignKey(blank=True, to='sites.Site', help_text='Restrict this object only for the selected site', null=True, verbose_name='Site')),
            ],
            options={
                'ordering': ['sort_order', 'title'],
                'verbose_name': 'contact form category',
                'verbose_name_plural': 'contact form categories',
            },
            bases=(models.Model,),
        ),
    ]

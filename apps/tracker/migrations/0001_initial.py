# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Concern',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('title', models.CharField(verbose_name='title', max_length=200, null=True, editable=False)),
                ('sort_order', models.IntegerField(default=0, verbose_name='Sort Order')),
                ('title_de', models.CharField(max_length=200, verbose_name='title')),
                ('title_en', models.CharField(max_length=200, verbose_name='title', blank=True)),
            ],
            options={
                'ordering': ['sort_order'],
                'verbose_name': 'Concern',
                'verbose_name_plural': 'Concerns',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.CharField(default=b'', help_text='Please select the related object.', max_length=255, verbose_name='Related object', blank=True)),
                ('submitted_date', models.DateTimeField(auto_now_add=True, verbose_name='submitted Date')),
                ('modified_date', models.DateTimeField(verbose_name='modified Date', null=True, editable=False, blank=True)),
                ('submitter_name', models.CharField(max_length=80, verbose_name='submitter name')),
                ('submitter_email', models.EmailField(max_length=75, verbose_name='submitter email')),
                ('description', models.TextField(verbose_name='description')),
                ('client_info', models.TextField(verbose_name='client info')),
                ('status', models.IntegerField(default=1, verbose_name='status', choices=[(1, 'Open'), (2, 'Working'), (3, 'Closed'), (4, 'Rejected')])),
                ('priority', models.IntegerField(default=1, verbose_name='priority', choices=[(1, 'Now'), (2, 'Soon'), (3, 'Someday')])),
                ('url', base_libs.models.fields.URLField(max_length=255, null=True, verbose_name="related object's URL", blank=True)),
                ('concern', models.ForeignKey(verbose_name='concern', to='tracker.Concern')),
                ('content_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', help_text='Please select the type (model) for the relation, you want to build.', null=True, verbose_name="Related object's type (model)")),
                ('modifier', models.ForeignKey(related_name='ticket_modifier', verbose_name='modifier', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('submitter', models.ForeignKey(related_name='ticket_submitter', verbose_name='submitter', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-submitted_date',),
                'verbose_name': 'ticket',
                'verbose_name_plural': 'tickets',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TicketModifications',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modified_date', models.DateTimeField(verbose_name='modified Date', editable=False)),
                ('modification', models.TextField(verbose_name='modification')),
                ('status', models.IntegerField(default=1, verbose_name='status', choices=[(1, 'Open'), (2, 'Working'), (3, 'Closed'), (4, 'Rejected')])),
                ('priority', models.IntegerField(default=1, verbose_name='priority', choices=[(1, 'Now'), (2, 'Soon'), (3, 'Someday')])),
                ('modifier', models.ForeignKey(related_name='ticket_modification_modifier', editable=False, to=settings.AUTH_USER_MODEL, verbose_name='modifier')),
                ('ticket', models.ForeignKey(related_name='ticket_modification', verbose_name='ticket', to='tracker.Ticket')),
            ],
            options={
                'ordering': ('modified_date',),
                'verbose_name': 'ticket history',
                'verbose_name_plural': 'ticket history',
            },
            bases=(models.Model,),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import base_libs.models.fields
import tagging_autocomplete.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='JobOffer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('published_from', models.DateTimeField(help_text="If not provided and the status is set to 'published', the entry will be published immediately.", null=True, verbose_name='publishing date', blank=True)),
                ('published_till', models.DateTimeField(help_text="If not provided and the status is set to 'published', the entry will be published forever.", null=True, verbose_name='published until', blank=True)),
                ('status', models.SmallIntegerField(default=0, verbose_name='status', choices=[(0, 'Draft'), (1, 'Published')])),
                ('position', models.CharField(max_length=255, verbose_name='Position')),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('offering_institution_title', models.CharField(max_length=255, verbose_name='Organizer', blank=True)),
                ('contact_person_name', models.CharField(max_length=255, verbose_name='Organizer', blank=True)),
                ('additional_info', models.TextField(verbose_name='Additional Info', blank=True)),
                ('phone0_country', models.CharField(default=b'49', max_length=4, verbose_name='Country Code', blank=True)),
                ('phone0_area', models.CharField(default=b'30', max_length=6, verbose_name='Area Code', blank=True)),
                ('phone0_number', models.CharField(max_length=25, verbose_name='Subscriber Number and Extension', blank=True)),
                ('is_phone0_default', models.BooleanField(default=True, verbose_name='Default?')),
                ('is_phone0_on_hold', models.BooleanField(default=False, verbose_name='On Hold?')),
                ('phone1_country', models.CharField(default=b'49', max_length=4, verbose_name='Country Code', blank=True)),
                ('phone1_area', models.CharField(default=b'30', max_length=6, verbose_name='Area Code', blank=True)),
                ('phone1_number', models.CharField(max_length=25, verbose_name='Subscriber Number and Extension', blank=True)),
                ('is_phone1_default', models.BooleanField(default=False, verbose_name='Default?')),
                ('is_phone1_on_hold', models.BooleanField(default=False, verbose_name='On Hold?')),
                ('phone2_country', models.CharField(default=b'49', max_length=4, verbose_name='Country Code', blank=True)),
                ('phone2_area', models.CharField(max_length=6, verbose_name='Area Code', blank=True)),
                ('phone2_number', models.CharField(max_length=25, verbose_name='Subscriber Number and Extension', blank=True)),
                ('is_phone2_default', models.BooleanField(default=False, verbose_name='Default?')),
                ('is_phone2_on_hold', models.BooleanField(default=False, verbose_name='On Hold?')),
                ('url0_link', base_libs.models.fields.URLField(verbose_name='URL', blank=True)),
                ('is_url0_default', models.BooleanField(default=True, verbose_name='Default?')),
                ('is_url0_on_hold', models.BooleanField(default=False, verbose_name='On Hold?')),
                ('url1_link', base_libs.models.fields.URLField(verbose_name='URL', blank=True)),
                ('is_url1_default', models.BooleanField(default=False, verbose_name='Default?')),
                ('is_url1_on_hold', models.BooleanField(default=False, verbose_name='On Hold?')),
                ('url2_link', base_libs.models.fields.URLField(verbose_name='URL', blank=True)),
                ('is_url2_default', models.BooleanField(default=False, verbose_name='Default?')),
                ('is_url2_on_hold', models.BooleanField(default=False, verbose_name='On Hold?')),
                ('im0_address', models.CharField(max_length=255, verbose_name='Instant Messenger', blank=True)),
                ('is_im0_default', models.BooleanField(default=True, verbose_name='Default?')),
                ('is_im0_on_hold', models.BooleanField(default=False, verbose_name='On Hold?')),
                ('im1_address', models.CharField(max_length=255, verbose_name='Instant Messenger', blank=True)),
                ('is_im1_default', models.BooleanField(default=False, verbose_name='Default?')),
                ('is_im1_on_hold', models.BooleanField(default=False, verbose_name='On Hold?')),
                ('im2_address', models.CharField(max_length=255, verbose_name='Instant Messenger', blank=True)),
                ('is_im2_default', models.BooleanField(default=False, verbose_name='Default?')),
                ('is_im2_on_hold', models.BooleanField(default=False, verbose_name='On Hold?')),
                ('email0_address', models.CharField(max_length=255, verbose_name='Email Address', blank=True)),
                ('is_email0_default', models.BooleanField(default=True, verbose_name='Default?')),
                ('is_email0_on_hold', models.BooleanField(default=False, verbose_name='On Hold?')),
                ('email1_address', models.CharField(max_length=255, verbose_name='Email Address', blank=True)),
                ('is_email1_default', models.BooleanField(default=False, verbose_name='Default?')),
                ('is_email1_on_hold', models.BooleanField(default=False, verbose_name='On Hold?')),
                ('email2_address', models.CharField(max_length=255, verbose_name='Email Address', blank=True)),
                ('is_email2_default', models.BooleanField(default=False, verbose_name='Default?')),
                ('is_email2_on_hold', models.BooleanField(default=False, verbose_name='On Hold?')),
                ('tags', tagging_autocomplete.models.TagAutocompleteField(default=b'', help_text='Separate different tags by comma', max_length=255, verbose_name='tags', blank=True)),
                ('publish_emails', models.BooleanField(default=False, verbose_name='Show email addresses to unregistered visitors?')),
                ('is_commercial', models.BooleanField(default=False, verbose_name='One has to pay to get information about the job')),
                ('talent_in_berlin', models.BooleanField(default=False, verbose_name='Export to www.talent-in-berlin.de')),
                ('author', models.ForeignKey(related_name='joboffer_author', blank=True, to=settings.AUTH_USER_MODEL, help_text='If you do not select an author, you will be the author!', null=True, verbose_name='author')),
            ],
            options={
                'ordering': ['position', 'creation_date'],
                'abstract': False,
                'verbose_name': 'job offer',
                'verbose_name_plural': 'job offers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='JobQualification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('title', base_libs.models.fields.MultilingualCharField(verbose_name='title', max_length=255, null=True, editable=False)),
                ('sort_order', models.IntegerField(default=0, verbose_name='Sort order')),
                ('title_de', models.CharField(max_length=255, verbose_name='title')),
                ('title_en', models.CharField(max_length=255, verbose_name='title', blank=True)),
            ],
            options={
                'ordering': ['sort_order', 'title'],
                'verbose_name': 'qualification',
                'verbose_name_plural': 'qualifications',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='JobSector',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('title', base_libs.models.fields.MultilingualCharField(verbose_name='title', max_length=255, null=True, editable=False)),
                ('sort_order', models.IntegerField(default=0, verbose_name='Sort order')),
                ('title_de', models.CharField(max_length=255, verbose_name='title')),
                ('title_en', models.CharField(max_length=255, verbose_name='title', blank=True)),
            ],
            options={
                'ordering': ['sort_order', 'title'],
                'verbose_name': 'job sector',
                'verbose_name_plural': 'job sectors',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='JobType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('title', base_libs.models.fields.MultilingualCharField(verbose_name='title', max_length=255, null=True, editable=False)),
                ('sort_order', models.IntegerField(default=0, verbose_name='Sort order')),
                ('is_internship', models.BooleanField(default=False, verbose_name='Internship?')),
                ('title_de', models.CharField(max_length=255, verbose_name='title')),
                ('title_en', models.CharField(max_length=255, verbose_name='title', blank=True)),
            ],
            options={
                'ordering': ['sort_order', 'title'],
                'verbose_name': 'job type',
                'verbose_name_plural': 'job types',
            },
            bases=(models.Model,),
        ),
    ]

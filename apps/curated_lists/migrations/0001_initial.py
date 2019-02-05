# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CuratedList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('slug', models.SlugField(max_length=255, verbose_name='Slug for URIs')),
                ('title', models.CharField(verbose_name='Title', max_length=255, null=True, editable=False)),
                ('sort_order', models.IntegerField(default=0, verbose_name='Sort order', blank=True)),
                ('privacy', models.CharField(default=b'public', max_length=20, verbose_name='Privacy', choices=[(b'private', 'Private'), (b'public', 'Public')])),
                ('title_en', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('title_de', models.CharField(max_length=255, verbose_name='Title')),
                ('owner', models.ForeignKey(verbose_name='Owner', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['sort_order'],
                'verbose_name': 'Curated List',
                'verbose_name_plural': 'Curated Lists',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ListItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('object_id', models.CharField(default=b'', help_text='Please select the related object.', max_length=255, verbose_name='Related object', blank=True)),
                ('representation', models.CharField(verbose_name='Representation', max_length=255, null=True, editable=False, blank=True)),
                ('sort_order', models.IntegerField(default=0, verbose_name='Sort order', blank=True)),
                ('representation_en', models.CharField(max_length=255, verbose_name='Representation', blank=True)),
                ('representation_de', models.CharField(max_length=255, verbose_name='Representation', blank=True)),
                ('content_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', help_text='Please select the type (model) for the relation, you want to build.', null=True, verbose_name="Related object's type (model)")),
                ('curated_list', models.ForeignKey(verbose_name='Curated list', to='curated_lists.CuratedList')),
            ],
            options={
                'ordering': ['sort_order'],
                'verbose_name': 'List Item',
                'verbose_name_plural': 'List Items',
            },
            bases=(models.Model,),
        ),
    ]

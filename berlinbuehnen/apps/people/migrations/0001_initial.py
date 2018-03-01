# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorshipType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('title', models.CharField(verbose_name='title', max_length=255, null=True, editable=False)),
                ('sort_order', models.IntegerField(default=0, verbose_name='Sort order')),
                ('title_de', models.CharField(max_length=255, verbose_name='title')),
                ('title_en', models.CharField(max_length=255, verbose_name='title', blank=True)),
            ],
            options={
                'ordering': ['sort_order'],
                'verbose_name': 'Authorship type',
                'verbose_name_plural': 'Authorship types',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InvolvementType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('title', models.CharField(verbose_name='title', max_length=255, null=True, editable=False)),
                ('sort_order', models.IntegerField(default=0, verbose_name='Sort order')),
                ('title_de', models.CharField(max_length=255, verbose_name='title')),
                ('title_en', models.CharField(max_length=255, verbose_name='title', blank=True)),
            ],
            options={
                'ordering': ['sort_order'],
                'verbose_name': 'Involvement type',
                'verbose_name_plural': 'Involvement types',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('first_name', models.CharField(max_length=255, verbose_name='First name', blank=True)),
                ('last_name', models.CharField(max_length=255, verbose_name='Last name', blank=True)),
                ('status', models.CharField(default=b'draft', max_length=20, verbose_name='Status', blank=True, choices=[(b'draft', 'Draft'), (b'published', 'Published'), (b'not_listed', 'Not Listed'), (b'import', 'Imported'), (b'trashed', 'Trashed')])),
                ('creator', models.ForeignKey(related_name='person_creator', on_delete=django.db.models.deletion.SET_NULL, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='creator')),
                ('modifier', models.ForeignKey(related_name='person_modifier', on_delete=django.db.models.deletion.SET_NULL, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='modifier')),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
                'verbose_name': 'person',
                'verbose_name_plural': 'people',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Prefix',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('title', models.CharField(verbose_name='title', max_length=255, null=True, editable=False)),
                ('sort_order', models.IntegerField(default=0, verbose_name='Sort order')),
                ('gender', models.CharField(blank=True, max_length=32, verbose_name='Gender', choices=[(b'M', 'Male'), (b'F', 'Female')])),
                ('title_de', models.CharField(max_length=255, verbose_name='title')),
                ('title_en', models.CharField(max_length=255, verbose_name='title', blank=True)),
            ],
            options={
                'ordering': ['sort_order'],
                'verbose_name': 'Prefix',
                'verbose_name_plural': 'Prefixes',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='person',
            name='prefix',
            field=models.ForeignKey(verbose_name='Prefix', blank=True, to='people.Prefix', null=True),
            preserve_default=True,
        ),
    ]

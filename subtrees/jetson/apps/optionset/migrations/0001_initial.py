# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('title', models.CharField(verbose_name='title', max_length=255, null=True, editable=False)),
                ('sort_order', models.IntegerField(default=0, verbose_name='Sort order')),
                ('title_de', models.CharField(max_length=255, verbose_name='title')),
                ('title_en', models.CharField(max_length=255, verbose_name='title', blank=True)),
            ],
            options={
                'ordering': ['sort_order', 'title'],
                'verbose_name': 'email type',
                'verbose_name_plural': 'email types',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IMType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('title', models.CharField(verbose_name='title', max_length=255, null=True, editable=False)),
                ('sort_order', models.IntegerField(default=0, verbose_name='Sort order')),
                ('title_de', models.CharField(max_length=255, verbose_name='title')),
                ('title_en', models.CharField(max_length=255, verbose_name='title', blank=True)),
            ],
            options={
                'ordering': ['sort_order', 'title'],
                'verbose_name': 'instant messenger type',
                'verbose_name_plural': 'instant messenger types',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IndividualLocationType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('title', models.CharField(verbose_name='title', max_length=255, null=True, editable=False)),
                ('sort_order', models.IntegerField(default=0, verbose_name='Sort order')),
                ('title_de', models.CharField(max_length=255, verbose_name='title')),
                ('title_en', models.CharField(max_length=255, verbose_name='title', blank=True)),
            ],
            options={
                'ordering': ['sort_order', 'title'],
                'verbose_name': 'individual location type',
                'verbose_name_plural': 'individual location types',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InstitutionalLocationType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('title', models.CharField(verbose_name='title', max_length=255, null=True, editable=False)),
                ('sort_order', models.IntegerField(default=0, verbose_name='Sort order')),
                ('title_de', models.CharField(max_length=255, verbose_name='title')),
                ('title_en', models.CharField(max_length=255, verbose_name='title', blank=True)),
            ],
            options={
                'ordering': ['sort_order', 'title'],
                'verbose_name': 'institutional location type',
                'verbose_name_plural': 'institutional location types',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PhoneType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('title', models.CharField(verbose_name='title', max_length=255, null=True, editable=False)),
                ('vcard_name', models.CharField(max_length=255, verbose_name='vCard Name', blank=True)),
                ('sort_order', models.IntegerField(default=0, verbose_name='Sort order')),
                ('title_de', models.CharField(max_length=255, verbose_name='title')),
                ('title_en', models.CharField(max_length=255, verbose_name='title', blank=True)),
            ],
            options={
                'ordering': ['sort_order', 'title'],
                'verbose_name': 'phone type',
                'verbose_name_plural': 'phone types',
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
                'ordering': ['sort_order', 'title'],
                'verbose_name': 'prefix',
                'verbose_name_plural': 'prefixes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Salutation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('title', models.CharField(verbose_name='title', max_length=255, null=True, editable=False)),
                ('template', models.CharField(help_text='takes the person as {{ person }} variable', max_length=255, null=True, editable=False, verbose_name='template')),
                ('sort_order', models.IntegerField(default=0, verbose_name='Sort Order')),
                ('title_de', models.CharField(max_length=255, verbose_name='title')),
                ('title_en', models.CharField(max_length=255, verbose_name='title', blank=True)),
                ('template_de', models.CharField(help_text='takes the person as {{ person }} variable', max_length=255, verbose_name='template')),
                ('template_en', models.CharField(help_text='takes the person as {{ person }} variable', max_length=255, verbose_name='template', blank=True)),
            ],
            options={
                'ordering': ['sort_order', 'title'],
                'verbose_name': 'salutation',
                'verbose_name_plural': 'salutations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='URLType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('title', models.CharField(verbose_name='title', max_length=255, null=True, editable=False)),
                ('sort_order', models.IntegerField(default=0, verbose_name='Sort order')),
                ('title_de', models.CharField(max_length=255, verbose_name='title')),
                ('title_en', models.CharField(max_length=255, verbose_name='title', blank=True)),
            ],
            options={
                'ordering': ['sort_order', 'title'],
                'verbose_name': 'url type',
                'verbose_name_plural': 'url types',
            },
            bases=(models.Model,),
        ),
    ]

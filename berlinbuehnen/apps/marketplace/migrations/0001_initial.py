# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import django.db.models.deletion
from django.conf import settings
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='JobCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('title', models.CharField(verbose_name='Title', max_length=200, null=True, editable=False)),
                ('title_de', models.CharField(max_length=200, verbose_name='Title')),
                ('title_en', models.CharField(max_length=200, verbose_name='Title', blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='marketplace.JobCategory', null=True)),
            ],
            options={
                'ordering': ['tree_id', 'lft'],
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='JobOffer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('description', models.TextField(default=b'', verbose_name='Description', null=True, editable=False, blank=True)),
                ('remarks', models.TextField(default=b'', verbose_name='Remarks', null=True, editable=False, blank=True)),
                ('position', models.CharField(verbose_name='Position', max_length=200, null=True, editable=False)),
                ('deadline', models.DateField(null=True, verbose_name='Deadline', blank=True)),
                ('start_contract_on', models.DateField(null=True, verbose_name='Start contract on', blank=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name', blank=True)),
                ('company', models.CharField(max_length=255, verbose_name='Company')),
                ('street_address', models.CharField(max_length=255, verbose_name='Street address')),
                ('street_address2', models.CharField(max_length=255, verbose_name='Street address (second line)', blank=True)),
                ('postal_code', models.CharField(max_length=255, verbose_name='Postal code')),
                ('city', models.CharField(default=b'Berlin', max_length=255, verbose_name='City')),
                ('latitude', models.FloatField(help_text='Latitude (Lat.) is the angle between any point and the equator (north pole is at 90; south pole is at -90).', null=True, verbose_name='Latitude', blank=True)),
                ('longitude', models.FloatField(help_text='Longitude (Long.) is the angle east or west of an arbitrary point on Earth from Greenwich (UK), which is the international zero-longitude point (longitude=0 degrees). The anti-meridian of Greenwich is both 180 (direction to east) and -180 (direction to west).', null=True, verbose_name='Longitude', blank=True)),
                ('phone_country', models.CharField(default=b'49', max_length=4, verbose_name='Country Code', blank=True)),
                ('phone_area', models.CharField(max_length=6, verbose_name='Area Code', blank=True)),
                ('phone_number', models.CharField(max_length=25, verbose_name='Subscriber Number and Extension', blank=True)),
                ('fax_country', models.CharField(default=b'49', max_length=4, verbose_name='Country Code', blank=True)),
                ('fax_area', models.CharField(max_length=6, verbose_name='Area Code', blank=True)),
                ('fax_number', models.CharField(max_length=25, verbose_name='Subscriber Number and Extension', blank=True)),
                ('email', models.EmailField(max_length=255, verbose_name='Email', blank=True)),
                ('website', base_libs.models.fields.URLField(verbose_name=b'Website', blank=True)),
                ('status', models.CharField(default=b'draft', max_length=20, verbose_name='Status', blank=True, choices=[(b'draft', 'Draft'), (b'published', 'Published'), (b'not_listed', 'Not Listed'), (b'import', 'Imported'), (b'trashed', 'Trashed')])),
                ('position_de', models.CharField(max_length=200, verbose_name='Position')),
                ('position_en', models.CharField(max_length=200, verbose_name='Position', blank=True)),
                ('description_de', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True)),
                ('description_de_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('description_en', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True)),
                ('description_en_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('remarks_de', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Anmerkungen', blank=True)),
                ('remarks_de_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('remarks_en', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Anmerkungen', blank=True)),
                ('remarks_en_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('categories', models.ManyToManyField(to='marketplace.JobCategory', verbose_name='Categories', blank=True)),
                ('creator', models.ForeignKey(related_name='joboffer_creator', on_delete=django.db.models.deletion.SET_NULL, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='creator')),
            ],
            options={
                'ordering': ['position'],
                'verbose_name': 'Job Offer',
                'verbose_name_plural': 'Job Offers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='JobType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('title', models.CharField(verbose_name='Title', max_length=200, null=True, editable=False)),
                ('sort_order', models.IntegerField(default=0, verbose_name='Sort Order')),
                ('title_de', models.CharField(max_length=200, verbose_name='Title')),
                ('title_en', models.CharField(max_length=200, verbose_name='Title', blank=True)),
            ],
            options={
                'ordering': ['sort_order'],
                'verbose_name': 'Job type',
                'verbose_name_plural': 'Job types',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='joboffer',
            name='job_type',
            field=models.ForeignKey(verbose_name='Job type', blank=True, to='marketplace.JobType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='joboffer',
            name='modifier',
            field=models.ForeignKey(related_name='joboffer_modifier', on_delete=django.db.models.deletion.SET_NULL, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='modifier'),
            preserve_default=True,
        ),
    ]

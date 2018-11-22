# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import datetime
from django.conf import settings
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClaimRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.CharField(default=b'', help_text='Please select the related object.', max_length=255, verbose_name='Related object')),
                ('name', models.CharField(max_length=80, verbose_name='Name')),
                ('email', models.EmailField(max_length=75, verbose_name='Email')),
                ('phone_country', models.CharField(max_length=4, null=True, verbose_name='Country Code', blank=True)),
                ('phone_area', models.CharField(max_length=5, null=True, verbose_name='Area Code', blank=True)),
                ('phone_number', models.CharField(max_length=15, null=True, verbose_name='Phone Number', blank=True)),
                ('best_time_to_call', models.CharField(blank=True, max_length=25, null=True, verbose_name='Best Time to Call', choices=[(b'morning', 'Morning'), (b'noon', 'Noon'), (b'afternoon', 'Afternoon'), (b'evening', 'Evening')])),
                ('role', models.CharField(max_length=80, null=True, verbose_name='Role', blank=True)),
                ('comments', models.TextField(null=True, verbose_name='Comments', blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modified')),
                ('status', models.IntegerField(blank=True, null=True, verbose_name='Status', choices=[(0, 'Requested'), (1, 'Approved'), (2, 'Denied')])),
                ('content_type', models.ForeignKey(verbose_name="Related object's type (model)", to='contenttypes.ContentType', help_text='Please select the type (model) for the relation, you want to build.')),
                ('modifier', models.ForeignKey(related_name='claimrequest_modifier', verbose_name='Modifier', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('user', models.ForeignKey(related_name='claimrequest_user', verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_date',),
                'db_table': 'system_claimrequest',
                'verbose_name': 'claim',
                'verbose_name_plural': 'claims',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContextItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('object_id', models.CharField(default=b'', help_text='Please select the related object.', max_length=255, verbose_name='Related object')),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('title', models.CharField(verbose_name='Title', max_length=255, null=True, editable=False, blank=True)),
                ('description', models.TextField(default=b'', verbose_name='Description', null=True, editable=False, blank=True)),
                ('status', models.CharField(max_length=20, blank=True)),
                ('additional_search_data', models.TextField(null=True, blank=True)),
                ('title_de', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('title_en', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('description_de', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True)),
                ('description_de_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('description_en', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True)),
                ('description_en_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('content_type', models.ForeignKey(verbose_name="Related object's type (model)", to='contenttypes.ContentType', help_text='Please select the type (model) for the relation, you want to build.')),
                ('context_categories', mptt.fields.TreeManyToManyField(to='structure.ContextCategory', verbose_name='Context categories', blank=True)),
                ('creative_sectors', mptt.fields.TreeManyToManyField(related_name='creative_industry_contextitems', verbose_name='Creative sectors', to='structure.Term', blank=True)),
                ('location_type', mptt.fields.TreeForeignKey(related_name='locality_contextitems', verbose_name='Location type', blank=True, to='structure.Term', null=True)),
            ],
            options={
                'ordering': ['title', 'creation_date'],
                'db_table': 'system_contextitem',
                'verbose_name': 'context item',
                'verbose_name_plural': 'context items',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MappedItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.CharField(default=b'', help_text='Please select the related object.', max_length=255, verbose_name='Related object')),
                ('rendered_en', models.TextField()),
                ('rendered_de', models.TextField()),
                ('lat', models.FloatField(help_text='Latitude (Lat.) is the angle between any point and the equator (north pole is at 90; south pole is at -90).', verbose_name='Latitude')),
                ('lng', models.FloatField(help_text='Longitude (Long.) is the angle east or west of an arbitrary point on Earth from Greenwich (UK), which is the international zero-longitude point (longitude=0 degrees). The anti-meridian of Greenwich is both 180 (direction to east) and -180 (direction to west).', verbose_name='Longitude')),
                ('content_type', models.ForeignKey(verbose_name="Related object's type (model)", to='contenttypes.ContentType', help_text='Please select the type (model) for the relation, you want to build.')),
            ],
            options={
                'verbose_name': 'mapped item',
                'verbose_name_plural': 'mapped items',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('last_activity', models.DateTimeField(default=datetime.datetime.now)),
                ('ip_address', models.IPAddressField(verbose_name='IP Address')),
                ('user_agent', models.CharField(max_length=255, verbose_name='User Agent')),
                ('session_key', models.CharField(max_length=255, verbose_name='Session ID')),
                ('user', models.ForeignKey(verbose_name='User', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-last_activity',),
            },
            bases=(models.Model,),
        ),
    ]

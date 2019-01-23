# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TipOfTheDay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('object_id', models.CharField(default=b'', help_text='Please select the related object.', max_length=255, verbose_name='Related object')),
                ('day', models.DateField(unique=True, verbose_name='Day')),
                ('starting_time', models.TimeField(null=True, verbose_name='Time', blank=True)),
                ('title', models.CharField(verbose_name='Title', max_length=255, null=True, editable=False)),
                ('subtitle', models.CharField(verbose_name='Subtitle', max_length=255, null=True, editable=False, blank=True)),
                ('image', filebrowser.fields.FileBrowseField(max_length=255, verbose_name='Image', blank=True)),
                ('location_title', models.CharField(verbose_name='Location Title', max_length=255, null=True, editable=False, blank=True)),
                ('event_type', models.CharField(verbose_name='Event Type', max_length=255, null=True, editable=False, blank=True)),
                ('subtitle_de', models.CharField(max_length=255, verbose_name='Subtitle', blank=True)),
                ('subtitle_en', models.CharField(max_length=255, verbose_name='Subtitle', blank=True)),
                ('subtitle_fr', models.CharField(max_length=255, verbose_name='Subtitle', blank=True)),
                ('subtitle_pl', models.CharField(max_length=255, verbose_name='Subtitle', blank=True)),
                ('subtitle_tr', models.CharField(max_length=255, verbose_name='Subtitle', blank=True)),
                ('subtitle_es', models.CharField(max_length=255, verbose_name='Subtitle', blank=True)),
                ('subtitle_it', models.CharField(max_length=255, verbose_name='Subtitle', blank=True)),
                ('event_type_de', models.CharField(max_length=255, verbose_name='Event Type', blank=True)),
                ('event_type_en', models.CharField(max_length=255, verbose_name='Event Type', blank=True)),
                ('event_type_fr', models.CharField(max_length=255, verbose_name='Event Type', blank=True)),
                ('event_type_pl', models.CharField(max_length=255, verbose_name='Event Type', blank=True)),
                ('event_type_tr', models.CharField(max_length=255, verbose_name='Event Type', blank=True)),
                ('event_type_es', models.CharField(max_length=255, verbose_name='Event Type', blank=True)),
                ('event_type_it', models.CharField(max_length=255, verbose_name='Event Type', blank=True)),
                ('title_de', models.CharField(max_length=255, verbose_name='Title')),
                ('title_en', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('title_fr', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('title_pl', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('title_tr', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('title_es', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('title_it', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('location_title_de', models.CharField(max_length=255, verbose_name='Location Title', blank=True)),
                ('location_title_en', models.CharField(max_length=255, verbose_name='Location Title', blank=True)),
                ('location_title_fr', models.CharField(max_length=255, verbose_name='Location Title', blank=True)),
                ('location_title_pl', models.CharField(max_length=255, verbose_name='Location Title', blank=True)),
                ('location_title_tr', models.CharField(max_length=255, verbose_name='Location Title', blank=True)),
                ('location_title_es', models.CharField(max_length=255, verbose_name='Location Title', blank=True)),
                ('location_title_it', models.CharField(max_length=255, verbose_name='Location Title', blank=True)),
                ('content_type', models.ForeignKey(verbose_name="Related object's type (model)", to='contenttypes.ContentType', help_text='Please select the type (model) for the relation, you want to build.')),
                ('creator', models.ForeignKey(related_name='tipoftheday_creator', on_delete=django.db.models.deletion.SET_NULL, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='creator')),
                ('modifier', models.ForeignKey(related_name='tipoftheday_modifier', on_delete=django.db.models.deletion.SET_NULL, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='modifier')),
            ],
            options={
                'verbose_name': 'Tip of the Day',
                'verbose_name_plural': 'Tips of the Day',
            },
        ),
    ]

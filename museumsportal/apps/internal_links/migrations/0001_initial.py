# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('exhibitions', '0001_initial'),
        ('events', '0002_auto_20180829_2035'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('museums', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LinkGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('group_title', models.CharField(max_length=255, verbose_name='Group title', blank=True)),
                ('language', models.CharField(max_length=5, verbose_name='Language', choices=[('de', 'Deutsch'), ('en', 'English'), ('fr', 'Fran\xe7ais'), ('pl', 'Polski'), ('tr', 'T\xfcrk\xe7e'), ('es', 'Espa\xf1ol'), ('it', 'Italiano')])),
                ('link_1_text', models.CharField(max_length=255, verbose_name='Link 1 Text', blank=True)),
                ('link_1_url', models.CharField(max_length=255, verbose_name='Link 1 URL', blank=True)),
                ('link_2_text', models.CharField(max_length=255, verbose_name='Link 2 Text', blank=True)),
                ('link_2_url', models.CharField(max_length=255, verbose_name='Link 2 URL', blank=True)),
                ('link_3_text', models.CharField(max_length=255, verbose_name='Link 3 Text', blank=True)),
                ('link_3_url', models.CharField(max_length=255, verbose_name='Link 3 URL', blank=True)),
                ('creator', models.ForeignKey(related_name='linkgroup_creator', on_delete=django.db.models.deletion.SET_NULL, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='creator')),
                ('events', models.ManyToManyField(to='events.Event', verbose_name='Events', blank=True)),
                ('exhibitions', models.ManyToManyField(to='exhibitions.Exhibition', verbose_name='Exhibitions', blank=True)),
                ('modifier', models.ForeignKey(related_name='linkgroup_modifier', on_delete=django.db.models.deletion.SET_NULL, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='modifier')),
                ('museums', models.ManyToManyField(to='museums.Museum', verbose_name='Museums', blank=True)),
            ],
            options={
                'verbose_name': 'Link Group',
                'verbose_name_plural': 'Link Groups',
            },
        ),
    ]

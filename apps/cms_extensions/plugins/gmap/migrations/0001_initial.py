# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0012_auto_20150607_2207'),
    ]

    operations = [
        migrations.CreateModel(
            name='GMap',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(max_length=100, null=True, verbose_name='map title', blank=True)),
                ('address', models.CharField(max_length=150, verbose_name='address')),
                ('zipcode', models.CharField(max_length=30, verbose_name='zip code')),
                ('city', models.CharField(max_length=100, verbose_name='city')),
                ('content', models.CharField(max_length=255, null=True, verbose_name='additional content', blank=True)),
                ('zoom', models.IntegerField(null=True, verbose_name='zoom level', blank=True)),
                ('lat', models.DecimalField(decimal_places=6, max_digits=10, blank=True, help_text='Use latitude & longitude to fine tune the map possiton.', null=True, verbose_name='latitude')),
                ('lng', models.DecimalField(null=True, verbose_name='longitude', max_digits=10, decimal_places=6, blank=True)),
                ('route_planer_title', models.CharField(default='Calculate your fastest way to here', max_length=150, null=True, verbose_name='route planer title', blank=True)),
                ('route_planer', models.BooleanField(default=False, verbose_name='route planer')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('i18n', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.CharField(max_length=255, verbose_name='State', blank=True)),
                ('city', models.CharField(max_length=255, verbose_name='City', blank=True)),
                ('street_address', models.CharField(max_length=255, verbose_name='Street Address', blank=True)),
                ('street_address2', models.CharField(max_length=255, verbose_name='Additional Address', blank=True)),
                ('street_address3', models.CharField(max_length=255, verbose_name='Additional Address', blank=True)),
                ('postal_code', models.CharField(max_length=10, verbose_name='Postal/ZIP Code', blank=True)),
                ('country', models.ForeignKey(default=b'DE', blank=True, to='i18n.Country', null=True, verbose_name='Country')),
            ],
            options={
                'verbose_name': 'address',
                'verbose_name_plural': 'addresses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Geoposition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('latitude', models.FloatField(help_text='Latitude (Lat.) is the angle between any point and the equator (north pole is at 90; south pole is at -90).', null=True, verbose_name='Latitude', blank=True)),
                ('longitude', models.FloatField(help_text='Longitude (Long.) is the angle east or west of an arbitrary point on Earth from Greenwich (UK), which is the international zero-longitude point (longitude=0 degrees). The anti-meridian of Greenwich is both 180 (direction to east) and -180 (direction to west).', null=True, verbose_name='Longitude', blank=True)),
                ('altitude', models.IntegerField(help_text='The elevation above the sea level measured in meters', null=True, verbose_name='Altitude', blank=True)),
                ('address', models.ForeignKey(to='location.Address')),
            ],
            options={
                'verbose_name': 'geoposition',
                'verbose_name_plural': 'geopositions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Locality',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('district', models.CharField(max_length=255, verbose_name='District', blank=True)),
                ('neighborhood', models.CharField(max_length=255, verbose_name='Neighborhood', blank=True)),
                ('address', models.ForeignKey(to='location.Address')),
            ],
            options={
                'verbose_name': 'locality',
                'verbose_name_plural': 'localities',
            },
            bases=(models.Model,),
        ),
    ]

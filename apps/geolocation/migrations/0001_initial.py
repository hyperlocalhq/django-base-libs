# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Geolocation',
            fields=[
                ('id', models.BigIntegerField(serialize=False, editable=False, primary_key=True, db_column=b'ID')),
                ('country', models.CharField(max_length=6, db_column=b'Country')),
                ('language', models.CharField(max_length=6, db_column=b'Language')),
                ('iso2', models.CharField(max_length=18, db_column=b'ISO2')),
                ('region1', models.CharField(max_length=180, db_column=b'Region1', blank=True)),
                ('region2', models.CharField(max_length=180, db_column=b'Region2', blank=True)),
                ('region3', models.CharField(max_length=180, db_column=b'Region3', blank=True)),
                ('region4', models.CharField(max_length=180, db_column=b'Region4', blank=True)),
                ('zip_code', models.CharField(max_length=30, db_column=b'ZIP')),
                ('city', models.CharField(max_length=180, db_column=b'City', blank=True)),
                ('area1', models.CharField(max_length=240, db_column=b'Area1', blank=True)),
                ('area2', models.CharField(max_length=240, db_column=b'Area2', blank=True)),
                ('lat', models.FloatField(db_column=b'Lat')),
                ('lng', models.FloatField(db_column=b'Lng')),
                ('tz', models.CharField(max_length=90, db_column=b'TZ')),
                ('utc', models.CharField(max_length=30, db_column=b'UTC')),
                ('dst', models.CharField(max_length=3, db_column=b'DST')),
            ],
            options={
                'db_table': 'GeoPC',
                'verbose_name': 'geolocation',
                'verbose_name_plural': 'geolocations',
            },
        ),
    ]

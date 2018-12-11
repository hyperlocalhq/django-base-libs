# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('productions', '0001_initial'),
        ('theater_of_the_week', '0002_cms_related'),
    ]

    operations = [
        migrations.CreateModel(
            name='TheaterOfTheWeekProduction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('sort_order', base_libs.models.fields.PositionField(default=None, verbose_name='Sort order')),
                ('production', models.ForeignKey(verbose_name='Production', to='productions.Production')),
                ('theater', models.ForeignKey(verbose_name='Theater of the week', to='theater_of_the_week.TheaterOfTheWeek')),
            ],
            options={
                'ordering': ['theater', 'sort_order'],
                'verbose_name': 'Production for Theater of the week',
                'verbose_name_plural': 'Productions for Theaters of the week',
            },
        ),
    ]

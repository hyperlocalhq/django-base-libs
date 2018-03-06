# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0018_pagenode'),
        ('theater_of_the_week', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TheaterOfTheWeekSelection',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='theater_of_the_week_theateroftheweekselection', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('theater_of_the_week', models.ForeignKey(to='theater_of_the_week.TheaterOfTheWeek')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]

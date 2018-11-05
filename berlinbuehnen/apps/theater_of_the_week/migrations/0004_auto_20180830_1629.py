# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theater_of_the_week', '0003_theateroftheweekproduction'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='theateroftheweek',
            options={'ordering': ['-published_from'], 'verbose_name': 'Theater of the week', 'verbose_name_plural': 'Theaters of the week'},
        ),
    ]

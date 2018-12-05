# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0003_location_sort_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='logo',
        ),
    ]

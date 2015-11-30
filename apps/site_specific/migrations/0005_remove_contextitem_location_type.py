# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('site_specific', '0004_assign_localitytypes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contextitem',
            name='location_type',
        ),
    ]

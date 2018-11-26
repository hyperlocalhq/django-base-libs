# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productions', '0002_auto_20181025_2131'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='classiccard',
        ),
        migrations.RemoveField(
            model_name='production',
            name='classiccard',
        ),
    ]

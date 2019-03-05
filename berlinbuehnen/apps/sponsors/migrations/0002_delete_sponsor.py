# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productions', '0003_auto_20181025_2307'),
        ('education', '0002_remove_project_sponsors'),
        ('sponsors', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Sponsor',
        ),
    ]

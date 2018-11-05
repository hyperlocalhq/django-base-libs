# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productions', '0002_auto_20181025_2131'),
        ('education', '0003_auto_20181025_2131'),
        ('sponsors', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Sponsor',
        ),
    ]

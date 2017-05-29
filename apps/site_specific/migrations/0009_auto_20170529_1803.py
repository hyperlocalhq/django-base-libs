# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_specific', '0008_auto_20170524_2201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit',
            name='ip_address',
            field=models.GenericIPAddressField(verbose_name='IP Address'),
        ),
    ]

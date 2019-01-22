# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_auto_20170524_2201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='ip_address',
            field=models.GenericIPAddressField(null=True, verbose_name='IP address', blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailchimp', '0007_auto_20170524_2201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='ip',
            field=models.GenericIPAddressField(null=True, verbose_name='IP Address', blank=True),
        ),
    ]

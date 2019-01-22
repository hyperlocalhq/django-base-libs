# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('external_services', '0007_auto_20170529_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='url',
            field=models.URLField(verbose_name='Feed URL'),
        ),
    ]

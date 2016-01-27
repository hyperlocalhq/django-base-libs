# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('site_specific', '0006_auto_20160121_2159'),
    ]

    operations = [
        migrations.AddField(
            model_name='contextitem',
            name='completeness',
            field=models.SmallIntegerField(default=0, verbose_name='Completeness in %'),
            preserve_default=True,
        ),
    ]

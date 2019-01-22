# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0004_auto_20160106_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution',
            name='completeness',
            field=models.SmallIntegerField(default=0, verbose_name='Completeness in %'),
            preserve_default=True,
        ),
    ]

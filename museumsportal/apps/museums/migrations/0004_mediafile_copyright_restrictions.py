# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museums', '0003_auto_20190129_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediafile',
            name='copyright_restrictions',
            field=models.CharField(blank=True, max_length=20, verbose_name='Copyright restrictions', choices=[(b'general_use', 'Released for general use'), (b'protected', 'Released for this and own site only'), (b'promotional', 'Released for promotional reasons')]),
        ),
    ]

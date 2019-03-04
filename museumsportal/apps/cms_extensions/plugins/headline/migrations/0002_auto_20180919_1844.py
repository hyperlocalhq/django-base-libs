# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('headline', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='headline',
            name='subtitle',
            field=models.CharField(max_length=200, verbose_name='Untertitel', blank=True),
        ),
    ]

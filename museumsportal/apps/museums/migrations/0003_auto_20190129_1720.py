# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museums', '0002_auto_20180919_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specialopeningtime',
            name='yyyy',
            field=models.PositiveIntegerField(blank=True, help_text='Leave this field empty, if the occasion happens every year at the same time.', null=True, verbose_name='Year', choices=[(2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023)]),
        ),
    ]

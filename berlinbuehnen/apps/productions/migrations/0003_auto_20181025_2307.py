# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productions', '0002_auto_20180830_1629'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='sponsors',
        ),
        migrations.RemoveField(
            model_name='production',
            name='sponsors',
        ),
        migrations.AlterField(
            model_name='event',
            name='price_from',
            field=models.DecimalField(null=True, verbose_name='Price from (\u20ac). Cents separated by comma.', max_digits=5, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='price_till',
            field=models.DecimalField(null=True, verbose_name='Price till (\u20ac). Cents separated by comma.', max_digits=5, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='production',
            name='price_from',
            field=models.DecimalField(null=True, verbose_name='Price from (\u20ac). Cents separated by comma.', max_digits=5, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='production',
            name='price_till',
            field=models.DecimalField(null=True, verbose_name='Price till (\u20ac). Cents separated by comma.', max_digits=5, decimal_places=2, blank=True),
        ),
    ]

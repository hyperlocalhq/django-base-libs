# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slideshows', '0003_auto_20170612_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slide',
            name='button',
            field=models.CharField(verbose_name='Button Text', max_length=200, null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='slide',
            name='button_de',
            field=models.CharField(max_length=200, verbose_name='Button Text', blank=True),
        ),
        migrations.AlterField(
            model_name='slide',
            name='button_en',
            field=models.CharField(max_length=200, verbose_name='Button Text', blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20160926_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='importance',
            field=models.IntegerField(default=0, help_text='The bigger the number, the more up-front it will be shown in the newsletter', verbose_name='Importance in newsletter'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='is_featured',
            field=models.BooleanField(default=False, verbose_name='Featured in newsletter'),
            preserve_default=True,
        ),
    ]

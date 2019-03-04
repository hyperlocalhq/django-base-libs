# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_auto_20160216_1704'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='featured_in_newsletter',
            field=models.BooleanField(default=False, verbose_name='Featured in newsletter'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='importance_in_newsletter',
            field=models.PositiveIntegerField(default=0, help_text='The bigger the number, the more up-front it will be shown in the newsletter', verbose_name='Importance in newsletter'),
            preserve_default=True,
        ),
    ]

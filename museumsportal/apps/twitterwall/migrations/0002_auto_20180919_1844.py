# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitterwall', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='by_user',
            field=models.BooleanField(default=False, verbose_name='by twitter user from user timeline settings'),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='from_search',
            field=models.BooleanField(default=False, verbose_name='from search by query'),
        ),
    ]

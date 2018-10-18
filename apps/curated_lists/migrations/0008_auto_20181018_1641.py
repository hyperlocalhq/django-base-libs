# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curated_lists', '0007_auto_20180626_2045'),
    ]

    operations = [
        migrations.AddField(
            model_name='listowner',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='email address', blank=True),
        ),
        migrations.AddField(
            model_name='listowner',
            name='first_name',
            field=models.CharField(max_length=30, verbose_name='first name', blank=True),
        ),
        migrations.AddField(
            model_name='listowner',
            name='last_name',
            field=models.CharField(max_length=30, verbose_name='last name', blank=True),
        ),
    ]

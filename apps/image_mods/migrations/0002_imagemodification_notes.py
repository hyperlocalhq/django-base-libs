# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_mods', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagemodification',
            name='notes',
            field=models.TextField(verbose_name='Notes', blank=True),
        ),
    ]

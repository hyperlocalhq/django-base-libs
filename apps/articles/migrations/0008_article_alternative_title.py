# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0007_articlecontentprovider_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='alternative_title',
            field=models.CharField(default=b'', max_length=200, verbose_name='Alternative Title', blank=True),
            preserve_default=True,
        ),
    ]

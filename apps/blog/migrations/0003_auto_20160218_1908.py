# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20160218_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='blog',
            field=models.ForeignKey(verbose_name='blog', to='blog.Blog'),
            preserve_default=True,
        ),
    ]

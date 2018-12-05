# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filebrowser', '0005_auto_20180619_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filedescription',
            name='copyright_limitations',
            field=models.CharField(help_text='If this field does not contain precise restrictions or if no restrictions are set, the rights of use are granted non-exclusively, and unrestricted in terms of time, place and content.', max_length=300, verbose_name='Copyright limitations', blank=True),
        ),
    ]

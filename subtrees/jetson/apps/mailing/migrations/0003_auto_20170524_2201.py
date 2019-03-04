# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0002_auto_20160606_2221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailmessage',
            name='sender_email',
            field=models.EmailField(max_length=254, null=True, verbose_name='Sender email', blank=True),
        ),
    ]

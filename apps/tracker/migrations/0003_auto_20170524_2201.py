# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_auto_20160606_2231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='submitter_email',
            field=models.EmailField(max_length=254, verbose_name='submitter email'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('productions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='sponsors',
        ),
        migrations.RemoveField(
            model_name='production',
            name='sponsors',
        ),
    ]

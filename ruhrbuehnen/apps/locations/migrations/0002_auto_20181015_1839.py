# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0002_remove_department_districts'),
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='districts',
        ),
        migrations.RemoveField(
            model_name='stage',
            name='district',
        ),
        migrations.DeleteModel(
            name='District',
        ),
    ]

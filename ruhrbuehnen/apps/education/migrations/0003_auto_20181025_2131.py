# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0002_remove_department_districts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='sponsors',
        ),
    ]

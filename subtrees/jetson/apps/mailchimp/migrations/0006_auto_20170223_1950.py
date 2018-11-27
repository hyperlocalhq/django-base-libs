# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mailchimp', '0005_auto_20160606_2221'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='status',
        ),
        migrations.AddField(
            model_name='campaign',
            name='sent',
            field=models.BooleanField(default=False, verbose_name='Sent', editable=False),
            preserve_default=True,
        ),
    ]

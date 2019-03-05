# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailchimp', '0015_auto_20171213_1841'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='sent_date',
            field=models.DateField(verbose_name='Sent date', null=True, editable=False, blank=True),
        ),
    ]

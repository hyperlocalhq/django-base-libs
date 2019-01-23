# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailchimp', '0002_auto_20180830_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='sender_email',
            field=models.EmailField(default='berlin-buehnen@kulturprojekte.berlin', max_length=254, verbose_name='Sender email'),
        ),
    ]

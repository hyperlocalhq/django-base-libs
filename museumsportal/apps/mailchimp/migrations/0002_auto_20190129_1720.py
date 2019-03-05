# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailchimp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='sender_email',
            field=models.EmailField(default='museumsportal@kulturprojekte.berlin', max_length=254, verbose_name='Sender email'),
        ),
    ]

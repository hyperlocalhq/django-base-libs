# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailchimp', '0010_auto_20170721_0535'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='mailinglist',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='subscriber',
        ),
        migrations.DeleteModel(
            name='Subscription',
        ),
    ]

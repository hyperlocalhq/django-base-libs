# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailchimp', '0011_auto_20170724_1833'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='settings',
            name='delete_member',
        ),
        migrations.RemoveField(
            model_name='settings',
            name='send_goodbye',
        ),
        migrations.RemoveField(
            model_name='settings',
            name='send_welcome',
        ),
        migrations.RemoveField(
            model_name='settings',
            name='update_existing',
        ),
    ]

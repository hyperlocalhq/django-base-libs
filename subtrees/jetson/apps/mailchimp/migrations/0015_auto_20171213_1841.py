# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jetson.apps.mailchimp.models


class Migration(migrations.Migration):

    dependencies = [
        ('mailchimp', '0014_auto_20170921_0512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='sender_email',
            field=models.EmailField(default=jetson.apps.mailchimp.models.get_default_from_email, max_length=254, verbose_name='Sender email'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='sender_name',
            field=models.CharField(default=jetson.apps.mailchimp.models.get_default_from_name, max_length=255, verbose_name='Sender name'),
        ),
        migrations.AlterField(
            model_name='mailingcontentblock',
            name='content_type',
            field=models.CharField(max_length=20, verbose_name=b'Content Type', blank=True),
        ),
    ]

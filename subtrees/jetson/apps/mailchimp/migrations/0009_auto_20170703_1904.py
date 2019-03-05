# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailchimp', '0008_auto_20170529_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='sender_email',
            field=models.EmailField(default='kb-contact@kulturprojekte-berlin.de', max_length=254, verbose_name='Sender email'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='sender_name',
            field=models.CharField(default='Kreatives Brandenburg', max_length=255, verbose_name='Sender name'),
        ),
    ]

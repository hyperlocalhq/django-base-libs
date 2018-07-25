# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mailchimp', '0009_auto_20170703_1904'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='username',
            field=models.CharField(max_length=200, verbose_name='Username', blank=True),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='sender_email',
            field=models.EmailField(default='ccb-contact@kulturprojekte-berlin.de', max_length=254, verbose_name='Sender email'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='sender_name',
            field=models.CharField(default='Creative City Berlin', max_length=255, verbose_name='Sender name'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='template',
            field=base_libs.models.fields.TemplatePathField(path=b'mailchimp/campaign/', verbose_name='Template', match=b'.+\\.html$'),
        ),
    ]

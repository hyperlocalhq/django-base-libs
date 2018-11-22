# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_auto_20160413_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticetype',
            name='message_template_de',
            field=base_libs.models.fields.PlainTextModelField(default=b'', help_text=b'This message will be shown in the website. Accepted template variables: {{ notified_user }}, {{ object }}, and specific extra context.', null=True, verbose_name='Message Template'),
        ),
        migrations.AlterField(
            model_name='noticetype',
            name='message_template_en',
            field=base_libs.models.fields.PlainTextModelField(default=b'', help_text=b'This message will be shown in the website. Accepted template variables: {{ notified_user }}, {{ object }}, and specific extra context.', null=True, verbose_name='Message Template', blank=True),
        ),
    ]

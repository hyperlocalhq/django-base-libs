# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0003_auto_20180619_2101'),
    ]

    operations = [
        migrations.AddField(
            model_name='extendedlogentry',
            name='change_message_es',
            field=base_libs.models.fields.PlainTextModelField(default=b'', null=True, verbose_name='\xc4nderungsmeldung', blank=True),
        ),
        migrations.AddField(
            model_name='extendedlogentry',
            name='change_message_fr',
            field=base_libs.models.fields.PlainTextModelField(default=b'', null=True, verbose_name='\xc4nderungsmeldung', blank=True),
        ),
        migrations.AddField(
            model_name='extendedlogentry',
            name='change_message_it',
            field=base_libs.models.fields.PlainTextModelField(default=b'', null=True, verbose_name='\xc4nderungsmeldung', blank=True),
        ),
        migrations.AddField(
            model_name='extendedlogentry',
            name='change_message_pl',
            field=base_libs.models.fields.PlainTextModelField(default=b'', null=True, verbose_name='\xc4nderungsmeldung', blank=True),
        ),
        migrations.AddField(
            model_name='extendedlogentry',
            name='change_message_tr',
            field=base_libs.models.fields.PlainTextModelField(default=b'', null=True, verbose_name='\xc4nderungsmeldung', blank=True),
        ),
        migrations.AlterField(
            model_name='extendedlogentry',
            name='change_message_de',
            field=base_libs.models.fields.PlainTextModelField(default=b'', null=True, verbose_name='\xc4nderungsmeldung', blank=True),
        ),
        migrations.AlterField(
            model_name='extendedlogentry',
            name='change_message_en',
            field=base_libs.models.fields.PlainTextModelField(default=b'', null=True, verbose_name='\xc4nderungsmeldung', blank=True),
        ),
    ]

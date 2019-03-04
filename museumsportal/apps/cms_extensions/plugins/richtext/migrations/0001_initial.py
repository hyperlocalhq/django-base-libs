# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0016_auto_20160608_1535'),
    ]

    operations = [
        migrations.CreateModel(
            name='RichText',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='richtext_richtext', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('body', base_libs.models.fields.ExtendedTextField(verbose_name='body')),
                ('body_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]

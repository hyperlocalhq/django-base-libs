# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('external_services', '0002_bulletinimportsource'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bulletinimportsource',
            name='default_status',
            field=models.CharField(default=b'draft', help_text='Status to apply to the imported bulletins by default.', max_length=20, verbose_name='status', choices=[(b'draft', 'Draft'), (b'published', 'Published'), (b'import', 'Imported')]),
            preserve_default=True,
        ),
    ]

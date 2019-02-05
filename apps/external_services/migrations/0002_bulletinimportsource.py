# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('bulletin_board', '0002_auto_20151218_1626'),
        ('structure', '0003_remove_category_sort_order'),
        ('external_services', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BulletinImportSource',
            fields=[
                ('service_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='external_services.Service')),
                ('default_status', models.CharField(default=b'draft', help_text='Status to apply to the imported bulletins by default.', max_length=20, verbose_name='status', choices=[(b'draft', 'Draft'), (b'published', 'Published')])),
                ('content_provider', models.ForeignKey(verbose_name='Content provider', blank=True, to='bulletin_board.BulletinContentProvider', null=True)),
                ('default_categories', mptt.fields.TreeManyToManyField(help_text='Categories to apply to the imported bulletins by default.', to='structure.Category', null=True, verbose_name='Categories', blank=True)),
            ],
            options={
                'ordering': ('title',),
                'db_table': 'external_services_bis',
                'verbose_name': 'bulletin-import source',
                'verbose_name_plural': 'bulletin-import sources',
            },
            bases=('external_services.service',),
        ),
    ]

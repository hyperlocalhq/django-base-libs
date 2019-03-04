# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InternalMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('subject', models.CharField(max_length=255, verbose_name='Subject', blank=True)),
                ('body', base_libs.models.fields.ExtendedTextField(verbose_name='Message', blank=True)),
                ('is_read', models.BooleanField(default=False, verbose_name='Read')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Deleted')),
                ('is_replied', models.BooleanField(default=False, verbose_name='Replied')),
                ('is_spam', models.BooleanField(default=False, verbose_name='Spam')),
                ('is_draft', models.BooleanField(default=False, verbose_name='Draft')),
                ('body_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('creator', models.ForeignKey(related_name='internalmessage_creator', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='creator')),
                ('modifier', models.ForeignKey(related_name='internalmessage_modifier', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='modifier')),
                ('recipient', models.ForeignKey(related_name='received_message_set', verbose_name='Recipient', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('sender', models.ForeignKey(related_name='sent_message_set', verbose_name='Sender', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-creation_date', 'subject'),
                'verbose_name': 'internal message',
                'verbose_name_plural': 'internal messages',
            },
            bases=(models.Model,),
        ),
    ]

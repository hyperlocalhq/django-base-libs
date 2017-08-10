# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtendedLogEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.CharField(default=b'', help_text='Please select the related object.', max_length=255, verbose_name='Related object', blank=True)),
                ('action_time', models.DateTimeField(auto_now=True, verbose_name='action time')),
                ('object_repr', models.CharField(max_length=200, verbose_name='object repr')),
                ('action_flag', models.PositiveSmallIntegerField(default=0, verbose_name='action', choices=[(0, 'Undefined'), (1, 'Add'), (4, 'Read'), (2, 'Change'), (3, 'Delete'), (5, 'Custom #1'), (6, 'Custom #2'), (7, 'Custom #3')])),
                ('change_message', models.TextField(default=b'', verbose_name='change message', null=True, editable=False, blank=True)),
                ('scope', models.PositiveSmallIntegerField(default=0, verbose_name='scope', choices=[(0, 'System'), (1, 'Private'), (2, 'Public')])),
                ('change_message_de', base_libs.models.fields.PlainTextModelField(default=b'', null=True, verbose_name='Nachricht \xe4ndern', blank=True)),
                ('change_message_en', base_libs.models.fields.PlainTextModelField(default=b'', null=True, verbose_name='Nachricht \xe4ndern', blank=True)),
                ('content_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', help_text='Please select the type (model) for the relation, you want to build.', null=True, verbose_name="Related object's type (model)")),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-action_time',),
                'verbose_name': 'log entry',
                'verbose_name_plural': 'log entries',
            },
            bases=(models.Model,),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sites', '0001_initial'),
        ('contact_form', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactformcategory',
            name='auto_answer_template',
            field=models.ForeignKey(blank=True, to='mailing.EmailTemplate', help_text='Nothing is sent back to the sender if the template is not selected', null=True, verbose_name='Email template for the automatic answer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contactformcategory',
            name='recipients',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, null=True, verbose_name='Recipient(s)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contactformcategory',
            name='site',
            field=models.ForeignKey(blank=True, to='sites.Site', help_text='Restrict this object only for the selected site', null=True, verbose_name='Site'),
            preserve_default=True,
        ),
    ]

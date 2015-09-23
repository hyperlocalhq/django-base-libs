# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='IndividualRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Created', null=True)),
                ('activation', models.DateTimeField(verbose_name='Activated', null=True, editable=False)),
                ('status', models.CharField(max_length=10, verbose_name='Status of the user #1', choices=[(b'inviting', 'Inviting'), (b'invited', 'Invited'), (b'denying', 'Denying'), (b'denied', 'Denied'), (b'blocking', 'Blocking'), (b'blocked', 'Blocked'), (b'confirmed', 'Confirmed')])),
                ('display_birthday', models.BooleanField(default=True, verbose_name='Display birthday to user #2')),
                ('display_address', models.BooleanField(default=True, verbose_name='Display address data to user #2')),
                ('display_phone', models.BooleanField(default=True, verbose_name='Display phone numbers to user #2')),
                ('display_fax', models.BooleanField(default=True, verbose_name='Display fax numbers to user #2')),
                ('display_mobile', models.BooleanField(default=True, verbose_name='Display mobile phones to user #2')),
                ('display_im', models.BooleanField(default=True, verbose_name='Display instant messengers to user #2')),
                ('message', models.TextField(verbose_name='Message from user #1 to user #2', blank=True)),
            ],
            options={
                'verbose_name': 'individual relation',
                'verbose_name_plural': 'individual relations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IndividualRelationType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('sort_order', models.IntegerField(default=0, verbose_name='sort order', editable=False, blank=True)),
                ('title', models.CharField(verbose_name='title', max_length=255, null=True, editable=False)),
                ('title_de', models.CharField(max_length=255, verbose_name='title')),
                ('title_en', models.CharField(max_length=255, verbose_name='title', blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('backwards', mptt.fields.TreeForeignKey(related_name='backwards_relation_set', verbose_name='Backwards relationship', blank=True, to='individual_relations.IndividualRelationType', null=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='child_set', blank=True, to='individual_relations.IndividualRelationType', null=True)),
            ],
            options={
                'ordering': ['tree_id', 'lft'],
                'abstract': False,
                'verbose_name': 'individual relation type',
                'verbose_name_plural': 'individual relation types',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='individualrelation',
            name='relation_types',
            field=mptt.fields.TreeManyToManyField(to='individual_relations.IndividualRelationType', verbose_name='is', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='individualrelation',
            name='to_user',
            field=models.ForeignKey(related_name='to_user', verbose_name='to user #2', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='individualrelation',
            name='user',
            field=models.ForeignKey(verbose_name='User #1', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='individualrelation',
            unique_together=set([('user', 'to_user')]),
        ),
    ]

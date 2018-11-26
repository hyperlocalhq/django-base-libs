# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_cms_related'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageandtext',
            name='cmsplugin_ptr',
            field=models.OneToOneField(parent_link=True, related_name='services_imageandtext', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin'),
        ),
        migrations.AlterField(
            model_name='indexitem',
            name='cmsplugin_ptr',
            field=models.OneToOneField(parent_link=True, related_name='services_indexitem', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin'),
        ),
        migrations.AlterField(
            model_name='linkcategory',
            name='cmsplugin_ptr',
            field=models.OneToOneField(parent_link=True, related_name='services_linkcategory', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin'),
        ),
        migrations.AlterField(
            model_name='servicegriditem',
            name='cmsplugin_ptr',
            field=models.OneToOneField(parent_link=True, related_name='services_servicegriditem', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin'),
        ),
        migrations.AlterField(
            model_name='servicelistitem',
            name='cmsplugin_ptr',
            field=models.OneToOneField(parent_link=True, related_name='services_servicelistitem', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin'),
        ),
        migrations.AlterField(
            model_name='servicepagebanner',
            name='cmsplugin_ptr',
            field=models.OneToOneField(parent_link=True, related_name='services_servicepagebanner', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin'),
        ),
        migrations.AlterField(
            model_name='titleandtext',
            name='cmsplugin_ptr',
            field=models.OneToOneField(parent_link=True, related_name='services_titleandtext', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin'),
        ),
    ]

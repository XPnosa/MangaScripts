# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-16 22:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mangascripts', '0010_auto_20161012_0354'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='read',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]

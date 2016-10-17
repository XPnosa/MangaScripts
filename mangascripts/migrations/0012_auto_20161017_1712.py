# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-17 15:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mangascripts', '0011_chapter_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='protected',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='manga',
            name='protected',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='volume',
            name='protected',
            field=models.BooleanField(default=False),
        ),
    ]

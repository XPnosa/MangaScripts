# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-24 02:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mangascripts', '0002_auto_20160924_0156'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chapter',
            name='manga',
        ),
    ]

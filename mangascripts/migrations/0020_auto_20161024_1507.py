# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-24 13:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mangascripts', '0019_auto_20161024_1330'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chapter',
            name='favorite',
        ),
        migrations.RemoveField(
            model_name='chapter',
            name='protected',
        ),
        migrations.RemoveField(
            model_name='chapter',
            name='read',
        ),
        migrations.RemoveField(
            model_name='manga',
            name='favorite',
        ),
        migrations.RemoveField(
            model_name='manga',
            name='protected',
        ),
        migrations.RemoveField(
            model_name='volume',
            name='favorite',
        ),
        migrations.RemoveField(
            model_name='volume',
            name='protected',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-23 23:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mangascripts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chapter',
            old_name='tittle',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='volume',
            old_name='tittle',
            new_name='title',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-28 18:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mangascripts', '0030_myuser'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MyUser',
            new_name='App_User',
        ),
    ]

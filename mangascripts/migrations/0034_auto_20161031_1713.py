# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-31 16:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mangascripts', '0033_app_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app_user',
            name='info',
            field=models.TextField(null=True),
        ),
    ]

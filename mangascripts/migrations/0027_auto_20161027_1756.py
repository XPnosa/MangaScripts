# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-27 15:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mangascripts', '0026_auto_20161026_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manga',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='manga',
            unique_together=set([]),
        ),
    ]

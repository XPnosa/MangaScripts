# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-18 09:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mangascripts', '0015_auto_20161017_2306'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='chapter',
            unique_together=set([('volume', 'n_chap')]),
        ),
    ]
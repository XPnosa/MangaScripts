# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-26 09:09
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mangascripts', '0025_auto_20161025_1643'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter_fav',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mangascripts.Chapter')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Manga_fav',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mangascripts.Manga')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Volume_fav',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('volume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mangascripts.Volume')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='volume_fav',
            unique_together=set([('user', 'volume')]),
        ),
        migrations.AlterUniqueTogether(
            name='manga_fav',
            unique_together=set([('user', 'manga')]),
        ),
        migrations.AlterUniqueTogether(
            name='chapter_fav',
            unique_together=set([('user', 'chapter')]),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-09 05:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20171009_0447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='tag_set',
            field=models.ManyToManyField(blank=True, to='home.Tag'),
        ),
    ]

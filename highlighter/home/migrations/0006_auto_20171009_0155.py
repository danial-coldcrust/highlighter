# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-09 01:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_project_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('d', 'Draft'), ('p', 'Published')], max_length=1),
        ),
    ]

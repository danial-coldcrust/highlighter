# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-08 19:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20171008_1927'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='author',
            field=models.CharField(default='익명사용자', max_length=20),
            preserve_default=False,
        ),
    ]

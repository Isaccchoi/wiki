# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-04 07:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('word', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='word',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]

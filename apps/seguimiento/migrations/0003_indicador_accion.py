# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-12 04:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seguimiento', '0002_auto_20161211_1630'),
    ]

    operations = [
        migrations.AddField(
            model_name='indicador',
            name='accion',
            field=models.TextField(null=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-26 03:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seguimiento', '0005_auto_20161225_1901'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Observaciones',
            new_name='Observacion',
        ),
    ]

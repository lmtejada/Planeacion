# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-07 04:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seguimiento', '0003_auto_20161206_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='respuesta',
            name='pregunta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='seguimiento.Pregunta'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-30 03:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seguimiento', '0002_formulario_formulariorespuesta_pregunta_respuesta'),
    ]

    operations = [
        migrations.AddField(
            model_name='respuesta',
            name='formulario_respuesta',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='seguimiento.FormularioRespuesta'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-03 21:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0004_auto_20171003_1636'),
    ]

    operations = [
        migrations.AddField(
            model_name='xerobookcalc',
            name='is_two_to_one',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='xerocalc',
            name='is_one_sided',
            field=models.BooleanField(default=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-03 16:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0003_xerobyweightcalc'),
    ]

    operations = [
        migrations.RenameField(
            model_name='xerosimplecalc',
            old_name='number_of_cards_from_form',
            new_name='number_of_cards_or_pages_from_form',
        ),
    ]
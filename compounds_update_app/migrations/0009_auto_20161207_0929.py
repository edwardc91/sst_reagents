# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-07 09:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compounds_update_app', '0008_auto_20161207_0914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reactivoupdate',
            name='n_einecs',
            field=models.CharField(blank=True, help_text='Ejemplos: 252-104-2, 200-887-6, etc', max_length=150, null=True, verbose_name='EINECS'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-12 13:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0004_auto_20190412_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_order',
            field=models.IntegerField(default=1),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-15 14:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0007_auto_20190415_1914'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='coment_retry',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='coment_retry_date',
        ),
    ]
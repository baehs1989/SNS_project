# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-04-27 01:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counter', '0003_visitor_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitor',
            name='name',
            field=models.TextField(max_length=100),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-04-08 05:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='post',
            unique_together=set([]),
        ),
    ]

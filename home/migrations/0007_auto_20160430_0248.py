# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-30 06:48
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20160430_0246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='championdata',
            name='last_update',
            field=models.DateTimeField(default=datetime.datetime.now, editable=False),
        ),
    ]

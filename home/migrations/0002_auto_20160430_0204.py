# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='championdata',
            name='last_update',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 30, 2, 4, 46, 958071), editable=False),
        ),
    ]

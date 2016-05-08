# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20160430_0204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='championdata',
            name='last_update',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 30, 2, 4, 51, 881570), editable=False),
        ),
    ]

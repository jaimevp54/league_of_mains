# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChampionData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', editable=False, max_length=25)),
                ('game_id', models.IntegerField(default=0, editable=False)),
                ('mastery_level', models.IntegerField(default=0, editable=False)),
                ('mastery_points', models.IntegerField(default=0, editable=False)),
                ('highest_grade', models.CharField(default='0', editable=False, max_length=2)),
                ('games', models.IntegerField(default=0, editable=False)),
                ('wins', models.IntegerField(default=0, editable=False)),
                ('losses', models.IntegerField(default=0, editable=False)),
                ('kills', models.IntegerField(default=0, editable=False)),
                ('deaths', models.IntegerField(default=0, editable=False)),
                ('assists', models.IntegerField(default=0, editable=False)),
                ('cs_count', models.IntegerField(default=0, editable=False)),
                ('first_blood_count', models.IntegerField(default=0, editable=False)),
                ('turret_kills', models.IntegerField(default=0, editable=False)),
                ('inhibitor_kills', models.IntegerField(default=0, editable=False)),
                ('wards_placed', models.IntegerField(default=0, editable=False)),
                ('ward_kills', models.IntegerField(default=0, editable=False)),
                ('penta_kills', models.IntegerField(default=0, editable=False)),
                ('quadra_kills', models.IntegerField(default=0, editable=False)),
                ('triple_kills', models.IntegerField(default=0, editable=False)),
                ('double_kills', models.IntegerField(default=0, editable=False)),
                ('largest_killing_spree', models.IntegerField(default=0, editable=False)),
                ('largest_cs_count', models.IntegerField(default=0, editable=False)),
                ('time_played', models.TimeField(default=0, editable=False)),
                ('last_update', models.DateTimeField(default=datetime.datetime(2016, 4, 30, 2, 3, 48, 157326), editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Summoner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(editable=False, max_length=25)),
                ('game_id', models.IntegerField(editable=False)),
                ('profile_icon_id', models.IntegerField(editable=False)),
            ],
        ),
        migrations.AddField(
            model_name='championdata',
            name='summoner',
            field=models.ForeignKey(to='home.Summoner'),
        ),
    ]

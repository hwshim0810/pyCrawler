# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DailyRank',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('rank', models.IntegerField()),
                ('singer', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=100)),
                ('album', models.CharField(max_length=150)),
                ('albumImg', models.TextField()),
                ('crawledDate', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
    ]

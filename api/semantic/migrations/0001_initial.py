# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='semantic',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('security', models.CharField(max_length=100)),
                ('sentence1', models.CharField(max_length=300)),
                ('result', models.CharField(max_length=30, default=None)),
            ],
        ),
    ]

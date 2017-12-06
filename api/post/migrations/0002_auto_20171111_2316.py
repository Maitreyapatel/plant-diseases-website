# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='id',
            field=models.UUIDField(serialize=False, default=uuid.uuid4, primary_key=True, editable=False),
        ),
    ]

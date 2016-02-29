# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('usermanager', '0007_auto_20160222_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useractivation',
            name='key_expires',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usermanager', '0008_auto_20160226_0707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetail',
            name='phone',
            field=models.CharField(null=True, blank=True, max_length=20),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliverydetail',
            name='price',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='deliverydetail',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='deliverydetail',
            name='total',
            field=models.FloatField(null=True, blank=True),
        ),
    ]

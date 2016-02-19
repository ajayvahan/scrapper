# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, null=True, max_length=255)),
                ('product_type', models.CharField(blank=True, null=True, max_length=30)),
                ('price', models.FloatField(blank=True, null=True, default=0.0)),
                ('description', models.CharField(blank=True, null=True, max_length=255)),
                ('scraped_date', models.DateTimeField(auto_now=True)),
                ('landing_url', models.URLField(blank=True, null=True)),
                ('image', models.URLField(blank=True, null=True)),
            ],
        ),
    ]

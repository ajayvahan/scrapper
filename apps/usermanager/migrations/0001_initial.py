# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.usermanager.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('date_of_birth', models.DateField(null=True, blank=True)),
                ('marital', models.CharField(null=True, max_length=1, blank=True, choices=[(1, 'Single'), (2, 'Married')])),
                ('gender', models.CharField(null=True, max_length=1, blank=True, choices=[(1, 'Male'), (2, 'Female')])),
                ('address', models.CharField(null=True, max_length=254, blank=True)),
                ('street', models.CharField(null=True, max_length=30, blank=True)),
                ('zip_code', models.CharField(null=True, max_length=6, blank=True)),
                ('phone', models.IntegerField(null=True, blank=True, default=0)),
                ('extra_note', models.CharField(null=True, max_length=254, blank=True)),
                ('mail', models.CharField(null=True, max_length=1, blank=True)),
                ('message', models.CharField(null=True, max_length=1, blank=True)),
                ('phonecall', models.CharField(null=True, max_length=1, blank=True)),
                ('other', models.CharField(null=True, max_length=1, blank=True)),
                ('image', models.ImageField(null=True, blank=True, upload_to=apps.usermanager.models.generate_filename)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

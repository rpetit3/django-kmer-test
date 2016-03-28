# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import kmer.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Binary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('string', models.BinaryField(unique=True, max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='String',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('string', kmer.models.FixedCharField(unique=True, max_length=31)),
            ],
        ),
    ]

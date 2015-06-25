# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kmer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='KmerBinaryTmp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('string', models.BinaryField(unique=True, max_length=8, db_index=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='KmerStringTmp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('string', models.CharField(unique=True, max_length=31, db_index=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

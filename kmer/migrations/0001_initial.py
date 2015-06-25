# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Kmer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.TextField(db_index=True)),
                ('version', models.TextField(default=b'1.0', db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='KmerBinary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('string', models.BinaryField(unique=True, max_length=8, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='KmerBinaryCount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.PositiveIntegerField()),
                ('kmer', models.ForeignKey(to='kmer.Kmer')),
                ('string', models.ForeignKey(to='kmer.KmerBinary')),
            ],
        ),
        migrations.CreateModel(
            name='KmerString',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('string', models.CharField(unique=True, max_length=31, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='KmerStringCount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.PositiveIntegerField()),
                ('kmer', models.ForeignKey(to='kmer.Kmer')),
                ('string', models.ForeignKey(to='kmer.KmerString')),
            ],
        ),
        migrations.CreateModel(
            name='KmerTotal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total', models.PositiveIntegerField()),
                ('singletons', models.PositiveIntegerField()),
                ('kmer', models.ForeignKey(to='kmer.Kmer')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='kmerstringcount',
            unique_together=set([('kmer', 'string')]),
        ),
        migrations.AlterUniqueTogether(
            name='kmerbinarycount',
            unique_together=set([('kmer', 'string')]),
        ),
    ]

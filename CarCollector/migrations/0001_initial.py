# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('price', models.DecimalField(default=0, max_digits=9, decimal_places=2)),
                ('license', models.CharField(max_length=20)),
                ('title', models.CharField(default=None, max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('url', models.URLField(default=None)),
                ('image_url', models.URLField(default=None)),
                ('brand', models.ForeignKey(to='CarCollector.Brand')),
            ],
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('brand', models.ForeignKey(to='CarCollector.Brand')),
            ],
        ),
        migrations.AddField(
            model_name='car',
            name='model',
            field=models.ForeignKey(to='CarCollector.Model'),
        ),
    ]

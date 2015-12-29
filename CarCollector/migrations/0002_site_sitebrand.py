# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CarCollector', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='SiteBrand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identification', models.CharField(max_length=200)),
                ('url', models.URLField()),
                ('brand', models.ForeignKey(to='CarCollector.Site')),
                ('model', models.ForeignKey(to='CarCollector.Brand')),
            ],
        ),
    ]

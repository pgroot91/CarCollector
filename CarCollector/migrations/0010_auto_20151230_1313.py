# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CarCollector', '0009_auto_20151229_1141'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(max_length=200)),
                ('url', models.URLField()),
            ],
        ),
        migrations.AddField(
            model_name='model',
            name='url',
            field=models.URLField(default='http://www.test.com/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sitemodel',
            name='model',
            field=models.ForeignKey(to='CarCollector.Model'),
        ),
        migrations.AddField(
            model_name='sitemodel',
            name='site',
            field=models.ForeignKey(to='CarCollector.Site'),
        ),
        migrations.AddField(
            model_name='model',
            name='site_models',
            field=models.ManyToManyField(to='CarCollector.Site', through='CarCollector.SiteModel'),
        ),
    ]

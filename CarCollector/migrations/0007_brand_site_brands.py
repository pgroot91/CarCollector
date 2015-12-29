# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CarCollector', '0006_auto_20151228_2242'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='site_brands',
            field=models.ManyToManyField(to='CarCollector.Site', through='CarCollector.SiteBrand'),
        ),
    ]

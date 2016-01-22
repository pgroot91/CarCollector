# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CarCollector', '0010_auto_20151230_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='model',
            name='brand',
            field=models.ForeignKey(to='CarCollector.Brand', null=True),
        ),
    ]

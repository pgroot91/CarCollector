# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CarCollector', '0004_auto_20151228_2235'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sitebrand',
            name='model',
        ),
        migrations.AddField(
            model_name='sitebrand',
            name='site',
            field=models.ForeignKey(default='f5c551c4-6871-45fa-b4e6-f8634c82c559', to='CarCollector.Site'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sitebrand',
            name='brand',
            field=models.ForeignKey(to='CarCollector.Brand'),
        ),
    ]

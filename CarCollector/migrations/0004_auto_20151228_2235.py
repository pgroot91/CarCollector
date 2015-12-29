# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CarCollector', '0003_auto_20151228_2213'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sitebrand',
            old_name='identification',
            new_name='identifier',
        ),
    ]

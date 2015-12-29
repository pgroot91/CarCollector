# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('CarCollector', '0002_site_sitebrand'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True),
        ),
    ]

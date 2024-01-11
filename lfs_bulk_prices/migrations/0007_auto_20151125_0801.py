# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lfs_bulk_prices", "0006_auto_20151124_1100"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bulkprice",
            name="amount",
            field=models.FloatField(verbose_name="Amount"),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lfs_bulk_prices", "0002_auto_20151116_0957"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bulkprice",
            name="price_percentual",
            field=models.DecimalField(default=0.0, verbose_name="Price", max_digits=10, decimal_places=2),
        ),
        migrations.AlterField(
            model_name="bulkprice",
            name="price_total",
            field=models.DecimalField(default=0.0, verbose_name="Price", max_digits=10, decimal_places=2),
        ),
    ]

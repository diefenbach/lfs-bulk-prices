# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lfs_bulk_prices", "0003_auto_20151116_0958"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bulkprice",
            name="price_percentual",
            field=models.FloatField(default=0.0, verbose_name="Price percentual"),
        ),
        migrations.AlterField(
            model_name="bulkprice",
            name="price_total",
            field=models.FloatField(default=0.0, verbose_name="Price absolute"),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lfs_bulk_prices", "0004_auto_20151116_1008"),
    ]

    operations = [
        migrations.RenameField(
            model_name="bulkprice",
            old_name="price_total",
            new_name="price_absolute",
        ),
        migrations.AlterUniqueTogether(
            name="bulkprice",
            unique_together=set([("product", "price_absolute")]),
        ),
    ]

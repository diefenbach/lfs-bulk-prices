# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lfs_bulk_prices', '0005_auto_20151117_1947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bulkprice',
            name='amount',
            field=models.SmallIntegerField(verbose_name='Amount'),
        ),
        migrations.AlterField(
            model_name='bulkprice',
            name='product',
            field=models.ForeignKey(verbose_name='Product', to='catalog.Product'),
        ),
        migrations.AlterUniqueTogether(
            name='bulkprice',
            unique_together=set([('product', 'price_absolute'), ('product', 'amount')]),
        ),
    ]

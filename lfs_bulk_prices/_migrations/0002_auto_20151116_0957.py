# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lfs_bulk_prices', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bulkprice',
            options={'ordering': ('amount',)},
        ),
        migrations.RenameField(
            model_name='bulkprice',
            old_name='price',
            new_name='price_total',
        ),
        migrations.AddField(
            model_name='bulkprice',
            name='amount',
            field=models.SmallIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bulkprice',
            name='price_percentual',
            field=models.DecimalField(default=0, verbose_name='Price', max_digits=10, decimal_places=2),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='bulkprice',
            unique_together=set([('product', 'price_total')]),
        ),
    ]

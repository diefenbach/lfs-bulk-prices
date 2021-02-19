# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    operations = [
        migrations.CreateModel(
            name='BulkPrice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.DecimalField(verbose_name='Price', max_digits=10, decimal_places=2)),
                ('product', models.ForeignKey(to='catalog.Product', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ('price',),
            },
        ),
        migrations.AlterUniqueTogether(
            name='bulkprice',
            unique_together=set([('product', 'price')]),
        ),
    ]

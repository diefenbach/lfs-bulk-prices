from django.db import models
from django.utils.translation import ugettext_lazy as _
from lfs.catalog.models import Product


class BulkPrice(models.Model):
    """
    """
    class Meta:
        ordering = ("amount", )
        unique_together = ("product", "price_absolute")

    product = models.ForeignKey(Product)
    amount = models.SmallIntegerField()
    price_absolute = models.FloatField(_(u"Price absolute"), default=0.0)
    price_percentual = models.FloatField(_(u"Price percentual"), default=0.0)
